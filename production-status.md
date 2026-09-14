# Production Status — Video 4

**Channel:** Why We Become  
**Input mode:** Title + Script  
**Locked title:** How the Self-Improvement Industry Made You Hate Yourself  
**Target Resolution:** 1920×1080 (1080p)

## Runtime & sheet calculation

```
word_count        = 1314
char_count        = 8008
estimated_seconds = 1314 ÷ 2.5 = 525.6 s (~8 min 45 s)
target_frames     = round(525.6 ÷ 2.1) = 250 frames
target_sheets     = ceil(250 ÷ 9) = 28 sheets
clamped_sheets    = 28 (min 16, max 48)
frame_pool        = 28 × 9 = 252 frames
```

## Narration split

```
parts = max(5, ceil(8008 ÷ 1800)) = 5
```

| File | Characters | Words | Under 2,000 | Status |
|---|---:|---:|---|---|
| narration-01.txt | 1716 | 280 | PASS | Ready |
| narration-02.txt | 1531 | 246 | PASS | Ready |
| narration-03.txt | 1608 | 268 | PASS | Ready |
| narration-04.txt | 1593 | 267 | PASS | Ready |
| narration-05.txt | 1552 | 253 | PASS | Ready |

## Status log
- [x] Initialized `video 4/` workspace
- [x] Saved validated script with requested canonical ending
- [x] Generated source log and evidence notes in `research.md`
- [x] Generated SEO package with ≤4-word thumbnail hook in `seo.md`
- [x] Calculated 28 contact sheets (252 frame pool)
- [x] Narration split into 5 balanced sequential files (<2,000 chars)
- [ ] Deepgram TTS audio synthesis (flux-miles-en) and verification
- [ ] 48 kHz mono normalization + concat + loudness normalization (-16 LUFS)
- [ ] Deepgram Nova-3 STT word timing generation (`voiceover.json`)
- [x] 28 contact-sheet prompts drafted in `generation-status.md`
- [x] Mandatory User Approval Gate received
- [x] 28 contact sheets generated and normalized to 1680×945
- [x] 252 panels cropped to numbered 1920×1080 frames
- [x] ASS word-timed karaoke captions generated and validated (1920×1080, yellow/white flow)
- [x] Shot list created in `manifest.csv` and `frames.txt`
- [x] 1080p video assembled with canonical 9-second end card
- [x] Final thumbnail generated
- [x] Final QA gate verification in `observer-log.md`
