# -*- coding: utf-8 -*-
"""
Main script for Wav2Lip-Sync
"""

import os
import numpy as np
import scipy.io.wavfile as wavfile
from dotenv import load_dotenv
from utils import get_audio, upload_video, process_video

# Load environment variables
load_dotenv()

# Step 1: Record audio
rate, data = get_audio()
wavfile.write('/content/sample_data/input_audio.wav', rate, data)

# Step 2: Upload your input video
upload_video()

# Step 3: Process the video and audio
process_video()

# Step 4: Variations to try
resize_factor = input("Enter resize factor (default 1): ") or "1"
padding = input("Enter padding (default 0 20 0 0): ") or "0 20 0 0"

# Resize video resolution
os.system(f'cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "/content/sample_data/input_video.mp4" --audio "/content/sample_data/input_audio.wav" --resize_factor {resize_factor}')

# More padding
os.system(f'cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "/content/sample_data/input_video.mp4" --audio "/content/sample_data/input_audio.wav" --pads {padding}')
