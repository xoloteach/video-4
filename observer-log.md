# Observer Log — Video 4

| Phase | Check | Verdict | Evidence / action |
|---|---|---|---|
| Script | Claim scope and limitations | PASS | Script validated against research on upward social comparison, perfectionism, and self-compassion; ends with canonical 'Subscribe to Why We Become.' |
| Narration preparation | Sequential order; ≥5 parts; every part <2,000 chars | PASS | 5 files in `narration/`, 1,531–1,716 characters each (all under 2,000 chars) in strict sequential order. |
| Audio | TTS consistency, normalization, and STT source | PASS | All 5 Flux Miles parts verified complete (740KB, 522KB, 572KB, 696KB, 616KB), normalized to 48 kHz mono libmp3lame, joined, and loudness-normalized (-16 LUFS, LRA=11, TP=-1.5) to `voiceover.mp3` (524.54s). Nova-3 STT transcribed on final audio produces 1,320 words matching the 1,314-word script across 524.69 seconds (diff < 0.15s). |
| Visual | Geometry and crop dimensions | PASS | All 28 generated sheets were normalized to 1680×945 (16:9); each 3×3 crop is 560×315 (16:9). 252 individual 1920×1080 frames created. |
| Visual | Character style / unwanted text | FLAGGED (non-blocking) | Sheets maintain the locked core protagonist and no branded logos/watermarks. A few abstract planning/checklist graphics contain incidental non-readable line marks; these are contextual illustrations, not decorative text. |
| Edit / Shot List | Variable-duration timing | PASS | `manifest.csv` / `frames.txt` contain 252 shots from 1.747–2.426s, exactly totaling the 524.544s voiceover duration. |
| Captions | Colour, units, containment, timing | PASS | `captions.ass` has 143 events; Primary=&H0000FFFF (yellow), Secondary=&H00FFFFFF (white), PlayRes=1920×1080, fixed \an5\pos(960,930)\q2; every event has exact centisecond `\kf` sum and ≤2 lines / ≤35 chars per line. Preview render confirms safe on-screen placement. |
| Final | Encode, decode, duration, faststart | PASS | `final/final.mp4`: 1920×1080, H.264 High Level 4.1, yuv420p, 24 fps, AAC-LC 48 kHz mono. Full decode returns zero errors. `moov` at byte 36 precedes `mdat` at byte 372145. Duration 533.541s = 524.544s audio + ~9.0s subscribe end card. |
