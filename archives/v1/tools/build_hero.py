#!/usr/bin/env python3
"""
Build the v1 hero band from a tall portrait photograph.

A portrait source cropped to a wide band keeps either the peak or the water,
never both. So: fit the FULL frame by height and centre it, sharp and unblurred,
and fill the flanks with a deep tone sampled from the photo itself. The section's
black overlay then covers the whole band uniformly.

If a LANDSCAPE source is supplied, this padding is unnecessary — the photo will
simply fill the band edge to edge.

Usage:  python3 tools/build_hero.py <source.jpg>
"""
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import sys, os

W, H = 2600, 1500
FEATHER = 300

def build(src_path, out_path='img/hero-mountains.jpg'):
    src = Image.open(src_path).convert('RGB')
    if src.width / src.height >= 1.2:
        # Landscape: cover-crop to fill the band edge to edge, no padding at all.
        # Bias the crop upward so more sky is kept behind the headline.
        sc = max(W / src.width, H / src.height)
        big = src.resize((int(src.width * sc), int(src.height * sc)), Image.LANCZOS)
        left = (big.width - W) // 2
        top = int((big.height - H) * 0.38)
        canvas = big.crop((left, top, left + W, top + H))
    else:
        # Portrait source: fit by height, sharp and centred, and pad the flanks
        # with a deep tone sampled from the photo itself.
        core = src.resize((max(1, int(src.width * H / src.height)), H), Image.LANCZOS)
        edge = src.resize((40, 24)).getpixel((1, 1))
        canvas = Image.new('RGB', (W, H), tuple(int(c * 0.35) for c in edge))
        canvas.paste(core, ((W - core.width) // 2, 0))
    canvas.save(out_path, quality=92)
    print(f'{out_path}  {canvas.size}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    build(sys.argv[1])
