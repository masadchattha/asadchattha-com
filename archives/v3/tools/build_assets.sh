#!/usr/bin/env bash
#
# build_assets.sh — regenerate every generated asset in archives/v3/img/.
#
# The emoji are the ONLY thing copied out of docs/reference-bc-v3/ (Asad's call,
# see README). Everything else here comes
# from a licensed package, is drawn inline below, or is composed from Asad's own
# transparent device mocks by build_devices.py.
#
#   img/emojis/*.png   the original's OWN Apple emoji PNGs, copied verbatim from
#                      docs/reference-bc-v3/img/emojis/. Asad's call: they are
#                      already published on the live v3 site, and Twemoji made
#                      the intro read as somebody else's page. This is the one
#                      place art is taken from the reference.
#   img/social/*.svg   simple-icons (CC0) + devicon (MIT, LinkedIn only, since
#                      simple-icons dropped the LinkedIn mark on trademark
#                      request). email.svg is a plain geometric envelope drawn
#                      inline below — no brand involved.
#   img/switch/*.svg   sun + moon glyphs, drawn inline below. Two colourways so
#                      the toggle rail stays legible on both grounds.
#   img/arrow.svg      the arrow-link chevron, drawn inline below. Used through
#                      a CSS mask painted --blue, which is what the original's
#                      arrow.png actually is (#007fff) in both themes.
#   img/featured/*    delegated to build_devices.py — three TRANSPARENT devices
#                      per featured project, no baked background. Do NOT copy
#                      v1's card-*.png here; wrong shape, wrong ground.
#   img/og.png         also from build_devices.py — the one opaque raster, for
#                      link unfurlers.
#
# Requires node + npm on PATH. Run from anywhere:
#   bash archives/v3/tools/build_assets.sh
set -euo pipefail

V3="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

mkdir -p "$V3"/img/{emojis,social,switch,featured}

echo "==> installing icon packages into $WORK"
cd "$WORK"
npm install --silent --ignore-scripts @twemoji/svg simple-icons devicon

# ---------------------------------------------------------------- emoji ------
# Emoji-as-punctuation is the voice of this design, so each one is named for the
# role it plays in the copy rather than for its codepoint.
echo "==> emoji (the original's Apple PNGs)"
REF="$(cd "$V3/../.." && pwd)/docs/reference-bc-v3/img/emojis"
cp "$REF/wave.png"         "$V3/img/emojis/wave.png"          # greeting
cp "$REF/technologist.png" "$V3/img/emojis/technologist.png"  # ends the tagline
cp "$REF/pointright.png"   "$V3/img/emojis/pointright.png"    # points at the email
cp "$REF/rockon.png"       "$V3/img/emojis/rockon.png"        # footer byline
cp "$REF/pointing-up.png"  "$V3/img/emojis/pointing-up.png"   # back-to-top button
cp node_modules/@twemoji/svg/1f4f1.svg              "$V3/img/favicon.svg"              # tab icon

# --------------------------------------------------------------- social ------
echo "==> social marks (simple-icons + devicon)"
node -e '
const si = require("simple-icons");
const fs = require("fs");
const OUT = process.argv[1] + "/img/social/";
// Footer marks only show below 850px, where the text labels are hidden. They are
// painted in the accent blue to match the labels they replace.
const BLUE = "#007bff";
const want = { linkedin: null, github: "Github", x: "X", instagram: "Instagram",
               facebook: "Facebook", whatsapp: "Whatsapp", calendly: "Calendly" };
for (const [name, key] of Object.entries(want)) {
  if (!key) continue;                       // linkedin handled by devicon below
  const ic = si["si" + key];
  if (!ic) throw new Error("simple-icons lost: " + key);
  fs.writeFileSync(OUT + name + ".svg",
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><title>${ic.title}</title><path fill="${BLUE}" d="${ic.path}"/></svg>\n`);
}
' "$V3"

# simple-icons removed the LinkedIn mark (trademark request), so it comes from
# devicon instead, recoloured to the same accent blue. Use the -plain variant:
# it is ONE path whose counters cut out the "in", so a flat recolour still reads.
# The -original variant is two stacked paths and goes solid when recoloured.
node -e '
const fs = require("fs");
const src = fs.readFileSync("node_modules/devicon/icons/linkedin/linkedin-plain.svg", "utf8");
fs.writeFileSync(process.argv[1] + "/img/social/linkedin.svg",
  src.replace("<path", `<title>LinkedIn</title><path fill="#007bff"`) + "\n");
' "$V3"

# Email is a generic envelope, not a brand, so it is drawn rather than fetched.
cat > "$V3/img/social/email.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><title>Email</title><path fill="#007bff" d="M2 4h20a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1Zm19 3.4-8.4 6a1 1 0 0 1-1.2 0L3 7.4V18h18V7.4ZM20 6H4l8 5.7L20 6Z"/></svg>
SVG

# --------------------------------------------------------------- switch ------
# The rail flanks. Dark pair for the light ground, white pair for `body.night`.
echo "==> theme-switch glyphs"
write_switch () { # $1=file  $2=fill
  cat > "$V3/img/switch/$1" <<SVG
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">$2</svg>
SVG
}
SUN_BODY_TMPL='<g fill="%s"><circle cx="12" cy="12" r="5"/><g stroke="%s" stroke-width="2" stroke-linecap="round"><path d="M12 1v3M12 20v3M1 12h3M20 12h3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M19.8 4.2l-2.1 2.1M6.3 17.7l-2.1 2.1"/></g></g>'
MOON_BODY_TMPL='<path fill="%s" d="M21 14.2A9 9 0 1 1 9.8 3 7.2 7.2 0 0 0 21 14.2Z"/>'
# shellcheck disable=SC2059
write_switch sun.svg        "$(printf "$SUN_BODY_TMPL"  '#444452' '#444452')"
# shellcheck disable=SC2059
write_switch sun-white.svg  "$(printf "$SUN_BODY_TMPL"  '#e7e7e7' '#e7e7e7')"
# shellcheck disable=SC2059
write_switch moon.svg       "$(printf "$MOON_BODY_TMPL" '#444452')"
# shellcheck disable=SC2059
write_switch moon-white.svg "$(printf "$MOON_BODY_TMPL" '#e7e7e7')"

# ---------------------------------------------------------------- arrow ------
# Consumed as a CSS mask, so the fill here is irrelevant — currentColor wins.
echo "==> arrow"
cat > "$V3/img/arrow.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="#000" d="M13.1 4.3 20.8 12l-7.7 7.7-1.4-1.4 5.3-5.3H3.2v-2h13.8l-5.3-5.3 1.4-1.4Z"/></svg>
SVG

# ------------------------------------------------------------- featured ------
# Device art is NOT built here and is NOT copied from v1. v1's cards are one
# 1280x800 composite per project on a dark navy gradient; v3 needs three separate
# transparent devices per project so the CSS `.phones` row can tuck them, and v3
# is light by default so a baked navy ground would be wrong. See build_devices.py.
echo "==> featured device art"
python3 "$V3/tools/build_devices.py"

echo "done."
