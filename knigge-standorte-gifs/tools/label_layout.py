"""Platziert die Ortsnamen der Karten so, dass jeder Name mit Abstand in seine Fläche passt.

Die Namen werden in der echten Schrift gemessen (Montserrat, variable Schrift aus dem Font-Cache, den
HyperFrames beim Rendern anlegt: ~/.cache/hyperframes/fonts/montserrat). Ein Name passt, wenn sein
Schriftbild mit CLEAR px Abstand innerhalb seiner Fläche liegt und weder Marker, Rhein, Logo,
Quellenhinweis, Bildrand noch einen anderen Namen berührt. Passt die Wunschposition nicht, wird in der
Fläche die nächstgelegene Position gesucht, die passt – notfalls in kleinerer Schrift.
"""
import glob
import math
import os

import shapely
from shapely.geometry import box

FONT_GLOB = os.path.expanduser("~/.cache/hyperframes/fonts/montserrat/*-normal-*.woff2")
ASC, DESC = 0.968, 0.251  # Montserrat (hhea), bestimmt die Grundlinie im Zeilenkasten
LINE_HEIGHT = 1.15
CLEAR = 4  # px Mindestabstand
STEP = 3  # px Suchraster
MIN_SIZE = 16  # px kleinste Schrift, bevor ein Name als „passt nicht“ gilt


class Measure:
    """Misst das Schriftbild eines Namens relativ zur Mitte seines Zeilenkastens."""

    def __init__(self):
        from fontTools.ttLib import TTFont
        from PIL import ImageFont

        self._font = ImageFont
        self.files = sorted(glob.glob(FONT_GLOB))
        if not self.files:
            raise FileNotFoundError("Montserrat nicht im HyperFrames-Font-Cache – erst einmal rendern")
        # HyperFrames legt Teilmengen der Schrift ab; je Text eine Datei wählen, die alle Zeichen enthält
        self.cmaps = {f: set(TTFont(f).getBestCmap()) for f in self.files}
        self.cache = {}

    def ink(self, text, size, weight):
        key = (text, size, weight)
        if key not in self.cache:
            f = next((f for f in self.files if all(ord(c) in self.cmaps[f] for c in text)), None)
            if f is None:
                raise LookupError("Zeichen fehlen im Font-Cache: %s" % text)
            ft = self._font.truetype(f, size, layout_engine=self._font.Layout.RAQM)
            ft.set_variation_by_axes([weight])
            adv = ft.getlength(text)
            x0, y0, x1, y1 = ft.getbbox(text, anchor="ls")
            base = size * ((ASC - DESC) / 2 - 0.06)  # Grundlinie unter der Kastenmitte (an Chromium abgeglichen)
            self.cache[key] = (-adv / 2 + x0, base + y0, -adv / 2 + x1, base + y1)
        return self.cache[key]


def _fits(x, y, ink, area, canvas, tree, blockers):
    b = box(x + ink[0] - CLEAR, y + ink[1] - CLEAR, x + ink[2] + CLEAR, y + ink[3] + CLEAR)
    if not canvas.contains(b) or (area is not None and not area.contains(b)):
        return None
    if tree is not None and len(tree.query(b, predicate="intersects")):
        return None
    if any(o.intersects(b) for o in blockers):
        return None
    inner = box(x + ink[0], y + ink[1], x + ink[2], y + ink[3])
    return area.boundary.distance(inner) if area is not None else CLEAR


def place(items, obstacles, W, H, measure, min_size=MIN_SIZE):
    """items: dicts mit text, size, weight, area (Polygon in px oder None), want (x, y),
    office (Marker-Mitte für Standort-Namen oder None). Ergebnis je Eintrag: x, y, size, status, clear.
    min_size: kleinste erlaubte Schrift, bevor ein Name als „passt nicht“ gilt."""
    canvas = box(0, 0, W, H)
    tree = shapely.STRtree(obstacles) if obstacles else None
    placed = []  # Schriftbilder bereits gesetzter Namen
    results = [None] * len(items)
    # Standort-Namen zuerst (feste Nähe zum Marker), dann kleine Flächen vor großen
    order = sorted(range(len(items)), key=lambda i: (items[i]["office"] is None,
                                                     items[i]["area"].area if items[i]["area"] is not None else 0))
    for i in order:
        it = items[i]
        area = it["area"]
        if area is not None:
            shapely.prepare(area)
        wx, wy = it["want"]
        best = None
        for size in range(it["size"], min_size - 1, -1):
            ink = measure.ink(it["text"], size, it["weight"])
            c = _fits(wx, wy, ink, area, canvas, tree, placed)
            if c is not None:
                best = (wx, wy, size, "ok" if size == it["size"] else "kleiner", c)
                break
            cands = []
            if it["office"] is not None:
                ox, oy = it["office"]
                for dy in list(range(34, 72, 2)) + list(range(-34, -72, -2)):
                    for dx in range(-150, 151, STEP):
                        cands.append((ox + dx, oy + dy, abs(dx) + abs(dy - 38) + (40 if dy < 0 else 0)))
            else:
                minx, miny, maxx, maxy = area.bounds
                gx = minx
                while gx <= maxx:
                    gy = miny
                    while gy <= maxy:
                        cands.append((gx, gy, math.hypot(gx - wx, gy - wy)))
                        gy += STEP
                    gx += STEP
            for x, y, cost in sorted(cands, key=lambda t: t[2]):
                if best is not None and cost - 2.5 * 12 > best[5]:
                    break  # weiter weg als die beste Lösung je ausgleichen kann
                c = _fits(x, y, ink, area, canvas, tree, placed)
                if c is None:
                    continue
                score = cost - 2.5 * min(c, 12)
                if best is None or score < best[5]:
                    best = (x, y, size, "verschoben" if size == it["size"] else "kleiner", c, score)
            if best is not None:
                break
        if best is None and it["office"] is not None:
            # Standort-Name passt nicht in seine (kleine) Fläche: neben dem Marker frei stellen, ohne etwas zu berühren
            ink = measure.ink(it["text"], it["size"], it["weight"])
            ox, oy = it["office"]
            for dy in list(range(34, 72, 2)) + list(range(-34, -72, -2)):
                for dx in sorted(range(-150, 151, STEP), key=abs):
                    if _fits(ox + dx, oy + dy, ink, None, canvas, tree, placed) is not None:
                        cost = abs(dx) + abs(dy - 38) + (40 if dy < 0 else 0)
                        if best is None or cost < best[5]:
                            best = (ox + dx, oy + dy, it["size"], "ragt über die Fläche", 0.0, cost)
                        break
        if best is None:
            best = (wx, wy, it["size"], "passt nicht", 0.0)
        x, y, size, status, c = best[:5]
        ink = measure.ink(it["text"], size, it["weight"])
        placed.append(box(x + ink[0], y + ink[1], x + ink[2], y + ink[3]))
        results[i] = {"x": x, "y": y, "size": size, "status": status, "clear": c}
    return results
