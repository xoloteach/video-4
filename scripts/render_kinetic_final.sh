#!/usr/bin/env bash
# Rebuild the final video from the original frames/audio with kinetic captions.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_kinetic_captions.py captions.ass captions-kinetic.ass
ffmpeg -y \
  -f concat -safe 0 -i frames.txt \
  -loop 1 -t 9 -i subscribe-end-card.jpeg \
  -i voiceover.mp3 \
  -filter_complex "[0:v]fps=24,scale=1920:1080,format=yuv420p[main];[1:v]scale=1920:1080,format=yuv420p[end];[main][end]concat=n=2:v=1:a=0,subtitles=captions-kinetic.ass:fontsdir=/usr/share/fonts/google-noto-vf[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart final/final-kinetic-captions.mp4
