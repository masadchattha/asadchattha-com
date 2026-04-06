# V1 Design Spec — Time Machine version 1 (clone of v1.brittanychiang.com, 2016)

Source of truth: her actual repo, cloned and read line by line — `github.com/bchiang7/v1`
(901-line `index.html`, 1,979-line `css/styles.css`, 23 MB `img/`). Live site cross-checked
at v1.brittanychiang.com. Local clone during research: scratchpad `bc-v1/`. Re-clone any time.

## 1. Tech stack (hers, to be followed exactly)

- **Static HTML, single page** `index.html` + `404.html`. No build system, no framework.
- **Bootstrap 3** (`css/bootstrap.css`, `js/bootstrap.min.js`) — grid `col-xs/sm/md`, modals, scrollspy (`body data-spy="scroll" data-target=".navbar-custom" data-offset="100"`).
- **jQuery 1.11 / 2.1.3** + `jquery.easing.1.3.js` + `jquery.scrollTo.min.js` — smooth anchor scroll, nav collapse, progress-bar animation triggers.
- **Font Awesome 4** (`font-awesome/`) — ALL icons come from FA4 (`fa fa-*`).
- **animate.css** — entrance animations (`animated fadeInDown delay-05s`, `fadeInUp`), plus `wp1..wp4` classes for scroll-triggered waypoints.
- **Google Fonts:** `Lato` (100–900 + italics) for headings/nav/UI, `Roboto Slab` (100,300,400,700) secondary. Body fallback: Helvetica Neue.
- Résumé PDF at repo root (`resume2016.pdf`) — ours: link `/resume.pdf` from main site.

## 2. Palette (from styles.css frequency scan)

| Token | Value | Use |
|---|---|---|
| Black | `#000` | Fixed navbar bg, hero/resume overlays, headings |
| White | `#fff` | Section bg, hero text, resume text |
| Brand blue | `#00009C` (9 uses) | Logo tint, link/accent moments |
| Alt section grey | `#F0F0F0` | Services + TL;DR strip bg |
| Footer | `#222` | Footer bg (white text) |
| Text grey | `#555` / `#333` / `#444` | Body copy |
| Accent yellow | `#fed136` | Small accents |
| Progress colors | red / blue / purple / green / orange (`progressred|blue|purple|green|orange`) | Skill bars |

## 3. Page structure (section by section, her exact order)

1. **Fixed nav** `.navbar-custom navbar-fixed-top` — bg `#000`, Lato uppercase.
   Left: logo image (`logo-transparent-white-30pt.png`) + NAME. Right links: ABOUT · PASSION · EXPERIENCE · WORK · CONTACT (scrollspy highlights).
2. **`#intro`** — full-screen hero. `background: url(img/mountain-dusk.jpg)` + `.overlay` (black, translucent). Centered `.intro-content` (`padding: 20% 0 5%`): `h1` 60px Lato "Hi, I'm Brittany" `animated fadeInDown delay-05s`; `p.subtitle` "Web Developer & UX Enthusiast" `fadeInUp`; `a.fa.fa-angle-down.page-scroll` bouncing arrow → `#about`.
3. **`#about`** — white, centered. `h2` "A Little Bit About Me"; circular headshot `#prof-pic` (`headshot1-square4.jpg`); one paragraph with inline links; then **TL;DR strip** `#tl-dr` (grey band): `h3` "TL;DR?  Self Proclamations:" + three `.tldr-proc` items, each a 50px FA icon circle + `h5` label: `fa-keyboard-o` Web Developer · `fa-pencil` UX Enthusiast · `fa-tree` Snowboarder.
4. **`#services`** — bg `#F0F0F0`, `h2` "What I Do", three columns each with big FA icon + title + blurb (icons incl. `fa-laptop`, `fa-lightbulb-o`, `fa-paper-plane-o`).
5. **`#experience`** — white, two halves:
   a. **Animated skill bars**: rows of `span.percent` + `span.progressbar.progress{red|blue|purple|green|orange}.wp3-N` for HTML/CSS/JavaScript/Angular/PHP — width animates on scroll-into-view, percent counts up (jQuery).
   b. **Skill icon grid**: `col-xs-3 col-sm-2` PNGs from `img/skills/` (html, css, sass, js, java, python, jquery, bootstrap, foundation, angular, node, mongodb, github, photoshop, indesign, jira, linux, tumblr).
   c. **"Where I've Worked:"** column with employer logos (Mullen octopus, Northeastern).
6. **`#resume`** — CTA band. `background: url(img/laptop-blur.jpg); background-attachment: fixed` (parallax) + black overlay. `h2` "Check out my résumé!" + ghost button `a.resume-btn.wp4` "Grab A Copy" → PDF.
7. **`#portfolio`** — white. `h2` "What I've Done" + `h5.coming-soon` "(more coming soon)". Grid of `.portfolio-item` cards (180px `.portfolio-hover` with image + hover overlay `.hover-text` showing title + `fa-search-plus` / `fa-link`). Each card opens a **Bootstrap modal** (`#courseSourceModal`, `#feedbackLoopModal`, `#webdevModal`, `#fontipsumsModal`, `#nuwitModal`, `#uscModal`, `#calendrModal`, `#bookmarksModal`, `#hciWebsiteModal`, `#humankindaModal`, `#lovesacModal`, `#medMilModal`, `#oblivionThemesModal`, `#oneCardForAllModal`) with screenshots, description, tech list, links.
8. **`footer`** — bg `#222`, white. "Beam me up, Scotty!" scroll-to-top link, social FA icons (`fa-linkedin`, `fa-twitter`, `fa-pinterest`, `fa-spotify`, ...), "© Brittany Chiang 2016".

## 4. Assets inventory (her repo → what we reuse vs replace)

**Reuse as-is (same icons/effects per Asad's instruction):** Font Awesome 4 kit, animate.css, Bootstrap 3, easing/scrollTo JS, section/overlay CSS patterns, progress-bar CSS classes.
**Reuse her background photos** (generic scenery, in cloned repo): `mountain-dusk.jpg` (hero), `laptop-blur.jpg` (resume band), alternates: `mountain-sunset.jpg`, `foggy-woods.jpg`, `milkiest-way.jpg`.
**Replace with ours:**
- Logo → Asad "A" monogram, white transparent PNG 30pt equivalent (source: main site favicon SVG → PNG).
- Headshot → Asad profile photo (square, will render as circle).
- Skill icon PNGs → swift, swiftui (custom), xcode, objective-c, firebase, supabase, github, figma, postman, linux (hers), python (hers), nodejs (hers). Style: flat single-logo PNGs on transparent, like `img/skills/*`.
- Employer logos → o9 Tech, Coder Crew, Pryvate Technologies, Elentra Tech (white/mono versions).
- Portfolio screenshots → app tiles already produced for main site (`main/public/images/projects/*.png`).

## 5. Content mapping (Asad's v1 content, 2016-era voice, honest)

- Nav name: **MUHAMMAD ASAD** · links ABOUT · PASSION · EXPERIENCE · WORK · CONTACT (keep her labels).
- Hero: "Hi, I'm Asad" / subtitle "iOS Engineer & App Craftsman". Same animations.
- About: 1 paragraph (6 years, 16 apps, Lahore; inline links to App Store profile + book). TL;DR trio: `fa-mobile` iOS Engineer · `fa-lightbulb-o` Indie Builder · `fa-tree` Hiker.
- What I Do (3 cols): `fa-mobile` Native iOS Apps · `fa-lock` Identity & Privacy (KYC, encryption) · `fa-line-chart` Ship & Grow (StoreKit, paywalls).
- Skill bars (5, her colors in order): Swift · SwiftUI · UIKit · Objective-C · CoreML (percents chosen when implementing; count-up animation identical).
- Where I've Worked: o9 Tech · Coder Crew · Pryvate · Elentra.
- Resume band: "Check out my résumé!" → `https://asadchattha.com/resume.pdf` (same ghost button).
- Portfolio grid + modals (8 cards): Athanify, Foqos, IDVKit, HiiKER, Pryvate, Votari, Going Solo, Focus Bear. Modal = screenshot, 2-3 lines, tech list, App Store/GitHub link. Keep "(more coming soon)".
- Footer: keep "Beam me up, Scotty!" (homage, like the CodePen credit on the main site) + Asad socials + "© Muhammad Asad".

## 6. Implementation plan

1. **Scaffold** `archives/v1/` in this repo: `index.html`, `css/` (bootstrap.css, styles.css port, animate.css, normalize), `js/` (same libs, CDN where she used CDN), `font-awesome/`, `img/`, copying her file layout name-for-name.
2. Port `styles.css` keeping selectors/ids identical; only content-specific values change.
3. Produce assets per §4 (skill PNGs, logo, headshot, bg photos copied from clone).
4. Netlify: second site (or same project + subdomain rule) serving `archives/v1` at **v1.asadchattha.com**; Spaceship DNS: CNAME `v1` → that Netlify site. HTTPS auto.
5. Main site: Time Machine v1 tile — replace "Coming soon" with live screenshot linking `https://v1.asadchattha.com`.
6. QA: scrollspy, modals, progress-bar animation, mobile collapse nav, then commit via backfill schedule.

**Effort:** scaffold+port ~1 session; assets ~1; content+modals ~1; deploy+DNS+tile ~0.5.

---

## 7. ADDENDUM — pixel-level details (extracted from styles.css + index.html, complete)

### Text selection & tap
- `::selection` / `::-moz-selection`: background **#fed136** (yellow), `text-shadow: none`. Images: selection transparent. `webkit-tap-highlight-color: #fed136` on body.

### Nav & favicon
- Favicon: `img/logo-transparent-00009C.png` (brand-blue logo). Ours: "A" monogram tinted #00009C equivalent.
- `.navbar-brand.page-scroll`: 16px, letter-spacing 1px. Nav shadow `.navbar-shadow: 0 1px 1px #444` appears after scroll. Mobile: Bootstrap `navbar-toggle` hamburger, collapse menu.

### Hero (#intro) — exact
- Full-screen, `background: url(img/mountain-dusk.jpg)` cover.
- `.overlay`: vertical black gradient `rgba(0,0,0,.8) 0% → .73 17% → .66 35% → .55 62% → .4 100%` (lighter toward bottom).
- `.intro-content`: absolute, `padding: 20% 0 5%` (mobile ≤768px: `30% 0 5%`).
- `h1`: 60px Lato, white, `animated fadeInDown delay-05s`. `p.subtitle`: color **#ddd**, `fadeInUp`.
- Chevron `a.fa.fa-angle-down`: 50px, color **#aaa** → hover **#fff**, `padding 10px 14px`, `margin-top: 175px` (mobile: 80px; ≥1600px: relative bottom 50px), `transition all .5s`, class `page-scroll` → jQuery scrollTo smooth-scrolls to `#about`.

### About
- `#prof-pic`: width **170px** (≤480px: 150px), circular via border-radius.
- TL;DR icons: `.tldr-icon` 50×50, line-height 50, font-size 36 (FA icons in circles).

### Experience — the B&W icon theme (confirmed)
- `.skills-section .skill-icon img`: **`filter: grayscale(100%)`**, `transition all .3s ease-in-out` → `:hover` removes grayscale (full color). This IS the black-and-white icon look; color is the hover reward. Ours must ship color logos + the same grayscale filter.
- Skill bars: `span.percent` counts up via jQuery; `.progressbar.progress{red|blue|purple|green|orange}` width animates when `.wp3-N` enters viewport.

### Résumé band (#resume) — the fixed-background effect
- `background: url(../img/laptop-blur.jpg); background-size: cover; background-position: center; background-attachment: fixed;` → the image stays pinned while content scrolls over it (classic parallax). Same black gradient overlay as hero.
- `a.resume-btn`: ghost button — transparent bg, `padding 10px 20px`, color **#ddd**, border **2px solid #ccc**, Lato → hover/active: color **#fff**, border stays #ccc.
- NOTE: `background-attachment: fixed` is ignored by iOS Safari (scrolls with content on phones) — that is true on HER live site too. Keep identical; do not "fix".

### Portfolio interactions
- Card: `.portfolio-hover` height 180px (mobile: 100%), image centered, cursor pointer.
- Hover: `.hover-text` (white, absolute, centered) `opacity 0 → 1` on `:hover`, showing title + icons `fa-search-plus` (opens modal) / `fa-link`.
- Click → Bootstrap modal: `h4.modal-title` + `h6.modal-title-description` (type label e.g. "Web App") + `img.img-responsive.img-centered` screenshot + `p.modal-description` + **`p.visit`: `Visit Site` or `View Source`** (both plain text links, `id=visit-btn`) + `button.btn.btn-default` Close.
- **Our button mapping:** "Visit Site" → **"App Store"** text link (NO Apple badge image — her 2016 aesthetic is plain text links; a black App Store badge would break it). "View Source" → kept, only for projects with public repos (IDVKit; others omit it). Type labels: "iOS App", "Open-Source SDK", etc.

### Get In Touch (#contact)
- `.email-icon` with `fa-paper-plane-o` (waypoint-animated), `h2` "Get In Touch!", blurb line, then **"Say Hello"** ghost button: `#email-button` — color **#000**, `border 2px solid #000`, Lato **20px**, `padding 10px 20px`, `transition .3s ease-in-out` (hover inverts to filled black/white text) → `mailto:`. Ours → `mailto:m.asad.chatthaa@gmail.com`.

### Footer
- bg #222. `ul.list-inline.social-buttons animated fadeIn` — FA icons used across page/footer: **facebook, twitter, instagram, spotify, github, codepen, linkedin**. Ours: github, linkedin, twitter(X), instagram + optional codepen→Medium swap (keep FA4 icon set only).
- "Beam me up, Scotty!" = scroll-to-top page-scroll link. "© Brittany Chiang 2016" → "© Muhammad Asad 2016-style".

### Mobile behavior summary (@media ≤768px)
- Container 95% width ≥768. Intro padding deepens to 30% top; chevron margin 80px.
- Hamburger nav (Bootstrap collapse). Skill bars stretch full width, `h3` centered 16px. Portfolio hover regions become full-height. Headshot 150px ≤480px. Resume parallax degrades to scrolling bg on iOS (matches her live site).
