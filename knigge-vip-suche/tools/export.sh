#!/usr/bin/env bash
# Leitet aus den 4K-Render-Mastern (renders/master/, siehe npm run render:*) die Auslieferungsdateien ab.
# Baut nur, was fehlt oder älter als sein Master ist.
#
#   renders/knigge-vip-suche-9x16-4k.mp4    2160x3840  YouTube Shorts · TV mit Hochkant-Wiedergabe
#   renders/knigge-vip-suche-9x16.mp4       1080x1920  Instagram Reels/Stories, Facebook
#   renders/knigge-vip-suche-tv-4k-*.mp4    3840x2160  TV hochkant montiert, ohne Drehfunktion
#                                                      (Inhalt 90° gedreht; steht das Bild auf dem
#                                                      Kopf, die andere Datei nehmen)
#   renders/knigge-vip-suche-16x9-4k.mp4    3840x2160  YouTube · TV quer
#   renders/knigge-vip-suche-16x9.mp4       1920x1080  Website, Präsentationen, Social quer
set -euo pipefail
cd "$(dirname "$0")/.."

N=knigge-vip-suche
mkdir -p renders/master
# Renders, die noch direkt in renders/ liegen, als Master übernehmen
for f in "$N-9x16-4k" "$N-16x9-4k"; do
  if [ -s "renders/$f.mp4" ] && [ ! -s "renders/master/$f.mp4" ]; then
    mv "renders/$f.mp4" "renders/master/$f.mp4"
  fi
done

H264=(-c:v libx264 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a copy)

# build <master> <ziel> <ffmpeg-optionen...>
build() {
  local src="renders/master/$1.mp4" dst="renders/$2.mp4"
  shift 2
  [ -s "$src" ] || return 0
  if [ -s "$dst" ] && [ "$dst" -nt "$src" ]; then
    echo "aktuell: $dst"
    return 0
  fi
  echo "erzeuge: $dst"
  ffmpeg -v error -y -i "$src" "$@" "${H264[@]}" "$dst.tmp.mp4"
  mv "$dst.tmp.mp4" "$dst"
}

# Hochkant
build "$N-9x16-4k" "$N-9x16-4k" -preset slow -crf 18 -level 5.1
build "$N-9x16-4k" "$N-9x16" -vf "scale=1080:1920:flags=lanczos" -preset slow -crf 17 -level 4.2
build "$N-9x16-4k" "$N-tv-4k-gedreht-im-uhrzeigersinn" -vf "transpose=1" -preset medium -crf 19 -level 5.1
build "$N-9x16-4k" "$N-tv-4k-gedreht-gegen-uhrzeigersinn" -vf "transpose=2" -preset medium -crf 19 -level 5.1

# Quer
build "$N-16x9-4k" "$N-16x9-4k" -preset slow -crf 18 -level 5.1
build "$N-16x9-4k" "$N-16x9" -vf "scale=1920:1080:flags=lanczos" -preset slow -crf 17 -level 4.2

ls -la renders/*.mp4
