#!/bin/bash

# Load environment variables
set -o allexport
source .env
set +o allexport

# Remove existing sample_data directory and create a new one
rm -rf /content/sample_data
mkdir /content/sample_data

# Clone the Wav2Lip repository
git clone https://github.com/zabique/Wav2Lip

# Download the pretrained model
wget "$CHECKPOINT_URL" -O '/content/Wav2Lip/checkpoints/wav2lip_gan.pth'

# Install additional dependencies
pip install https://raw.githubusercontent.com/AwaleSajil/ghc/master/ghc-1.0-py3-none-any.whl
pip install -r Wav2Lip/requirements.txt
wget "$FACE_DETECTION_MODEL_URL" -O "/content/Wav2Lip/face_detection/detection/sfd/s3fd.pth"
pip install -q youtube-dl ffmpeg-python librosa==0.9.1
