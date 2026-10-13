#!/usr/bin/env bash
# Rendert die drei Standort-Animationen als transparente PNG-Sequenzen und baut daraus
#   renders/knigge-standort-<ort>.gif   GIF, 1-Bit-Transparenz (überall einsetzbar)
#   renders/knigge-standort-<ort>.webp  animiertes WebP mit weicher Transparenz (Websites)
set -euo pipefail
cd "$(dirname "$0")/.."

HF="npx --yes hyperframes@0.8.152"
FPS=25

export_one() {
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
  # WebP: weiche Alphakanten
  ffmpeg -v error -y -framerate "$FPS" -i "$frames/frame_%06d.png" \
    -c:v libwebp_anim -lossless 1 -compression_level 6 -loop 0 "renders/knigge-standort-$name.webp"
  rm -rf "$frames"
  ls -la "renders/knigge-standort-$name.gif" "renders/knigge-standort-$name.webp"
}

export_one bergisch-gladbach index.html
export_one koeln formats/koeln.html
export_one wipperfuerth formats/wipperfuerth.html
