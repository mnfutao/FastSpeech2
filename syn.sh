#!/bin/bash
rm results/M2VoC/*
# python generate.py --speaker  tutor_ldd --source results/data.list --step 750000  --speaker_emb --x_vec
python generate.py --speaker  tutor_lq --source results/data.list --step 750000  --speaker_emb --x_vec
# python generate.py --speaker  tutor_lfq --source results/data.list --step 750000  --speaker_emb --x_vec
# python generate.py --speaker  tutor_dy --source results/data.list --step 750000  --speaker_emb --x_vec
# python generate.py --speaker  yaya --source results/data.list --step 750000  --speaker_emb --x_vec
# python generate.py --speaker  snowball_v2 --source results/data.list --step 750000  --speaker_emb --x_vec
# python generate.py --speaker  snowball_newer --source results/data.list --step 750000  --speaker_emb --x_vec
# python generate.py --speaker  speechocean_man10h --source results/data.list --step 750000  --speaker_emb --x_vec
