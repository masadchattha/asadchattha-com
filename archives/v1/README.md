# v1 — asadchattha.com (archived version 1)

Frozen snapshot of the first version of Asad's personal site. Lives at
**v1.asadchattha.com** and is linked from the Time Machine on the current site.

Built 2026-08-14.

## What it is

A single-page portfolio in the classic 2016-era Bootstrap 3 pattern: fixed
transparent nav that goes solid on scroll, a full-bleed parallax hero, and
waypoint-triggered fade-ins per section.

Deliberately period-accurate. It is the "version 1" in the Time Machine, so it
should look like a first personal site, not like the current one.

## Stack

No build step. Open `index.html` and it runs.

| Layer | What |
|---|---|
| Grid / components | Bootstrap 3 (`css/bootstrap.min.css`, `js/bootstrap.min.js`) |
| Animations | animate.css + jQuery Waypoints (`js/custom.js` wires `.wp1`–`.wp6`) |
| Icons | Font Awesome 4 |
| Smooth scroll | jQuery easing + scrollTo |
| Type | Lato (headings, nav, buttons) + Roboto Slab (body copy) via Google Fonts |

## Design tokens

| Token | Value |
|---|---|
| Accent | `#00009C` |
| Body text | `#000` |
| Alt section background | `#F0F0F0` |
| Footer background | `#222`, social tiles `#333` |
| Hero h1 | 60px / weight 300 / letter-spacing 3px / uppercase |
| Section h2 | Lato 300, uppercase, letter-spacing 1px |
| Body copy | Roboto Slab 300, 16px, line-height 1.7 |
| Hero + résumé overlay | black gradient, 0.8 top → 0.4 bottom, `background-attachment: fixed` |

To reskin to the teal used on the current site, change `#00009C` in
`css/styles.css` (7 occurrences) and `img/favicon.svg`.

## Files

```
index.html                  the whole page
css/styles.css              layout system + v1 overrides (bottom of file)
js/custom.js                waypoints, nav collapse, smooth scroll, to-top hover
img/hero-mountains.jpg      hero background. Built from a licensed Unsplash photo
                            (matteo-catanese-4KrQq8Z6Y5c) by tools/build_hero.py:
                            the tall portrait is fitted by HEIGHT and centred so
                            sky, peak and reflection all survive, then the flanks
                            are filled with the same frame stretched horizontally
                            and blurred, feathered in over 300px. Stretching keeps
                            every horizontal line at its original height, so the
                            horizon and shore continue across the band.
img/resume-band.jpg         résumé band background — generated locally with PIL
img/headshot.jpg            Asad's profile photo, cropped square
img/skills/*.svg            18 OFFICIAL brand logos. Multi-colour originals from
                            `devicon` (MIT) where they exist, single-colour brand
                            marks from `simple-icons` (CC0) for the rest.
                            Greyscale by default, true colour on hover, name
                            revealed under the icon on hover.
img/logo-*.svg              4 employer wordmarks
img/logo-white.svg          "A" monogram, thin-stroke line mark. Nav brand links
                            to https://asadchattha.com
img/favicon.svg             the same mark in the accent #00009C
img/rocket.svg              back-to-top mark
img/card-*.png              16 project cards, all 1280x800 on one shared navy backdrop
                            (built from ~/Documents/Career/Claude/mockups + main/public/images/projects
                             by the card builder — auto-crops the phone band out of each mockup,
                             drops the title and App Store badge, then composites with a drop shadow)
resume2026.pdf
```

Both background images are generated, not stock photography — regenerate or
swap them freely, they carry no licence obligations.

## Content rules

Everything claimed on this page must be true and verifiable:

- Only apps Asad actually built. Forking or studying a repo is not authorship.
  Foqos is NOT his and must never appear here.
- App Store links only where the app is live and the link is verified against
  `memory/user_portfolio_app_store_links.md`, which is the source of truth.
- IDVKit has no public listing, so its modal deliberately has no "View on the
  App Store" button. Do not add one.
- Soar is a real client app but no mockup exists yet, so it is not in the grid.
  Add it when artwork arrives.
- Positioning is deliberately BROAD. Screen Time is one niche among many —
  health, fintech, maps, encryption/VoIP, blockchain, social, on-device ML,
  productivity. Do not narrow the page back down to Screen Time.

## Deploy

Separate Netlify site from the main one, same repo.

1. Netlify → Add new site → Import from `masadchattha/asadchattha-com`
2. Base directory `archives/v1`, build command empty, publish directory `archives/v1`
3. Domain management → add custom domain `v1.asadchattha.com`
4. Spaceship DNS → add `CNAME` record: host `v1` → value `<site-name>.netlify.app`
5. Wait for the Let's Encrypt cert, then link it from the Time Machine on the main site

DNS lives at Spaceship (registrar + nameservers). Do not create a Cloudflare
zone for this domain.

## Local preview

```bash
cd archives/v1
python3 -m http.server 8917
open http://localhost:8917/index.html
```

`file://` will not work — the Chrome extension rejects it and relative asset
paths behave differently. Always use the local server.


## Regenerating assets

### Project cards
```bash
python3 tools/build_cards.py
```
Card rule, which also lives in `~/.claude/CLAUDE.md` and applies to every future
archived version:

- The card background is ONE flat gradient. Nothing else.
- Device frames sit DIRECTLY on that gradient, side by side, straight out of the
  mockup. No inner panel, no rounded card behind them, no drop shadow, no second
  background layer.
- The mockup's own background is keyed out, so source mockups must sit on a FLAT
  background. Artwork already on its own gradient cannot be keyed — put it in
  `PLACEHOLDERS` until a flat mockup exists.
- Missing artwork gets a plain text card on the same gradient. Never invent app UI.

Source priority — always work down this list:

1. **`TRANSPARENT`** — real transparent RGBA device PNGs. Nothing to key, nothing
   to guess. **This is the preferred source.**
   `~/Documents/Career/Other Docs/Mocks/`
   Devices are laid out equal size, evenly spaced, and **never overlapping**.
2. **`AS_IS`** — brand graphics that already carry their own designed background.
   Used exactly as supplied, contained so nothing is cropped, padded with the
   artwork's own background colour. **No gradient behind these.** IDVKit is the
   only one today.
3. **`MOCKUPS`** — everything else, keyed onto the gradient.

Two keying modes for `MOCKUPS`:

| `key` | For | Example |
|---|---|---|
| `'flat'` | Mockup on a solid background. Also strips the title row and the App Store badge. | `~/Documents/Career/Claude/mockups/*.png` |
| `'gradient'` | Artwork already on its own smooth gradient. Models the background per row from the left/right edge and masks anything that departs from it. | `main/public/images/projects/*.png` |

IDVKit is a brand graphic rather than devices, so it is cropped to the passport
half (`crop=(0.47, 0, 1, 1)`) — the dark IDVKit wordmark would be unreadable on
the dark gradient.

**Soar** is deliberately not in the grid.

Plant Health's third frame (`IMG_9174`) shipped as flat RGB on black, and the
phone's own bezel is the same black, so an edge key would eat the frame. It is
instead cropped to its content box and given a rounded-rect alpha mask, saved as
`img/src/planthealth-diagnosis.png`.

### PII redaction — check this on EVERY new mockup

App screenshots routinely contain Asad's real personal data. Two were caught on
this build and are mosaicked in `img/src/`, which the builder uses in place of
the originals:

| File | What was exposed |
|---|---|
| `img/src/votari-passport-redacted.png` | Passport photo, passport number, surname, given name, date of birth, nationality |
| `img/src/pryvate-number-redacted.png` | Real mobile number |
| `img/src/hiiker-email-redacted.png` | Real name and email address |

Redaction is mosaic-then-blur, never blur alone — a plain blur at web scale can
still be read when zoomed. Originals in `~/Documents/Career/Other Docs/Mocks/`
are left untouched.

**Before adding any new card, open every screen at full size and look for:**
phone numbers, email addresses, real names, passport or CNIC data, dates of
birth, addresses, account balances, API keys, client names under NDA.

### Asset source paths
| What | Where |
|---|---|
| v0 / current-site project art (on their own gradient) | `main/public/images/projects/` |
| Flat device mockups | `~/Documents/Career/Claude/mockups/` |
| More mockups incl. iPad frames | `~/Documents/Business/Project images/Nomal - upwork style/` and `Large Mockups/` |
| **Transparent device mocks (preferred)** | `~/Documents/Career/Other Docs/Mocks/` — Athanify, Shelly ("Shelby"), Votari, Peptify, Focus Bear, HiiKER |
| **Transparent device mocks (preferred)** | `~/Documents/Business/Freelancer.com/Mocups/` — 1st-Response, GoingSolo, Hiiker, Offietree |
| App icons | `~/Desktop/portfolio icons/` |

**Never key a background off the v0 art in `main/public/images/projects/`.** If a
transparent mock is missing, ask Asad for it rather than keying.

Still waiting on transparent mocks:

| Project | Status |
|---|---|
| Block | flat mockup only |
| Chapter | flat mockup only |
| Bright Start | flat mockup only |
| Fonder Cards | flat mockup only |
| Focus Bear | only ONE transparent screen exists, so its card shows a single device — needs two more |
| Headshot source | `../../shared-assets/asad-portrait-office.jpg` |

### Skill logos
Official marks, never drawings. Two packages, in this order:

1. **`devicon`** (MIT) — `<name>/<name>-original.svg` are the true MULTI-COLOUR
   logos. Always prefer these: Swift, Xcode, Firebase, Figma, SQLite, Postman,
   Git, GitHub. Objective-C only ships `-plain`.
2. **`simple-icons`** (CC0) — single-colour marks, filled with the official
   brand hex, for anything devicon lacks: iOS, App Store, Apple Pay, RevenueCat,
   Stripe, Bitcoin SV, CocoaPods, Fastlane, Charles.

```bash
mkdir -p /tmp/icons2 && cd /tmp/icons2 && npm install devicon --ignore-scripts
cp node_modules/devicon/icons/swift/swift-original.svg <repo>/archives/v1/img/skills/swift.svg
# ...and so on for the devicon set
```

The `simple-icons` half:

```bash
mkdir -p /tmp/icons && cd /tmp/icons && npm install simple-icons --ignore-scripts
node -e "const si=require('simple-icons'),fs=require('fs');
const OUT='<repo>/archives/v1/img/skills/';
const want=['swift','ios','xcode','appstore','applepay','firebase','revenuecat','stripe',
            'sqlite','cocoapods','fastlane','charles','postman','kotlin','android','git','github','figma'];
const override={ios:'#000000',applepay:'#000000',charles:'#5A6B73',fastlane:'#00B300'};
for(const w of want){const ic=si['si'+w[0].toUpperCase()+w.slice(1)];
 fs.writeFileSync(OUT+w+'.svg','<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"96\" height=\"96\"><path fill=\"'+(override[w]||'#'+ic.hex)+'\" d=\"'+ic.path+'\"/></svg>');}"
```

Deliberately NOT in the grid: **Android** and **Kotlin** — Asad is an iOS
engineer and neither is a load-bearing skill, so they read as padding.

`img/skills/proxyman.png` is the only raster icon — Asad supplied the official
app icon directly because Proxyman is in neither package.

**Still impossible — no official logo in either package, and none supplied:**
OneSignal, Superwall, Tap2Pay, Swift Package Manager, Core Data, SwiftData,
HealthKit, watchOS, Core ML, Create ML, OpenAI/ChatGPT. Do not hand-draw
substitutes; Asad rejected drawn icons. SQLite stands in for Core Data /
SwiftData because Core Data sits on SQLite and at least has a real mark.

Skill names sit under each icon: hidden at rest, revealed on hover, and always
visible on touch devices where there is no hover.

**Why no SwiftUI / HealthKit / Core ML / MapKit / Core Data:**
Apple ships no downloadable logo for its frameworks, and simple-icons has none
either. Rather than draw fakes, those frameworks are named in the About and
"What I Do" copy instead. Do not substitute hand-drawn glyphs for them — Asad
rejected that.

Note: simple-icons' `uikit` is the UIkit CSS framework, NOT Apple's UIKit.
Never use it here.
