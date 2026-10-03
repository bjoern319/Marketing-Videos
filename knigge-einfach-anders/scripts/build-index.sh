#!/usr/bin/env bash
# Baut index.html aus STORYBOARD.md + Frames + audio_meta.json neu
# (Assembler und Übergänge aus dem HyperFrames-Skill "product-launch-video").
set -euo pipefail
cd "$(dirname "$0")/.."

SK="${HYPERFRAMES_SKILLS_DIR:-$HOME/.claude/skills}/product-launch-video/scripts"

node "$SK/assemble-index.mjs" --storyboard ./STORYBOARD.md --hyperframes . --audio-meta ./audio_meta.json
node "$SK/transitions.mjs" inject --storyboard ./STORYBOARD.md --hyperframes .
node "$SK/transitions.mjs" verify --storyboard ./STORYBOARD.md --index ./index.html

# GSAP lokal statt CDN (Render funktioniert auch ohne Netzwerk), Sprache Deutsch.
node -e '
const fs = require("fs");
let s = fs.readFileSync("index.html", "utf8");
s = s.replace(/<script src="https:\/\/cdn\.jsdelivr\.net\/npm\/gsap@[^"]+"[^>]*><\/script>/, "<script src=\"assets/vendor/gsap.min.js\"></script>");
s = s.replace("<html lang=\"en\">", "<html lang=\"de\">");
fs.writeFileSync("index.html", s);
'
echo "index.html neu gebaut."
