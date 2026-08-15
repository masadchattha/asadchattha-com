#!/usr/bin/env python3
"""
Build the three generated parallax backgrounds for v2.

The original v2 put a licensed photograph behind Services, Experience and
Contact. Nothing from that repo is reused here, so these are synthesised
locally instead: a dark base, a few wide radial glows in the site's own teal
and purple, a faint contour field, film grain and a vignette.

Every section paints `rgba(0,0,0,0.61)` over its background, so these only ever
read as depth and colour temperature. They are deliberately quiet.

The intro background is NOT generated here. It reuses
`archives/v1/img/hero-mountains.jpg`, which was itself built by
`archives/v1/tools/build_hero.py` from a licensed photograph.

Usage:  python3 tools/build_backgrounds.py
Output: img/bg-services.jpg, img/bg-experience.jpg, img/bg-contact.jpg
"""
from PIL import Image, ImageDraw, ImageFilter
import math
import os
import random

W, H = 2600, 1500

TEAL = (0, 183, 199)
PURPLE = (77, 12, 232)
BASE = (16, 18, 22)

# name -> (glow list, contour tilt, seed)
# each glow is (cx, cy, radius, colour, strength)
SCENES = {
    "services": (
        [
            (0.18, 0.24, 0.85, TEAL, 0.55),
            (0.82, 0.78, 0.95, PURPLE, 0.42),
            (0.55, 0.10, 0.55, TEAL, 0.22),
        ],
        -0.22,
        11,
    ),
    "experience": (
        [
            (0.86, 0.20, 0.90, TEAL, 0.40),
            (0.12, 0.82, 1.00, PURPLE, 0.50),
            (0.45, 0.55, 0.60, TEAL, 0.18),
        ],
        0.30,
        29,
    ),
    "contact": (
        [
            (0.50, 0.86, 1.10, PURPLE, 0.48),
            (0.10, 0.14, 0.75, TEAL, 0.46),
            (0.90, 0.50, 0.70, TEAL, 0.20),
        ],
        -0.08,
        47,
    ),
}


def radial_glow(size, cx, cy, radius, colour, strength):
    """One wide, soft radial wash. Built small and upscaled so it stays smooth."""
    w, h = size
    sw, sh = w // 8, h // 8
    layer = Image.new("L", (sw, sh), 0)
    px = layer.load()
    ccx, ccy = cx * sw, cy * sh
    rr = radius * max(sw, sh)
    for y in range(sh):
        for x in range(sw):
            d = math.hypot(x - ccx, y - ccy) / rr
            if d >= 1.0:
                continue
            # smoothstep falloff, squared for a softer shoulder
            v = 1.0 - d
            px[x, y] = int(255 * strength * v * v)
    layer = layer.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(60))
    return Image.new("RGB", (w, h), colour), layer


def contours(size, tilt, seed):
    """A faint topographic band field, drawn once and blurred flat."""
    w, h = size
    rnd = random.Random(seed)
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    step = 46
    amp = h * 0.10
    for i in range(-6, int(h / step) + 8):
        y0 = i * step
        phase = rnd.uniform(0, math.tau)
        pts = []
        for x in range(0, w + 40, 40):
            t = x / w
            y = y0 + tilt * x + amp * math.sin(t * math.tau * 1.6 + phase) * 0.5
            pts.append((x, y))
        d.line(pts, fill=rnd.randint(26, 46), width=2)
    return layer.filter(ImageFilter.GaussianBlur(1.4))


def grain(size, seed, amount=9):
    w, h = size
    rnd = random.Random(seed)
    small = Image.new("L", (w // 3, h // 3))
    small.putdata([128 + rnd.randint(-amount, amount) for _ in range(small.width * small.height)])
    return small.resize((w, h), Image.BILINEAR)


def vignette(size, power=0.72):
    w, h = size
    sw, sh = w // 8, h // 8
    m = Image.new("L", (sw, sh))
    px = m.load()
    cx, cy = sw / 2, sh / 2
    mx = math.hypot(cx, cy)
    for y in range(sh):
        for x in range(sw):
            d = math.hypot(x - cx, y - cy) / mx
            px[x, y] = int(255 * (1.0 - power * d * d))
    return m.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))


def build(name, glows, tilt, seed, out_dir="img"):
    size = (W, H)
    canvas = Image.new("RGB", size, BASE)

    for cx, cy, r, colour, strength in glows:
        wash, mask = radial_glow(size, cx, cy, r, colour, strength)
        canvas = Image.composite(wash, canvas, mask)
        canvas = Image.blend(canvas, Image.new("RGB", size, BASE), 0.18)

    # contours, tinted toward the section's dominant colour
    band = contours(size, tilt, seed)
    tint = Image.new("RGB", size, tuple(min(255, int(c * 0.9) + 30) for c in glows[0][3]))
    canvas = Image.composite(tint, canvas, band)

    # grain and vignette
    g = grain(size, seed)
    canvas = Image.blend(canvas, Image.merge("RGB", (g, g, g)), 0.045)
    canvas = Image.composite(canvas, Image.new("RGB", size, (6, 7, 9)), vignette(size))

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"bg-{name}.jpg")
    canvas.save(out, quality=88, optimize=True)
    print(f"{out}  {canvas.size}")


def build_intro(out_dir="img"):
    """The intro plate. The source is archives/v1/img/hero-mountains.jpg, which
    build_hero.py already assembled from a licensed photograph.

    The intro section is the ONE section with no black overlay over its
    background, and the raw frame is a bright daylit mountain, so white type on
    top of it barely holds. It is darkened here rather than in CSS so the
    section keeps the original's markup: photo, type, nothing between them.
    A slight cool grade lands it in the same family as the other three."""
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       '..', 'v1', 'img', 'hero-mountains.jpg')
    im = Image.open(src).convert("RGB")

    # top-weighted darkening: heaviest behind the headline, lighter at the foot
    shade = Image.new("L", im.size)
    d = ImageDraw.Draw(shade)
    for y in range(im.height):
        t = y / im.height
        d.line([(0, y), (im.width, y)], fill=int(255 * (0.30 + 0.22 * t)))
    im = Image.composite(im, Image.new("RGB", im.size, (8, 12, 20)), shade)

    # cool the frame toward the site's teal
    r, g, b = im.split()
    im = Image.merge("RGB", (r.point(lambda v: int(v * 0.92)), g, b))

    im = Image.composite(im, Image.new("RGB", im.size, (6, 7, 9)), vignette(im.size, 0.55))
    out = os.path.join(out_dir, "bg-intro.jpg")
    im.save(out, quality=88, optimize=True)
    print(f"{out}  {im.size}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(here)
    for name, (glows, tilt, seed) in SCENES.items():
        build(name, glows, tilt, seed)
    build_intro()
