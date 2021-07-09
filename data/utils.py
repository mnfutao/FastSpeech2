import os
import random
import json

import tgt
import torch
import librosa
import numpy as np
import pyworld as pw
from scipy.interpolate import interp1d
from sklearn.preprocessing import StandardScaler
import sys
sys.path.append('../')
import audio as Audio
import hparams as hp

from tqdm import tqdm
import soundfile as sf


def build_from_path(in_dir, out_dir): # ./raw_data/M2VoC   ./preprocessed_data/M2VoC
    print("Processing Data ...")
    index = 1
    out = list()
    n_frames = 0
    f0_scaler = StandardScaler()
    energy_scaler = StandardScaler()

    speakers = {}
    for i, speaker in enumerate(os.listdir(in_dir)):
        speakers[speaker] = i
        print(f'【{speaker}】')
        for wav_name in tqdm(os.listdir(os.path.join(in_dir, speaker))):
            if ".wav" not in wav_name:
                continue

            basename = wav_name[:-4]
            tg_path = os.path.join(
                out_dir, "TextGrid", speaker, "{}.TextGrid".format(basename)
            )
            if os.path.exists(tg_path):
                ret = process_utterance(in_dir, out_dir, speaker, basename)
                if ret is None:
                    continue
                else:
                    info, f0, energy, f_max, f_min, e_max, e_min, n = ret
                out.append(info)

            # if index % 100 == 0:
            #     print("Done %d" % index)
            index = index + 1

            if len(f0) > 0 and len(energy) > 0:
                f0_scaler.partial_fit(f0.reshape((-1, 1)))
                energy_scaler.partial_fit(energy.reshape((-1, 1)))

            n_frames += n

    f0_mean = f0_scaler.mean_[0]
    f0_std = f0_scaler.scale_[0]
    energy_mean = energy_scaler.mean_[0]
    energy_std = energy_scaler.scale_[0]

    print("Normalizing Data ...")
    f0_min, f0_max = normalize(os.path.join(out_dir, "f0"), f0_mean, f0_std)
    energy_min, energy_max = normalize(
        os.path.join(out_dir, "energy"), energy_mean, energy_std
    )

    with open(os.path.join(out_dir, "speakers.json"), "w") as f:
        f.write(json.dumps(speakers))

    with open(os.path.join(out_dir, "stat.txt"), "w", encoding="utf-8") as f:
        strs = [
            "Total time: {} hours".format(
                n_frames * hp.hop_length / hp.sampling_rate / 3600
            ),
            "Total frames: {}".format(n_frames),
            "Mean F0: {}".format(f0_mean),
            "Stdev F0: {}".format(f0_std),
            "Min F0: {}".format(f0_min),
            "Max F0: {}".format(f0_max),
            "Min energy: {}".format(energy_min),
            "Max energy: {}".format(energy_max),
        ]
        for s in strs:
            print(s)
            f.write(s + "\n")

    random.shuffle(out)
    out = [r for r in out if r is not None]

    return out


def process_utterance(in_dir, out_dir, speaker, basename):
    wav_path = os.path.join(in_dir, speaker, "{}.wav".format(basename))
    tg_path = os.path.join(out_dir, "TextGrid", speaker, "{}.TextGrid".format(basename))

    # Get alignments
    textgrid = tgt.io.read_textgrid(tg_path)
    phone, duration, start, end = get_alignment(textgrid.get_tier_by_name("phones"))
    text = "{" + " ".join(phone) + "}"
    if start >= end:
        return None

    # Read and trim wav files
    wav, _ = sf.read(wav_path)
    wav = wav[int(hp.sampling_rate * start) : int(hp.sampling_rate * end)].astype(
        np.float32
    )

    # Compute fundamental frequency
    f0, t = pw.dio(
        wav.astype(np.float64),
        hp.sampling_rate,
        frame_period=hp.hop_length / hp.sampling_rate * 1000,
    )
    f0 = pw.stonemask(wav.astype(np.float64), f0, t, hp.sampling_rate)

    f0 = f0[: sum(duration)]
    if np.all(f0 == 0):
        return None

    # perform linear interpolation
    nonzero_ids = np.where(f0 != 0)[0]
    interp_fn = interp1d(
        nonzero_ids,
        f0[nonzero_ids],
        fill_value=(f0[nonzero_ids[0]], f0[nonzero_ids[-1]]),
        bounds_error=False,
    )
    f0 = interp_fn(np.arange(0, len(f0)))

    # Compute mel-scale spectrogram and energy
       

    mel_spectrogram, energy = Audio.tools.get_mel_from_wav(wav)
    mel_spectrogram = mel_spectrogram.numpy().astype(np.float32)[:, : sum(duration)]
    energy = energy.numpy().astype(np.float32)[: sum(duration)]
    if mel_spectrogram.shape[1] >= hp.max_seq_len:
        return None

    # Phoneme-level average
    pos = 0
    for i, d in enumerate(duration):
        f0[i] = np.mean(f0[pos : pos + d])
        energy[i] = np.mean(energy[pos : pos + d])
        pos += d
    f0 = f0[: len(duration)]
    energy = energy[: len(duration)]

    # Save wav
    wav_filename = "{}-wav-{}.wav".format(hp.dataset, basename)
    sf.write(os.path.join(out_dir, "wav", wav_filename), wav, hp.sampling_rate)
    

    # Save alignment
    ali_filename = "{}-ali-{}.npy".format(hp.dataset, basename)
    np.save(
        os.path.join(out_dir, "alignment", ali_filename), duration, allow_pickle=False
    )

    # Save fundamental prequency
    f0_filename = "{}-f0-{}.npy".format(hp.dataset, basename)
    np.save(os.path.join(out_dir, "f0", f0_filename), f0, allow_pickle=False)

    # Save energy
    energy_filename = "{}-energy-{}.npy".format(hp.dataset, basename)
    np.save(
        os.path.join(out_dir, "energy", energy_filename), energy, allow_pickle=False
    )

    # Save spectrogram
    mel_filename = "{}-mel-{}.npy".format(hp.dataset, basename)
    np.save(
        os.path.join(out_dir, "mel", mel_filename),
        mel_spectrogram.T,
        allow_pickle=False,
    )
    # exit()

    return (
        "|".join([basename, speaker, text]),
        remove_outlier(f0),
        remove_outlier(energy),
        max(f0),
        min([f for f in f0 if f != 0]),
        max(energy),
        min(energy),
        mel_spectrogram.shape[1],
    )


def get_alignment(tier):
    sil_phones = ["sil", "sp", "spn", '']
    punctuation_phones = [ ',', '.']

    phones = []
    durations = []
    durations_real = []
    durations_int = []
    start_time = 0
    end_time = 0
    end_idx = 0

    pre_phone = ''
    cur_phone = ''
    for t in tier._objects:
        s, e, p = t.start_time, t.end_time, t.text

        p_dur_time = int(
                np.round(e * hp.sampling_rate / hp.hop_length)
                - np.round(s * hp.sampling_rate / hp.hop_length)
            )

        # Trimming leading silences
        if phones == []:
            if p in sil_phones:
                continue
            else:
                start_time = s

        if p not in sil_phones:
            # 当前phone非sil_phone, 判断前一个phone是不是sil_phone的情况
            if phones and phones[-1] in sil_phones:  
                # 若前一phone为sil_phoen, 且市场大于15帧， 那么将前一个phone转为，
                if durations[-1]  > 15:
                    phones[-1] = ','
                # 若前一phone为sil_phoen, 且市场小于15帧， 那么需要将前一个sil的时间与前前一个phone进行合并
                else: 
                    phones.pop()
                    pre_sil_phone_time = durations.pop()
                    durations[-1] += pre_sil_phone_time

            phones.append(p)
            
            
        # 当前phone为sil_phone, 判断前一个phone是不是sil_phone的情况
        else:
            # 若前一phone为sil_phone
            if phones and phones[-1] in sil_phones:
                # 那么需要将两个连续出现的sil_phone合并为一个标点
                phones.pop()
                p_dur_time += durations.pop()
                p = ',' if p == 'sp' else '.'
            # 若前一phone为punctuation_phone
            elif phones and phones[-1] in punctuation_phones:
                # 那么需要将当前的sil_phone和之前的标点符号合并
                p = phones.pop()
                p_dur_time += durations.pop()
            else:
                pass


            phones.append(p)

        durations.append(p_dur_time)
        end_time = e
        end_idx = len(phones)


    # Trimming tailing silences
    phones = phones[:end_idx]
    durations = durations[:end_idx]

    return phones, durations, start_time, end_time


def remove_outlier(values):
    p25 = np.percentile(values, 25)
    p75 = np.percentile(values, 75)
    lower = p25 - 1.5 * (p75 - p25)
    upper = p75 + 1.5 * (p75 - p25)
    normal_indices = np.logical_and(values > lower, values < upper)
    return values[normal_indices]


def normalize(in_dir, mean, std):
    max_value = -100
    min_value = 100
    for filename in os.listdir(in_dir):
        filename = os.path.join(in_dir, filename)
        values = (np.load(filename) - mean) / std
        np.save(filename, values, allow_pickle=False)

        max_value = max(max_value, max(values))
        min_value = min(min_value, min(values))

    return min_value, max_value


if __name__ == "__main__":
    print('OK')