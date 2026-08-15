#!/usr/bin/env python3
"""
Build the per-device portfolio artwork for v2.

v2's portfolio rows are FULL WIDTH and stacked, and the phone variant
stair-steps up to four devices at 26% width each, every one 15px lower than the
last. v1's 1280x800 gradient cards are the wrong shape and the wrong
composition for that, so nothing from v1/img is reused here.

Adapted from `archives/v1/tools/build_cards.py`. What carried over: the
transparent-mock path, the flat-background flood key, the gradient-aware key,
watch detection, and the "equal size, evenly spaced, never overlapping" rule.
What changed: the output is ONE DEVICE PER FILE on a transparent canvas, not a
composite card on a gradient.

Every device is written onto the SAME canvas size, so the four `<img>` elements
in a row are identical boxes and the 15px stair-step lands exactly where the CSS
says it does. Phones fill the canvas height. A watch is detected by aspect ratio
and scaled down inside the same canvas rather than stretched to phone height.

Shadows are NOT baked in. The page applies `filter: drop-shadow(...)`, which
follows the device silhouette instead of a rectangle.

Output is WebP, not PNG. These are photographic screenshots that need an alpha
channel, and PNG cannot do both: the same 28 files come out at 12 MB as PNG and
1.2 MB as WebP at quality 82, with no visible difference at any zoom. A 256
colour PNG was tried first and bands badly in every sky and gradient.

PII: three screens carry Asad's real personal data. The already-redacted copies
in `archives/v1/img/src/` (mosaic-then-blur, never blur alone) are used in place
of the originals and are listed in REDACTED below.

Usage:  python3 tools/build_devices.py
Output: img/portfolio/<slug>/<slug>-1.webp ... -4.webp
"""
from PIL import Image, ImageFilter
import os
import sys

# One canvas for every device. Roughly an iPhone 15 Pro Max transparent frame,
# which is what most of the source mocks are.
CANVAS = (660, 1360)
FILL = 0.98          # phones use this much of the canvas height
WATCH_SCALE = 0.62   # a watch inside the same canvas
WATCH_ASPECT = 0.55  # phones sit near 0.49, watches near 0.61
QUALITY = 82         # WebP, alpha preserved

OUT_ROOT = 'img/portfolio'

T = os.path.expanduser('~/Documents/Career/Other Docs/Mocks')
F = os.path.expanduser('~/Documents/Business/Freelancer.com/Mocups')
U = os.path.expanduser('~/Documents/Business/upwork/Mockups')
V1SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     '..', 'v1', 'img', 'src')

# Screens that were caught carrying Asad's real personal data. Always the
# redacted copy, never the original.
REDACTED = {
    'votari-2':  os.path.join(V1SRC, 'votari-passport-redacted.png'),   # passport photo, number, name, DOB
    'pryvate-2': os.path.join(V1SRC, 'pryvate-number-redacted.png'),    # real mobile number
    'hiiker-1':  os.path.join(V1SRC, 'hiiker-email-redacted.png'),      # real name and email
    'pryvate-4': 'img/src/pryvate-chats-redacted.png',                  # two numbers, a contact name, a face
    'officetree-4': 'img/src/officetree-recent-redacted.png',           # a contact name x2, six numbers
}

# slug -> list of source paths. The index here only fixes the FILENAME suffix
# (-1 .. -4); the left-to-right order in a row is set by the order of the <img>
# tags in index.html, so a row can be re-sequenced without rebuilding artwork.
PROJECTS = [
    ('athanify', [
        f'{T}/Athanify/qibla-ar.png',
        f'{T}/Athanify/makkah-hero-light.png',
        f'{T}/Athanify/sleep-stories-1.png',
        f'{T}/Athanify/(4-last) screen-time-2.png',
    ]),
    ('shelly', [
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9914-portrait.png',
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9915-portrait.png',
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9916-portrait.png',
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/(4-End) IMG_0447-portrait.png',
    ]),
    ('peptify', [
        f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9903-portrait.png',
        f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9905-portrait.png',
        f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9906-portrait.png',
        f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/(4-End) IMG_0450-portrait.png',
    ]),
    # 4 devices: three phones then the Apple Watch companion
    ('hiiker', [
        REDACTED['hiiker-1'],
        f'{F}/Hiiker/IMG_6967-portrait.png',
        f'{F}/Hiiker/IMG_6969-portrait.png',
        f'{T}/Hiiker/incoming-C41FF231-17E7-48F8-8593-320A66181E79-portrait.png',
    ]),
    ('votari', [
        f'{T}/(Votari) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9918-portrait.png',
        REDACTED['votari-2'],
        f'{T}/(Votari) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9898-portrait.png',
        f'{T}/(Votari) apple-iphone-15-pro-max-white-titanium-mockup/(4-End) IMG_0454-portrait.png',
    ]),
    ('pryvate', [
        f'{T}/(Pryvate) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9893-portrait.png',
        REDACTED['pryvate-2'],
        f'{T}/(Pryvate) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9896-portrait.png',
        REDACTED['pryvate-4'],
    ]),
    ('officetree', [
        f'{F}/Offietree/1_Officetree_Home.png',
        'img/src/officetree-text-redacted.png',       # seven sender numbers mosaicked out
        'img/src/officetree-voicemail-redacted.png',  # attendant direct number mosaicked out
        REDACTED['officetree-4'],
    ]),
    ('block', [
        f'{T}/Block/1. 460x996bb-portrait.png',
        f'{T}/Block/2. 460x996bb-portrait.png',
        f'{T}/Block/3. 460x996bb -portrait.png',
        f'{T}/Block/(4-End) IMG_0465-portrait.png',
    ]),
    ('planthealth', [
        f'{T}/PLant Health/IMG_0353-portrait.png',
        # IMG_9174 shipped as flat RGB on black and the phone bezel is the same
        # black, so an edge key eats the frame. v1 solved it with a content-box
        # crop plus a rounded-rect alpha mask; that result is reused verbatim.
        os.path.join(V1SRC, 'planthealth-diagnosis.png'),
        f'{T}/PLant Health/IMG_8989-portrait.png',
        f'{T}/PLant Health/(4-End) IMG_0451-portrait.png',
    ]),
]


def trim_alpha(im):
    bb = im.split()[-1].getbbox()
    return im.crop(bb) if bb else im


def key_out(im, tol=42):
    """Flood the mockup's own background to transparent from all four edges.
    Only needed for sources that are NOT already RGBA with real alpha."""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    seeds = []
    for x in range(0, w, max(1, w // 60)):
        seeds += [(x, 0), (x, h - 1)]
    for y in range(0, h, max(1, h // 60)):
        seeds += [(0, y), (w - 1, y)]
    bgs = [px[s][:3] for s in seeds[:8]]
    bg = tuple(sorted(c[i] for c in bgs)[len(bgs) // 2] for i in range(3))

    alpha = Image.new('L', (w, h), 255)
    ap = alpha.load()
    stack, seen = list(seeds), set()
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        r, g, b, _ = px[x, y]
        if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > tol:
            continue
        ap[x, y] = 0
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    im.putalpha(alpha.filter(ImageFilter.GaussianBlur(0.6)))
    return im


def load_device(path):
    """Return a trimmed RGBA device. Sources with real alpha are used as-is;
    anything opaque is flood-keyed from the edges first."""
    im = Image.open(path)
    if im.mode != 'RGBA' or im.split()[-1].getextrema()[0] == 255:
        im = key_out(im)
    else:
        im = im.convert('RGBA')
    return trim_alpha(im)


def place(dev):
    """Centre one device on the shared canvas at the right scale for its type."""
    cw, ch = CANVAS
    is_watch = dev.width / dev.height > WATCH_ASPECT
    target_h = ch * FILL * (WATCH_SCALE if is_watch else 1.0)
    sc = min(target_h / dev.height, cw * FILL / dev.width)
    dev = dev.resize((max(1, int(dev.width * sc)), max(1, int(dev.height * sc))), Image.LANCZOS)
    canvas = Image.new('RGBA', CANVAS, (0, 0, 0, 0))
    canvas.paste(dev, ((cw - dev.width) // 2, (ch - dev.height) // 2), dev)
    return canvas, is_watch


def build(slug, srcs):
    out_dir = os.path.join(OUT_ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    n = 0
    for i, src in enumerate(srcs, start=1):
        if not os.path.exists(src):
            print(f'  !! MISSING {slug}-{i}: {src}', file=sys.stderr)
            continue
        canvas, is_watch = place(load_device(src))
        out = os.path.join(out_dir, f'{slug}-{i}.webp')
        canvas.save(out, format='WEBP', quality=QUALITY, method=6)
        n += 1
        print(f'  {slug}-{i}.webp  {"watch" if is_watch else "phone"}  <- {os.path.basename(src)}')
    return n


if __name__ == '__main__':
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(here)
    print('building device artwork:')
    total = 0
    for slug, srcs in PROJECTS:
        total += build(slug, srcs)
    print(f'{total} device images written to {OUT_ROOT}/')
