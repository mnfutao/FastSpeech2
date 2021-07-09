import os


# Dataset
dataset = "M2VoC"
aishell3_path = "./AISHELL-3"
m2voc_path = "./M2VoC"

text_cleaners = []
language = "zh"


# Some paths
raw_path = os.path.join("./raw_data/", dataset) # ./raw_data/M2VoC
preprocessed_path = os.path.join("./preprocessed_data/", dataset) # ./preprocessed_data/M2VoC
checkpoint_path = os.path.join("./ckpt/", dataset) # ./ckpt/M2VoC
synth_path = os.path.join("./synth/", dataset)  # ./synth/M2VoC
log_path = os.path.join("./log/", dataset)  # ./log/M2VoC
test_path = os.path.join("./results/", dataset) # ./results/M2VoC


# Audio and mel
sampling_rate = 22050
filter_length = 1024
hop_length = 256
win_length = 1024

preemph = 0.0
max_wav_value = 32768.0
n_mel_channels = 80
mel_fmin = 0.0
mel_fmax = 8000


# FastSpeech 2
encoder_layer = 4
encoder_head = 2
encoder_hidden = 256
decoder_layer = 6
decoder_head = 2
decoder_hidden = 256
fft_conv1d_filter_size = 1024
fft_conv1d_kernel_size = (9, 1)
encoder_dropout = 0.2
decoder_dropout = 0.2

variance_predictor_filter_size = 256
variance_predictor_kernel_size = 3
variance_predictor_dropout = 0.5

max_seq_len = 1000


#total time: 79.87095832703453 hours
#Total frames: 24766237
#Mean F0: 241.91543808941768
#Stdev F0: 89.42275421804817
#Min F0: -2.025137235699036
#Max F0: 6.49714096696279
#Min energy: -1.4232845306396484
#Max energy: 8.448925018310547


# Quantization for F0 and energy
f0_min = -2.025137235699036
f0_max = 6.49714096696279
energy_min = -1.4232845306396484
energy_max = 8.448925018310547

# For plotting F0 curves
f0_mean = 241.91543808941768
f0_std = 89.42275421804817

n_bins = 256


# Optimizer
batch_size = 16
epochs = 5000
n_warm_up_step = 4000
grad_clip_thresh = 1.0
acc_steps = 1

betas = (0.9, 0.98)
eps = 1e-9
weight_decay = 0.0

aneal_steps = [300000, 400000, 500000]
aneal_rate = 0.3

# Log-scaled duration
log_offset = 1.0


# Save, log and synthesis
save_step = 50000
synth_step = 1000
log_step = 1000
clear_Time = 20

# Pretrained speaker representations
d_vec_size = 128
x_vec_size = 128
adain_emb_size = 128


# Jointly optimized speaker representations
speaker_emb_size = 128

# GST
ref_filters = [32, 32, 64, 64, 128, 128]
ref_gru_hidden = 128
gst_size = 128
n_style_token = 10
n_style_attn_head = 4
