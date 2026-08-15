# v3 — asadchattha.com (archived version 3)

Frozen snapshot of the third version of Asad's personal site. Lives at
**v3.asadchattha.com** and is linked from the Time Machine on the current site.

Built 2026-08-14.

## What it is

A faithful rebuild of the **v3.brittanychiang.com** layout, carrying Muhammad
Asad's content. Structure and layout only — none of her copy, none of her images.

The reference source is cloned at `docs/reference-bc-v3/` (Jekyll + SCSS + gulp).
This archive is plain static output instead: open `index.html` and it runs.

Nine sections, ~7,300px tall at 1440:

```
switch → intro (100vh) → background → skills → experience
       → featured-projects → other-projects → footer → top-button
```

## Stack

No build step, no framework, no jQuery.

| Layer | What |
|---|---|
| Markup | one hand-written `index.html` |
| Styles | one hand-written `css/main.css`, in the original's SCSS partial order |
| Behaviour | `js/main.js` — theme toggle, back-to-top, waving hand, scroll reveal |
| Type | Work Sans 300/400/500/700 + Inconsolata 400/700, Google Fonts |
| Emoji | the original's own Apple emoji PNGs, copied from `docs/reference-bc-v3/img/emojis/` |
| Icons | simple-icons (CC0) + devicon (MIT) |

## Design tokens

Straight from `_scss/partials/_globals.scss`.

| Token | Value |
|---|---|
| `--night` | `#171c28` |
| `--black` | `#36363c` |
| `--dark-grey` | `#444452` |
| `--blue` (accent) | `#007bff` |
| `--slate` | `#afafbf` |
| `--off-white` | `#e7e7e7` |
| `--green` (toggle on, status LED) | `#bae67e` |
| `--yellow` (`::selection`) | `#ffdc00` |

| | Light | Dark (`body.night`) |
|---|---|---|
| Background | `#ffffff` | `#171c28` |
| Body text | `#444452` | `#afafbf` |
| Links, headings, `strong` | `#36363c` | `#e7e7e7` |
| Section titles | `#007bff` | `#007bff` (unchanged) |

Type: root 16px. `.intro__hello` / `.intro__tagline` 2.5rem weight **300**,
line-height 60px. `.intro__contact` 20px. `.section__title` 16px/700 uppercase,
letter-spacing 2px, right-aligned, 200px wide. `.section__content` 16px weight
300, max-width 650px.

Layout: `.intro` is `padding: 120px 100px`, flex column, `space-around`,
max-width 1440, centred. `.section` is `display:flex; padding: 100px 170px` with
a 200px right-aligned title column, `margin-right: 70px`, then a 650px content
column.

**There is no heading margin reset.** The original leans on UA-default h1/h2/h3
margins and the intro spacing is wrong without them. Do not add one.

Breakpoints (all max-width): `1280 · 1024 · 850 · 768 · 630 · 550 · 480 · 360 ·
330`. At 768 `.section` switches from flex to block; at 850 the footer swaps its
text labels for icons.

The signature interaction is `.highlight-link` on the email address:
`box-shadow: inset 0 -3px 0 #007bff` growing to `inset 0 -33px 0 0 #007bff` on
hover, text going white. A highlighter wipe, not a text-decoration.

## Deliberate changes from the original

Everything below is a decision, not an omission.

| Change | Why |
|---|---|
| **Apercu → Work Sans** | Apercu is a retail licence and cannot be redistributed. Work Sans is the closest free geometric grotesque that ships a real 300 weight, which the whole page is set in. Inconsolata is kept as-is for mono. |
| **Emoji kept as the original's Apple PNGs** | Asad's call, overriding an earlier Twemoji substitution: the files are already published on the live v3 site, and Twemoji made the intro read as somebody else's page. This is the one place art is taken from `docs/reference-bc-v3/`. Emoji-as-punctuation is the voice: a wave in the greeting, a technologist ending the tagline, a pointer at the email, horns in the footer, a finger on the top button. |
| **Clock-based theme → `prefers-color-scheme` + `localStorage`** | The original picked dark between 7pm and 7am and never remembered your choice, so it would overrule you on every reload. Now the OS decides the first visit and the visitor's own choice wins forever after. It keeps following the OS only while no choice has been made. |
| **Toggle listener moved to the input's `change`** | The original listened on the LABEL and read `input.checked` *before* the click applied, so its branches read inverted. On `change` the state is already flipped: checked IS night, no inversion. Rewiring one without the other flips the whole page. |
| **`.intro { height: 100vh }` → `min-height`** | The original clips its own content on a short viewport. |
| **`maximum-scale` / `user-scalable=no` dropped, `lang="en"` added** | Blocking pinch-zoom is an accessibility failure, and the document had no language. |
| **`:focus-visible` added to `.highlight-link`** | The one interactive element in the hero had no keyboard state at all. Also added to the theme toggle, whose input is visually hidden, so the ring is drawn on the rail. |
| **ScrollReveal (unversioned CDN) → IntersectionObserver** | The original pulled `unpkg.com/scrollreveal` with no version pin, so the page's animation could change under it at any time. The replacement uses the original's OWN easing and offset, which were already sitting unused in `_base.scss` as the `.waypoint` / `.in-view` pair: `opacity 0→1`, `translate3d(0,20px,0)→translateZ(0)`, `0.6s cubic-bezier(.694,0,.335,1)`. Per-section view factors (0.3 / 0.3 / 0.2 / 0.1 / 0.05) are carried over verbatim. |
| **jQuery dropped** | It was there for a fade and a scroll animation. Both are one CSS class and one `scrollTo({behavior:'smooth'})`. |
| **`twitter:card` → `summary_large_image`** | The card carries a 1200x630 image. |
| **`arrow.png` → `arrow.svg` through a CSS mask** | Same glyph, one file, no separate white copy. The mask is painted `--blue`, not `currentColor`: the original's `arrow.png` is a flat `#007fff` arrow and stays blue in BOTH themes, so inheriting the text colour was wrong. |
| **`position: relative` added to `.status__light`** | Not a port, a fix. The ring and the LED are absolutely positioned with no positioned ancestor in the original, so they would have flown to the page corner. The block was commented out in `_includes/background.html`, so the bug never shipped. |
| **Featured images are WebP** | Nine photographic screens that must keep a real alpha channel. As PNG-24 the set is ~3 MB; as WebP it is ~370 KB for the same picture. Alpha-WebP goes back to Safari 14 / iOS 14, so there is no fallback to carry. |
| **`height: auto` on featured images** | They carry `width`/`height` attributes so the row does not jump as the WebP loads. Those attributes also land as a presentational `height: 900px`, which stretches every device once the width goes fluid. |
| **Scroll-past fallback in the reveal** | An IntersectionObserver only fires on a change, so a section jumped clean over (deep link, restored scroll position, End key) never intersects and would stay invisible for good. Anything above the fold is now revealed unconditionally. Also `prefers-reduced-motion` and `html.no-js` short-circuit the whole effect. |
| **The `.status` badge is switched ON** | Fully styled but commented out in the original. Used here for "Open to remote work and to relocation with visa sponsorship". |

## Content

Every fact comes from `docs/CONTENT.md`. Nothing is invented.

- **intro** — `Hello! 👋` / `I'm Muhammad Asad, a senior iOS engineer …  👨‍💻` /
  `Get in touch 👉 m.asad.chatthaa@gmail.com`
- **background** — bio, book, SwifterSwift, IDVKit, and the relocation status badge
- **skills** — Languages / UI / Apple frameworks / Tools, mapped off CONTENT.md's
  skill block. The original's fourth column is "Design"; there is no design
  column here because Asad is not a designer.
- **experience** — the four employers, most recent first. Company names are plain
  text, not links: CONTENT.md has no employer URLs and inventing them is not on.
- **featured-projects** — Athanify, Shelly, HiiKER. HiiKER's third device is the
  Apple Watch, not a third phone: the watch is the part of HiiKER that earns the
  "works where the signal does not" claim, and it reads as a platform rather
  than as three screenshots.
- **other-projects** — the remaining 13 apps plus the book and SwifterSwift.
  Votari sits here now that Shelly has taken its place in the featured row.

Positioning is deliberately BROAD. Screen Time is one niche among many — health,
fintech, mapping, encryption and VoIP, blockchain, social, on-device ML, NFC,
productivity. Do not narrow the page back down to Screen Time.

Only apps Asad actually built. **Foqos is NOT his and must never appear.** Verify
every App Store link against `memory/user_portfolio_app_store_links.md`.

## Files

```
index.html                  the whole page
css/main.css                one stylesheet, in the original's partial order,
                            then the nine breakpoints at the bottom
js/main.js                  theme, top button, wave, scroll reveal
img/emojis/*.png            the original's Apple emoji — wave, technologist,
                            pointright, rockon, pointing-up
img/social/*.svg            8 footer marks, all painted #007bff
img/switch/*.svg            sun + moon, two colourways for the two grounds
img/arrow.svg               the arrow-link chevron, used as a CSS mask
img/favicon.svg             Twemoji mobile phone
img/featured/*.webp         9 transparent devices, 3 per featured project
img/og.jpg                  1200x630 social preview
tools/build_assets.sh       regenerates every icon, emoji and glyph
tools/build_devices.py      regenerates the featured device art + og.jpg
Muhammad_Asad_Resume_2026.pdf   frozen copy, same file v1 ships
netlify.toml
```

## Regenerating assets

```bash
bash archives/v3/tools/build_assets.sh      # icons, emoji, glyphs, then calls:
python3 archives/v3/tools/build_devices.py  # featured device art + og.jpg
```

`build_assets.sh` installs `@twemoji/svg`, `simple-icons` and `devicon` into a
temp dir with `--ignore-scripts` and writes only into `img/`. It needs node on
PATH. `curl` is blocked in the sandbox; `npm` works.

Note: simple-icons **dropped the LinkedIn mark** on a trademark request, so
LinkedIn comes from devicon's `linkedin-plain.svg`. Use `-plain`, not
`-original`: `-plain` is one path whose counters cut out the "in", so a flat
recolour still reads. `-original` is two stacked paths and goes solid.

### Featured device art — the rule that matters

**Do NOT reuse `archives/v1/img/card-*.png` here.** v1 composites each project
into one 1280x800 card on a dark navy gradient. Both halves of that are wrong
for v3:

1. v3's featured row is `.project__pic.phones` — a flex row of three **separate**
   `.phone` elements pulled together by `margin: 0 -7%`. The tucking is done in
   CSS, so the art has to arrive as three individual devices.
2. v3 is **light by default**. A baked navy gradient sits as a heavy rectangle
   on a white page.

So `build_devices.py` emits transparent devices with no background at all, and
the page ground shows through — white in light, `#171c28` in `body.night`.

Everything else carries over from `archives/v1/tools/build_cards.py`, which is
still the reference for the keying paths, the watch detection (aspect > 0.55 →
scale 0.58) and the layout maths. Read it before changing anything here.

**The transparent padding on each plate is load-bearing.** Solve the flex row:
three items, each `-7%` of the container (the first `-5%` on its left), shrunk to
fit width W. Content width settles at `0.467W`, and neighbouring content boxes
overlap by `0.14W` — 30% of a canvas. The original's phone plates carry 19.4%
transparent padding per side, so 38.8% of clear space absorbs that 30% and the
**devices never actually touch**; only the empty canvases do. Trim the padding
off and the same CSS drives the phones straight through each other. `DEVICE_FRAC
= 0.613` in the script is that ratio, measured off the original plates.

Sources are real transparent RGBA mocks only. Nothing is keyed, nothing is
guessed. If a project has no transparent mock it does not go in the featured row.

| Project | Source |
|---|---|
| Athanify | `~/Documents/Career/Other Docs/Mocks/Athanify/` |
| Shelly | `~/Documents/Career/Other Docs/Mocks/(Shelby) apple-iphone-15-pro-max-white-titanium-mockup/` |
| HiiKER | `~/Documents/Business/Freelancer.com/Mocups/Hiiker/` (phones) + `~/Documents/Career/Other Docs/Mocks/Hiiker/` (Apple Watch) |

The lead screen of each set is deliberately the most colourful one. On a white
ground a near-white app screen collapses into the page and only the rim reads.

### PII — check this on EVERY new mockup

Three screens carry Asad's real personal data. The mosaic-then-blur copies in
`archives/v1/img/src/` stand in for them, and `build_devices.py` **exits** if a
source filename matches the un-redacted original:

| Redacted copy | Replaces | What was exposed |
|---|---|---|
| `votari-passport-redacted.png` | `IMG_9907-portrait.png` | Passport photo, number, surname, given name, DOB, nationality (Votari is no longer in the featured row, but the guard stays) |
| `pryvate-number-redacted.png` | `IMG_9894-portrait.png` | Real mobile number |
| `hiiker-email-redacted.png` | `IMG_6966-portrait.png` | Real name and email address |

All nine screens in this build were opened at full size and checked. Redaction is
mosaic-then-blur, never blur alone — a plain blur at web scale is still readable
when zoomed. Originals are left untouched.

Before adding any new device, open every screen at full size and look for: phone
numbers, email addresses, real names, passport or CNIC data, dates of birth,
addresses, account balances, API keys, client names under NDA.

## Local preview

```bash
cd archives/v3
python3 -m http.server 8919
open http://localhost:8919/index.html
```

`file://` will not work — relative asset paths and `localStorage` both behave
differently there. Always use the local server.

Scroll-revealed sections are invisible until scrolled. To check layout in one
shot, render a temporary copy with the reveal disabled and delete it after:

```bash
python3 - <<'PY'
s = open('index.html').read()
open('_revealall.html', 'w').write(s.replace(
    '<link rel="stylesheet" href="css/main.css">',
    '<link rel="stylesheet" href="css/main.css">\n'
    '  <style>.waypoint{opacity:1!important;transform:none!important}</style>'))
PY
```

## Deploy

Separate Netlify site from the main one and from v1, same repo.

1. Netlify → Add new site → Import from `masadchattha/asadchattha-com`
2. Base directory `archives/v3`, build command empty, publish directory `archives/v3`
3. Domain management → add custom domain `v3.asadchattha.com`
4. Spaceship DNS → add `CNAME` record: host `v3` → value `<site-name>.netlify.app`
5. Wait for the Let's Encrypt cert, then link it from the Time Machine on the main site

DNS lives at Spaceship (registrar + nameservers). Do not create a Cloudflare zone
for this domain.
