#!/usr/bin/env bash
# Copies the Pixabay sound effects this film uses from the HyperFrames media-use skill
# (installed by `npx hyperframes init` or `npx hyperframes skills update media-use`).
# The files are not committed: the Pixabay Content License does not allow redistributing
# unaltered files on a standalone basis.
set -euo pipefail
cd "$(dirname "$0")/.."

FILES=(chime click-soft ping pop sparkle whoosh whoosh-short)
DEST=assets/audio/sfx
mkdir -p "$DEST"

have_all() {
  for f in "${FILES[@]}"; do [ -f "$1/$f.mp3" ] || return 1; done
}

if have_all "$DEST"; then
  exit 0
fi

SRC=""
for c in \
  "$HOME/.agents/skills/media-use/audio/assets/sfx" \
  "$HOME/.claude/skills/media-use/audio/assets/sfx" \
  "$(npm root -g 2>/dev/null)/hyperframes/dist/skills/media-use/audio/assets/sfx"; do
  if have_all "$c"; then SRC="$c"; break; fi
done

if [ -z "$SRC" ]; then
  # Fallback: the published package of the pinned CLI version ships the same files.
  TMP="$(mktemp -d)"
  (cd "$TMP" && npm pack --silent hyperframes@0.8.111 >/dev/null && tar xzf hyperframes-*.tgz)
  SRC="$TMP/package/dist/skills/media-use/audio/assets/sfx"
fi

for f in "${FILES[@]}"; do cp "$SRC/$f.mp3" "$DEST/$f.mp3"; done
echo "SFX kopiert aus $SRC"
