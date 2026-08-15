#!/usr/bin/env python3
"""
Build the featured-project device art for archives/v3.

Adapted from archives/v1/tools/build_cards.py. Read that file first — the
keying, watch detection and layout maths all come from it.

WHY THIS IS NOT build_cards.py
------------------------------
v1 composites each project into ONE 1280x800 card sitting on a dark navy
gradient. v3 cannot use those:

  1. v3's featured row is `.project__pic.phones` — a flex row of three SEPARATE
     `.phone` elements pulled together by `margin: 0 -7%`. The tucking is done
     in CSS, so the art has to arrive as three individual devices, not as one
     pre-composed strip.
  2. v3's default theme is LIGHT. A dark navy gradient baked into the PNG would
     sit as a heavy rectangle on a white page.

So this script outputs TRANSPARENT devices with no background at all. The page
ground shows through — white in the light theme, #171c28 in `body.night`.

RULES CARRIED OVER FROM v1 (see ~/.claude/CLAUDE.md)
  - Real transparent RGBA device mocks are the ONLY source used here. Nothing is
    keyed, nothing is guessed. If a project has no transparent mock, it does not
    go in the featured row.
  - Devices are equal size, evenly spaced and never overlapping IN THE ART. The
    only tucking is the -7% CSS margin, which is v3's own published design.
  - No re-framing: no panel, no rounded card, no drop shadow, no second layer.
  - PII: three screens carry Asad's real data and are replaced by the
    mosaic-then-blur copies in archives/v1/img/src/. Never point at the originals.

Usage:  python3 archives/v3/tools/build_devices.py
"""
from PIL import Image
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
V1 = os.path.join(os.path.dirname(V3), 'v1')
OUT = os.path.join(V3, 'img', 'featured')

# Rendered width of one .phone is roughly 240 CSS px at the 1440 breakpoint.
# 900px of art is ~3.7x that, which survives a 3x display with room to spare and
# still keeps each file in the low hundreds of KB.
DEVICE_H = 900

# Fraction of the canvas width the device itself occupies. Measured off the
# original v3 phone plates (326px of device on a 532px canvas = 0.613), because
# `.phones` overlaps the CANVASES by design and relies on that clear margin.
DEVICE_FRAC = 0.613

T = os.path.expanduser('~/Documents/Career/Other Docs/Mocks')
F = os.path.expanduser('~/Documents/Business/Freelancer.com/Mocups')
SRC = os.path.join(V1, 'img', 'src')          # the PII-redacted copies

# Screens are listed left to right, exactly as they appear in the row.
# The lead screen of each set is deliberately the most colourful one — on a white
# ground a near-white app screen collapses into the page and only the rim reads.
PROJECTS = {
    'athanify': [
        f'{T}/Athanify/qibla-ar.png',
        f'{T}/Athanify/makkah-hero-light.png',
        f'{T}/Athanify/sleep-stories-1.png',
    ],
    'shelly': [
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9914-portrait.png',
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9915-portrait.png',
        f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9916-portrait.png',
    ],
    # The third HiiKER slot is the Apple Watch, not a third phone. The watch is
    # the part of HiiKER that actually earns the "works where the signal does
    # not" claim, and a watch beside two phones reads as a platform rather than
    # as three screenshots. is_watch() catches it on aspect (0.606 > 0.55) and
    # scales it down instead of stretching it to phone height.
    'hiiker': [
        f'{F}/Hiiker/IMG_6967-portrait.png',
        f'{SRC}/hiiker-email-redacted.png',      # PII: real name + email address
        f'{T}/Hiiker/incoming-C41FF231-17E7-48F8-8593-320A66181E79-portrait.png',
    ],
}

# Sources that must NEVER be referenced directly — the redacted copy above stands
# in for each. Guarded rather than commented, so a future edit cannot quietly
# reintroduce one.
PII_ORIGINALS = {
    'IMG_9907-portrait.png',   # Votari passport
    'IMG_9894-portrait.png',   # Pryvate real mobile number
    'IMG_6966-portrait.png',   # Hiiker real name + email
}


def is_watch(im):
    """Phones sit near 0.49, watches near 0.61. Carried over from v1."""
    return im.width / im.height > 0.55


def build(name, sources):
    for s in sources:
        if os.path.basename(s) in PII_ORIGINALS:
            sys.exit(f'REFUSING to use un-redacted source: {s}')

    devs = []
    for s in sources:
        if not os.path.exists(s):
            sys.exit(f'missing source: {s}')
        im = Image.open(s).convert('RGBA')
        bb = im.split()[-1].getbbox()
        if bb is None:
            sys.exit(f'fully transparent source: {s}')
        devs.append(im.crop(bb))

    # Every device in a row shares one height, so the row reads as one object.
    # A watch is much shorter and wider, so it is scaled down rather than
    # stretched to phone height.
    scaled = []
    for im in devs:
        h = int(DEVICE_H * (0.58 if is_watch(im) else 1.0))
        w = max(1, round(im.width * h / im.height))
        scaled.append(im.resize((w, h), Image.LANCZOS))

    # All three files are padded to one common canvas. `.phone` is a plain flex
    # item with no width of its own, so equal intrinsic sizes are what make the
    # three columns come out equal and the -7% margins symmetrical.
    #
    # The horizontal padding is not decoration, it is what makes `.phones` work.
    # Solve the flex row: three items, each margin -7% of the container (the
    # first -5% on its left), shrunk to fit width W. Content width per phone
    # settles at 0.467W and neighbouring content boxes overlap by 0.14W, which is
    # 30% of a canvas. The original's phone PNGs carry 19.4% transparent padding
    # per side, so 38.8% of clear space absorbs that 30% and the DEVICES never
    # actually touch — only the empty canvases do. Trim the padding off and the
    # same CSS would drive the phones straight through each other.
    cw = max(round(p.width / DEVICE_FRAC) for p in scaled)
    ch = max(p.height for p in scaled)

    for i, p in enumerate(scaled, start=1):
        canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        canvas.paste(p, ((cw - p.width) // 2, (ch - p.height) // 2), p)
        # WebP, not PNG. These are nine photographic screens that must keep a real
        # alpha channel; as PNG-24 the set lands around 3 MB, as WebP around 350 KB
        # for the same picture. Alpha-WebP is supported everywhere back to Safari
        # 14 / iOS 14, so there is no fallback to carry.
        path = os.path.join(OUT, f'{name}-{i}.webp')
        canvas.save(path, format='WEBP', quality=82, method=6)
        kb = os.path.getsize(path) // 1024
        print(f'  {name}-{i}.webp  {cw}x{ch}  {kb} KB  <- {os.path.basename(sources[i-1])}')


def build_og():
    """The social preview card. Not a project card and not part of the page —
    link unfurlers need one opaque, fixed-size raster, so this is the one place a
    background is painted in. Same three devices, same order, on the light ground
    the page itself uses."""
    W, H = 1200, 630
    card = Image.new('RGB', (W, H), (255, 255, 255))
    devs = []
    for s in PROJECTS['athanify']:
        im = Image.open(s).convert('RGBA')
        devs.append(im.crop(im.split()[-1].getbbox()))
    h = int(H * 0.86)
    devs = [d.resize((round(d.width * h / d.height), h), Image.LANCZOS) for d in devs]
    gap = int(h * 0.04)
    total = sum(d.width for d in devs) + gap * (len(devs) - 1)
    x = (W - total) // 2
    for d in devs:
        card.paste(d, (x, (H - d.height) // 2), d)
        x += d.width + gap
    # JPEG, not PNG: it is opaque by definition and three photographic screens
    # cost ~530 KB as PNG against ~110 KB here, for a raster nobody zooms into.
    path = os.path.join(V3, 'img', 'og.jpg')
    card.save(path, quality=88, optimize=True, progressive=True)
    print(f'  og.jpg  {W}x{H}  {os.path.getsize(path) // 1024} KB')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    print('building v3 device art (transparent, no background):')
    for name, srcs in PROJECTS.items():
        build(name, srcs)
    build_og()
