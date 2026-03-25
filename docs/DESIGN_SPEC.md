# asadchattha.com — Design Spec (100% match to brittanychiang.com v5 main)

**Source of truth for the build.** Every value below is CONFIRMED from her live computed styles (2026-07-23). Do not deviate without a change-order note.

---

## Font stack

**Primary:** **Inter** (via Fontsource-Inter, self-hosted)
- Fallback: `-apple-system, BlinkMacSystemFont, sans-serif`
- She uses Inter for EVERYTHING — no separate mono, no serif hero
- Font loader hash on hers: `__inter_20b187` (Next.js internal)

**Astro setup:**
```bash
npm i @fontsource-variable/inter
```
Then in base layout:
```js
import '@fontsource-variable/inter/index.css';
```

---

## Color palette (Tailwind slate + teal — CONFIRMED)

```css
:root {
  /* Base */
  --bg: rgb(15, 23, 42);              /* slate-900 — main background */
  --surface: rgb(30, 41, 59);         /* slate-800 — cards */
  --border: rgb(51, 65, 85);          /* slate-700 */
  
  /* Text */
  --text-body: rgb(148, 163, 184);    /* slate-400 — body text (confirmed) */
  --text-heading: rgb(226, 232, 240); /* slate-200 — headings (confirmed) */
  --text-strong: rgb(241, 245, 249);  /* slate-100 — name/emphasized */
  
  /* Accent — teal (confirmed via selection styles) */
  --accent: rgb(94, 234, 212);        /* teal-300 */
  --accent-strong: rgb(20, 184, 166); /* teal-500 */
  --accent-dim: rgb(153, 246, 228);   /* teal-200 */
  
  /* Selection */
  --selection-bg: rgb(94, 234, 212);  /* teal-300 (confirmed) */
  --selection-fg: rgb(19, 78, 74);    /* teal-900 (confirmed) */
  
  /* Spotlight */
  --spotlight: rgba(29, 78, 216, 0.15); /* blue-700 @ 15% opacity */
}
```

---

## Typography (CONFIRMED from her live computed styles)

| Element | Size | Line-height | Weight | Color | Letter-spacing | Notes |
|---|---|---|---|---|---|---|
| `body` | 16px | 26px | 400 | slate-400 | normal | Inter |
| `h1` (name) | 36px | 40px | 700 | slate-200 | -0.9px | Hero name only |
| `h2` (job title) | 18px | 28px | 500 | slate-200 | -0.45px | Below name |
| `h2` (section title) | 18px | 28px | 500 | slate-200 | -0.45px | Section headers |
| `p` (paragraph) | 16px | 24px | 400 | slate-400 | normal | margin-top 16px |
| Nav `a` | 16px | 26px | 400 | slate-400 | normal | Same as body |
| Footer social icons | 12px | — | — | slate-400 | — | Small icons |
| Skip-to-content link | 14px | 20px | 700 | slate-900 | 1.4px | UPPERCASE, hidden until focus |

**Paragraph spacing:** `margin-top: 16px` between paragraphs (Tailwind `mt-4`).

---

## Section rhythm (CONFIRMED)

```css
section {
  padding: 0;
  margin-bottom: 64px; /* Tailwind mb-16 — CONFIRMED */
}
```

**Container:** max-width around `1280px` with padding.

**Split layout (desktop ≥ 1024px):**
- Left sticky column: `w-1/2 lg:sticky lg:top-0 lg:flex lg:h-screen lg:max-h-screen lg:py-24`
- Right scrolling column: `lg:w-1/2 lg:py-24`

**Mobile (below 1024px):**
- Stacked single column
- No sticky sidebar
- Section spacing collapses to 48px

---

## Links

**Default state:**
```css
a { color: var(--text-body); transition: color 300ms; }
```

**Hover state:**
```css
a:hover, a:focus { color: var(--accent); }
```

**Inline text links with underline animation** (her signature):
```css
.link-underline {
  position: relative;
  color: var(--accent);
}
.link-underline::after {
  content: '';
  position: absolute;
  left: 0; bottom: -2px;
  width: 100%; height: 1px;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 300ms ease-in-out;
}
.link-underline:hover::after {
  transform: scaleX(1);
}
```

**External link arrow icon** (small, top-right after text):
- Icon: Lucide `arrow-up-right`
- Size: 12px
- Color: matches link
- Rotates 45° on hover with 300ms transition

---

## Nav (sticky sidebar left)

**Structure:**
```html
<nav aria-label="In-page jump links">
  <ul>
    <li><a href="#about" class="group">
      <span class="nav-dash"></span>
      <span class="nav-label">About</span>
    </a></li>
    <li><a href="#experience">Experience</a></li>
    <li><a href="#projects">Projects</a></li>
    <li><a href="#writing">Writing</a></li>
  </ul>
</nav>
```

**Nav item states:**
- Default: 16px, slate-500, weight 500, uppercase, letter-spacing 1.4px
- Hover: color → slate-200, dash grows from 32px → 64px
- Active (via IntersectionObserver): color → slate-200, dash 64px, teal accent

**Dash animation:**
```css
.nav-dash {
  display: inline-block;
  width: 32px;
  height: 1px;
  background: currentColor;
  margin-right: 16px;
  transition: width 200ms ease, background 200ms ease;
}
a:hover .nav-dash,
a.active .nav-dash {
  width: 64px;
  background: var(--accent);
}
```

---

## Hero (top-left, sticky)

```
Muhammad Asad          ← H1: 36/40, weight 700, slate-200, -0.9px
Senior iOS Engineer    ← H2: 18/28, weight 500, slate-200, -0.45px

I build native iOS apps that Muslims actually use.  ← P: 16/24, slate-400, mt-16

[nav: About · Experience · Projects · Writing]
                        ↑ sticky column bottom-anchored

[socials: GitHub · LinkedIn · X · Instagram · App Store]
```

Hero title = your NAME only.
Subtitle = short role title.
Tagline = one sentence, 15 words max.

---

## Spotlight (cursor glow)

```html
<div class="spotlight" aria-hidden="true"></div>
```

```css
/* CORRECTED 2026-07-28 — exact computed style pulled live from her site:
   radial-gradient(600px at X Y, rgba(29,78,216,0.15), rgba(0,0,0,0) 80%)
   Fade stop is 80% NOT 40% (40% renders the glow half as wide).
   No `circle` keyword. Transition 300ms cubic-bezier(0.4,0,0.2,1).
   Her classes: pointer-events-none fixed inset-0 z-30 transition duration-300 lg:absolute */
.spotlight {
  position: fixed; inset: 0;
  pointer-events: none;
  z-index: 30;
  background: radial-gradient(
    600px at var(--mx, 50%) var(--my, 50%),
    rgba(29, 78, 216, 0.15),
    rgba(0, 0, 0, 0) 80%
  );
  transition: background 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
@media (hover: none) { .spotlight { display: none; } }
```

```js
document.body.addEventListener('mousemove', (e) => {
  document.body.style.setProperty('--mx', e.clientX + 'px');
  document.body.style.setProperty('--my', e.clientY + 'px');
}, { passive: true });
```

**No custom cursor** — default browser cursor.

---

## Time Machine popup

**REBUILT 2026-07-29 to match her EXACT live implementation (extracted from her DOM + computed CSS):**

**Trigger (her TARDIS pattern, ours = astrolabe):**
- Position: `absolute bottom-0 right-0` INSIDE the page container (NOT fixed top-right) — appears at the very bottom of the page content
- Button: `inline-flex items-center px-2 py-4 font-medium text-slate-400 hover:-translate-y-2 hover:text-teal-300` + sr-only "Click to time travel"
- Astrolabe 72px, rings rotating 60s/40s-rev/20s, hover speeds to 8s/5s/3s

**Dialog (full-screen, not a card modal):**
- Overlay: `.portal fixed inset-0 z-40 bg-slate-900/10 backdrop-blur` + `background: radial-gradient(circle at 50% 35%, rgb(51,68,85), rgba(0,0,0,0.7))`
- **Portal orb ("A Portal to Tomorrow" by @jasesmith, codepen.io/jasesmith/pen/qqgvZe — credit link required bottom):** 5 divs in `.portal-inner`, each: absolute center, `font-size: 20vmin; width/height: 3.5em; border-radius: 90% 95% 85% 105%; background: rgb(0,255,0); mix-blend-mode: screen; box-shadow: #000 0 0 .5em .2em inset, #fff 0 0 .15em 0; animation: wobble calc(.15s * var(--t)) linear infinite`
- Per-ring vars: (--x/-53% --y/-53% --t:37) (-47/-52/58) (-45/-50/46) (-53/-45/72) (-55/-45/62)
- `@keyframes wobble { 100% { filter: hue-rotate(1turn); transform: translate(var(--x),var(--y)) rotate(1turn); } }`
- Content: `fixed left-1/2 top-1/2 z-40 flex h-full w-full -translate-x-1/2 -translate-y-1/2 justify-center sm:items-center` + close X `absolute right-0 top-0 p-4`
- Grid wrapper: `<div style="perspective:400px"><div class="star-wars-skew">` where `.star-wars-skew { transform: rotateX(25deg) translateZ(100px); }` (verified: matrix3d matches hers digit-for-digit)
- Title: `mx-auto mb-12 max-w-xs text-center text-2xl font-semibold leading-tight tracking-tight text-slate-700 sm:text-3xl lg:max-w-md lg:text-4xl` — "Looking for a different site? Go back in time..."
- Tiles: `ul.inline-grid.grid-cols-1.gap-2.md:grid-cols-2` > a.group with screenshot img (`rounded border-2 border-zinc-900/30 drop-shadow-md group-hover:drop-shadow-xl`, 180px wide) + hover overlay (`bg-zinc-900/30 backdrop-blur-sm border-4 border-teal-400/0 opacity-0 group-hover:opacity-100 lg:flex` with white version label)
- Credit link: `absolute inset-x-0 bottom-0 z-40 block p-8 text-center text-xs text-slate-500 underline hover:text-slate-200 sm:left-auto md:p-4`

**OLD SPEC BELOW (superseded — kept for history):**
**Trigger:** rotating astrolabe icon top-right (40px desktop, 32px mobile)

**Modal:**
- Max width: 800px
- Max height: 600px
- Centered via flexbox
- NOT full-screen

**Backdrop:**
```css
.tm-backdrop {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.9); /* slate-900 @ 90% */
  backdrop-filter: blur(20px);
  z-index: 40;
  display: flex; align-items: center; justify-content: center;
  animation: fade-in 300ms ease;
}
```

**Orb effect** (huge radial gradient centered in modal):
```css
.tm-orb {
  position: absolute; inset: 0;
  background: radial-gradient(
    ellipse 60% 60% at center,
    rgba(196, 181, 253, 0.4) 0%,      /* violet-300 soft glow */
    rgba(216, 180, 254, 0.3) 20%,     /* purple-300 */
    rgba(233, 213, 255, 0.2) 40%,     /* purple-200 */
    transparent 70%
  );
  filter: blur(40px);
  pointer-events: none;
}
```

**Content grid inside orb:**
- Title: "Looking for a different site? Go back in time..." (italic, editorial)
- 2×2 grid of version thumbnails
- On Day 1: only v1 tile is real, others say "Coming soon"

**Close mechanisms:**
- X button top-right (Lucide `x` icon)
- Click backdrop
- Esc key

---

## Astrolabe icon

**File:** `shared-assets/astrolabe.svg` (already saved)
- 3 concentric rings rotating at 60s / 40s reverse / 20s
- Rub el Hizb 8-point Islamic star center
- On hover: rings speed to 8s / 5s / 3s
- Placement: `top: 24px; right: 24px; position: fixed; z-index: 50`
- Size: 40px desktop, 32px mobile
- Cursor: pointer

---

## Mobile (below 1024px)

**Breakpoints (from her v4 variables):**
- Mobile S: 330px
- Mobile M: 400px
- Mobile L: 480px
- Phablet: 600px
- Tablet: 768px
- Desktop: 1024px

**Below 1024px:**
- Sidebar unstacks: hero flows above content
- No sticky nav (or becomes a hamburger overlay per v4 pattern)
- Section spacing: 48px (down from 64px)
- Container padding: 24px (from 48px)
- Astrolabe: 32px, still top-right

**Below 768px:**
- Time Machine modal: 90vw wide, scrollable body
- Cursor spotlight: disabled (touch device)
- Font sizes: fluid `clamp()`
  - H1: `clamp(28px, 5vw, 36px)`
  - H2: `clamp(16px, 3vw, 18px)`
  - P: 16px fixed

**Below 480px:**
- Container padding: 16px
- Astrolabe: 28px
- Social icons row: 10px each

---

## Animation timings (subtle, earned)

- Section fade+lift on scroll enter: **800ms, `ease-out`, 8px translateY**
- Word-by-word hero reveal: **100ms stagger, 400ms per word**
- Link color transition: **300ms `ease-in-out`**
- Underline grow: **300ms `ease-in-out`** from `scaleX(0)` to `scaleX(1)`
- Nav dash grow: **200ms `ease`** from 32px to 64px
- Modal fade in: **300ms `ease`**
- Astrolabe hover speedup: **transition to hover animation-duration in 200ms**

**Reduced motion:** all animations become instant OR opacity-only per `@media (prefers-reduced-motion: reduce)`.

---

## Sitemap

- `/` — home (hero + about + experience + selected work + get in touch)
- `/archive` — table of all 16 apps + client work (Year · Project · Made at · Built with · Link)
- Time Machine modal (opened from astrolabe, no route)

---

## Social icons (footer, 5 icons, 12px each)

Order: GitHub · LinkedIn · X · Instagram · App Store

Icon library: **Lucide** (`@lucide/astro`).
- GitHub: `<Github />`
- LinkedIn: `<Linkedin />`
- X: `<Twitter />` (Lucide still calls it Twitter)
- Instagram: `<Instagram />`
- App Store: `<AppStore />` (or custom SVG since Lucide may not have it — I'll draw a simple Apple silhouette or "A↗" text link)

All colored slate-400, hover slate-200, 300ms transition.

---

## Footer (bottom-left below social row)

```
Design inspiration: brittanychiang.com
Built with Astro and Tailwind, deployed on Cloudflare Pages.
Loosely designed in Figma. Text set in Inter.
View source on GitHub ↗
```

Font: 12px, slate-500, line-height 20px.

---

## Verification checklist for build

When we scaffold, cross-check each of these against her live main:

- [ ] Background `#0f172a` exact
- [ ] Body text `#94a3b8` exact
- [ ] H1 36px / 40lh / 700 / -0.9px letter-spacing
- [ ] H2 18px / 28lh / 500 / -0.45px letter-spacing
- [ ] P margin-top 16px between
- [ ] Section margin-bottom 64px
- [ ] Font is Inter (Fontsource variable)
- [ ] Nav dash 32→64px on hover/active
- [ ] Nav dash accent teal `#5eead4` on active
- [ ] Link underline grows left-to-right 300ms
- [ ] Cursor spotlight 600px circle, blue-700 @ 15% opacity
- [ ] Selection bg teal-300, text teal-900
- [ ] No custom cursor (default browser)
- [ ] Astrolabe top-right 24px offset, 40px size, always rotating
- [ ] Time Machine popup 800px max width, blur backdrop, teal-tinted orb glow
- [ ] Mobile breakpoint at 1024px stacks sidebar
- [ ] Cursor spotlight disabled on touch

---

## Source of truth

This document + `shared-assets/astrolabe.svg` = complete design spec.
Update this file when we discover any deviation from her main during build.
