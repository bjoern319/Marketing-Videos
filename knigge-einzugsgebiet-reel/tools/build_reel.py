#!/usr/bin/env python3
"""Erzeugt das Instagram-Reel „Drei Facetten“ (Version 2; 1080×1920, 18 s, 30 fps):
index.html und compositions/*.html.

Idee (STORYLINES.md A, SPEC.md „Version 2“): Die KNIGGE-Bildmarke besteht aus drei Facetten. Sie
zerfällt, jede Facette fliegt als Standort-Pin auf die Karte (Köln, Bergisch Gladbach, Wipperfürth),
die Kamera besucht die drei Standorte, ein Zähler zeigt die 19 Städte und Gemeinden, am Ende fliegen
die Facetten zurück und setzen das Logo wieder zusammen.

Grundlage ist die Einzugsgebiet-Karte aus ../knigge-standorte-gifs: Gemeinden, Standorte, Farben und
Logo aus tools/build_maps.py, Flächen aus assets/geo/region.json, Beschriftung über
tools/label_layout.py (jeder Name mindestens 28 px, mit Abstand in seiner Fläche).

Kamera: Transformation der Karte über die CSS-Variablen --cx, --cy (Kartenpunkt in der Bildmitte)
und --z (Zoom); Pins rechnen ihre Bildposition aus denselben Variablen und bleiben gleich groß.
Ortsnamen erscheinen nur, während die Kamera steht.

Ändern: Texte in TEXT, Zeiten in SCENES, dann `python3 tools/build_reel.py` und `npm run check`.
(Version 1 – ruhige Kamerafahrt, 15 s – liegt in der Git-Historie: personal-website 4b93cc2, Marketing-Videos 08783a5.)
"""
import json
import math
import os
import sys

import numpy as np
import shapely
from shapely.geometry import shape, Point, box
from shapely.ops import unary_union, polylabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIFS = os.path.normpath(os.path.join(ROOT, "..", "knigge-standorte-gifs"))
sys.path.insert(0, os.path.join(GIFS, "tools"))
import build_maps  # noqa: E402  Gemeinden, Standorte, Farben, Logo
import label_layout  # noqa: E402

W, H, FPS, DURATION = 1080, 1920, 30, 18.0
AX, AY = 540, 850  # Bildpunkt, auf den die Kamera ihren Kartenpunkt legt
INK, MUTED, RED, TINT = "#444f4f", "#5e6a6a", "#ca2c35", "#f1d0d3"
COLORS = build_maps.COLORS
OFFICES = build_maps.OFFICES
AREAS = build_maps.MAPS["formats/karte-einzugsgebiet.html"]["areas"]  # (Name, Rolle) – wie im GIF
OFFICE_AREA = {"koeln": "Köln", "bgl": "Bergisch Gladbach", "wipperfuerth": "Wipperfürth"}

BAND_TOP, BAND_BOTTOM, RAIL = 168, 1330, box(940, 1000, W, H)  # Instagram-Oberfläche

TEXT = {
    "hook": ["Drei Standorte.", "Eine Region."],
    "region": ["Zwischen Köln", "und Oberberg"],
    "koeln": ("Standort", ["Köln"]),
    "bgl": ("Hauptsitz", ["Bergisch", "Gladbach"]),
    "wipperfuerth": ("Standort", ["Wipperfürth"]),
    "zahl": ("19", "Städte und Gemeinden"),
    "close": ["Ein Ansprechpartner", "für Ihre Immobilie."],
    "url": "knigge-immobilien.de",
}

SCENES = [
    {"id": "s1-hook", "start": 0.0, "dur": 2.4},
    {"id": "s2-region", "start": 2.4, "dur": 1.6},
    # zoom: Faktor über „alles im Rahmen“ hinaus, damit jeder Name in 30 px in seine Fläche passt
    {"id": "s3-koeln", "start": 4.0, "dur": 2.6, "move": 0.75, "zoom": 1.15, "text": "koeln", "office": "koeln",
     "frame": ["Köln", "Leverkusen", "Pulheim", "Frechen", "Hürth"],
     "names": ["Leverkusen", "Pulheim", "Frechen", "Hürth"]},
    {"id": "s4-bergisch-gladbach", "start": 6.6, "dur": 2.6, "move": 0.75, "zoom": 1.2, "text": "bgl", "office": "bgl",
     "frame": ["Bergisch Gladbach", "Burscheid", "Kürten", "Leichlingen", "Odenthal", "Overath", "Rösrath",
               "Wermelskirchen"],
     "names": ["Burscheid", "Kürten", "Leichlingen", "Odenthal", "Overath", "Rösrath", "Wermelskirchen"]},
    {"id": "s5-wipperfuerth", "start": 9.2, "dur": 2.6, "move": 0.75, "zoom": 1.3, "text": "wipperfuerth",
     "office": "wipperfuerth",
     "frame": ["Wipperfürth", "Hückeswagen", "Radevormwald", "Marienheide", "Lindlar", "Engelskirchen"],
     "names": ["Hückeswagen", "Radevormwald", "Marienheide", "Lindlar", "Engelskirchen"]},
    {"id": "s6-zahl", "start": 11.8, "dur": 2.8, "move": 0.75},
    {"id": "s7-abschluss", "start": 14.6, "dur": 3.4},
]
BY_ID = {s["id"]: s for s in SCENES}

OVERVIEW = (50, 470, 1030, 1230)  # Rahmen der Gesamtkarte (Kamera bei --z 1)
ZAHL_SHIFT = 80  # Gesamtkarte im Zähler-Bild etwas tiefer, Platz für „19“
LABEL, MIN_LABEL = 30, 28
TAG_TOP, TAG_H, TITLE_TOP, TITLE, TITLE_LH = 196, 58, 272, 124, 1.0

# Bildmarke: drei Facetten (Koordinaten 0–100 wie im Logo) → Standort
FACETS = [
    {"key": "A", "office": "koeln", "pts": [(0, 0), (79.5, 0), (0, 100)], "spin": -18,
     "grad": ("0", "0", "48.9", "39.6", [("0", "#5e0f18"), ("0.56", "#a4222b"), ("0.8", "#c12a33"), ("0.93", "#ca2c35")])},
    {"key": "R", "office": "wipperfuerth", "pts": [(79.5, 0), (100, 0), (100, 100), (47.5, 40.2)], "spin": 16,
     "grad": ("47.5", "40.2", "100", "0", [("0", "#4a0a13"), ("1", "#b0252e")])},
    {"key": "B", "office": "bgl", "pts": [(0, 100), (47.5, 40.2), (100, 100)], "spin": 12,
     "grad": ("0", "100", "100", "100", [("0", "#480a12"), ("0.5", "#a2222b"), ("0.85", "#ca2c35")])},
]
HOOK_MARK = (540, 880, 330)  # Mitte x, Mitte y, Kantenlänge des großen K im Einstieg
LOGO_W, LOGO_LEFT, LOGO_TOP = 820, 130, 636  # Logo im Abschluss (Bildmarke + Wortmarke)
PIN_SCALE = 0.12  # Facettengröße am Pin (Anteil der Marke)

# Marker-Strich (aus der Registry-Komponente marker-highlight, Stil „underline“)
UNDERLINE_D = "M 2 7 C 20 4.5, 46 8.5, 66 6 C 80 4.5, 92 7.5, 98 5.5"


def load_region():
    with open(os.path.join(GIFS, "assets/geo/region.json"), encoding="utf-8") as f:
        region = json.load(f)
    by = {a["name"]: shape(a["geometry"]) for a in region["areas"] if a["kind"] == "gemeinde"}
    return region, {n: by[n] for n, _ in AREAS}


class Base:
    """Kartenkoordinaten = Bildpunkte der Gesamtansicht (Kamera dort: --z 1)."""

    def __init__(self, bounds, rect):
        minx, miny, maxx, maxy = bounds
        self.k = math.cos(math.radians((miny + maxy) / 2))
        w, h = (maxx - minx) * self.k, maxy - miny
        self.s = min((rect[2] - rect[0]) / w, (rect[3] - rect[1]) / h)
        self.lon, self.lat = (minx + maxx) / 2, (miny + maxy) / 2
        self.cx, self.cy = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2

    def __call__(self, lon, lat):
        return ((lon - self.lon) * self.k * self.s + self.cx, -(lat - self.lat) * self.s + self.cy)

    def geom(self, g):
        return shapely.transform(g, lambda c: np.column_stack(self(c[:, 0], c[:, 1])))


class Cam:
    def __init__(self, cx, cy, z):
        self.cx, self.cy, self.z = cx, cy, z

    def pt(self, x, y):
        return ((x - self.cx) * self.z + AX, (y - self.cy) * self.z + AY)

    def geom(self, g):
        return shapely.transform(g, lambda c: np.column_stack(self.pt(c[:, 0], c[:, 1])))

    def js(self):
        return f'"--cx": {self.cx:.2f}, "--cy": {self.cy:.2f}, "--z": {self.z:.4f}'

    @classmethod
    def fit(cls, g, rect, zoom=1.0):
        x0, y0, x1, y1 = g.bounds
        z = min((rect[2] - rect[0]) / (x1 - x0), (rect[3] - rect[1]) / (y1 - y0)) * zoom
        rx, ry = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2
        return cls((x0 + x1) / 2 - (rx - AX) / z, (y0 + y1) / 2 - (ry - AY) / z, z)


def path(g):
    polys = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
    return " ".join("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ring.coords) + " Z"
                    for p in polys for ring in [p.exterior, *p.interiors])


def centroid(pts):
    """Flächenschwerpunkt eines Polygons (Koordinaten 0–100)."""
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    return cx / (3 * a), cy / (3 * a)


def bezier_length(d):
    """Länge des Marker-Pfads (nur M und C) – für das Strichmuster, ohne getTotalLength im Browser."""
    nums = [float(t) for t in d.replace("M", " ").replace("C", " ").replace(",", " ").split()]
    pts = list(zip(nums[0::2], nums[1::2]))
    length, cur = 0.0, pts[0]
    for i in range(1, len(pts), 3):
        p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2]
        prev = cur
        for k in range(1, 101):
            t = k / 100
            x = (1 - t) ** 3 * cur[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * cur[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            length += math.hypot(x - prev[0], y - prev[1])
            prev = (x, y)
        cur = p3
    return length


def ink_w(measure, text, size, weight):
    i = measure.ink(text, size, weight)
    return i[2] - i[0]


def place_names(measure, cam, base_areas, names, obstacles):
    items = []
    for n in names:
        a = cam.geom(base_areas[n]).buffer(0)
        vis = a.intersection(box(40, BAND_TOP, W - 40, BAND_BOTTOM))
        part = max(getattr(vis, "geoms", [vis]), key=lambda p: p.area) if not vis.is_empty else a
        want = polylabel(part, 1.0) if part.geom_type == "Polygon" else part.representative_point()
        items.append({"text": n, "size": LABEL, "weight": 500, "area": a, "want": (want.x, want.y), "office": None})
    res = label_layout.place(items, obstacles, W, H, measure, min_size=MIN_LABEL)
    return list(zip(items, res))


# ------------------------------------------------------------------------------------------------
# HTML-Bausteine
# ------------------------------------------------------------------------------------------------
SCENE_HEAD = '''<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template id="{id}-template">
      <style>
        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          font-family: "Montserrat", sans-serif;
          color: {ink};
        }}
{css}
      </style>
      <div id="root" data-composition-id="{id}" data-width="{W}" data-height="{H}" data-duration="{dur}">
'''
SCENE_TAIL = '''      </div>
      <script>
        (function () {{
{pre}
          const tl = gsap.timeline({{ paused: true }});
{js}
          window.__timelines["{id}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''


def scene(sid, css, body, js, pre=""):
    s = BY_ID[sid]
    return (SCENE_HEAD.format(id=sid, ink=INK, css=css, W=W, H=H, dur=s["dur"]) + body
            + SCENE_TAIL.format(pre=pre, js="\n".join("          " + j for j in js), id=sid))


def words_html(p, k, line, cls="w"):
    return " ".join(f'<span class="{p}-{cls}" id="{p}-l{k}w{i}">{w}</span>' for i, w in enumerate(line.split(" ")))


def letters_html(p, k, line):
    return "".join(f'<span class="{p}-ch" id="{p}-l{k}c{i}">{"&nbsp;" if ch == " " else ch}</span>'
                   for i, ch in enumerate(line))


def facet_svg(f, gid):
    x1, y1, x2, y2, stops = f["grad"]
    st = "".join(f'<stop offset="{o}" stop-color="{c}" />' for o, c in stops)
    pts = " ".join(f"{x},{y}" for x, y in f["pts"])
    return (f'<svg viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient></defs>'
            f'<polygon points="{pts}" fill="url(#{gid})" /></svg>')


BASE_TEXT_CSS = '''        .{p}-ch,
        .{p}-w {{
          display: inline-block;
        }}
        .{p}-lpos {{
          position: absolute;
          transform: translate(-50%, -50%);
        }}
        .{p}-name {{
          display: block;
          white-space: nowrap;
          font-size: {label}px;
          font-weight: 500;
          line-height: 1.15;
          color: {muted};
        }}
'''


def build():
    region, geo = load_region()
    union = unary_union(list(geo.values()))
    base = Base(union.bounds, OVERVIEW)
    base_areas = {n: base.geom(g) for n, g in geo.items()}
    base_union = unary_union(list(base_areas.values()))
    rhein_base = []
    for ln in region["rhein"]:
        seg = shape(ln).intersection(union.buffer(0.01))
        for s in getattr(seg, "geoms", [seg]):
            if s.geom_type == "LineString" and s.length > 0.01:
                rhein_base.append(base.geom(s))
    office_base = {k: base(*OFFICES[k]) for k in OFFICE_AREA}
    measure = label_layout.Measure()
    report, files = [], {}

    # Kameras
    cam_over = Cam(AX, AY, 1.0)
    cam_zahl = Cam(AX, AY - ZAHL_SHIFT, 1.0)
    head_bottom = {}
    cams = {}
    for s in SCENES:
        if "frame" in s:
            n_lines = len(TEXT[s["text"]][1])
            head_bottom[s["id"]] = TITLE_TOP + n_lines * TITLE * TITLE_LH
            frame = (60, head_bottom[s["id"]] + 40, 1020, 1330)
            cams[s["id"]] = Cam.fit(unary_union([base_areas[n] for n in s["frame"]]), frame, s["zoom"])
    # Abschluss: die Karte schrumpft um ihren Schwerpunkt in die Bildmarke – als Bildtransformation, nicht
    # über die Kamera (deren Mitte und Zoom getrennt zu interpolieren ließe die Karte erst seitlich wegziehen)
    k_logo = LOGO_W / 452
    mark = 100 * k_logo
    mark_cx, mark_cy = LOGO_LEFT + mark / 2, LOGO_TOP + mark / 2
    shrink = 0.16
    ucx, ucy = cam_zahl.pt(base_union.centroid.x, base_union.centroid.y)

    # ------------------------------------------------------------------ Karte
    roles = dict(AREAS)
    names = list(base_areas)
    bgl = base_areas["Bergisch Gladbach"].centroid
    dist = {n: base_areas[n].centroid.distance(bgl) for n in names}
    dmax = max(dist.values()) or 1
    area_svg = "\n".join(
        f'            <path class="karte-area{" focus" if roles[n] == "focus" else ""}" id="karte-a{i}" d="{path(g)}" />'
        for i, (n, g) in enumerate(base_areas.items()))
    rhein_d = ["M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ln.coords) for ln in rhein_base]
    rhein_svg = "\n".join(f'            <path class="karte-rhein draw" id="karte-rd{k}" pathLength="100" d="{d}" />\n'
                          f'            <path class="karte-rhein ganz" id="karte-rh{k}" d="{d}" />' for k, d in enumerate(rhein_d))
    pins = []
    for k, key in enumerate(OFFICE_AREA):
        mx, my = office_base[key]
        pins.append(f'''          <div class="karte-mpos" style="transform: translate(calc({AX}px + ({mx:.1f} - var(--cx)) * var(--z) * 1px), calc({AY}px + ({my:.1f} - var(--cy)) * var(--z) * 1px))">
            <svg class="karte-ring" viewBox="-170 -170 340 340" aria-hidden="true"><circle id="karte-r{k}" cx="0" cy="0" r="20" stroke-width="0" /></svg>
            <div class="karte-pin" id="karte-p{k}">
              <svg viewBox="-24 -24 48 48" aria-hidden="true"><circle cx="0" cy="0" r="19" fill="{RED}" stroke="#ffffff" stroke-width="6" /><circle cx="0" cy="0" r="6.5" fill="#ffffff" /></svg>
            </div>
          </div>''')
    css = f'''        #karte-world {{
          position: absolute;
          inset: 0;
          background: #ffffff;
          transform-origin: {ucx:.1f}px {ucy:.1f}px;
        }}
        #karte-svg {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}
        #karte-cam {{
          transform-box: view-box;
          transform-origin: 0 0;
          transform: translate({AX}px, {AY}px) scale(var(--z)) translate(calc(var(--cx) * -1px), calc(var(--cy) * -1px));
        }}
        .karte-area {{
          fill: {COLORS["area"]};
          stroke: {COLORS["stroke"]};
          stroke-width: 3;
          stroke-linejoin: round;
          vector-effect: non-scaling-stroke;
          transform-box: fill-box;
          transform-origin: 50% 50%;
          transform: scale(var(--s, 0));
        }}
        .karte-area.focus {{
          fill: {COLORS["focus"]};
        }}
        .karte-rhein {{
          fill: none;
          stroke: {COLORS["rhein"]};
          stroke-width: 7;
          stroke-linecap: round;
          stroke-linejoin: round;
          vector-effect: non-scaling-stroke;
        }}
        .karte-rhein.draw {{
          stroke-dasharray: 100 120;
          stroke-dashoffset: 110;
        }}
        .karte-rhein.ganz {{
          opacity: 0;
        }}
        .karte-mpos {{
          position: absolute;
          left: 0;
          top: 0;
          width: 0;
          height: 0;
        }}
        .karte-ring {{
          position: absolute;
          left: -170px;
          top: -170px;
          width: 340px;
          height: 340px;
          overflow: visible;
        }}
        .karte-ring circle {{
          fill: none;
          stroke: {RED};
        }}
        .karte-pin {{
          position: absolute;
          left: -24px;
          top: -24px;
          width: 48px;
          height: 48px;
          opacity: 0;
        }}
        .karte-pin svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}'''
    js = ['const world = document.getElementById("karte-world");',
          f'tl.set(world, {{ {cam_over.js()} }}, 0);',
          '// Gemeinden wachsen von Bergisch Gladbach aus auf']
    for i, n in enumerate(names):
        js.append(f'tl.fromTo("#karte-a{i}", {{ "--s": 0 }}, {{ "--s": 1, duration: 0.5, ease: "back.out(1.25)" }}, {1.1 + dist[n] / dmax * 0.6:.3f});')
    js += ['// Rhein zeichnet sich ein, danach übernimmt die durchgehende Linie',
           'tl.fromTo(".karte-rhein.draw", { strokeDashoffset: 110 }, { strokeDashoffset: 0, duration: 0.9, ease: "power1.inOut" }, 1.45);',
           'tl.set(".karte-rhein.ganz", { opacity: 1 }, 2.38);',
           'tl.set(".karte-rhein.draw", { opacity: 0 }, 2.38);',
           '// Facetten landen als Pins (Szene s1-hook), Ringe pulsen']

    def pulse(k, t, first):
        return [f'tl.fromTo("#karte-r{k}", {{ attr: {{ r: 20 }}, strokeWidth: 0 }}, {{ strokeWidth: 6, duration: 0.04, ease: "none", immediateRender: {"true" if first else "false"} }}, {t:.2f});',
                f'tl.to("#karte-r{k}", {{ attr: {{ r: 140 }}, strokeWidth: 0, duration: 1.1, ease: "power2.out" }}, {t + 0.04:.2f});']

    for k in range(3):
        js.append(f'tl.fromTo("#karte-p{k}", {{ opacity: 0, scale: 0.45 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {2.16 + 0.04 * k:.2f});')
        js += pulse(k, 2.2 + 0.04 * k, True)
    js.append('// Kamera: Köln → Bergisch Gladbach → Wipperfürth → Übersicht')
    for s in SCENES[2:5]:
        js.append(f'tl.to(world, {{ {cams[s["id"]].js()}, duration: {s["move"]}, ease: "power3.inOut" }}, {s["start"]:.2f});')
        # Standort-Gemeinde färbt sich, solange ihre Szene läuft
        a = names.index(OFFICE_AREA[s["office"]])
        t_in, t_out = s["start"] + s["move"] - 0.2, s["start"] + s["dur"] - 0.3
        js.append(f'tl.fromTo("#karte-a{a}", {{ fill: "{COLORS["focus"]}" }}, {{ fill: "{TINT}", duration: 0.3, ease: "power2.out", immediateRender: false }}, {t_in:.2f});')
        js.append(f'tl.to("#karte-a{a}", {{ fill: "{COLORS["focus"]}", duration: 0.25, ease: "power2.in" }}, {t_out:.2f});')
        # ihr Pin pulst, sobald die Kamera steht
        js += pulse(list(OFFICE_AREA).index(s["office"]), s["start"] + s["move"] - 0.05, False)
    z = BY_ID["s6-zahl"]
    js.append(f'tl.to(world, {{ {cam_zahl.js()}, duration: {z["move"]}, ease: "power3.inOut" }}, {z["start"]:.2f});')
    js.append('// Zähler-Welle: die 19 Gemeinden leuchten nacheinander auf')
    t_wave = z["start"] + 0.65
    for i, n in enumerate(sorted(names, key=lambda n: dist[n])):
        a = names.index(n)
        base_fill = COLORS["focus"] if roles[n] == "focus" else COLORS["area"]
        t = t_wave + i * 0.06
        js.append(f'tl.fromTo("#karte-a{a}", {{ fill: "{base_fill}" }}, {{ fill: "{TINT}", duration: 0.14, ease: "power2.out", immediateRender: false }}, {t:.2f});')
        js.append(f'tl.to("#karte-a{a}", {{ fill: "{base_fill}", duration: 0.5, ease: "power1.inOut" }}, {t + 0.5:.2f});')
    e = BY_ID["s7-abschluss"]
    js.append('// Abschluss: Pins heben ab (die Facetten übernehmen), die Karte schrumpft in die Bildmarke')
    for k in range(3):
        js.append(f'tl.to("#karte-p{k}", {{ opacity: 0, scale: 0.4, duration: 0.12, ease: "power2.in" }}, {e["start"]:.2f});')
    js.append(f'tl.to(world, {{ x: {mark_cx - ucx:.1f}, y: {mark_cy - ucy:.1f}, scale: {shrink}, duration: 0.7, ease: "power2.inOut" }}, {e["start"]:.2f});')
    js.append(f'tl.to("#karte-svg", {{ opacity: 0, duration: 0.5, ease: "power1.in" }}, {e["start"] + 0.15:.2f});')
    files["compositions/karte.html"] = (
        SCENE_HEAD.format(id="karte", ink=INK, css=css, W=W, H=H, dur=DURATION)
        + f'''        <div id="karte-world" style="{cam_over.js().replace('"', '').replace(',', ';')}">
          <svg id="karte-svg" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
            <g id="karte-cam">
{area_svg}
{rhein_svg}
            </g>
          </svg>
{chr(10).join(pins)}
        </div>
''' + SCENE_TAIL.format(pre="", js="\n".join("          " + j for j in js), id="karte"))

    # ------------------------------------------------------------------ s1: Einstieg + Facetten
    p = "s1"
    hook_size = 104
    while max(ink_w(measure, t, hook_size, 900) for t in TEXT["hook"]) > 960:
        hook_size -= 2
    hx, hy, hs = HOOK_MARK
    mx0, my0 = hx - hs / 2, hy - hs / 2
    line2_w = ink_w(measure, TEXT["hook"][1], hook_size, 900)
    ul_len = bezier_length(UNDERLINE_D)
    ul_top = 196 + hook_size * 1.04 * 2 - 6
    facets, fjs = [], []
    for f in FACETS:
        cx, cy = centroid(f["pts"])
        px, py = office_base[f["office"]]  # Kamera bei --z 1: Kartenpunkt = Bildpunkt
        sx, sy = mx0 + cx / 100 * hs, my0 + cy / 100 * hs  # Schwerpunkt im Bild
        dx, dy = cx - 50, cy - 50
        norm = math.hypot(dx, dy) or 1
        # Drehpunkt = Schwerpunkt der Facette, damit sie genau auf dem Pin landet
        facets.append(f'        <div class="{p}-facet" id="{p}-f{f["key"]}" style="left: {mx0:.1f}px; top: {my0:.1f}px; width: {hs}px; height: {hs}px; transform-origin: {cx:.2f}% {cy:.2f}%">'
                      f'{facet_svg(f, p + "-g" + f["key"])}</div>')
        fjs += [f'tl.fromTo("#{p}-f{f["key"]}", {{ x: 0, y: 0, rotation: 0, scale: 1 }}, {{ x: {dx / norm * 30:.1f}, y: {dy / norm * 30:.1f}, rotation: {f["spin"] * 0.4:.1f}, duration: 0.3, ease: "expo.out" }}, 1.0);',
                f'tl.to("#{p}-f{f["key"]}", {{ x: {px - sx:.1f}, duration: 0.7, ease: "power2.inOut" }}, 1.45);',
                f'tl.to("#{p}-f{f["key"]}", {{ y: {py - sy:.1f}, duration: 0.7, ease: "power3.in" }}, 1.45);',
                f'tl.to("#{p}-f{f["key"]}", {{ scale: {PIN_SCALE}, rotation: {f["spin"]}, duration: 0.7, ease: "power2.in" }}, 1.45);',
                f'tl.to("#{p}-f{f["key"]}", {{ opacity: 0, duration: 0.08, ease: "none" }}, 2.15);']
    css = BASE_TEXT_CSS.format(p=p, label=LABEL, muted=MUTED) + f'''        .{p}-kopf {{
          position: absolute;
          left: 40px;
          right: 40px;
          top: 196px;
          text-align: center;
          font-size: {hook_size}px;
          font-weight: 900;
          letter-spacing: -0.035em;
          line-height: 1.04;
        }}
        .{p}-zeile {{
          display: block;
          white-space: nowrap;
        }}
        .{p}-zeile.akzent {{
          color: {RED};
        }}
        .{p}-strich {{
          position: absolute;
          left: {540 - line2_w * 0.54:.1f}px;
          top: {ul_top:.1f}px;
          width: {line2_w * 1.08:.1f}px;
          height: 30px;
          overflow: visible;
        }}
        .{p}-strich path {{
          fill: none;
          stroke: {RED};
          stroke-width: 4.5;
          stroke-linecap: round;
          stroke-dasharray: {ul_len:.2f};
          stroke-dashoffset: {ul_len:.2f};
          opacity: 0;
        }}
        .{p}-facet {{
          position: absolute;
        }}
        .{p}-facet svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}'''
    body = f'''        <div class="{p}-kopf">
          <span class="{p}-zeile" id="{p}-z1">{TEXT["hook"][0]}</span>
          <span class="{p}-zeile akzent" id="{p}-z2">{words_html(p, 2, TEXT["hook"][1])}</span>
        </div>
        <svg class="{p}-strich" viewBox="0 0 100 12" preserveAspectRatio="none" aria-hidden="true"><path id="{p}-ul" d="{UNDERLINE_D}" /></svg>
{chr(10).join(facets)}
'''
    js = [f'tl.fromTo("#{p}-l2w{i}", {{ opacity: 0, scale: 1.25, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.18, ease: "expo.out" }}, {0.33 + 0.09 * i:.2f});'
          for i in range(len(TEXT["hook"][1].split(" ")))]
    js += [f'tl.set("#{p}-ul", {{ opacity: 1 }}, 0.72);',
           f'tl.fromTo("#{p}-ul", {{ strokeDashoffset: {ul_len:.2f} }}, {{ strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut" }}, 0.72);']
    js += fjs
    js += [f'tl.to("#{p}-z1", {{ opacity: 0, filter: "blur(10px)", duration: 0.18, ease: "power2.in" }}, 2.08);',
           f'tl.to(["#{p}-z2", "#{p}-ul"], {{ opacity: 0, filter: "blur(10px)", duration: 0.18, ease: "power2.in" }}, 2.14);']
    files[f"compositions/{BY_ID['s1-hook']['id']}.html"] = scene("s1-hook", css, body, js)

    # ------------------------------------------------------------------ s2: Region
    p = "s2"
    css = BASE_TEXT_CSS.format(p=p, label=LABEL, muted=MUTED) + f'''        .{p}-kopf {{
          position: absolute;
          left: 40px;
          right: 40px;
          top: 200px;
          text-align: center;
          font-size: 84px;
          font-weight: 900;
          letter-spacing: -0.03em;
          line-height: 1.06;
        }}
        .{p}-zeile {{
          display: block;
          white-space: nowrap;
        }}'''
    body = f'''        <div class="{p}-kopf">
''' + "\n".join(f'          <span class="{p}-zeile">{words_html(p, k, ln)}</span>' for k, ln in enumerate(TEXT["region"])) + '''
        </div>
'''
    js, t = [], 0.12
    for k, ln in enumerate(TEXT["region"]):
        for i, _ in enumerate(ln.split(" ")):
            js.append(f'tl.fromTo("#{p}-l{k}w{i}", {{ color: "#d6dad8" }}, {{ color: "{RED if k == 0 and i == 1 else INK}", duration: 0.22, ease: "power2.out" }}, {t:.2f});')
            js.append(f'tl.fromTo("#{p}-l{k}w{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, ease: "none" }}, {t:.2f});')
            t += 0.09
    js.append(f'tl.to(".{p}-w", {{ opacity: 0, filter: "blur(10px)", duration: 0.16, ease: "power2.in", stagger: 0.02 }}, {BY_ID["s2-region"]["dur"] - 0.24:.2f});')
    files["compositions/s2-region.html"] = scene("s2-region", css, body, js)

    # ------------------------------------------------------------------ s3–s5: Standorte
    for s in SCENES[2:5]:
        p = s["id"].split("-")[0]
        tag, lines = TEXT[s["text"]]
        cam = cams[s["id"]]
        obs = [box(0, 0, W, BAND_TOP), box(0, BAND_BOTTOM, W, H), RAIL,
               box(0, 0, W, head_bottom[s["id"]] + 24)]
        obs += [Point(*cam.pt(*office_base[k])).buffer(34) for k in OFFICE_AREA]
        obs += [cam.geom(ln).buffer(6) for ln in rhein_base]
        placed = place_names(measure, cam, base_areas, s["names"], obs)
        report.append((s["id"], placed))
        tag_w = ink_w(measure, tag, 36, 800) + 36
        css = BASE_TEXT_CSS.format(p=p, label=LABEL, muted=MUTED) + f'''        .{p}-tag {{
          position: absolute;
          left: {540 - tag_w / 2:.1f}px;
          top: {TAG_TOP}px;
          width: {tag_w:.1f}px;
          height: {TAG_H - 6}px;
          border-radius: 8px;
          background: {RED};
          color: #ffffff;
          font-size: 36px;
          font-weight: 800;
          line-height: {TAG_H - 6}px;
          text-align: center;
          letter-spacing: 0.01em;
        }}
        .{p}-titel {{
          position: absolute;
          left: 30px;
          right: 30px;
          top: {TITLE_TOP}px;
          text-align: center;
          font-size: {TITLE}px;
          font-weight: 900;
          letter-spacing: -0.04em;
          line-height: {TITLE_LH};
        }}
        .{p}-zeile {{
          display: block;
          white-space: nowrap;
          overflow: hidden;
          padding: 0.14em 0 0.06em;
          margin: -0.14em 0 -0.06em;
        }}'''
        names_html = []
        for k, (it, r) in enumerate(placed):
            fs = f' style="font-size: {r["size"]}px"' if r["size"] != it["size"] else ""
            names_html.append(f'        <div class="{p}-lpos" style="left: {r["x"]:.1f}px; top: {r["y"]:.1f}px">'
                              f'<span class="{p}-name" id="{p}-n{k}"{fs}>{it["text"]}</span></div>')
        body = (f'        <div class="{p}-tag" id="{p}-tag">{tag}</div>\n        <div class="{p}-titel">\n'
                + "\n".join(f'          <span class="{p}-zeile">{letters_html(p, k, ln)}</span>' for k, ln in enumerate(lines))
                + "\n        </div>\n" + "\n".join(names_html) + "\n")
        mv, dur = s["move"], s["dur"]
        js = [f'tl.fromTo("#{p}-tag", {{ clipPath: "inset(0% 100% 0% 0% round 8px)" }}, {{ clipPath: "inset(0% 0% 0% 0% round 8px)", duration: 0.28, ease: "power3.out" }}, {mv * 0.4:.2f});']
        t = mv * 0.45
        for k, ln in enumerate(lines):
            for i, _ in enumerate(ln):
                js.append(f'tl.fromTo("#{p}-l{k}c{i}", {{ yPercent: 115 }}, {{ yPercent: 0, duration: 0.42, ease: "expo.out" }}, {t:.3f});')
                t += 0.035
        js += [f'tl.fromTo("#{p}-n{k}", {{ opacity: 0, scale: 0.8, filter: "blur(6px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.2, ease: "expo.out" }}, {mv + 0.08 + 0.06 * k:.2f});'
               for k in range(len(placed))]
        t_out = dur - 0.26
        js.append(f'tl.to(".{p}-name", {{ opacity: 0, filter: "blur(8px)", duration: 0.14, ease: "power2.in" }}, {t_out - 0.04:.2f});')
        js.append(f'tl.to(".{p}-ch", {{ yPercent: -115, duration: 0.22, ease: "power3.in", stagger: 0.012 }}, {t_out:.2f});')
        js.append(f'tl.to("#{p}-tag", {{ clipPath: "inset(0% 0% 0% 100% round 8px)", duration: 0.2, ease: "power3.in" }}, {t_out + 0.02:.2f});')
        files[f"compositions/{s['id']}.html"] = scene(s["id"], css, body, js)

    # ------------------------------------------------------------------ s6: 19 Städte und Gemeinden
    p = "s6"
    zahl, zlabel = TEXT["zahl"]
    css = BASE_TEXT_CSS.format(p=p, label=LABEL, muted=MUTED) + f'''        .{p}-zahl {{
          position: absolute;
          left: 0;
          right: 0;
          top: 176px;
          text-align: center;
          font-size: 270px;
          font-weight: 900;
          letter-spacing: -0.05em;
          line-height: 1;
          color: {RED};
        }}
        .{p}-label {{
          position: absolute;
          left: 40px;
          right: 40px;
          top: 452px;
          text-align: center;
          font-size: 62px;
          font-weight: 900;
          letter-spacing: -0.03em;
          line-height: 1.05;
        }}
        /* Zahlenrad (Registry: number-wheel) */
        .hf-number-wheel {{
          display: inline-flex;
          align-items: baseline;
          gap: 0.02em;
          font-variant-numeric: tabular-nums;
        }}
        .hf-number-wheel-digit {{
          display: inline-block;
          height: 1em;
          overflow: hidden;
        }}
        .hf-number-wheel-strip {{
          display: grid;
        }}
        .hf-number-wheel-strip span {{
          height: 1em;
          line-height: 1em;
        }}'''
    body = f'''        <div class="{p}-zahl" id="{p}-zahl"><span class="hf-number-wheel" id="{p}-rad" data-value="{zahl}" data-layout-ignore></span></div>
        <div class="{p}-label" id="{p}-label">{words_html(p, 0, zlabel)}</div>
'''
    # Zahlenrad aufbauen (aus compositions/components/number-wheel.html, eine Extra-Umdrehung)
    pre = f'''          document.querySelectorAll("#{p}-rad").forEach((el) => {{
            if (el.dataset.ready === "1") return;
            const value = el.dataset.value || "0";
            el.textContent = "";
            for (const ch of value) {{
              const stops = 10 + Number(ch);
              const frame = document.createElement("span");
              frame.className = "hf-number-wheel-digit";
              const strip = document.createElement("span");
              strip.className = "hf-number-wheel-strip";
              strip.dataset.stops = String(stops);
              for (let i = 0; i <= stops; i++) {{
                const step = document.createElement("span");
                step.textContent = String(i % 10);
                strip.appendChild(step);
              }}
              frame.appendChild(strip);
              el.appendChild(frame);
            }}
            el.dataset.ready = "1";
          }});'''
    t0 = z["move"] - 0.2
    js = [f'tl.fromTo("#{p}-zahl", {{ opacity: 0, scale: 0.86, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {t0:.2f});',
          f'tl.fromTo("#{p}-rad .hf-number-wheel-strip", {{ y: 0 }}, {{ y: (i, el) => -Number(el.dataset.stops) + "em", duration: 1.2, ease: "power3.out", stagger: 0.08 }}, {t0:.2f});']
    js += [f'tl.fromTo("#{p}-l0w{i}", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.16, ease: "power4.out" }}, {t0 + 0.35 + 0.08 * i:.2f});'
           for i in range(len(zlabel.split(" ")))]
    js.append(f'tl.to(["#{p}-zahl", "#{p}-label"], {{ opacity: 0, filter: "blur(12px)", duration: 0.18, ease: "power2.in" }}, {z["dur"] - 0.22:.2f});')
    files["compositions/s6-zahl.html"] = scene("s6-zahl", css, body, js, pre=pre)

    # ------------------------------------------------------------------ s7: Logo setzt sich zusammen
    p = "s7"
    close_size = 82
    while max(ink_w(measure, t, close_size, 900) for t in TEXT["close"]) > 960:
        close_size -= 2
    zmark = []
    fjs = []
    for f in FACETS:
        cx, cy = centroid(f["pts"])
        px, py = cam_zahl.pt(*office_base[f["office"]])  # Pin-Position am Ende des Zähler-Bilds
        sx, sy = LOGO_LEFT + cx / 100 * mark, LOGO_TOP + cy / 100 * mark
        zmark.append(f'        <div class="{p}-facet" id="{p}-f{f["key"]}" style="left: {LOGO_LEFT}px; top: {LOGO_TOP}px; width: {mark:.1f}px; height: {mark:.1f}px; transform-origin: {cx:.2f}% {cy:.2f}%">'
                     f'{facet_svg(f, p + "-g" + f["key"])}</div>')
        s_start = PIN_SCALE * HOOK_MARK[2] / mark
        t0 = 0.05 * FACETS.index(f)  # Facetten nacheinander, A – R – B
        # löst den Pin ab (Überblendung 3 Frames), dann Bogenflug: x und y mit verschiedenen Kurven
        fjs += [f'tl.fromTo("#{p}-f{f["key"]}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, ease: "none" }}, 0.0);',
                f'tl.fromTo("#{p}-f{f["key"]}", {{ x: {px - sx:.1f}, scale: {s_start:.3f}, rotation: {f["spin"]} }}, {{ x: 0, scale: 1, rotation: 0, duration: 0.8, ease: "power3.inOut" }}, {t0:.2f});',
                f'tl.fromTo("#{p}-f{f["key"]}", {{ y: {py - sy:.1f} }}, {{ y: 0, duration: 0.8, ease: "power2.inOut" }}, {t0:.2f});']
    css = BASE_TEXT_CSS.format(p=p, label=LABEL, muted=MUTED) + f'''        .{p}-kopf {{
          position: absolute;
          left: 40px;
          right: 40px;
          top: 300px;
          text-align: center;
          font-size: {close_size}px;
          font-weight: 900;
          letter-spacing: -0.03em;
          line-height: 1.08;
        }}
        .{p}-zeile {{
          display: block;
          white-space: nowrap;
        }}
        .{p}-zeile.akzent {{
          color: {RED};
        }}
        .{p}-facet {{
          position: absolute;
        }}
        .{p}-facet svg,
        .{p}-wort svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}
        .{p}-wort {{
          position: absolute;
          left: {LOGO_LEFT + 120 * k_logo:.1f}px;
          top: {LOGO_TOP}px;
          width: {340 * k_logo:.1f}px;
          height: {mark:.1f}px;
        }}
        .{p}-wort text {{
          font-family: "Montserrat", sans-serif;
          fill: {INK};
        }}
        .{p}-adresse {{
          position: absolute;
          left: 40px;
          right: 40px;
          top: {LOGO_TOP + mark + 70:.0f}px;
          text-align: center;
          font-size: 46px;
          font-weight: 700;
          letter-spacing: -0.01em;
          line-height: 1.1;
        }}'''
    body = (f'''        <div class="{p}-kopf">
          <span class="{p}-zeile akzent">{words_html(p, 0, TEXT["close"][0])}</span>
          <span class="{p}-zeile">{words_html(p, 1, TEXT["close"][1])}</span>
        </div>
''' + "\n".join(zmark) + f'''
        <div class="{p}-wort" id="{p}-wort">
          <svg viewBox="120 0 340 100" aria-hidden="true"><text x="125.2" y="53" font-size="77" font-weight="700" textLength="328.5" lengthAdjust="spacing">KNIGGE</text><text x="125.5" y="100" font-size="44.3" font-weight="400" textLength="330.5" lengthAdjust="spacing">IMMOBILIEN</text></svg>
        </div>
        <div class="{p}-adresse" id="{p}-adresse">{TEXT["url"]}</div>
''')
    js = list(fjs)
    js.append(f'tl.fromTo("#{p}-wort", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }}, 0.8);')
    t = 0.9
    for k, ln in enumerate(TEXT["close"]):
        for i, _ in enumerate(ln.split(" ")):
            js.append(f'tl.fromTo("#{p}-l{k}w{i}", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.16, ease: "power4.out" }}, {t:.2f});')
            t += 0.07
    # Adresse als letzte Zeile: mindestens 2 s bis zum Ende
    js.append(f'tl.fromTo("#{p}-adresse", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }}, 1.2);')
    files["compositions/s7-abschluss.html"] = scene("s7-abschluss", css, body, js)

    # ------------------------------------------------------------------ index.html
    hosts = [f'      <div id="karte" data-composition-id="karte" data-composition-src="compositions/karte.html" data-start="0" data-duration="{DURATION}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>']
    for s in SCENES:
        hosts.append(f'      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    files["index.html"] = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>KNIGGE Immobilien – Drei Standorte. Eine Region. (Instagram-Reel)</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: {W}px;
        height: {H}px;
        overflow: hidden;
        background: #ffffff;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #ffffff;
      }}
    </style>
  </head>
  <body>
    <!--
      KNIGGE Immobilien – Instagram-Reel „Drei Facetten“ (1080×1920, 18 s, ohne Ton)
      erzeugt von tools/build_reel.py – Texte dort in TEXT ändern
    -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="{W}" data-height="{H}" data-fps="{FPS}" data-motion-blur="on">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
    # alte Szenen von Version 1 entfernen
    for old in ("b1-hook", "b2-koeln", "b3-bergisch-gladbach", "b4-wipperfuerth", "b5-abschluss"):
        fp = os.path.join(ROOT, "compositions", old + ".html")
        if os.path.exists(fp):
            os.remove(fp)
    for rel, html in files.items():
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(html)
        print("geschrieben:", rel)
    print(f"Einstieg {hook_size} px, Abschluss {close_size} px")
    for k, c in {**{"übersicht": cam_over, "zahl": cam_zahl}, **cams}.items():
        print(f"  Kamera {k}: Mitte ({c.cx:.0f}, {c.cy:.0f}), Zoom {c.z:.2f}")
    for sid, placed in report:
        bad = [(it["text"], r) for it, r in placed if r["status"] != "ok"]
        print(f"  {sid}: {len(placed)} Namen" + ("" if not bad else " – " + ", ".join(
            f"{t} {r['status']} ({r['size']} px)" for t, r in bad)))


if __name__ == "__main__":
    build()
