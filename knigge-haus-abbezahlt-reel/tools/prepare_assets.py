#!/usr/bin/env python3
"""Bereitet Fotos und Musik für das Reel vor (einmalig; Ergebnis liegt in assets/img und assets/audio).

Fotos: Quelle sind die Screenshots der sechs Karussell-Folien (assets/source/, 1206 px breit, mit
eingebrannter Schrift und Instagram-Oberfläche). Je Foto wird ein Ausschnitt gewählt, der den freien
Bildteil zeigt; was an Schrift in den Ausschnitt ragt, wird übermalt (OpenCV-Inpainting) und liegt
im Film zusätzlich unter dem weißen Lichtschleier. Skalierung mit Lanczos, leichtes Nachschärfen.

Musik: Schnitt aus der KNIGGE-Musik (../knigge-wohnen-im-ruhestand, 80 BPM, 1 Takt = 3 s) auf
Taktgrenzen – 8,25–30 s und 69–75 s, 80 ms Überblendung auf der Taktgrenze bei 21,75 s.

Benötigt: pip install opencv-python-headless pillow numpy; ffmpeg.

    python3 tools/prepare_assets.py
"""
import os
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "source")
IMG = os.path.join(ROOT, "assets", "img")
AUDIO = os.path.join(ROOT, "assets", "audio")
THEME = os.path.normpath(os.path.join(ROOT, "..", "knigge-wohnen-im-ruhestand", "assets", "audio", "knigge-theme.m4a"))

# Eingebrannte Schrift: je Zeile ein Kasten (x0, y0, x1, y1 im Screenshot). Darin gilt jedes dunkle
# oder rote Pixel als Schrift und wird übermalt.
TEXT_LINES = {
    "folie-1-haus.jpg": [(62, 168, 190, 200),  # roter Strich
                         (62, 248, 500, 338), (62, 352, 700, 448), (58, 468, 692, 568), (58, 578, 535, 672),
                         (58, 684, 695, 782), (62, 822, 620, 882), (62, 884, 615, 942), (62, 944, 245, 998)],
    "folie-6-ende.jpg": [(62, 122, 190, 152),
                         (62, 198, 570, 298), (62, 296, 755, 408), (58, 398, 550, 488),
                         (68, 538, 610, 600), (68, 588, 610, 650), (68, 640, 610, 700), (68, 690, 610, 750),
                         (68, 740, 610, 800), (68, 790, 610, 850)],
}
# Bereiche, in denen Schrift auf hellem Grund über die Abweichung vom Median-Hintergrund gefunden wird
TEXT_REGIONS = {
    "folie-5-andrea.jpg": [(500, 200, 705, 725)],
}
# ganze Flächen (der rote Knopf auf Folie 6)
FILL_RECTS = {
    "folie-6-ende.jpg": [(70, 886, 650, 1054)],
}

# Ausschnitt (x0, y0, x1, y1) und Zielgröße in px; die Lage im Bild steht in tools/build_reel.py
PHOTOS = {
    "haus.jpg": ("folie-1-haus.jpg", (306, 0, 1206, 1210), 1.2),
    "haus-rund.jpg": ("folie-1-haus.jpg", (700, 200, 1206, 706), 360 / 506),
    "kosten.jpg": ("folie-2-kosten.jpg", (0, 250, 510, 1200), 1.4),
    "andrea.jpg": ("folie-5-andrea.jpg", (560, 180, 1206, 1490), 1.0),
    "tisch.jpg": ("folie-6-ende.jpg", (400, 100, 1206, 1233), 1.2),
}


def clean(name):
    img = cv2.imread(os.path.join(SRC, name))
    mask = np.zeros(img.shape[:2], np.uint8)
    for x0, y0, x1, y1 in TEXT_LINES.get(name, []):
        b, g, r = [img[y0:y1, x0:x1, c].astype(int) for c in range(3)]
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        ink = (lum < 182) | ((r - g > 38) & (r > 105))
        mask[y0:y1, x0:x1] |= ink.astype(np.uint8) * 255
    for x0, y0, x1, y1 in TEXT_REGIONS.get(name, []):
        roi = img[y0:y1, x0:x1]
        bg = cv2.medianBlur(roi, 51)  # Hintergrund ohne Schriftzüge
        diff = cv2.absdiff(roi, bg).max(axis=2)
        mask[y0:y1, x0:x1] |= (diff > 26).astype(np.uint8) * 255
    for x0, y0, x1, y1 in FILL_RECTS.get(name, []):
        mask[y0:y1, x0:x1] = 255
    if mask.any():
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=3)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def photos():
    os.makedirs(IMG, exist_ok=True)
    cache = {}
    for out, (src, box, scale) in PHOTOS.items():
        if src not in cache:
            cache[src] = clean(src)
        part = cache[src].crop(box)
        size = (round(part.width * scale), round(part.height * scale))
        part = part.resize(size, Image.LANCZOS)
        if scale > 1:
            part = part.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
        part.save(os.path.join(IMG, out), quality=90, optimize=True)
        print(f"{out}: {size[0]}×{size[1]}")


def music():
    os.makedirs(AUDIO, exist_ok=True)
    out = os.path.join(AUDIO, "knigge-theme-reel.m4a")
    graph = ("[0:a]atrim=8.25:30.04,asetpts=PTS-STARTPTS,afade=t=in:d=0.2[a];"
             "[0:a]atrim=68.96:75,asetpts=PTS-STARTPTS[b];"
             "[a][b]acrossfade=d=0.08:c1=tri:c2=tri[m]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", THEME, "-filter_complex", graph, "-map", "[m]",
                    "-c:a", "aac", "-b:a", "192k", out], check=True)
    print("knigge-theme-reel.m4a")


if __name__ == "__main__":
    photos()
    music()
