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
