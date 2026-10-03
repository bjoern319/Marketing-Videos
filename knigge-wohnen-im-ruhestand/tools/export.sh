#!/usr/bin/env bash
# Leitet aus den 4K-Mastern (npm run render:9x16-4k / render:16x9-4k) die Plattform-Dateien ab.
#
#   renders/knigge-wohnen-im-ruhestand-16x9-4k.mp4   3840x2160  Master quer: YouTube, Fernseher quer
#   renders/knigge-wohnen-im-ruhestand-16x9.mp4      1920x1080  Website, Präsentationen, Social quer
#   renders/knigge-wohnen-im-ruhestand-9x16-4k.mp4   2160x3840  Master hochkant: YouTube Shorts, TV mit Hochkant-Modus
#   renders/knigge-wohnen-im-ruhestand-9x16.mp4      1080x1920  Instagram Reels/Stories, Facebook
#   renders/knigge-wohnen-im-ruhestand-tv-4k-*.mp4   3840x2160  TV hochkant montiert, ohne Drehfunktion
#                                                               (Bildinhalt um 90° gedreht; steht das Bild
#                                                               auf dem Kopf, die andere Datei nehmen)
set -euo pipefail
cd "$(dirname "$0")/.."

MASTER=renders/knigge-wohnen-im-ruhestand-9x16-4k.mp4
[ -s "$MASTER" ] || { echo "Master fehlt: $MASTER (zuerst npm run render:9x16-4k)"; exit 1; }

H264=(-c:v libx264 -preset slow -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a copy)

# Instagram: 1080x1920, aus 4K heruntergerechnet (Supersampling = besonders saubere Kanten)
ffmpeg -v error -y -i "$MASTER" -vf "scale=1080:1920:flags=lanczos" -crf 17 -level 4.2 "${H264[@]}" \
  renders/knigge-wohnen-im-ruhestand-9x16.mp4

# Fernseher hochkant ohne Drehfunktion: Querformat-Datei mit gedrehtem Inhalt
ffmpeg -v error -y -i "$MASTER" -vf "transpose=1" -crf 19 -level 5.1 "${H264[@]}" \
  renders/knigge-wohnen-im-ruhestand-tv-4k-gedreht-im-uhrzeigersinn.mp4
ffmpeg -v error -y -i "$MASTER" -vf "transpose=2" -crf 19 -level 5.1 "${H264[@]}" \
  renders/knigge-wohnen-im-ruhestand-tv-4k-gedreht-gegen-uhrzeigersinn.mp4

# Querformat: 1920x1080 aus dem 4K-Master
LANDSCAPE=renders/knigge-wohnen-im-ruhestand-16x9-4k.mp4
if [ -s "$LANDSCAPE" ]; then
  ffmpeg -v error -y -i "$LANDSCAPE" -vf "scale=1920:1080:flags=lanczos" -crf 17 -level 4.2 "${H264[@]}" \
    renders/knigge-wohnen-im-ruhestand-16x9.mp4
fi

ls -la renders/*.mp4
