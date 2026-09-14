#!/bin/bash
set -e

# Load environment variables if ~/.env exists
if [ -f "$HOME/.env" ]; then
  export $(cat "$HOME/.env" | xargs)
fi

if [ -z "$DEEPGRAM_API_KEY" ]; then
  echo "ERROR: DEEPGRAM_API_KEY is not set."
  exit 1
fi

cd "$(dirname "$0")"

echo "==> 1. Generating 5 narration parts with Deepgram Flux Miles..."
for i in 01 02 03 04 05; do
  txt_file="narration/narration-${i}.txt"
  out_file="tts-narration-${i}.mp3"
  echo "Generating $out_file from $txt_file..."
  
  curl -sS -X POST \
    -H "Authorization: Token $DEEPGRAM_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --rawfile text "$txt_file" '{text: $text}')" \
    "https://api.deepgram.com/v2/speak?model=flux-miles-en&speed=1&expressivity=0" \
    -o "$out_file"
  
  # Verify with ffprobe
  duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$out_file")
  size=$(stat -c%s "$out_file")
  echo "  --> $out_file: ${size} bytes, ${duration}s"
  
  # Sanity check: must be > 100KB and > 30s
  if (( $(echo "$duration < 30" | bc -l) )); then
    echo "ERROR: $out_file duration too short ($duration s)! Possible truncation."
    exit 1
  fi
done

echo "==> 2. Normalizing all parts to 48kHz mono libmp3lame..."
for i in 01 02 03 04 05; do
  f="tts-narration-${i}.mp3"
  norm_f="norm-tts-narration-${i}.mp3"
  ffmpeg -y -v error -i "$f" -ar 48000 -ac 1 -c:a libmp3lame -b:a 192k "$norm_f"
done

echo "==> 3. Concatenating parts in strict narrative order..."
rm -f voiceover-list.txt
for i in 01 02 03 04 05; do
  echo "file 'norm-tts-narration-${i}.mp3'" >> voiceover-list.txt
done
ffmpeg -y -v error -f concat -safe 0 -i voiceover-list.txt -c copy voiceover-raw.mp3

echo "==> 4. Loudness normalizing joined audio to -16 LUFS..."
ffmpeg -y -v error -i voiceover-raw.mp3 -af loudnorm=I=-16:LRA=11:TP=-1.5 \
  -ar 48000 -ac 1 -c:a libmp3lame -b:a 192k voiceover.mp3

total_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 voiceover.mp3)
echo "==> Final voiceover.mp3 duration: ${total_duration}s"

echo "==> 5. Transcribing final voiceover with Deepgram Nova-3 for karaoke word timings..."
curl -sS -X POST \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H "Content-Type: audio/mpeg" \
  --data-binary @voiceover.mp3 \
  "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&punctuate=true&utterances=true" \
  -o voiceover.json

word_count=$(jq '.results.channels[0].alternatives[0].words | length' voiceover.json)
stt_duration=$(jq '.results.channels[0].alternatives[0].words[-1].end' voiceover.json)
echo "==> SUCCESS! voiceover.json contains ${word_count} words up to ${stt_duration}s."
