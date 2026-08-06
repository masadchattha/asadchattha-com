# Reference version research — brittanychiang.com v1 → v4

Captured live from the running sites on 2026-08-14 via the browser, reading
computed styles and CSS custom properties rather than guessing from screenshots.

Purpose: know exactly what each era looked like before building
`v2.asadchattha.com`, `v3.asadchattha.com`, `v4.asadchattha.com`.

---

## v1 — 2016, Bootstrap 3 era  ✅ ALREADY BUILT

Fully documented in `archives/v1/README.md`. Summary for comparison:

| | |
|---|---|
| Theme | Light, white sections alternating `#F0F0F0` |
| Accent | `#00009C` deep navy |
| Type | Lato (headings, nav) + Roboto Slab (body) |
| Hero | Full-bleed photo, black gradient overlay 0.8 → 0.4, `background-attachment: fixed` |
| Nav | Fixed, transparent over hero, solid black on scroll |
| Motion | jQuery Waypoints + animate.css fade-ins |
| Contact | `mailto:` link, opens in a new tab |
| Stack | Bootstrap 3, jQuery, Font Awesome 4 |

---

## v2 — the dark parallax era

| | |
|---|---|
| Theme | **Dark.** Body `#1B1B1B`, text `#F2F2F2` |
| Accent | **`rgb(0,183,199)` — cyan/teal.** Hover state `rgb(0,144,156)` |
| Type | **Chronicle Display Bold** (serif) for h1, **Gotham** for h2, **Whitney** for body |
| h1 | 72px, weight 700, serif — a big serif name over a starfield photo |
| h2 | 20px, Gotham, weight 700, **uppercase** |
| Hero | Full-screen night-sky/mountain photo, name centred, subtitle in spaced uppercase |
| Nav | **Dot nav** (`#dot-nav`) — fixed vertical dots on the right, one per section |
| Motion | **skrollr** parallax (`#skrollr-body`) — background images move at a different rate to content |
| Sections | intro · about · services · skills · experience (`#timeline`) · portfolio · contact · footer |
| Experience | A **vertical timeline**, not a logo row |
| Contact | **A real contact form** (name / email / subject / message) posting to Formspree, with a `_gotcha` honeypot field |
| Extras | Circular headshot; thin accent rule under the intro line |

**What to steal for v2.asadchattha.com:** the dot nav, the parallax, the serif
display face over a photographic hero, the timeline treatment for the o9 Tech /
Coder Crew / Pryvate / Elentra run, and a working contact form.

---

## v3 — the minimalist single-screen era

| | |
|---|---|
| Theme | **Light by default, `#FFFFFF`**, text `rgb(68,68,82)` |
| Accent | **`#007BFF` blue** |
| Type | **Apercu** for everything, **Inconsolata** for monospace |
| h1 | Only 40px, weight **300** — deliberately quiet |
| Layout | **One screen. No sections, no nav, no scroll.** Just a greeting, one sentence, and an email link |
| Copy | `Hello! 👋` then "I'm Brittany Chiang, a design-minded front-end software engineer focused on building beautiful interfaces & experiences 👩‍💻" |
| Emoji | **Used as punctuation** — 👋 in the greeting, 👩‍💻 ending the sentence, 👉 pointing at the email |
| Theme toggle | **Yes.** `#switch` / `#toggle`, a sun icon + pill switch + moon icon, top right |
| Contact | Plain `mailto:` link, underlined in the accent blue |
| Extras | `#top-button` back-to-top |

**What to steal for v3.asadchattha.com:** the discipline. One screen, one
sentence, one link, a light/dark toggle. This is the version that proves taste
by subtraction — the hardest one to get right and the fastest to build.

---

## v4 — the navy/teal era  ⚠️ PARTIAL CAPTURE

This is the design the **current asadchattha.com is already modelled on**, so
v4.asadchattha.com would collide with the live site. Worth deciding whether to
build it at all, or to skip from v3 straight to the current site.

Palette captured directly from its CSS custom properties:

```css
--navy:           #0a192f
--light-navy:     #112240
--slate:          #8892b0
--light-slate:    #a8b2d1
--lightest-slate: #ccd6f6
--green:          #64ffda      /* the teal accent */
--font-sans:      'Calibre','Inter','San Francisco','SF Pro Text',-apple-system,system-ui,sans-serif
--font-mono:      'SF Mono','Fira Code','Fira Mono','Roboto Mono',monospace
```

| | |
|---|---|
| Theme | Dark navy `#0a192f`, body text `#8892b0`, base size **20px** |
| Accent | `#64ffda` teal |
| Type | **Calibre** sans + **SF Mono** for numbering, section labels and small caps |
| Stack | Gatsby / React SPA with an animated intro loader |

**Gap:** the intro loader did not finish in the capture environment, so the DOM
never rendered — section structure, nav, project cards, hover behaviour and the
scroll-reveal timings are NOT yet documented. That needs a second pass with the
loader bypassed or the GitHub source read directly
(`github.com/bchiang7/v4.brittanychiang.com`).

---

## The arc, in one line each

- **v1** — light, Bootstrap, photographic hero, "here is everything about me"
- **v2** — dark, parallax, serif display, dot nav, timeline, contact form
- **v3** — light, one screen, one sentence, emoji, theme toggle
- **v4** — navy + teal, monospace accents, React, animated reveals
- **v5 / current** — refinement of v4 with a cursor spotlight

Each version gets **quieter and more confident**. v1 shouts, v3 whispers.

---

## Still to research

1. **v4 section structure** — bypass the loader or read the GitHub source
2. **v5 / current brittanychiang.com** — the cursor spotlight, the sticky
   left column, the experience list hover states
3. Per version: exact scroll-reveal timings, easing curves, link hover
   transitions, focus states, mobile breakpoints, 404 page, favicon, OG image
4. Whether each version's source is on GitHub — `bchiang7` has public repos for
   several, which would settle every open question far faster than probing the
   live DOM

## Content that carries across every version

Regardless of era, each rebuild needs Asad's own: 16 App Store projects, the
o9 Tech / Coder Crew / Pryvate / Elentra history, SwifterSwift, the UIKit book,
and the same PII discipline — every screenshot checked before it ships.
