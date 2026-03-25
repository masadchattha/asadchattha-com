# asadchattha.com — Portfolio

Solo iOS engineer + Muslim founder portfolio.

## Version strategy

- **`main/`** — the current active portfolio (v1 on launch). Deploys to `asadchattha.com`.
- **`archives/`** — frozen snapshots of past versions. Deploys to `v1.asadchattha.com`, `v2.asadchattha.com`, etc.
- **`shared-assets/`** — cross-version assets (astrolabe SVG, favicons, brand tokens).
- **`docs/`** — decisions, changelog, design notes.

## Tech stack (main)

- **Framework:** Astro (islands architecture, ships zero JS by default)
- **Styling:** Tailwind CSS
- **Animation:** GSAP 3 + ScrollTrigger + Lenis
- **Font:** Inter (self-hosted via Fontsource) + JetBrains Mono for numbers/code
- **Hosting:** Cloudflare Pages (unlimited bandwidth, free, commercial-safe)
- **Repo:** GitHub (public — portfolio-as-code = credibility signal)
- **Domain:** asadchattha.com (via Cloudflare Registrar, purchase later after local finalization)

## Time Machine feature

Bottom-right astrolabe (see `shared-assets/astrolabe.svg`) opens a glowing-orb modal listing archived versions. On Day 1 shows just v1 in the grid. Future versions unlock slots as they ship.

## Deploy flow

1. Local dev: `cd main && npm run dev`
2. Push to GitHub main branch → Cloudflare Pages auto-deploys
3. When starting v2: `cp -R main archives/v1` (freeze v1), then evolve `main/` into the new design

## Design credit

Inspired by [brittanychiang.com](https://brittanychiang.com) (Next.js + Tailwind) and its v4 archive.

## Local paths

- Root: `/Users/masadchattha/Documents/Development/Websites/asadchattha-com/`
- Registered in `~/.claude/CLAUDE.md` under Portfolio Project section.
