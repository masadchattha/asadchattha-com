# v2 — asadchattha.com (archived version 2)

Frozen snapshot of the second version of Asad's personal site. Lives at
**v2.asadchattha.com** and is linked from the Time Machine on the current site.

Built 2026-08-14.

## What it is

A one-page dark portfolio in the 2017 idiom: a full-bleed photographic intro
with the name wiping up behind a mask, four parallax section backgrounds, a
fixed dot navigation on the right, a full-screen teal overlay menu on mobile,
a centre-spine alternating experience timeline, full-width stacked portfolio
rows, and a gradient footer.

Structurally faithful to the original v2. Only the copy, the artwork and the
substitutions listed below are Asad's.

## Stack

No build step. Serve the folder and it runs.

| Layer | What |
|---|---|
| Markup | one hand-written `index.html` |
| Styles | one hand-written `css/main.css`, ordered as the original's Sass partials |
| Behaviour | `js/main.js`, plain DOM, no jQuery, no skrollr |
| Type | Playfair Display 700, Montserrat 500/600/700, Inter 300/400/500/700 via Google Fonts |
| Icons | `lucide-static` (ISC) for UI glyphs, `simple-icons` (CC0) and `devicon` (MIT) for brand marks |
| Form | Formspree, submitted with `fetch` |

## Design tokens

| Token | Value |
|---|---|
| Body background | `#1b1b1b` |
| Alternating section background | `#5b5b5b` (odd), `#1b1b1b` (even) |
| Text | `#f2f2f2`, secondary `#cbcbcb`, muted `#777777` |
| Accent | `#00b7c7` |
| Block button | rests at `#00909c`, hovers to `#00b7c7` |
| Footer | `linear-gradient(45deg, #00b7c7 0%, #4d0ce8 100%)` |
| Section background overlay | `rgba(0,0,0,0.61)` |
| Section shell | `min-height: 700px`, padding `100px` / `100px 50px` ≤900 / `100px 25px` ≤400 |
| Display h1 | Playfair Display 700, `4.5em` in the intro, `3em` per section |
| Section h2 | Montserrat 700, uppercase |
| Body copy | Inter, `1.3em` in section wrappers, `1.15em` in About |
| Timeline spine | 2px `#00b7c7`, cards `#1b1b1b` at 0.85 opacity, 1.0 on hover |
| Breakpoints | 1170 · 1000 · 900 · 768 · 660 · 600 · 480 · 440 · 400 · 330, all max-width |

## Deliberate changes from the original

Everything here is a change I made on purpose, with the reason.

| # | Change | Why |
|---|---|---|
| 1 | **Fonts substituted.** Chronicle Display Bold → Playfair Display 700. Gotham → Montserrat. Whitney → Inter. | Chronicle, Gotham and Whitney are retail licences. Montserrat sets noticeably wider than Gotham, so every uppercase size is trimmed (service headings 20px → 18px, dot labels 1em → 0.85em, portfolio buttons and the contact button down a step) and letter-spacing is reduced. |
| 2 | **Contact form gives feedback.** Same Formspree v1 endpoint, same runtime-assembled address, same `_gotcha` honeypot, but submitted with `fetch` and reported in place: sending, success, error, and the button disables while in flight. | The original did a native POST, so the visitor was navigated away to a Formspree page and got nothing back on failure. |
| 3 | **Floating-label bug fixed.** `is-completed` is only removed on blur when the field is empty. | The original removed it unconditionally, so a filled field's label dropped back down on top of the text the visitor had just typed. |
| 4 | **Footer icon transition moved to the base rule.** | The original declared `transition` inside `:hover`, so the icon animated up and then snapped back. |
| 5 | **`rel="noopener noreferrer"` on every `target="_blank"`.** | Reverse tabnabbing. |
| 6 | **`maximum-scale` and `user-scalable=no` dropped from the viewport meta.** | They blocked pinch zoom. |
| 7 | **skrollr replaced.** An `IntersectionObserver` marks which background plates are on screen and one rAF-throttled scroll handler writes `translate3d` to those only. Same 300px of travel. jQuery is gone too. | skrollr 0.6.30 is unmaintained, and the original loaded 90KB of jQuery to do six things. Nothing here needs either. |
| 8 | **`prefers-reduced-motion` guard added.** Parallax is skipped entirely in JS, and the intro wipe, the rule sweep and the mobile menu stagger are switched off in CSS. Smooth scrolling falls back to instant. | The original had no guard at all. |
| 9 | **Background plates are 300px taller than their section and start 150px high.** | The original let the plate scrape its own edge at the extremes of the parallax range. |
| 10 | **Portfolio defaults to the stair-stepped device layout,** the original's `.screentime` special case, renamed `.devices`. Up to four devices at 26% width, each 15px lower than the last. The triptych (`.img-lg` / `.img-md` / `.img-sm`, 70% / 27% / 15%) is kept in the CSS but unused. | The triptych is a desktop-tablet-mobile arrangement built for web projects. This is an iOS portfolio. |
| 11 | **Device artwork is transparent WebP with a CSS `drop-shadow`,** not opaque JPG with `border-radius` and `box-shadow`. | The shadow follows the device silhouette instead of drawing a rectangle around it. See the note on WebP under *Regenerating assets*. |
| 12 | **Skills group two renders logos knocked out to white,** brightening on hover, rather than plain greyscale. | The original's logo band sat on light grey. This one sits on `#1b1b1b`, and one of the marks (Apple Pay) is solid black, so a plain `grayscale(100%)` made it invisible. |
| 13 | **Skills group headings remapped** to Development · Payments and Data · Tools · Frameworks. | "Design" as a logo wall does not describe an iOS engineer. The four rendering treatments are unchanged. |
| 14 | **The hamburger is a `<button>`** with `aria-expanded`, the dot nav and overlay menu are labelled `<nav>` elements, and Escape closes the menu. | The original used a `<div>` with a click handler and no keyboard path. |
| 15 | **Backgrounds are generated, not photographed** (except the intro). | Nothing is copied out of `docs/reference-bc-v2/`. |

## Files

```
index.html                    the whole page
css/main.css                  every rule, ordered as the original's Sass partials
js/main.js                    dot nav, mobile menu, parallax, form, floating labels
img/bg-intro.jpg              the intro plate. archives/v1/img/hero-mountains.jpg
                              darkened top-weighted and graded cool by
                              tools/build_backgrounds.py. The intro is the one
                              section with no black overlay over its background,
                              and the raw frame is a bright daylit mountain that
                              white type cannot hold against.
img/bg-services.jpg           generated. dark base, wide radial washes in the
img/bg-experience.jpg         site's teal and purple, a faint contour field,
img/bg-contact.jpg            grain, vignette. Each sits under rgba(0,0,0,0.61),
                              so they only ever read as depth and temperature.
img/portfolio/<slug>/*.webp   28 device images, 9 projects. One device per file,
                              all on the same 660x1360 transparent canvas so the
                              stair-step lands exactly where the CSS says.
img/src/*.png                 redacted source screens, consumed by the builder
img/icons/*.svg               13 lucide glyphs, recoloured to #f2f2f2
img/skills/*.svg              6 brand marks for the Payments and Data group
img/social/*.svg              8 footer marks
img/headshot.jpg              Asad's profile photo, cropped square (from v1)
img/logo-white.svg            "A" monogram. Also the intro scroll-down mark.
img/favicon.svg               the same mark in accent
Muhammad_Asad_Resume_2026.pdf frozen résumé, linked from the first block button
tools/build_backgrounds.py    the four parallax plates
tools/build_devices.py        the 28 device images
tools/redact.py               PII redaction, mosaic then blur
```

Both background sets are generated or derived locally. Neither carries a licence
obligation, and no asset is copied from the reference repo.

## Content rules

Everything claimed on this page must be true and verifiable. Source of truth is
`docs/CONTENT.md`.

- Only apps Asad actually built. **Foqos is NOT his** and must never appear.
- App Store links verified against `memory/user_portfolio_app_store_links.md`.
- Positioning is deliberately BROAD. Screen Time is one niche among many. The
  four "What I Do" pillars are development, payments, privacy and on-device ML,
  and release, not four flavours of Screen Time.
- Employer descriptions state stack and responsibility. The only per-employer
  app attributions are the ones that are certain: the four products Asad is sole
  iOS engineer on at o9 Tech, and Pryvate Technologies' own two products.
- The name is always "Muhammad Asad" or "Asad", never "Muhammad" alone.

## PII

Five screens carry personal data. All five ship redacted, and the builder reads
the redacted copy, never the original.

| Screen | What was exposed | Redacted copy |
|---|---|---|
| Votari passport review | passport photo, passport number, surname, given name, date of birth | `../v1/img/src/votari-passport-redacted.png` |
| Pryvate header | real mobile number | `../v1/img/src/pryvate-number-redacted.png` |
| HiiKER account row | real name and email address | `../v1/img/src/hiiker-email-redacted.png` |
| Officetree messages | seven inbound sender phone numbers, plus one political campaign message body | `img/src/officetree-text-redacted.png` |
| Officetree voicemail | the primary attendant's direct number | `img/src/officetree-voicemail-redacted.png` |

The first three were already redacted for v1 and are reused as-is. The last two
were caught on this pass and are produced by `tools/redact.py`.

Redaction is **mosaic then blur, never blur alone** — a plain blur at web scale
can still be read when zoomed. Originals are left untouched.

**Before adding any new device image, open every screen at full size and look
for:** phone numbers, email addresses, real names, passport or CNIC data, dates
of birth, addresses, account balances, API keys, client names under NDA.

## Local preview

```bash
cd archives/v2
python3 -m http.server 8918
open http://localhost:8918/index.html
```

`file://` will not work — relative asset paths and the fetch-based form both
need a real origin.

Note when screenshotting: the device images are `loading="lazy"`, and a
headless full-page capture will render the rows empty. Copy `index.html`,
strip `loading="lazy"` from the copy, shoot that, and delete it.

## Regenerating assets

### Parallax backgrounds
```bash
python3 tools/build_backgrounds.py
```
Writes all four plates, including the darkened intro derived from
`../v1/img/hero-mountains.jpg`. Roughly two seconds.

### Device artwork
```bash
python3 tools/redact.py        # first, the two Officetree screens
python3 tools/build_devices.py # then the 28 device images
```

Adapted from `archives/v1/tools/build_cards.py`. What carried over: the
transparent-mock path, the flat-background flood key, watch detection by aspect
ratio, and the "equal size, evenly spaced, never overlapping" rule. What
changed: the output is one device per file on a shared transparent canvas, not a
composite card on a gradient. v1's 1280x800 cards are the wrong shape and the
wrong composition for a full-width stacked row.

Source priority, unchanged from v1:

1. **Real transparent RGBA device PNGs.** Nothing to key, nothing to guess.
   `~/Documents/Career/Other Docs/Mocks/`,
   `~/Documents/Business/Freelancer.com/Mocups/`,
   `~/Documents/Business/upwork/Mockups/`
2. Flat-background mockups, flood-keyed from the edges. Last resort.
3. No artwork means the project does not appear. Never invent app UI.

Every device lands on the same 660x1360 canvas. Phones fill 98% of the height.
A watch is detected at aspect > 0.55 and drops to 62%, centred, rather than
being stretched to phone height. HiiKER is the one four-device row: three phones
and the Apple Watch companion.

**Why WebP.** These are photographic screenshots that need an alpha channel, and
PNG cannot do both cheaply: the same 28 files are 12 MB as PNG and 1.2 MB as
WebP at quality 82, with no visible difference at any zoom. A 256-colour PNG was
tried first and bands badly in every sky and gradient.

### Icons
```bash
npm install lucide-static simple-icons devicon --ignore-scripts
```

- **`lucide-static`** (ISC) for the UI glyphs: `smartphone`, `credit-card`,
  `shield-check`, `rocket`, `code-xml`, `wallet`, `wrench`, `lightbulb`,
  `briefcase`, `graduation-cap`, `check`, `download`, `mail`. They ship with
  `stroke="currentColor"`, which does not resolve when a file is used as a CSS
  `background-image`, so every one is rewritten to `#f2f2f2`.
- **`simple-icons`** (CC0) for GitHub, X, Instagram, Facebook, WhatsApp,
  Calendly, and the six Payments and Data marks reused from v1.
- **`devicon`** (MIT) for LinkedIn only. simple-icons no longer ships a LinkedIn
  mark, so `linkedin-plain.svg` is used with a white fill.

Never hand-draw a brand logo. Asad has rejected drawn substitutes before. The
generic UI glyphs above are a different thing and come from a real icon set.

## Deploy

Separate Netlify site from the main one and from v1, same repo.

1. Netlify → Add new site → Import from `masadchattha/asadchattha-com`
2. Base directory `archives/v2`, build command empty, publish directory `archives/v2`
3. Domain management → add custom domain `v2.asadchattha.com`
4. Spaceship DNS → add `CNAME` record: host `v2` → value `<site-name>.netlify.app`
5. Wait for the Let's Encrypt cert, then link it from the Time Machine on the main site

DNS lives at Spaceship (registrar + nameservers). Do not create a Cloudflare
zone for this domain.

## Known gaps

- The Formspree v1 address-style endpoint is what the original used and is what
  is wired here. Formspree has since moved to project-scoped form IDs, so if the
  form ever stops delivering, swap the assembled URL in the inline script at the
  foot of `index.html` for a modern `https://formspree.io/f/<id>` endpoint. The
  `fetch` handler needs no changes.
- Nine of the sixteen apps are in the portfolio. The rest have no device art in a
  usable state: Focus Bear has one phone and one watch, Chapter, Bright Start,
  Going Solo and 1st-Response have frames but were cut for length, Fonder Cards
  has only a flat white mockup, IDVKit is a brand graphic rather than devices,
  and Soar has nothing. Add rows as artwork arrives.
- `.fade-in` is carried over from the original as an inert hook. It had no CSS
  there either. If a scroll reveal is ever wanted, it is the place to put it.
