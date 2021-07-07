import os

import hparams as hp
from data.utils import build_from_path


def write_metadata(train, out_dir):
    with open(os.path.join(out_dir, "train.txt"), "w", encoding="utf-8") as f:
        for m in train:
            f.write(m + "\n")


def main():
    in_dir = hp.raw_path # ./raw_data/M2VoC
    out_dir = hp.preprocessed_path  # ./preprocessed_data/M2VoC

    wav_out_dir = os.path.join(out_dir, "wav")  # ./preprocessed_data/M2VoC/mel
    if not os.path.exists(wav_out_dir):
        os.makedirs(wav_out_dir, exist_ok=True)
    mel_out_dir = os.path.join(out_dir, "mel")  # ./preprocessed_data/M2VoC/mel
    if not os.path.exists(mel_out_dir):
        os.makedirs(mel_out_dir, exist_ok=True)
    ali_out_dir = os.path.join(out_dir, "alignment")    # ./preprocessed_data/M2VoC/alignment
    if not os.path.exists(ali_out_dir):
        os.makedirs(ali_out_dir, exist_ok=True) # ./preprocessed_data/M2VoC/f0
    f0_out_dir = os.path.join(out_dir, "f0")    
    if not os.path.exists(f0_out_dir):
        os.makedirs(f0_out_dir, exist_ok=True)
    energy_out_dir = os.path.join(out_dir, "energy") # ./preprocessed_data/M2VoC/energy
    if not os.path.exists(energy_out_dir):
        os.makedirs(energy_out_dir, exist_ok=True)

    train = build_from_path(in_dir, out_dir)
    write_metadata(train, out_dir)


if __name__ == "__main__":
    main()
