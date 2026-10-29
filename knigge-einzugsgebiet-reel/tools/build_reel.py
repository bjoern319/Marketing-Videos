#!/usr/bin/env python3
"""Erzeugt das Instagram-Reel „Drei Standorte. Eine Region." (1080×1920, 15 s, 30 fps):
index.html und compositions/*.html.

Grundlage ist die Einzugsgebiet-Karte aus ../knigge-standorte-gifs: Gemeinden, Standorte, Farben und
Logo aus tools/build_maps.py, Flächen aus assets/geo/region.json, Beschriftung über
tools/label_layout.py (jeder Name passt mit Abstand in seine Fläche, mindestens 28 px groß).

Ablauf (SPEC.md): Übersicht → Köln → Bergisch Gladbach → Wipperfürth → Übersicht mit Abschluss.
Die Kamera ist eine Transformation der Karte über die CSS-Variablen --cx, --cy (Kartenpunkt in der
Bildmitte) und --z (Zoom); die Marker rechnen ihre Bildposition aus denselben Variablen und
bleiben dadurch gleich groß. Ortsnamen erscheinen nur, während die Kamera steht.

Ändern: Texte in TEXT, Zeiten in BEATS, dann `python3 tools/build_reel.py` und `npm run check`.
"""
import json
import math
import os
import sys

import numpy as np
import shapely
from shapely.geometry import shape, Point, LineString, box
from shapely.ops import unary_union, polylabel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIFS = os.path.normpath(os.path.join(ROOT, "..", "knigge-standorte-gifs"))
sys.path.insert(0, os.path.join(GIFS, "tools"))
import build_maps  # noqa: E402  Gemeinden, Standorte, Farben, Logo
import label_layout  # noqa: E402

W, H, FPS, DURATION = 1080, 1920, 30, 15.0
AX, AY = 540, 850  # Bildpunkt, auf den die Kamera ihren Kartenpunkt legt
INK, MUTED, RED = "#444f4f", "#5e6a6a", "#ca2c35"
COLORS = build_maps.COLORS
OFFICES = build_maps.OFFICES
AREAS = build_maps.MAPS["formats/karte-einzugsgebiet.html"]["areas"]  # (Name, Rolle) – wie im GIF

# Reels-Oberfläche: Text nur im Band 168–1330 px, nicht unter der Aktionsleiste rechts
BAND_TOP, BAND_BOTTOM, RAIL = 168, 1330, box(940, 1000, W, H)

TEXT = {
    "hook": ["Drei Standorte.", "Eine Region."],
    "koeln": ("Standort", "Köln"),
    "bgl": ("Hauptsitz", "Bergisch Gladbach"),
    "wipperfuerth": ("Standort", "Wipperfürth"),
    "close": ["Ein Ansprechpartner", "für Ihre Immobilie."],
    "url": "knigge-immobilien.de",
}

# Szenen: id, Start, Dauer, Kameraziel (Gemeinden, die ins Bild sollen), Namen auf der Karte
BEATS = [
    {"id": "b1-hook", "start": 0.0, "dur": 2.6},
    # zoom: Faktor über „alles im Rahmen“ hinaus, damit jeder Name in 30 px in seine Fläche passt
    {"id": "b2-koeln", "start": 2.6, "dur": 2.8, "move": 0.9, "zoom": 1.15, "text": "koeln", "office": "koeln",
     "frame": ["Köln", "Leverkusen", "Pulheim", "Frechen", "Hürth"],
     "names": ["Leverkusen", "Pulheim", "Frechen", "Hürth"]},
    {"id": "b3-bergisch-gladbach", "start": 5.4, "dur": 2.8, "move": 0.8, "zoom": 1.3, "text": "bgl", "office": "bgl",
     "frame": ["Bergisch Gladbach", "Burscheid", "Kürten", "Leichlingen", "Odenthal", "Overath", "Rösrath",
               "Wermelskirchen"],
     "names": ["Burscheid", "Kürten", "Leichlingen", "Odenthal", "Overath", "Rösrath", "Wermelskirchen"]},
    {"id": "b4-wipperfuerth", "start": 8.2, "dur": 2.8, "move": 0.8, "zoom": 1.3, "text": "wipperfuerth", "office": "wipperfuerth",
     "frame": ["Wipperfürth", "Hückeswagen", "Radevormwald", "Marienheide", "Lindlar", "Engelskirchen"],
     "names": ["Hückeswagen", "Radevormwald", "Marienheide", "Lindlar", "Engelskirchen"]},
    {"id": "b5-abschluss", "start": 11.0, "dur": 4.0, "move": 0.9},
]
OFFICE_NAMES = {"koeln": "Köln", "bgl": "Bergisch Gladbach", "wipperfuerth": "Wipperfürth"}

OVERVIEW = (50, 470, 1030, 1230)  # Rahmen der Gesamtkarte am Anfang
FINAL = (90, 400, 990, 1000)  # Rahmen der Gesamtkarte im Abschluss (darunter Logo und Adresse)
BEAT_FRAME = (60, 450, 1020, 1330)  # Rahmen für die Gemeinden einer Standort-Szene (vor dem Zoom-Faktor)
LABEL, OFFICE_LABEL, MIN_LABEL = 30, 32, 28
HEAD_TOP, KICKER, HEAD, HEAD_LH = 196, 40, 92, 1.04
LOGO_W, LOGO_TOP, URL_TOP = 600, 1046, 1212


def load_region():
    with open(os.path.join(GIFS, "assets/geo/region.json"), encoding="utf-8") as f:
        region = json.load(f)
    by = {a["name"]: shape(a["geometry"]) for a in region["areas"] if a["kind"] == "gemeinde"}
    return region, {n: by[n] for n, _ in AREAS}


class Base:
    """Kartenkoordinaten: Bildpunkte der Gesamtansicht am Anfang (Kamera dort: --z 1)."""

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

    @classmethod
    def fit(cls, g, rect):
        x0, y0, x1, y1 = g.bounds
        z = min((rect[2] - rect[0]) / (x1 - x0), (rect[3] - rect[1]) / (y1 - y0))
        rx, ry = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2
        return cls((x0 + x1) / 2 - (rx - AX) / z, (y0 + y1) / 2 - (ry - AY) / z, z)


def path(g, nd=1):
    polys = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            out.append("M" + " L".join(f"{x:.{nd}f} {y:.{nd}f}" for x, y in ring.coords) + " Z")
    return " ".join(out)


def fit_size(measure, lines, size, weight, width):
    """Größte Schrift ≤ size, bei der jede Zeile höchstens width breit ist."""
    while size > MIN_LABEL:
        if all(measure.ink(t, size, weight)[2] - measure.ink(t, size, weight)[0] <= width for t in lines):
            return size
        size -= 2
    return size


def head_lines(measure, text):
    """Ortsname in einer Zeile, wenn er passt, sonst an Leerzeichen umbrechen."""
    ink = measure.ink(text, HEAD, 800)
    return [text] if ink[2] - ink[0] <= 940 else text.split(" ", 1)


def head_bottom(n_lines):
    return HEAD_TOP + KICKER * 1.15 + n_lines * HEAD * HEAD_LH


def place_names(measure, cam, base_areas, names, office_key, obstacles, extra_office=None):
    items = []
    for n in names:
        a = cam.geom(base_areas[n]).buffer(0)
        vis = a.intersection(box(40, BAND_TOP, W - 40, BAND_BOTTOM))
        part = max(getattr(vis, "geoms", [vis]), key=lambda p: p.area) if not vis.is_empty else a
        want = polylabel(part, 1.0) if part.geom_type == "Polygon" else part.representative_point()
        items.append({"text": n, "size": LABEL, "weight": 500, "area": a, "want": (want.x, want.y), "office": None})
    for key in extra_office or []:
        ox, oy = extra_office[key]
        home = next((cam.geom(base_areas[n]).buffer(0) for n, _ in AREAS
                     if cam.geom(base_areas[n]).contains(Point(ox, oy))), None)
        items.append({"text": OFFICE_NAMES[key], "size": OFFICE_LABEL, "weight": 700, "area": home,
                      "want": (ox, oy + 46), "office": (ox, oy)})
    res = label_layout.place(items, obstacles, W, H, measure, min_size=MIN_LABEL)
    return [(it, r) for it, r in zip(items, res)]


def common_obstacles(cam, rhein_base, markers_px):
    obs = [box(0, 0, W, BAND_TOP), box(0, BAND_BOTTOM, W, H), RAIL]
    obs += [Point(x, y).buffer(30) for x, y in markers_px]
    obs += [cam.geom(ln).buffer(6) for ln in rhein_base]
    return obs


# ------------------------------------------------------------------------------------------------
# HTML
# ------------------------------------------------------------------------------------------------
SCENE_HEAD = '''<!doctype html>
<html lang="de"{vars}>
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
          const tl = gsap.timeline({{ paused: true }});
{js}
          window.__timelines["{id}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''

TEXT_CSS = '''        .{p}-kopf {{
          position: absolute;
          left: 60px;
          right: 60px;
          top: {top}px;
          text-align: center;
        }}
        .{p}-zeile {{
          display: block;
          white-space: nowrap;
          font-weight: 800;
          letter-spacing: -0.03em;
          line-height: {lh};
        }}
        .{p}-dach {{
          display: block;
          font-size: {kicker}px;
          font-weight: 700;
          line-height: 1.15;
          color: {red};
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
        .{p}-name.ort {{
          font-weight: 700;
          color: {ink};
        }}
'''


def variables(spec):
    return " data-composition-variables='" + json.dumps(spec, ensure_ascii=False) + "'"


def blur_in(sel, t, dur=0.15):
    return (f'          tl.fromTo("{sel}", {{ opacity: 0, filter: "blur(8px)" }}, '
            f'{{ opacity: 1, filter: "blur(0px)", duration: {dur}, ease: "power4.out" }}, {t:.2f});')


def blur_out(sel, t, dur=0.15):
    return (f'          tl.to("{sel}", {{ opacity: 0, filter: "blur(8px)", duration: {dur}, ease: "power2.in" }}, {t:.2f});')


def name_divs(p, placed):
    out = []
    for k, (it, r) in enumerate(placed):
        cls = f"{p}-name ort" if it["office"] else f"{p}-name"
        fs = f' style="font-size: {r["size"]}px"' if r["size"] != it["size"] else ""
        out.append(f'        <div class="{p}-lpos" style="left: {r["x"]:.1f}px; top: {r["y"]:.1f}px">'
                   f'<span class="{cls}" id="{p}-n{k}"{fs}>{it["text"]}</span></div>')
    return "\n".join(out)


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
    office_base = {k: base(*OFFICES[k]) for k in OFFICE_NAMES}

    cams = {"b1-hook": Cam(AX, AY, 1.0)}
    for b in BEATS:
        if "frame" in b:
            c = Cam.fit(unary_union([base_areas[n] for n in b["frame"]]), BEAT_FRAME)
            cams[b["id"]] = Cam(c.cx, c.cy, c.z * b["zoom"])
    cams["b5-abschluss"] = Cam.fit(base_union, FINAL)

    measure = label_layout.Measure()
    report = []
    files = {}

    # --- Karte: Flächen, Rhein, Marker, Kamera -------------------------------------------------
    roles = dict(AREAS)
    area_svg = "\n".join(
        f'            <path class="karte-area{" focus" if roles[n] == "focus" else ""}" id="karte-a{i}" d="{path(g)}" />'
        for i, (n, g) in enumerate(base_areas.items()))
    # Rhein doppelt: gestrichelt zum Einzeichnen (nur bei Zoom 1), dann die durchgehende Linie
    # (ein Strichmuster würde mit non-scaling-stroke beim Zoomen falsch skalieren)
    rhein_d = ["M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ln.coords) for ln in rhein_base]
    rhein_svg = "\n".join(f'            <path class="karte-rhein draw" id="karte-rd{k}" pathLength="100" d="{d}" />\n'
                           f'            <path class="karte-rhein ganz" id="karte-rh{k}" d="{d}" />'
                           for k, d in enumerate(rhein_d))
    marker_html = []
    for k, key in enumerate(OFFICE_NAMES):
        mx, my = office_base[key]
        marker_html.append(f'''        <div class="karte-mpos" style="transform: translate(calc({AX}px + ({mx:.1f} - var(--cx)) * var(--z) * 1px), calc({AY}px + ({my:.1f} - var(--cy)) * var(--z) * 1px))">
          <svg class="karte-ring" viewBox="-160 -160 320 320" aria-hidden="true"><circle id="karte-r{k}" cx="0" cy="0" r="20" stroke-width="0" /></svg>
          <div class="karte-marker" id="karte-m{k}">
            <svg viewBox="-22 -22 44 44" aria-hidden="true"><circle cx="0" cy="0" r="17" fill="#ffffff" stroke="{INK}" stroke-width="5" /><circle cx="0" cy="0" r="7" fill="{RED}" /></svg>
          </div>
        </div>''')
    karte_css = f'''        #karte-world {{
          position: absolute;
          inset: 0;
          background: #ffffff;
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
          left: -160px;
          top: -160px;
          width: 320px;
          height: 320px;
          overflow: visible;
        }}
        .karte-ring circle {{
          fill: none;
          stroke: {RED};
        }}
        .karte-marker {{
          position: absolute;
          left: -22px;
          top: -22px;
          width: 44px;
          height: 44px;
        }}
        .karte-marker svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}'''
    A = cams["b1-hook"]
    js = [f'          const world = document.getElementById("karte-world");',
          f'          tl.set(world, {{ "--cx": {A.cx:.2f}, "--cy": {A.cy:.2f}, "--z": {A.z:.4f} }}, 0);',
          '          // Rhein zeichnet sich ein, danach übernimmt die durchgehende Linie',
          '          tl.fromTo(".karte-rhein.draw", { strokeDashoffset: 110 }, { strokeDashoffset: 0, duration: 1.0, ease: "power1.inOut" }, 0.17);',
          '          tl.set(".karte-rhein.ganz", { opacity: 1 }, 1.2);',
          '          tl.set(".karte-rhein.draw", { opacity: 0 }, 1.2);',
          '          // drei Standorte fallen nacheinander, jeder pulst einmal']

    def pulse(k, t, first):
        return [f'          tl.fromTo("#karte-r{k}", {{ attr: {{ r: 20 }}, strokeWidth: 0 }}, {{ strokeWidth: 5, duration: 0.04, ease: "none", immediateRender: {"true" if first else "false"} }}, {t:.2f});',
                f'          tl.to("#karte-r{k}", {{ attr: {{ r: 130 }}, strokeWidth: 0, duration: 1.2, ease: "power2.out" }}, {t + 0.04:.2f});']

    for k in range(3):
        t = 0.47 + k * 0.23
        js.append(f'          tl.fromTo("#karte-m{k}", {{ y: -40, scale: 0 }}, {{ y: 0, scale: 1, duration: 0.47, ease: "back.out(1.7)" }}, {t:.2f});')
        js += pulse(k, t + 0.4, True)
    js.append('          // Kamera: Köln → Bergisch Gladbach → Wipperfürth → Übersicht')
    for b in BEATS[1:]:
        c = cams[b["id"]]
        js.append(f'          tl.to(world, {{ "--cx": {c.cx:.2f}, "--cy": {c.cy:.2f}, "--z": {c.z:.4f}, duration: {b["move"]}, ease: "power2.inOut" }}, {b["start"]:.2f});')
    t_end = BEATS[-1]["start"] + BEATS[-1]["move"]
    js.append('          // Abschluss: alle drei Standorte pulsen gemeinsam')
    for k in range(3):
        js += pulse(k, t_end + k * 0.12, False)
    files["compositions/karte.html"] = (
        SCENE_HEAD.format(vars="", id="karte", ink=INK, css=karte_css, W=W, H=H, dur=DURATION)
        + f'''        <div id="karte-world" style="--cx: {A.cx:.2f}; --cy: {A.cy:.2f}; --z: {A.z:.4f}">
          <svg id="karte-svg" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
            <g id="karte-cam">
{area_svg}
{rhein_svg}
            </g>
          </svg>
{chr(10).join(marker_html)}
        </div>
''' + SCENE_TAIL.format(js="\n".join(js), id="karte"))

    def marker_px(cam):
        return [cam.pt(*office_base[k]) for k in OFFICE_NAMES]

    # --- b1: Einstieg ---------------------------------------------------------------------------
    hook_size = fit_size(measure, TEXT["hook"], 96, 800, 940)
    css = TEXT_CSS.format(p="b1", top=HEAD_TOP, lh=1.04, kicker=KICKER, red=RED, label=LABEL, muted=MUTED, ink=INK)
    css += f'''        .b1-zeile {{
          font-size: {hook_size}px;
        }}
        .b1-zeile.akzent {{
          color: {RED};
        }}'''
    vs = [{"id": "zeile1", "type": "string", "label": "Einstieg, Zeile 1", "default": TEXT["hook"][0]},
          {"id": "zeile2", "type": "string", "label": "Einstieg, Zeile 2", "default": TEXT["hook"][1]}]
    body = f'''        <div class="b1-kopf">
          <span class="b1-zeile" id="b1-z1" data-var-text="zeile1">{TEXT["hook"][0]}</span>
          <span class="b1-zeile akzent" id="b1-z2" data-var-text="zeile2">{TEXT["hook"][1]}</span>
        </div>
'''
    b = BEATS[0]
    js = [blur_out("#b1-z1", b["dur"] - 0.2), blur_out("#b1-z2", b["dur"] - 0.15)]
    files["compositions/b1-hook.html"] = (SCENE_HEAD.format(vars=variables(vs), id="b1-hook", ink=INK, css=css, W=W, H=H, dur=b["dur"])
                                          + body + SCENE_TAIL.format(js="\n".join(js), id="b1-hook"))

    # --- b2–b4: Standorte -----------------------------------------------------------------------
    for b in BEATS[1:4]:
        p = b["id"].split("-")[0]
        kicker, ort = TEXT[b["text"]]
        lines = head_lines(measure, ort)
        cam = cams[b["id"]]
        obs = common_obstacles(cam, rhein_base, marker_px(cam))
        obs.append(box(0, 0, W, head_bottom(len(lines)) + 16))
        placed = place_names(measure, cam, base_areas, b["names"], b["office"], obs)
        report.append((b["id"], placed))
        css = TEXT_CSS.format(p=p, top=HEAD_TOP, lh=HEAD_LH, kicker=KICKER, red=RED, label=LABEL, muted=MUTED, ink=INK)
        css += f'''        .{p}-zeile {{
          font-size: {HEAD}px;
        }}'''
        vs = [{"id": "dach", "type": "string", "label": "Dachzeile", "default": kicker}]
        vs += [{"id": f"ort{i + 1}", "type": "string", "label": f"Ort, Zeile {i + 1}", "default": ln} for i, ln in enumerate(lines)]
        heads = "\n".join(f'          <span class="{p}-zeile" id="{p}-z{i + 1}" data-var-text="ort{i + 1}">{ln}</span>' for i, ln in enumerate(lines))
        body = f'''        <div class="{p}-kopf">
          <span class="{p}-dach" id="{p}-dach" data-var-text="dach">{kicker}</span>
{heads}
        </div>
{name_divs(p, placed)}
'''
        t_head = b["move"] * 0.45  # Ortsname steht fest im Bild – er darf schon während der Fahrt kommen
        t_names = b["move"] + 0.05
        t_out = b["dur"] - 0.25
        js = [blur_in(f"#{p}-dach", t_head)]
        js += [blur_in(f"#{p}-z{i + 1}", t_head + 0.07 * (i + 1)) for i in range(len(lines))]
        js += [blur_in(f"#{p}-n{k}", t_names + 0.07 * k) for k in range(len(placed))]
        js += [blur_out(f".{p}-name", t_out - 0.05), blur_out(f"#{p}-dach", t_out), ]
        js += [blur_out(f"#{p}-z{i + 1}", t_out + 0.04 * (i + 1)) for i in range(len(lines))]
        files[f"compositions/{b['id']}.html"] = (SCENE_HEAD.format(vars=variables(vs), id=b["id"], ink=INK, css=css, W=W, H=H, dur=b["dur"])
                                                 + body + SCENE_TAIL.format(js="\n".join(js), id=b["id"]))

    # --- b5: Abschluss --------------------------------------------------------------------------
    b = BEATS[4]
    cam = cams[b["id"]]
    close_size = fit_size(measure, TEXT["close"], 66, 800, 940)
    lh = LOGO_W * 100 / 452
    obs = common_obstacles(cam, rhein_base, marker_px(cam))
    obs += [box(0, 0, W, HEAD_TOP + 2 * close_size * 1.1 + 20), box(0, LOGO_TOP - 20, W, H)]
    placed = place_names(measure, cam, base_areas, [], None, obs, extra_office=dict(zip(OFFICE_NAMES, marker_px(cam))))
    report.append((b["id"], placed))
    css = TEXT_CSS.format(p="b5", top=HEAD_TOP, lh=1.1, kicker=KICKER, red=RED, label=OFFICE_LABEL, muted=MUTED, ink=INK)
    css += f'''        .b5-zeile {{
          font-size: {close_size}px;
        }}
        .b5-zeile.akzent {{
          color: {RED};
        }}
        .b5-logo {{
          position: absolute;
          left: {(W - LOGO_W) / 2:.0f}px;
          top: {LOGO_TOP}px;
          width: {LOGO_W}px;
          height: {lh:.1f}px;
        }}
        .b5-logo svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}
        .word {{
          font-family: "Montserrat", sans-serif;
          fill: {INK};
        }}
        .b5-adresse {{
          position: absolute;
          left: 60px;
          right: 60px;
          top: {URL_TOP}px;
          text-align: center;
          font-size: 40px;
          font-weight: 600;
          line-height: 1.15;
          letter-spacing: -0.01em;
          color: {INK};
        }}'''
    vs = [{"id": "zeile1", "type": "string", "label": "Abschluss, Zeile 1", "default": TEXT["close"][0]},
          {"id": "zeile2", "type": "string", "label": "Abschluss, Zeile 2", "default": TEXT["close"][1]},
          {"id": "adresse", "type": "string", "label": "Adresse", "default": TEXT["url"]}]
    logo = build_maps.LOGO_SVG.replace('id="k-', 'id="b5-k-').replace("url(#k-", "url(#b5-k-")
    body = f'''        <div class="b5-kopf">
          <span class="b5-zeile akzent" id="b5-z1" data-var-text="zeile1">{TEXT["close"][0]}</span>
          <span class="b5-zeile" id="b5-z2" data-var-text="zeile2">{TEXT["close"][1]}</span>
        </div>
{name_divs("b5", placed)}
        <div class="b5-logo" id="b5-logo">
        {logo}
        </div>
        <div class="b5-adresse" id="b5-adresse" data-var-text="adresse">{TEXT["url"]}</div>
'''
    t0 = b["move"]
    js = [blur_in("#b5-z1", t0 - 0.45), blur_in("#b5-z2", t0 - 0.38)]
    js += [blur_in(f"#b5-n{k}", t0 + 0.05 + 0.07 * k) for k in range(len(placed))]
    js.append('          tl.fromTo("#b5-logo", { opacity: 0, scale: 0.94, filter: "blur(8px)" }, '
              f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {t0 + 0.3:.2f});')
    js.append(blur_in("#b5-adresse", t0 + 0.6, 0.18))
    files["compositions/b5-abschluss.html"] = (SCENE_HEAD.format(vars=variables(vs), id="b5-abschluss", ink=INK, css=css, W=W, H=H, dur=b["dur"])
                                               + body + SCENE_TAIL.format(js="\n".join(js), id="b5-abschluss"))

    # --- index.html -----------------------------------------------------------------------------
    hosts = [f'      <div id="karte" data-composition-id="karte" data-composition-src="compositions/karte.html" data-start="0" data-duration="{DURATION}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>']
    for b in BEATS:
        hosts.append(f'      <div id="{b["id"]}" data-composition-id="{b["id"]}" data-composition-src="compositions/{b["id"]}.html" data-start="{b["start"]}" data-duration="{b["dur"]}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
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
      KNIGGE Immobilien – Instagram-Reel „Drei Standorte. Eine Region." (1080×1920, 15 s, ohne Ton)
      erzeugt von tools/build_reel.py – Texte lassen sich in Studio über die Variablen der Szenen ändern
    -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
    for rel, html in files.items():
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(html)
        print("geschrieben:", rel)
    print(f"Einstieg {hook_size} px, Abschluss {close_size} px")
    for k, c in cams.items():
        print(f"  Kamera {k}: Mitte ({c.cx:.0f}, {c.cy:.0f}), Zoom {c.z:.2f}")
    for bid, placed in report:
        bad = [(it["text"], r) for it, r in placed if r["status"] != "ok"]
        print(f"  {bid}: {len(placed)} Namen" + ("" if not bad else " – " + ", ".join(
            f"{t} {r['status']} ({r['size']} px)" for t, r in bad)))


if __name__ == "__main__":
    build()
