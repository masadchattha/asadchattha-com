#!/usr/bin/env python3
"""
Build the project cards for an archived version of asadchattha.com.

RULE (set 2026-08-14, applies to v1 and EVERY future archived version):
  - The card background is ONE flat gradient. Nothing else.
  - The device frames / demo screenshots sit DIRECTLY on that gradient,
    side by side, exactly as they come out of the mockup.
  - Do NOT re-frame the artwork: no inner panel, no rounded card behind it,
    no drop shadow, no second background layer.
  - The mockup's own background is keyed out so only the devices remain.
  - If there is no mockup for a project, render a plain text card on the same
    gradient and swap in real artwork when it arrives.

Usage:  python3 tools/build_cards.py
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
import os, sys

CW, CH = 1280, 800
OUT = 'img'

# ---------------------------------------------------------------- gradient
def backdrop():
    """The single flat blue gradient every card sits on."""
    im = Image.new('RGB', (CW, CH))
    d = ImageDraw.Draw(im)
    for y in range(CH):
        t = y / CH
        d.line([(0, y), (CW, y)], fill=(int(13 + 16*t), int(16 + 18*t), int(44 + 30*t)))
    glow = Image.new('RGB', (CW, CH), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([CW*0.5 - 540, -320, CW*0.5 + 540, 460], fill=(72, 78, 214))
    gd.ellipse([-220, CH - 280, 400, CH + 240], fill=(38, 92, 184))
    return ImageChops.add(im, glow.filter(ImageFilter.GaussianBlur(200)).point(lambda v: int(v*0.30)))

# ------------------------------------------------------------ background key
def key_out(im, tol=42):
    """Flood the mockup's own background to transparent from all four edges."""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    seeds, bgs = [], []
    for x in range(0, w, max(1, w // 60)):
        seeds += [(x, 0), (x, h - 1)]
    for y in range(0, h, max(1, h // 60)):
        seeds += [(0, y), (w - 1, y)]
    for s in seeds[:8]:
        bgs.append(px[s][:3])
    bg = tuple(sorted(c[i] for c in bgs)[len(bgs)//2] for i in range(3))

    alpha = Image.new('L', (w, h), 255)
    ap = alpha.load()
    stack = list(seeds)
    seen = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        r, g, b, _ = px[x, y]
        if abs(r-bg[0]) + abs(g-bg[1]) + abs(b-bg[2]) > tol:
            continue
        ap[x, y] = 0
        stack += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    im.putalpha(alpha.filter(ImageFilter.GaussianBlur(0.6)))
    return im

def key_gradient(im, tol=46, edge=18):
    """Key out a SMOOTH gradient background. Models the background per row by
    interpolating between the left and right edge, then masks anything that
    departs from that model. Use for artwork already sitting on a gradient."""
    im = im.convert('RGB')
    w, h = im.size
    sc = 480 / w
    sm = im.resize((480, max(1, int(h*sc))), Image.BILINEAR)
    sw, sh = sm.size
    px = sm.load()
    mask = Image.new('L', (sw, sh), 0)
    mp = mask.load()
    e = max(2, int(edge*sc))
    for y in range(sh):
        L = [px[x, y] for x in range(e)]
        R = [px[sw-1-x, y] for x in range(e)]
        lm = tuple(sorted(c[i] for c in L)[len(L)//2] for i in range(3))
        rm = tuple(sorted(c[i] for c in R)[len(R)//2] for i in range(3))
        for x in range(sw):
            t = x/(sw-1)
            p = px[x, y]
            if (abs(p[0]-(lm[0]+(rm[0]-lm[0])*t))
              + abs(p[1]-(lm[1]+(rm[1]-lm[1])*t))
              + abs(p[2]-(lm[2]+(rm[2]-lm[2])*t))) > tol:
                mp[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    mask = mask.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert('RGBA')
    out.putalpha(mask)
    bb = mask.getbbox()
    return out.crop(bb) if bb else out

def trim_alpha(im):
    bb = im.split()[-1].getbbox()
    return im.crop(bb) if bb else im

def drop_bands(im):
    """Remove the mockup's title row and App Store badge, keep the device band."""
    a = im.split()[-1]
    w, h = im.size
    on = []
    for y in range(h):
        bb = a.crop((0, y, w, y+1)).getbbox()
        on.append(bb is not None and (bb[2]-bb[0]) > w * 0.05)
    runs, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        elif not v and s is not None: runs.append((s, i)); s = None
    if s is not None: runs.append((s, h))
    if not runs: return im
    y0, y1 = max(runs, key=lambda r: r[1]-r[0])
    return trim_alpha(im.crop((0, y0, w, y1)))

# ----------------------------------------------------------------- builders
def from_mockup(src, out, fill=0.90, key='flat', crop=None):
    """key='flat'     -> mockup sits on a solid background (title + badge stripped)
       key='gradient' -> mockup already sits on its own gradient
       crop=(l,t,r,b) fractions applied before keying"""
    im = Image.open(src)
    if crop:
        w, h = im.size
        im = im.crop((int(w*crop[0]), int(h*crop[1]), int(w*crop[2]), int(h*crop[3])))
    if key == 'gradient':
        art = key_gradient(im)
    elif key == 'flat':
        art = drop_bands(key_out(im))
    else:
        art = trim_alpha(im.convert('RGBA'))
    sc = min(CW*fill/art.width, CH*fill/art.height)
    art = art.resize((int(art.width*sc), int(art.height*sc)), Image.LANCZOS)
    card = backdrop()
    card.paste(art, ((CW-art.width)//2, (CH-art.height)//2), art)
    card.save(out, quality=92)
    print(f'  {os.path.basename(out):26s} <- {os.path.basename(src)}')

def from_transparent(srcs, out, fill=0.90, lift=0.0):
    """Preferred path: real transparent RGBA device PNGs laid out side by side on
    the gradient. Equal size, evenly spaced, never overlapping — at grid size a
    uniform ||| row stays legible where a fanned or stepped arrangement does not."""
    devs = [Image.open(s).convert('RGBA') for s in srcs]
    devs = [d.crop(d.split()[-1].getbbox()) for d in devs]
    n = len(devs)
    mid = n // 2
    # Phones all share one height. A watch is much shorter and wider, so it is
    # scaled down and centred rather than stretched to phone height.
    def is_watch(d):
        return d.width / d.height > 0.55        # phones sit near 0.49, watches near 0.61
    scale = [0.82 if is_watch(d) else 1.0 for d in devs]
    # positive: devices must never overlap. A watch beside a phone gets roughly
    # double the breathing room so the pair reads as two separate objects.
    gap = 0.10 if any(is_watch(d) for d in devs) else 0.045
    unit_w = sum(d.width/d.height * scale[i] for i, d in enumerate(devs))
    unit_w += gap * (n - 1)
    target_h = min(CH*fill, CW*fill/unit_w)
    placed = []
    for i, d in enumerate(devs):
        h = int(target_h * scale[i])
        w = max(1, int(d.width * h / d.height))
        placed.append(d.resize((w, h), Image.LANCZOS))
    total_w = sum(p.width for p in placed) + int(gap*target_h)*(n-1)
    card = backdrop()
    x = (CW - total_w)//2
    for pimg in placed:
        card.paste(pimg, (x, (CH - pimg.height)//2), pimg)   # each device centred on its own height
        x += pimg.width + int(gap*target_h)
    card.save(out, quality=92)
    print(f'  {os.path.basename(out):26s} <- {len(srcs)} transparent device(s)')

def as_is(src, out):
    """Artwork used exactly as supplied — no gradient, no keying, nothing cropped.
    For brand graphics that already carry their own designed background."""
    im = Image.open(src).convert('RGB')
    corner = im.getpixel((2, 2))
    sc = min(CW/im.width, CH/im.height)          # contain, so nothing is lost
    im = im.resize((int(im.width*sc), int(im.height*sc)), Image.LANCZOS)
    card = Image.new('RGB', (CW, CH), corner)    # pad with the artwork's own bg
    card.paste(im, ((CW-im.width)//2, (CH-im.height)//2))
    card.save(out, quality=92)
    print(f'  {os.path.basename(out):26s} <- as-is, no gradient')

def font(size, bold=False):
    for p in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold
              else '/System/Library/Fonts/Supplemental/Arial.ttf',
              '/System/Library/Fonts/Helvetica.ttc'):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def text_card(name, sub, out):
    """Placeholder for a project with no artwork yet. Same gradient, nothing else."""
    card = backdrop()
    d = ImageDraw.Draw(card)
    f1, f2 = font(78, True), font(30)
    for txt, f, y, col in ((name, f1, 350, (255, 255, 255)), (sub, f2, 452, (168, 178, 224))):
        w = d.textbbox((0, 0), txt, font=f)[2]
        d.text(((CW-w)//2, y), txt, font=f, fill=col)
    d.text((CW//2 - 108, 540), 'screenshots coming', font=font(22), fill=(110, 122, 176))
    card.save(out, quality=92)
    print(f'  {os.path.basename(out):26s} <- text placeholder')

M = os.path.expanduser('~/Documents/Career/Claude/mockups')
P = os.path.expanduser('~/Documents/Development/Websites/asadchattha-com/main/public/images/projects')

# Sources must be device mockups on a FLAT background so the background can be
# keyed out. Anything already sitting on its own gradient cannot be keyed and
# belongs in PLACEHOLDERS until a proper mockup exists.
T = os.path.expanduser('~/Documents/Career/Other Docs/Mocks')
F = os.path.expanduser('~/Documents/Business/Freelancer.com/Mocups')
U = os.path.expanduser('~/Documents/Business/upwork/Mockups')

# 1st choice: true transparent device PNGs. Nothing to key, nothing to guess.
# Screens are listed in the order they appear on the card, left to right.
TRANSPARENT = [
    ('card-athanify.png', [f'{T}/Athanify/qibla-ar.png',
                           f'{T}/Athanify/makkah-hero-light.png',
                           f'{T}/Athanify/sleep-stories-1.png']),
    ('card-shelly.png',   [f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9914-portrait.png',
                           f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9915-portrait.png',
                           f'{T}/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9916-portrait.png']),
    ('card-peptify.png',  [f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9903-portrait.png',
                           f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9905-portrait.png',
                           f'{T}/(peptify) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9906-portrait.png']),
    ('card-focusbear.png',[f'{T}/Focuc Bear/(Focus Bear iPhone) IMG_9890-portrait.png',
                           f'{T}/Focuc Bear/(focus bear) 300x375bb-portrait.png']),
    ('card-chapter.png',  [f'{U}/Chapter/Frames/IMG_4284-portrait.png',
                           f'{U}/Chapter/Frames/IMG_4286-portrait.png',
                           f'{U}/Chapter/Frames/IMG_4288-portrait.png']),
    ('card-brightstart.png',[f'{U}/Bright Start/Frames/IMG_2376-portrait.png',
                           f'{U}/Bright Start/Frames/IMG_2373-portrait.png',
                           f'{U}/Bright Start/Frames/IMG_2375-portrait.png']),
    ('card-officetree.png',[f'{F}/Offietree/1_Officetree_Home.png',
                           f'{F}/Offietree/2_Officetree_Text.png',
                           f'{F}/Offietree/3_Officetree_voicemail.png']),
    # 1st and 3rd swapped per Asad, middle screen unchanged
    ('card-goingsolo.png',[f'{F}/GoingSolo/IMG_6962-portrait.png',
                           f'{F}/GoingSolo/IMG_6960-portrait.png',
                           f'{F}/GoingSolo/IMG_6959-portrait.png']),
    ('card-pryvate.png',  [f'{T}/(Pryvate) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9893-portrait.png',
                           'img/src/pryvate-number-redacted.png',   # real phone number mosaicked out
                           f'{T}/(Pryvate) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9896-portrait.png']),
    # 1st and 3rd swapped per Asad, middle screen unchanged
    ('card-votari.png',   [f'{T}/(Votari) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9918-portrait.png',
                           'img/src/votari-passport-redacted.png',  # real passport data mosaicked out
                           f'{T}/(Votari) apple-iphone-15-pro-max-white-titanium-mockup/IMG_9898-portrait.png']),
    ('card-hiiker.png',   ['img/src/hiiker-email-redacted.png',     # real name + email mosaicked out
                           f'{T}/Hiiker/incoming-C41FF231-17E7-48F8-8593-320A66181E79-portrait.png']),
    ('card-planthealth.png',[f'{T}/PLant Health/IMG_0353-portrait.png',
                           'img/src/planthealth-diagnosis.png',   # black bg keyed to a rounded device
                           f'{T}/PLant Health/IMG_8989-portrait.png']),
    ('card-block.png',    [f'{T}/Block/1. 460x996bb-portrait.png',
                           f'{T}/Block/2. 460x996bb-portrait.png',
                           f'{T}/Block/3. 460x996bb -portrait.png']),
    ('card-firstresponse.png',[f'{F}/1st-response/IMG_6982-portrait.png',
                           f'{F}/1st-response/IMG_6983-portrait.png',
                           f'{F}/1st-response/IMG_6985-portrait.png']),
]

# Brand graphics that already carry their own designed background: used exactly
# as supplied, no gradient behind them.
AS_IS = [
    ('card-idvkit.png', f'{P}/idvkit.png'),
]

# Flat-background mockups. No transparent version exists for these four yet.
MOCKUPS = [
    ('card-fonder.png',        f'{M}/fonder-mockup.png'),
]
# Waiting on flat-background mockups from Asad. Swap each into MOCKUPS as it lands.
PLACEHOLDERS = []

if __name__ == '__main__':
    print('building cards:')
    for out, srcs in TRANSPARENT:
        gone = [x for x in srcs if not os.path.exists(x)]
        for g in gone:
            print(f'  !! MISSING source for {out}: {g}', file=sys.stderr)
        have = [x for x in srcs if os.path.exists(x)]
        if have:
            from_transparent(have, f'{OUT}/{out}')
        else:
            print(f'  !! no transparent source at all for {out}', file=sys.stderr)
    for out, src in AS_IS:
        if os.path.exists(src):
            as_is(src, f'{OUT}/{out}')
    for entry in MOCKUPS:
        out, src = entry[0], entry[1]
        opts = entry[2] if len(entry) > 2 else {}
        if os.path.exists(src):
            from_mockup(src, f'{OUT}/{out}', **opts)
        else:
            print(f'  !! missing source: {src}', file=sys.stderr)
    for out, name, sub in PLACEHOLDERS:
        text_card(name, sub, f'{OUT}/{out}')
