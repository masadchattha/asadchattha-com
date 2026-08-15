#!/usr/bin/env python3
"""
Redact personal data out of source mockups for v2.

Three screens were already redacted for v1 and those copies are reused as-is
(`archives/v1/img/src/`): Votari's passport screen, Pryvate's header, HiiKER's
account row.

Two more were caught on the v2 pass, both in Officetree, which is a business
phone app and therefore full of real numbers:

| Screen | What was exposed |
|---|---|
| `2_Officetree_Text.png` | seven inbound sender phone numbers, plus one political campaign message body |
| `3_Officetree_voicemail.png` | the primary attendant's direct number |

Redaction is MOSAIC THEN BLUR, never blur alone. A plain blur at web scale can
still be read when zoomed; pixelating first destroys the glyphs and the blur
then removes the pixel edges so it does not read as a censor bar.

Boxes are given as fractions of the device's own alpha bounding box, so they
survive any rescale of the source.

Usage:  python3 tools/redact.py
Output: img/src/*-redacted.png   (consumed by tools/build_devices.py)
"""
from PIL import Image, ImageFilter
import os

F = os.path.expanduser('~/Documents/Business/Freelancer.com/Mocups')
T = os.path.expanduser('~/Documents/Career/Other Docs/Mocks')
OUT = 'img/src'

# (left, top, right, bottom) as fractions of the trimmed device
JOBS = [
    (f'{F}/Offietree/2_Officetree_Text.png', 'officetree-text-redacted.png', [
        (0.170, 0.209, 0.500, 0.243),   # sender number 1
        (0.170, 0.243, 0.825, 0.297),   # campaign message body
        (0.170, 0.311, 0.500, 0.345),   # sender number 2
        (0.170, 0.514, 0.350, 0.548),   # sender number 4
        (0.170, 0.616, 0.350, 0.650),   # sender number 5
        (0.170, 0.717, 0.350, 0.751),   # sender number 6
        (0.170, 0.791, 0.510, 0.828),   # sender number 7
        (0.170, 0.888, 0.510, 0.905),   # sender number 8, clipped by the tab bar
    ]),
    (f'{F}/Offietree/3_Officetree_voicemail.png', 'officetree-voicemail-redacted.png', [
        (0.105, 0.240, 0.610, 0.273),   # primary attendant direct number
    ]),

    # Caught on the four-device pass. Both closing screens are contact lists,
    # which is the worst case for this: real names, a real face, real numbers.
    (f'{T}/(Pryvate) apple-iphone-15-pro-max-white-titanium-mockup/(4-End) IMG_0452-portrait.png',
     'pryvate-chats-redacted.png', [
        (0.210, 0.255, 0.470, 0.285),   # chat 1, real mobile number
        (0.108, 0.318, 0.205, 0.378),   # chat 2, contact's real profile photo
        (0.210, 0.330, 0.380, 0.360),   # chat 2, contact's real name
        (0.210, 0.405, 0.470, 0.437),   # chat 3, real mobile number
    ]),
    (f'{T}/Officetree/(4-End) IMG_0453-portrait.png',
     'officetree-recent-redacted.png', [
        (0.195, 0.174, 0.500, 0.200),   # caller 1, real name
        (0.195, 0.275, 0.500, 0.301),   # caller 2, same real name
        (0.195, 0.376, 0.550, 0.402),   # caller 3, real number
        (0.195, 0.477, 0.550, 0.503),   # caller 4, real number
        (0.195, 0.578, 0.550, 0.604),   # caller 5, real number
        (0.195, 0.679, 0.550, 0.705),   # caller 6, real number
        (0.195, 0.779, 0.550, 0.805),   # caller 7, real number
        (0.195, 0.878, 0.550, 0.900),   # caller 8, real number, clipped by tab bar
    ]),
]

MOSAIC = 20     # px block size, measured on the redacted region itself
BLUR = 5.0


def redact(src, out, boxes):
    im = Image.open(src).convert('RGBA')
    bb = im.split()[-1].getbbox() or (0, 0, im.width, im.height)
    bx, by = bb[0], bb[1]
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]

    for l, t, r, b in boxes:
        box = (int(bx + l * bw), int(by + t * bh), int(bx + r * bw), int(by + b * bh))
        w, h = box[2] - box[0], box[3] - box[1]
        if w < 2 or h < 2:
            continue
        patch = im.crop(box)
        patch = patch.resize((max(1, w // MOSAIC), max(1, h // MOSAIC)), Image.BILINEAR)
        patch = patch.resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(BLUR))
        im.paste(patch, box)

    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, out)
    im.save(dst)
    print(f'  {out}  <- {os.path.basename(src)}  ({len(boxes)} region(s))')


if __name__ == '__main__':
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(here)
    print('redacting:')
    for src, out, boxes in JOBS:
        if os.path.exists(src):
            redact(src, out, boxes)
        else:
            print(f'  !! missing {src}')
