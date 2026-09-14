#!/usr/bin/env python3
"""Convert word-timed karaoke ASS into a base-white + animated yellow glow track."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from PIL import ImageFont

DIALOGUE = re.compile(r"^Dialogue: \d+,([0-9:.]+),([0-9:.]+),([^,]+),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)$")
KARAOKE = re.compile(r"\{\\kf(\d+)\}([^{}]+)")
POS = re.compile(r"\\pos\((\d+),(\d+)\)")
TAG = re.compile(r"\{[^}]*\}")

def as_seconds(value: str) -> float:
    h, m, s = value.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def ass_time(seconds: float) -> str:
    seconds = max(0, seconds)
    h, seconds = divmod(seconds, 3600)
    m, seconds = divmod(seconds, 60)
    return f"{int(h)}:{int(m):02d}:{seconds:05.2f}"

def esc(text: str) -> str:
    return text.replace('\\', r'\\').replace('{', r'\{').replace('}', r'\}')

def font():
    # Match libass's available fallback in minimal Linux render environments.
    for path in ['/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf']:
        if Path(path).exists(): return ImageFont.truetype(path, 54)
    raise SystemExit('No usable sans-serif caption font found')

def word_width(f, word):
    return f.getlength(word)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    source = args.input.read_text()
    header = source.split('[Events]')[0]
    # Crisp yellow foreground plus a blurred, low-opacity duplicate creates the glow.
    header = header.replace('Style: Default,DejaVu Sans,54,&H0000FFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4.0,2.0,5,90,90,60,1',
'''Style: Base,Noto Sans,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4.0,2.0,5,90,90,60,1
Style: Glow,Noto Sans,54,&H0000FFFF,&H0000FFFF,&H0000FFFF,&HFF000000,-1,0,0,0,100,100,1,0,1,8.0,0.0,5,90,90,60,1
Style: Active,Noto Sans,54,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4.0,2.0,5,90,90,60,1''')
    out = [header, '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    f = font()
    for raw in source.split('[Events]', 1)[1].splitlines():
        match = DIALOGUE.match(raw)
        if not match: continue
        start, end, _style, body = match.groups()
        pos_match = POS.search(body)
        cx, y = map(float, pos_match.groups()) if pos_match else (960.0, 930.0)
        chunks = KARAOKE.findall(body)
        if not chunks: continue
        # The permanently visible base line stays white. It must not contain karaoke tags.
        base = TAG.sub('', body).replace(r'\N', r'\N')
        out.append(f'Dialogue: 0,{start},{end},Base,,0,0,0,,{{\\an5\\pos({cx:.0f},{y:.0f})\\q2}}{base}')
        # Build x-centres separately for each rendered line.
        lines = []
        current = []
        for duration, token in chunks:
            if r'\N' in token:
                before, after = token.split(r'\N', 1)
                if before: current.append((duration, before))
                lines.append(current); current = []
                if after: current.append((duration, after))
            else: current.append((duration, token))
        lines.append(current)
        line_y = [y - 34, y + 34] if len(lines) == 2 else [y]
        time_cursor = as_seconds(start)
        for line_index, line in enumerate(lines):
            clean_words = [re.sub(r'\s+', ' ', w).strip() for _, w in line]
            widths = [word_width(f, w) for w in clean_words]
            total = sum(widths) + max(0, len(widths) - 1) * word_width(f, ' ')
            x = cx - total / 2
            for (duration_cs, _raw_word), word, width in zip(line, clean_words, widths):
                duration = int(duration_cs) / 100
                word_start, word_end = time_cursor, time_cursor + duration
                word_cx = x + width / 2
                # 110 ms entrance + short settle, then a 120 ms fade away.
                glow = (f'{{\\an5\\pos({word_cx:.1f},{line_y[line_index]:.1f})\\1a&H88&\\blur(9)'
                        f'\\t(0,110,\\1a&H22&\\blur(14)\\fscx(116)\\fscy(116))'
                        f'\\t({max(0,int(duration*1000-130))},{int(duration*1000)},\\1a&HFF&)}}{esc(word)}')
                active = (f'{{\\an5\\pos({word_cx:.1f},{line_y[line_index]:.1f})\\1a&HFF&'
                          f'\\t(0,110,\\1a&H00&\\fscx(112)\\fscy(112))'
                          f'\\t(110,220,\\fscx(100)\\fscy(100))'
                          f'\\t({max(0,int(duration*1000-120))},{int(duration*1000)},\\1a&HFF&)}}{esc(word)}')
                out.append(f'Dialogue: 2,{ass_time(word_start)},{ass_time(word_end)},Glow,,0,0,0,,{glow}')
                out.append(f'Dialogue: 3,{ass_time(word_start)},{ass_time(word_end)},Active,,0,0,0,,{active}')
                x += width + word_width(f, ' ')
                time_cursor = word_end
    args.output.write_text('\n'.join(out) + '\n')

if __name__ == '__main__': main()
