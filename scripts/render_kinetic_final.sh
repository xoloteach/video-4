#!/usr/bin/env bash
# Rebuild the final video with animated captions.
set -euo pipefail
cd "$(dirname "$0")/.."

FONTS_DIR="/home/xoloteach/.local/share/fonts"

ffmpeg -y \
  -f concat -safe 0 -i full-timeline.txt \
  -i voiceover.mp3 \
  -filter_complex "[0:v]scale=1920:1080,fps=24,subtitles=captions.ass:fontsdir=${FONTS_DIR}[v];[1:a]apad=whole_dur=533.544[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart final/final.mp4

cp final/final.mp4 final/final-kinetic-captions.mp4
echo "==> Render completed: final/final.mp4 and final/final-kinetic-captions.mp4"
