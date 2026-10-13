#!/usr/bin/env bash
# Rendert die Standort-Animationen als transparente PNG-Sequenzen und baut daraus
#   renders/knigge-standort-<ort>.gif   GIF, 1-Bit-Transparenz (überall einsetzbar)
#   renders/knigge-standort-<ort>.webp  animiertes WebP mit weicher Transparenz (Websites)
# Benötigt: ffmpeg mit libwebp; optional gifsicle (verkleinert die GIFs verlustfrei)
set -euo pipefail
cd "$(dirname "$0")/.."

HF="npx --yes hyperframes@0.8.152"
FPS=25

_export_one() {
  local name="$1" entry="$2"
  local frames="renders/frames-$name"
  rm -rf "$frames"
  if [ "$entry" = "index.html" ]; then
    $HF render --format png-sequence --fps "$FPS" -o "$frames"
  else
    $HF render --format png-sequence --fps "$FPS" -c "$entry" -o "$frames"
  fi
  # GIF: eigene Palette, keine Dither-Muster, Kanten ab 50 % Deckkraft sichtbar
  ffmpeg -v error -y -framerate "$FPS" -i "$frames/frame_%06d.png" \
    -filter_complex "[0:v]split[a][b];[a]palettegen=reserve_transparent=1:stats_mode=full[p];[b][p]paletteuse=dither=none:alpha_threshold=128" \
    -loop 0 "renders/knigge-standort-$name.gif"
  # verlustfrei verkleinern: gleiche Bilder zusammenfassen, nur geänderte Bereiche speichern
  if command -v gifsicle > /dev/null; then
    gifsicle -O3 --no-warnings -b "renders/knigge-standort-$name.gif"
  fi
  # WebP: weiche Alphakanten
  ffmpeg -v error -y -framerate "$FPS" -i "$frames/frame_%06d.png" \
    -c:v libwebp_anim -lossless 1 -compression_level 6 -loop 0 "renders/knigge-standort-$name.webp"
  rm -rf "$frames"
  ls -la "renders/knigge-standort-$name.gif" "renders/knigge-standort-$name.webp"
}

ONLY="${1:-}"  # optional: nur einen Namen exportieren, z. B. `bash tools/export.sh karte-koeln`
export_one() {
  [ -n "$ONLY" ] && [ "$ONLY" != "$1" ] && return 0
  _export_one "$@"
}

export_one bergisch-gladbach index.html
export_one koeln formats/koeln.html
export_one wipperfuerth formats/wipperfuerth.html
export_one rheinisch-bergischer-kreis formats/rheinisch-bergischer-kreis.html
export_one einzugsgebiet formats/einzugsgebiet.html
# Karten im Stil der Gebietskarte
export_one karte-bergisch-gladbach formats/karte-bergisch-gladbach.html
export_one karte-koeln formats/karte-koeln.html
export_one karte-wipperfuerth formats/karte-wipperfuerth.html
export_one karte-rheinisch-bergischer-kreis formats/karte-rheinisch-bergischer-kreis.html
export_one karte-einzugsgebiet formats/karte-einzugsgebiet.html
