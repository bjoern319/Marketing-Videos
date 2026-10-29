#!/usr/bin/env python3
"""Erzeugt das Halloween-Reel „Hausgeist Herbert“ (1080×1920, 28 s, 30 fps): index.html und
compositions/*.html.

Geschichte (STORYLINES.md A, SPEC.md): Hausgeist Herbert springt bei Vollmond aus dem Fenster – „BUH!“
– aber niemand ist da. „Seit die Kinder ausgezogen sind, erschreck ich nur noch Spinnen.“ Viel zu viel
Haus für einen Geist. Dann kommt KNIGGE: Nacht wird Tag, VERKAUFT, eine Familie zieht ein – und ein Kind
im Bettlaken erschreckt Herbert. „Der Spuk ist vorbei.“ Endkarte mit kostenloser Wertermittlung.

Aufbau: `welt` (Spur 0, ganze Länge) enthält Himmel, Haus, Garten, die Kamera und die Figuren; die
Szenen s1–s5 (Spur 1) tragen Titel, Sprechblasen und die Endkarte. Musik und Geräusche liegen im
index.html (Musik: tools/make_audio.py).

Kamera: Weltpunkt (cx, cy) liegt mit Zoom z in der Bildmitte (540, 960). Figuren leben im Bild (nicht
in der Kamera); wo sie an einem Fenster oder der Tür stehen, wird ihre Bildlage aus der Kamera
berechnet und gleichzeitig mit ihr bewegt.

Ändern: Texte in TEXT, Zeiten in den Konstanten der Szenen; dann `python3 tools/build_reel.py` und
`npm run check`.
"""
import math
import os

from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF = os.path.join(ROOT, "assets", "fonts", "red-hat-display.ttf")
W, H, FPS, DURATION = 1080, 1920, 30, 28.0
INK, RED, CREAM = "#323c44", "#ca2c35", "#f3ecd8"
EYE = "#1d2328"

TEXT = {
    "hook": ["Dieses Haus", "spukt."],
    "buh": "BUH!",
    "blase1": ["Seit die Kinder", "ausgezogen sind …"],
    "blase2": ["… erschreck ich nur", "noch Spinnen."],
    "zu_gross": ["Viel zu viel Haus", "für einen Geist."],
    "neu": ["Zeit für", "neues Leben."],
    "verkauft": "VERKAUFT",
    "kind_buh": "BUH!",
    "aaah": "AAAH!",
    "vorbei": ["Der Spuk", "ist vorbei."],
    "ende": ["Jedes Haus verdient", "ein zweites Leben."],
    "cta": "Kostenlose Wertermittlung",
    "url": "knigge-immobilien.de",
}

SCENES = [
    {"id": "s1-spuk", "start": 0.0, "dur": 4.0},
    {"id": "s2-allein", "start": 4.0, "dur": 6.0},
    {"id": "s3-zu-gross", "start": 10.0, "dur": 3.0},
    {"id": "s4-neues-leben", "start": 13.0, "dur": 9.0},
    {"id": "s5-ende", "start": 22.0, "dur": 6.0},
]
BY_ID = {s["id"]: s for s in SCENES}

# Kamera-Einstellungen: (Weltpunkt x, Weltpunkt y, Zoom)
CAM = {
    "W": (540, 960, 1.0),    # ganzes Haus
    "P": (700, 1000, 1.35),  # Fahrt ans Spukfenster oben rechts
    "M": (560, 980, 1.12),   # Herberts Monolog
    "Z": (540, 1000, 0.92),  # „viel zu viel Haus“
    "E": (540, 840, 0.78),   # Endkarte: Haus tiefer, Platz für Text
    "T": (520, 1230, 1.65),  # an der Tür: Kind erschreckt Herbert
}

# Farben Nacht → Tag
PAL = {
    "himmel": ("#26303a", "#e6f1f6"), "huegel": ("#1b2328", "#8cbf6e"), "weg": ("#2a3238", "#d9c7a8"),
    "wand": ("#3b474f", "#f4ede1"), "dach": ("#1c2329", "#a9443c"), "dachkante": ("#12181c", "#8a342e"),
    "kamin": ("#2a3238", "#7b5446"), "fenster": ("#161c20", "#ffd98a"), "rahmen": ("#2a3238", "#f7f2e8"),
    "laden": ("#2a343b", "#3f6e5b"), "tuer": ("#20282d", RED), "knauf": ("#7d8378", "#f2c14e"),
    "zaun": ("#2c353b", "#f7f2e8"), "baum": ("#12191d", "#6e4b36"), "stufe": ("#252d33", "#cdbfa8"),
}

# Fenster (links, oben) – 120 × 130
LATTEN = []  # Schräglage der Zaunlatten bei Nacht (Grad), gefüllt von world_svg()
WINDOWS = {"OL": (300, 965), "OR": (660, 965), "UL": (300, 1175), "UR": (660, 1175)}
WIN_W, WIN_H = 120, 130


class Measure:
    def __init__(self):
        self.fonts = {}

    def width(self, text, size, weight, track=0.0):
        key = (size, weight)
        if key not in self.fonts:
            f = ImageFont.truetype(TTF, size, layout_engine=ImageFont.Layout.RAQM)
            f.set_variation_by_axes([weight])
            self.fonts[key] = f
        return self.fonts[key].getlength(text) + track * size * len(text)


M = Measure()


def cam_screen(state, x, y):
    cx, cy, z = CAM[state]
    return ((x - cx) * z + 540, (y - cy) * z + 960)


def cam_js(state):
    """GSAP-Werte für #welt-kamera (transform-origin 0 0)."""
    cx, cy, z = CAM[state]
    return f"x: {540 - cx * z:.2f}, y: {960 - cy * z:.2f}, scale: {z}"


# ------------------------------------------------------------------------------------------------
# HTML-Gerüst
# ------------------------------------------------------------------------------------------------
FONT_FACE = '''        @font-face {
          font-family: "Red Hat Display";
          src: url("assets/fonts/red-hat-display.woff2") format("woff2");
          font-weight: 300 900;
          font-style: normal;
          font-display: block;
        }'''

SCENE_HEAD = '''<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template id="{id}-template">
      <style>
{font}
        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          font-family: "Red Hat Display", sans-serif;
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


def scene(sid, dur, css, body, js):
    return (SCENE_HEAD.format(id=sid, font=FONT_FACE, ink=INK, css=css, W=W, H=H, dur=dur) + body
            + SCENE_TAIL.format(js="\n".join("          " + j for j in js), id=sid))


def words(p, k, line):
    return " ".join(f'<span class="{p}-w" id="{p}-l{k}w{i}">{w}</span>' for i, w in enumerate(line.split(" ")))


def word_ids(p, lines):
    return [f"#{p}-l{k}w{i}" for k, line in enumerate(lines) for i, _ in enumerate(line.split(" "))]


def blur_in(sel, t, dur=0.16):
    return (f'tl.fromTo("{sel}", {{ opacity: 0, filter: "blur(10px)" }}, '
            f'{{ opacity: 1, filter: "blur(0px)", duration: {dur}, ease: "power4.out" }}, {t:.3f});')


def blur_out(sels, t, dur=0.2):
    arr = ", ".join(f'"{s}"' for s in sels)
    return f'tl.to([{arr}], {{ opacity: 0, filter: "blur(10px)", duration: {dur}, ease: "power2.in" }}, {t:.3f});'


def title_css(p, size, color, top=226):
    return f'''        .{p}-titel {{
          position: absolute;
          left: 72px;
          right: 60px;
          top: {top}px;
          font-size: {size}px;
          font-weight: 900;
          letter-spacing: -0.02em;
          line-height: 1.02;
          color: {color};
        }}
        .{p}-zeile {{
          display: block;
          white-space: nowrap;
        }}
        .{p}-zeile.rot {{
          color: {RED};
        }}
        .{p}-w {{
          display: inline-block;
        }}'''


def title_html(p, lines, red=()):
    return (f'        <div class="{p}-titel">\n'
            + "\n".join(f'          <span class="{p}-zeile{" rot" if k in red else ""}">{words(p, k, line)}</span>'
                        for k, line in enumerate(lines))
            + "\n        </div>")


def title_in(p, lines, t0, step=0.08):
    return [blur_in(sel, t0 + step * i) for i, sel in enumerate(word_ids(p, lines))]


def bubble_css(p):
    return f'''        .{p}-blase {{
          position: absolute;
          background: #ffffff;
          border-radius: 30px;
          padding: 26px 34px 30px;
          box-shadow: 0 14px 30px rgba(10, 14, 18, 0.28);
          color: {INK};
          font-size: 46px;
          font-weight: 700;
          line-height: 1.16;
        }}
        .{p}-blase span {{
          display: block;
          white-space: nowrap;
        }}
        .{p}-blase svg {{
          position: absolute;
          overflow: visible;
        }}'''


def bubble_html(p, bid, left, top, lines, tail, size=46, pad=(26, 34, 30), weight=700, color=None, cls=""):
    """Sprechblase; tail = Spitze (x, y) relativ zur Blase (links oben), der Schwanz sitzt am unteren Rand."""
    w = max(M.width(l, size, weight) for l in lines) + 2 * pad[1]
    h = pad[0] + pad[2] + len(lines) * size * 1.16
    tx, ty = tail
    bx = min(max(tx + 40, 60), w - 60)
    svg = (f'<svg width="1" height="1" style="left: 0; top: 0" aria-hidden="true">'
           f'<path d="M{bx - 26:.0f} {h - 6:.0f} L{tx} {ty} L{bx + 26:.0f} {h - 6:.0f} Z" fill="#ffffff" /></svg>')
    style = f"left: {left}px; top: {top}px; width: {w:.0f}px; padding: {pad[0]}px {pad[1]}px {pad[2]}px; font-size: {size}px; font-weight: {weight}"
    if color:
        style += f"; color: {color}"
    return (f'        <div class="{p}-blase{cls}" id="{bid}" style="{style}">'
            + "".join(f"<span>{l}</span>" for l in lines) + svg + "</div>")


def pop_in(sel, t, origin):
    return (f'tl.fromTo("{sel}", {{ scale: 0.6, opacity: 0, transformOrigin: "{origin}" }}, '
            f'{{ scale: 1, opacity: 1, duration: 0.27, ease: "back.out(1.8)" }}, {t:.3f});')


# ------------------------------------------------------------------------------------------------
# Welt: Himmel, Haus, Garten (Weltkoordinaten = Bild bei Kamera W)
# ------------------------------------------------------------------------------------------------
def tint(key):
    return f'class="t-{key}" fill="{PAL[key][0]}"'


def world_svg():
    out = []
    a = out.append
    a(f'<rect x="-600" y="-900" width="2280" height="3600" {tint("himmel")} />')
    # Sterne (fest verteilt)
    stars = [(80, 210), (190, 330), (320, 180), (430, 420), (610, 260), (960, 240), (1010, 520), (140, 560),
             (520, 120), (700, 560), (880, 640), (260, 680), (40, 760), (1040, 760), (380, 600), (590, 690)]
    a('<g id="sterne">' + "".join(f'<circle cx="{x}" cy="{y}" r="{2.2 + (i % 3) * 0.8:.1f}" fill="#e8e0c4" />'
                                   for i, (x, y) in enumerate(stars)) + "</g>")
    # Mond und Sonne (die Sonne geht hinter dem Dach auf)
    a('<g id="mond"><circle cx="860" cy="560" r="88" fill="#efe6c8" /><circle cx="834" cy="542" r="15" fill="#e2d7b3" />'
      '<circle cx="886" cy="588" r="11" fill="#e2d7b3" /><circle cx="860" cy="610" r="7" fill="#e2d7b3" /></g>')
    a('<circle id="sonne" cx="900" cy="620" r="84" fill="#ffd166" />')
    # Fledermäuse
    bat = ("M0 0 C6 -9 14 -11 20 -4 C24 -13 30 -13 32 -6 C34 -13 40 -13 44 -4 C50 -11 58 -9 64 0 "
           "C56 -2 50 2 46 9 C40 4 36 6 32 13 C28 6 24 4 18 9 C14 2 8 -2 0 0 Z")
    for k in range(3):
        a(f'<g id="fm{k}"><path d="{bat}" fill="#11171b" transform="translate(-32 0)" /></g>')
    # Hügel und Weg
    a(f'<path d="M-600 1398 C -100 1390, 300 1372, 700 1382 C 900 1386, 1100 1372, 1700 1360 L1700 2700 L-600 2700 Z" {tint("huegel")} />')
    a(f'<path d="M500 1400 H580 L680 2700 H400 Z" {tint("weg")} />')
    # Baum links: Stamm und kahle Äste; das Laub kommt am Tag
    branches = ["M150 1402 C152 1300 140 1200 146 1078", "M146 1170 C112 1132 84 1110 48 1068",
                "M148 1138 C182 1098 212 1086 248 1046", "M145 1092 C132 1046 120 1012 98 982",
                "M147 1104 C162 1056 178 1024 204 994", "M100 984 C88 962 84 946 70 930",
                "M204 994 C214 970 228 958 244 944"]
    widths = [22, 10, 10, 8, 8, 5, 5]
    a('<g id="baum">' + "".join(f'<path d="{d}" class="t-baum-s" stroke="{PAL["baum"][0]}" stroke-width="{w}" '
                                 f'stroke-linecap="round" fill="none" />' for d, w in zip(branches, widths)) + "</g>")
    leaves = [(70, 1040, 46, "#e9a23b"), (130, 990, 58, "#d9622b"), (200, 1010, 52, "#f2c14e"), (250, 1060, 40, "#e9a23b"),
              (100, 1090, 44, "#f2c14e"), (175, 1080, 48, "#e9a23b"), (60, 960, 36, "#d9622b"), (225, 950, 40, "#d9622b"),
              (150, 930, 44, "#e9a23b")]
    a('<g id="laub">' + "".join(f'<circle class="blatt" cx="{x}" cy="{y}" r="{r}" fill="{c}" />' for x, y, r, c in leaves) + "</g>")
    # Haus
    a(f'<rect x="250" y="905" width="580" height="497" {tint("wand")} />')
    a('<g id="risse" stroke="#2c363d" stroke-width="3" fill="none" stroke-linecap="round">'
      '<path d="M280 1120 l18 26 l-10 20 l16 30" /><path d="M790 1010 l-14 22 l8 16 l-12 28" /><path d="M620 1340 l12 -20 l-6 -18" /></g>')
    a('<g opacity="0.08" stroke="#000" stroke-width="2"><path d="M250 1000 H830 M250 1100 H830 M250 1150 H830 M250 1340 H830" /></g>')
    a(f'<polygon points="205,922 540,640 875,922" {tint("dach")} />')
    a(f'<path d="M198 926 L540 634 L882 926" class="t-dachkante-s" stroke="{PAL["dachkante"][0]}" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round" />')
    a(f'<rect x="680" y="690" width="60" height="120" {tint("kamin")} /><rect x="672" y="680" width="76" height="16" {tint("kamin")} />')
    a(f'<circle cx="540" cy="820" r="40" {tint("fenster")} /><circle cx="540" cy="820" r="40" fill="none" class="t-rahmen-s" stroke="{PAL["rahmen"][0]}" stroke-width="8" />'
      f'<path d="M540 780 V860 M500 820 H580" class="t-rahmen-s" stroke="{PAL["rahmen"][0]}" stroke-width="6" />')
    for key, (x, y) in WINDOWS.items():
        a(f'<rect x="{x - 48}" y="{y}" width="44" height="{WIN_H}" {tint("laden")} id="laden-{key}-l" />')
        a(f'<rect x="{x + WIN_W + 4}" y="{y}" width="44" height="{WIN_H}" {tint("laden")} id="laden-{key}-r" />')
        a(f'<rect x="{x}" y="{y}" width="{WIN_W}" height="{WIN_H}" {tint("fenster")} />')
        if key == "OR":
            a(f'<rect id="spuklicht" x="{x}" y="{y}" width="{WIN_W}" height="{WIN_H}" fill="#d8c27a" opacity="0.35" />')
        if key == "OL":
            # Familie (Silhouetten), steigt am Tag aus dem Fensterbrett auf
            a(f'<clipPath id="fenster-ol-clip"><rect x="{x}" y="{y}" width="{WIN_W}" height="{WIN_H}" /></clipPath>'
              f'<g clip-path="url(#fenster-ol-clip)"><g id="familie">'
              f'<circle cx="{x + 36}" cy="{y + 58}" r="15" fill="#3a464e" /><path d="M{x + 12} {y + 132} C{x + 12} {y + 92} {x + 60} {y + 92} {x + 60} {y + 132} Z" fill="#3a464e" />'
              f'<circle cx="{x + 84}" cy="{y + 52}" r="16" fill="#46525a" /><path d="M{x + 58} {y + 132} C{x + 58} {y + 88} {x + 110} {y + 88} {x + 110} {y + 132} Z" fill="#46525a" />'
              f'<rect id="familie-arm" x="{x + 102}" y="{y + 48}" width="10" height="40" rx="5" fill="#46525a" /></g></g>')
        a(f'<rect x="{x}" y="{y}" width="{WIN_W}" height="{WIN_H}" fill="none" class="t-rahmen-s" stroke="{PAL["rahmen"][0]}" stroke-width="8" />'
          f'<path d="M{x + WIN_W / 2} {y} V{y + WIN_H} M{x} {y + WIN_H / 2} H{x + WIN_W}" class="t-rahmen-s" stroke="{PAL["rahmen"][0]}" stroke-width="6" />')
    # Bretter vor dem Fenster unten links (nachts)
    ux, uy = WINDOWS["UL"]
    a(f'<g id="bretter"><rect x="{ux - 26}" y="{uy + 48}" width="172" height="22" rx="3" fill="#5c4636" transform="rotate(18 {ux + 60} {uy + 59})" />'
      f'<rect x="{ux - 26}" y="{uy + 62}" width="172" height="22" rx="3" fill="#6b5240" transform="rotate(-16 {ux + 60} {uy + 73})" /></g>')
    # Tür, Knauf, Stufe
    a(f'<rect x="480" y="1205" width="120" height="196" {tint("tuer")} />'
      f'<rect x="480" y="1205" width="120" height="196" fill="none" class="t-rahmen-s" stroke="{PAL["rahmen"][0]}" stroke-width="8" />'
      f'<circle cx="582" cy="1310" r="7" {tint("knauf")} /><rect x="458" y="1398" width="164" height="14" {tint("stufe")} />')
    # Spinnweben (nachts)
    webs = []
    for (cx, cy, r, a0, a1) in [(252, 924, 92, 0, 90), (600, 1207, 70, 90, 180)]:
        rays = [a0 + (a1 - a0) * k / 4 for k in range(5)]
        pts = lambda rr: [(cx + rr * math.cos(math.radians(t)), cy + rr * math.sin(math.radians(t))) for t in rays]
        d = "".join(f"M{cx} {cy} L{x:.1f} {y:.1f} " for x, y in pts(r))
        for rr in (r * 0.35, r * 0.62, r * 0.9):
            ps = pts(rr)
            d += f"M{ps[0][0]:.1f} {ps[0][1]:.1f} " + "".join(f"Q{(ps[i][0] + ps[i + 1][0]) / 2 + (cx - (ps[i][0] + ps[i + 1][0]) / 2) * 0.12:.1f} "
                                                               f"{(ps[i][1] + ps[i + 1][1]) / 2 + (cy - (ps[i][1] + ps[i + 1][1]) / 2) * 0.12:.1f} "
                                                               f"{ps[i + 1][0]:.1f} {ps[i + 1][1]:.1f} " for i in range(4))
        webs.append(f'<path d="{d}" stroke="#c9d1d6" stroke-width="2" fill="none" opacity="0.8" />')
    a('<g id="spinnweben">' + "".join(webs) + "</g>")
    # Kürbis: nachts böse, tags freundlich
    a('<g id="kuerbis"><ellipse cx="410" cy="1366" rx="48" ry="38" fill="#e07b2a" />'
      '<path d="M390 1332 C380 1352 380 1384 392 1402 M430 1332 C440 1352 440 1384 428 1402" stroke="#c9661f" stroke-width="4" fill="none" />'
      '<rect x="404" y="1318" width="12" height="18" rx="4" fill="#5d7a3a" />'
      '<g id="kuerbis-boese" fill="#ffcf5a"><path d="M384 1352 l12 -14 l8 16 Z" /><path d="M418 1354 l10 -16 l10 14 Z" />'
      '<path d="M380 1374 l10 6 l8 -6 l8 6 l8 -6 l8 6 l8 -6 l8 6 l4 -6 l-4 16 h-56 Z" /></g>'
      '<g id="kuerbis-froh" opacity="0"><circle cx="394" cy="1356" r="6" fill="#5b3a1d" /><circle cx="426" cy="1356" r="6" fill="#5b3a1d" />'
      '<path d="M390 1374 Q410 1392 430 1374" stroke="#5b3a1d" stroke-width="6" fill="none" stroke-linecap="round" /></g></g>')
    # Zaun (Latten nachts schief)
    pickets = []
    LATTEN.clear()
    k = 0
    for x in range(26, 1060, 52):
        if 420 < x < 640:
            continue
        rot = [0, -9, 6, -14, 3, 11, -5, 8][k % 8]
        LATTEN.append(rot)
        pickets.append(f'<path id="latte{k}" class="latte t-zaun" fill="{PAL["zaun"][0]}" '
                       f'd="M{x} 1462 V1400 L{x + 15} 1384 L{x + 30} 1400 V1462 Z" />')
        k += 1
    a(f'<g id="zaun"><rect x="-200" y="1412" width="625" height="10" {tint("zaun")} /><rect x="640" y="1412" width="640" height="10" {tint("zaun")} />'
      + "".join(pickets) + "</g>")
    # Blumen (tags)
    flowers = [(270, 1392, "#ca2c35"), (300, 1395, "#f2c14e"), (335, 1390, "#ffffff"), (640, 1393, "#e9a23b"), (680, 1390, "#ca2c35"),
               (720, 1394, "#ffffff"), (760, 1391, "#f2c14e"), (800, 1394, "#ca2c35"), (60, 1440, "#ca2c35"), (330, 1446, "#f2c14e"),
               (720, 1450, "#ffffff"), (960, 1440, "#ca2c35"), (1010, 1452, "#f2c14e")]
    a('<g id="blumen">' + "".join(f'<g class="blume"><path d="M{x} {y} V{y + 26}" stroke="#4f8a3c" stroke-width="4" />'
                                   f'<circle cx="{x}" cy="{y}" r="11" fill="{c}" /><circle cx="{x}" cy="{y}" r="4" fill="#f7d36a" /></g>'
                                   for x, y, c in flowers) + "</g>")
    # Umzugskartons (tags)
    a('<g id="kartons"><rect x="618" y="1338" width="92" height="64" rx="4" fill="#c99a5b" /><path d="M664 1338 V1402" stroke="#b07f44" stroke-width="6" />'
      '<rect x="640" y="1292" width="70" height="48" rx="4" fill="#d6a868" /><path d="M675 1292 V1340" stroke="#b07f44" stroke-width="5" /></g>')
    return "\n".join(out)


def sign_html():
    """Gartenschild mit KNIGGE-Logo (Weltkoordinaten), VERKAUFT-Band liegt darüber."""
    logo = ('<svg viewBox="0 0 452 100" width="190" height="42" aria-hidden="true"><defs>'
            '<linearGradient id="sg-a" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="48.9" y2="39.6"><stop offset="0" stop-color="#5e0f18" /><stop offset="0.56" stop-color="#a4222b" /><stop offset="0.93" stop-color="#ca2c35" /></linearGradient>'
            '<linearGradient id="sg-r" gradientUnits="userSpaceOnUse" x1="47.5" y1="40.2" x2="100" y2="0"><stop offset="0" stop-color="#4a0a13" /><stop offset="1" stop-color="#b0252e" /></linearGradient>'
            '<linearGradient id="sg-b" gradientUnits="userSpaceOnUse" x1="0" y1="100" x2="100" y2="100"><stop offset="0" stop-color="#480a12" /><stop offset="0.5" stop-color="#a2222b" /><stop offset="0.85" stop-color="#ca2c35" /></linearGradient></defs>'
            '<path d="M0 0 H79.5 L0 100 Z" fill="url(#sg-a)" /><path d="M79.5 0 H100 V100 L47.5 40.2 Z" fill="url(#sg-r)" /><path d="M0 100 L47.5 40.2 L100 100 Z" fill="url(#sg-b)" />'
            '<text x="125.2" y="53" font-size="77" font-weight="700" textLength="328.5" lengthAdjust="spacing" fill="#323c44" font-family="Montserrat, sans-serif">KNIGGE</text>'
            '<text x="125.5" y="100" font-size="44.3" font-weight="400" textLength="330.5" lengthAdjust="spacing" fill="#323c44" font-family="Montserrat, sans-serif">IMMOBILIEN</text></svg>')
    return f'''          <div id="schild" class="welt-schild">
            <div class="welt-schild-pfosten"></div>
            <div class="welt-schild-brett" data-layout-ignore>{logo}</div>
            <div class="welt-band" id="schild-band">{TEXT["verkauft"]}</div>
          </div>'''


# ------------------------------------------------------------------------------------------------
# Figuren
# ------------------------------------------------------------------------------------------------
def herbert_svg():
    body = ("M100 12 C150 12 176 52 176 104 L176 198 Q163 224 148 204 Q133 228 117 204 Q100 230 84 204 "
            "Q68 228 53 204 Q38 224 24 198 L24 104 C24 52 50 12 100 12 Z")
    shade = "M150 30 C170 52 176 80 176 104 L176 198 Q163 224 148 204 C156 150 160 80 150 30 Z"
    return f'''<svg viewBox="0 0 200 240" aria-hidden="true">
              <g id="herbert-koffer" opacity="0"><rect x="150" y="150" width="58" height="44" rx="6" fill="#a9443c" /><path d="M166 150 v-10 h26 v10" stroke="#7a2f2a" stroke-width="5" fill="none" /><rect x="150" y="166" width="58" height="5" fill="#7a2f2a" /></g>
              <path id="herbert-arm-l" d="M30 112 Q2 118 6 140 Q12 154 34 142" fill="#f8f5ee" />
              <path id="herbert-arm-r" d="M170 112 Q198 118 194 140 Q188 154 166 142" fill="#f8f5ee" />
              <path d="{body}" fill="#f8f5ee" />
              <path d="{shade}" fill="#e5dfd1" />
              <ellipse cx="64" cy="118" rx="12" ry="7" fill="#f2b8b2" opacity="0.8" />
              <ellipse cx="136" cy="118" rx="12" ry="7" fill="#f2b8b2" opacity="0.8" />
              <g id="herbert-augen"><g id="herbert-pupillen">
                <ellipse cx="76" cy="86" rx="13" ry="19" fill="{EYE}" /><ellipse cx="124" cy="86" rx="13" ry="19" fill="{EYE}" />
                <circle cx="80" cy="78" r="4.5" fill="#ffffff" /><circle cx="128" cy="78" r="4.5" fill="#ffffff" /></g></g>
              <path id="herbert-brauen" d="M58 70 L88 60 M142 70 L112 60" stroke="{EYE}" stroke-width="5" stroke-linecap="round" opacity="0" />
              <ellipse id="herbert-mund-o" cx="100" cy="134" rx="15" ry="19" fill="{EYE}" />
              <path id="herbert-mund-flach" d="M86 134 Q100 130 114 134" stroke="{EYE}" stroke-width="6" stroke-linecap="round" fill="none" opacity="0" />
              <path id="herbert-mund-lachen" d="M80 126 Q100 156 120 126 Z" fill="{EYE}" opacity="0" />
              <ellipse id="herbert-mund-schrei" cx="100" cy="140" rx="22" ry="30" fill="{EYE}" opacity="0" />
            </svg>'''


def kind_svg():
    sheet = ("M80 10 C122 10 140 42 142 86 L150 174 Q132 186 114 176 Q97 188 80 178 Q63 188 46 176 Q28 186 10 174 "
             "L18 86 C20 42 38 10 80 10 Z")
    return f'''<svg viewBox="0 0 160 214" aria-hidden="true">
              <g id="kind-schuh-l"><ellipse cx="58" cy="196" rx="20" ry="11" fill="{RED}" /><rect x="38" y="200" width="40" height="6" rx="3" fill="#ffffff" /></g>
              <g id="kind-schuh-r"><ellipse cx="102" cy="196" rx="20" ry="11" fill="{RED}" /><rect x="82" y="200" width="40" height="6" rx="3" fill="#ffffff" /></g>
              <path d="{sheet}" fill="#ffffff" stroke="#d8d2c4" stroke-width="2" />
              <path d="M48 120 C56 140 52 160 46 176 M112 120 C104 142 110 160 114 176" stroke="#e4ded2" stroke-width="3" fill="none" />
              <ellipse cx="62" cy="72" rx="10" ry="13" fill="{EYE}" /><ellipse cx="98" cy="72" rx="10" ry="13" fill="{EYE}" />
            </svg>'''


def spinne_svg():
    legs = []
    for side in (-1, 1):
        for k, (ang, kn) in enumerate([(-30, 30), (-8, 36), (12, 36), (32, 30)]):
            x1, y1 = side * 16, 6 + k * 4
            kx, ky = side * (16 + kn), y1 - 18 + k * 6
            fx, fy = side * (22 + kn + 10), y1 + 18 + k * 7
            legs.append(f'<path d="M{x1} {y1} Q{kx} {ky} {fx} {fy}" stroke="{EYE}" stroke-width="5" fill="none" stroke-linecap="round" />')
    return f'''<svg viewBox="-80 -60 160 120" aria-hidden="true">
              <path d="M0 -2600 V-26" stroke="#aab2b7" stroke-width="2" />
              <g id="spinne-beine">{"".join(legs)}</g>
              <ellipse cx="0" cy="12" rx="22" ry="20" fill="{EYE}" />
              <circle cx="0" cy="-14" r="13" fill="{EYE}" />
              <circle cx="-5" cy="-15" r="4.5" fill="#ffffff" /><circle cx="5" cy="-15" r="4.5" fill="#ffffff" />
              <rect x="-11" y="-21" width="22" height="6" fill="{EYE}" />
            </svg>'''


# ------------------------------------------------------------------------------------------------
# Szenen
# ------------------------------------------------------------------------------------------------
def build():
    files = {}

    # Figuren-Lagen (Bildkoordinaten, Mitte der Figur) zu wichtigen Zeiten
    win_or = (WINDOWS["OR"][0] + WIN_W / 2, WINDOWS["OR"][1] + WIN_H / 2)
    win_ol = (WINDOWS["OL"][0] + WIN_W / 2, WINDOWS["OL"][1] + WIN_H / 2)
    h_pop0 = cam_screen("P", *win_or)
    h_win_z = cam_screen("Z", *win_ol)
    h_win_w = cam_screen("W", *win_ol)
    door_world = (430, 1262)  # Herbert neben der Tür (Welt bei Kamera W)
    kid_world = (650, 1300)   # Mitte des Kindes
    h_door_e = cam_screen("E", *door_world)
    kid_e = cam_screen("E", *kid_world)
    h_door_t = cam_screen("T", *door_world)
    kid_t = cam_screen("T", *kid_world)
    zt = CAM["T"][2]

    # ---------------------------------------------------------------- welt (ganze Länge)
    css = f'''        #welt-kamera {{
          position: absolute;
          left: 0;
          top: 0;
          width: {W}px;
          height: {H}px;
          transform-origin: 0 0;
        }}
        #welt-svg {{
          position: absolute;
          left: 0;
          top: 0;
          width: {W}px;
          height: {H}px;
          overflow: visible;
        }}
        .welt-schild {{
          position: absolute;
          left: 88px;
          top: 1226px;
          width: 236px;
          height: 250px;
          transform-origin: 50% 100%;
        }}
        .welt-schild-pfosten {{
          position: absolute;
          left: 110px;
          top: 110px;
          width: 16px;
          height: 140px;
          background: #5b4636;
          border-radius: 4px;
        }}
        .welt-schild-brett {{
          position: absolute;
          left: 0;
          top: 0;
          width: 236px;
          height: 120px;
          background: #ffffff;
          border: 6px solid {RED};
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-sizing: border-box;
        }}
        .welt-band {{
          position: absolute;
          left: 6px;
          top: 36px;
          width: 224px;
          height: 54px;
          background: {RED};
          color: #ffffff;
          font-size: 36px;
          font-weight: 900;
          letter-spacing: 0.06em;
          line-height: 54px;
          text-align: center;
          border-radius: 6px;
        }}
        .figur {{
          position: absolute;
          left: 0;
          top: 0;
        }}
        .figur svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}
        #herbert {{
          left: -100px;
          top: -120px;
          width: 200px;
          height: 240px;
        }}
        #kind {{
          left: -80px;
          top: -107px;
          width: 160px;
          height: 214px;
        }}
        #spinne {{
          left: -80px;
          top: -60px;
          width: 160px;
          height: 120px;
        }}
'''
    body = f'''        <div id="welt-kamera" data-layout-allow-overflow>
          <svg id="welt-svg" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
{world_svg()}
          </svg>
{sign_html()}
        </div>
        <div class="figur" id="spinne" data-layout-ignore>{spinne_svg()}</div>
        <div class="figur" id="herbert" data-layout-ignore>{herbert_svg()}</div>
        <div class="figur" id="kind" data-layout-ignore>{kind_svg()}</div>
'''
    js = []
    J = js.append
    # Kamera
    J(f'tl.set("#welt-kamera", {{ {cam_js("W")} }}, 0);')
    for sel, origin in [("#herbert-arm-l", "100% 20%"), ("#herbert-arm-r", "0% 20%"), ("#herbert-augen", "50% 50%"),
                        ("#spinne-beine", "50% 30%"), ("#familie-arm", "50% 90%")]:
        J(f'tl.set("{sel}", {{ transformOrigin: "{origin}" }}, 0);')
    J('tl.set("#laden-OL-l", { rotation: 24, transformOrigin: "100% 0%" }, 0);')
    for k, rot in enumerate(LATTEN):
        J(f'tl.set("#latte{k}", {{ rotation: {rot}, transformOrigin: "50% 100%" }}, 0);')
    J(f'tl.to("#welt-kamera", {{ {cam_js("P")}, duration: 0.95, ease: "power2.in" }}, 1.2);')
    J(f'tl.to("#welt-kamera", {{ {cam_js("M")}, duration: 0.6, ease: "power2.inOut" }}, 4.0);')
    J(f'tl.to("#welt-kamera", {{ {cam_js("Z")}, duration: 0.8, ease: "power2.inOut" }}, 10.0);')
    J(f'tl.to("#welt-kamera", {{ {cam_js("W")}, duration: 0.6, ease: "power2.inOut" }}, 13.0);')
    J(f'tl.to("#welt-kamera", {{ {cam_js("E")}, duration: 0.7, ease: "power2.inOut" }}, 22.0);')
    # Nacht: Fledermäuse, Spuklicht
    for k, (y0, t0) in enumerate([(300, 0.25), (380, 0.55), (250, 0.85)]):
        J(f'tl.fromTo("#fm{k}", {{ x: 1180, y: {y0} }}, {{ x: -140, y: {y0 - 60}, duration: 1.6, ease: "none" }}, {t0});')
        J(f'tl.set("#fm{k}", {{ opacity: 0 }}, {t0 + 1.62:.2f});')
        J(f'tl.fromTo("#fm{k} path", {{ scaleY: 1, transformOrigin: "50% 50%" }}, {{ scaleY: 0.35, duration: 0.12, ease: "sine.inOut", yoyo: true, repeat: 13 }}, {t0});')
    for t, o in [(0.3, 0.7), (0.5, 0.2), (0.62, 0.6), (1.1, 0.25), (1.4, 0.75), (1.9, 0.3), (2.15, 0.9)]:
        J(f'tl.to("#spuklicht", {{ opacity: {o}, duration: 0.05, ease: "none" }}, {t});')
    J('tl.to("#spuklicht", { opacity: 0.4, duration: 0.3, ease: "power1.out" }, 2.6);')

    # Herbert ------------------------------------------------------------
    h = "#herbert"
    J(f'tl.set("{h}", {{ x: {h_pop0[0]:.1f}, y: {h_pop0[1]:.1f}, scale: 0.18, opacity: 0 }}, 0);')
    J(f'tl.set("{h}", {{ opacity: 1 }}, 2.12);')
    J(f'tl.to("{h}", {{ x: 540, y: 1090, scale: 2.1, duration: 0.24, ease: "back.out(2.2)" }}, 2.14);')
    J(f'tl.fromTo("{h} svg", {{ scaleX: 1, scaleY: 1 }}, {{ scaleX: 0.88, scaleY: 1.16, duration: 0.1, ease: "power2.out", transformOrigin: "50% 100%" }}, 2.14);')
    J(f'tl.to("{h} svg", {{ scaleX: 1, scaleY: 1, duration: 0.3, ease: "elastic.out(1, 0.45)" }}, 2.26);')
    J('tl.fromTo("#herbert-arm-l", { rotation: 0 }, { rotation: -55, duration: 0.14, ease: "back.out(2)" }, 2.16);')
    J('tl.fromTo("#herbert-arm-r", { rotation: 0 }, { rotation: 55, duration: 0.14, ease: "back.out(2)" }, 2.19);')
    # niemand da: links, rechts schauen
    J('tl.to("#herbert-pupillen", { x: -9, duration: 0.16, ease: "power2.out" }, 2.85);')
    J('tl.to("#herbert-pupillen", { x: 9, duration: 0.2, ease: "power2.inOut" }, 3.18);')
    J('tl.to("#herbert-pupillen", { x: 0, y: 4, duration: 0.2, ease: "power2.inOut" }, 3.5);')
    # zusammensacken
    J('tl.to("#herbert-arm-l", { rotation: 18, duration: 0.3, ease: "power2.inOut" }, 3.45);')
    J('tl.to("#herbert-arm-r", { rotation: -14, duration: 0.34, ease: "power2.inOut" }, 3.5);')
    J(f'tl.to("{h} svg", {{ scaleY: 0.9, scaleX: 1.05, duration: 0.3, ease: "power2.inOut" }}, 3.5);')
    J('tl.set("#herbert-mund-o", { opacity: 0 }, 3.5);')
    J('tl.set("#herbert-mund-flach", { opacity: 1 }, 3.5);')
    J('tl.to("#herbert-brauen", { opacity: 1, duration: 0.15 }, 3.5);')
    # in den Vordergrund für den Monolog
    J(f'tl.to("{h}", {{ x: 330, y: 1150, scale: 1.9, duration: 0.6, ease: "power2.inOut" }}, 4.0);')
    J(f'tl.to("{h} svg", {{ scaleY: 1, scaleX: 1, duration: 0.4, ease: "power2.out" }}, 4.0);')
    # Schweben (endlich oft)
    J(f'tl.fromTo("{h} svg", {{ y: 0 }}, {{ y: -12, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 3 }}, 4.6);')
    # Sprechen: Mund auf/zu
    for t0 in (4.3, 6.7):
        for i in range(4):
            J(f'tl.set("#herbert-mund-o", {{ opacity: {1 if i % 2 == 0 else 0} }}, {t0 + i * 0.16:.2f});')
            J(f'tl.set("#herbert-mund-flach", {{ opacity: {0 if i % 2 == 0 else 1} }}, {t0 + i * 0.16:.2f});')
    # Spinne: fällt, Herbert „buh“, Spinne zuckt mit den Schultern
    J('tl.fromTo("#spinne", { x: 905, y: -200, scale: 1.6 }, { y: 1010, duration: 0.42, ease: "power2.in" }, 7.3);')
    J('tl.to("#spinne", { y: 990, duration: 0.25, ease: "back.out(3)" }, 7.72);')
    J('tl.to("#herbert-pupillen", { x: 10, y: 0, duration: 0.18, ease: "power2.out" }, 7.5);')
    J(f'tl.to("{h}", {{ rotation: 8, duration: 0.18, ease: "power2.out" }}, 7.75);')
    J('tl.set("#herbert-mund-flach", { opacity: 0 }, 7.78);')
    J('tl.set("#herbert-mund-o", { opacity: 1, scale: 0.6, transformOrigin: "50% 50%" }, 7.78);')
    J('tl.set("#herbert-mund-o", { opacity: 0 }, 8.1);')
    J('tl.set("#herbert-mund-flach", { opacity: 1 }, 8.1);')
    J(f'tl.to("{h}", {{ rotation: 0, duration: 0.3, ease: "power2.inOut" }}, 8.2);')
    J('tl.fromTo("#spinne-beine", { scaleY: 1, y: 0 }, { scaleY: 1.25, y: -8, duration: 0.16, ease: "power2.out" }, 8.3);')
    J('tl.to("#spinne-beine", { scaleY: 1, y: 0, duration: 0.24, ease: "power2.inOut" }, 8.62);')
    J('tl.to("#spinne", { y: -260, duration: 0.6, ease: "power2.in" }, 9.3);')
    # Herbert schwebt winzig ins Fenster, Kamera zieht auf
    J(f'tl.to("{h}", {{ x: {h_win_z[0]:.1f}, y: {h_win_z[1]:.1f}, scale: 0.32, rotation: 0, duration: 0.8, ease: "power2.inOut" }}, 10.0);')
    J('tl.set("#herbert-mund-o", { scale: 1 }, 10.0);')
    # bei Tag folgt er dem Fenster
    J(f'tl.to("{h}", {{ x: {h_win_w[0]:.1f}, y: {h_win_w[1]:.1f}, scale: 0.35, duration: 0.6, ease: "power2.inOut" }}, 13.0);')
    J('tl.to("#herbert-brauen", { opacity: 0, duration: 0.1 }, 13.3);')
    J('tl.set("#herbert-mund-flach", { opacity: 0 }, 13.3);')
    J('tl.set("#herbert-mund-o", { opacity: 1 }, 13.3);')
    J('tl.fromTo("#herbert-augen", { scale: 1 }, { scale: 1.25, duration: 0.15, ease: "back.out(2)" }, 13.3);')
    J('tl.to("#herbert-augen", { scale: 1, duration: 0.3, ease: "power2.out" }, 14.0);')
    J('tl.set("#herbert-mund-o", { opacity: 0 }, 14.0);')
    J('tl.set("#herbert-mund-lachen", { opacity: 1 }, 14.0);')
    # raus zur Tür
    J(f'tl.to("#welt-kamera", {{ {cam_js("T")}, duration: 0.7, ease: "power2.inOut" }}, 15.3);')
    J(f'tl.to("{h}", {{ x: {h_door_t[0]:.1f}, y: {h_door_t[1]:.1f}, scale: {0.62 * zt:.3f}, duration: 0.7, ease: "power2.inOut" }}, 15.3);')
    J('tl.to("#herbert-pupillen", { x: 9, duration: 0.2, ease: "power2.out" }, 16.1);')
    # Kind läuft herein
    J(f'tl.fromTo("#kind", {{ x: 1300, y: {kid_t[1]:.1f}, scale: {0.75 * zt:.3f} }}, {{ x: {kid_t[0]:.1f}, duration: 0.7, ease: "power1.out" }}, 16.0);')
    for i in range(5):
        J(f'tl.to("#kind-schuh-{"l" if i % 2 == 0 else "r"}", {{ y: -10, duration: 0.07, ease: "power1.out", yoyo: true, repeat: 1 }}, {16.0 + i * 0.14:.2f});')
    J('tl.fromTo("#kind svg", { y: 0 }, { y: -10, duration: 0.07, ease: "power1.out", yoyo: true, repeat: 9 }, 16.0);')
    # Kind: BUH! – Herbert springt
    J('tl.fromTo("#kind svg", { scaleY: 1, scaleX: 1 }, { scaleY: 1.12, scaleX: 0.94, duration: 0.1, ease: "power2.out", transformOrigin: "50% 100%" }, 16.75);')
    J('tl.to("#kind svg", { scaleY: 1, scaleX: 1, duration: 0.25, ease: "elastic.out(1, 0.5)" }, 16.86);')
    J(f'tl.to("{h} svg", {{ scaleY: 0.82, scaleX: 1.1, duration: 0.07, ease: "power2.in" }}, 16.8);')
    J(f'tl.to("{h}", {{ y: {h_door_t[1] - 330:.1f}, duration: 0.26, ease: "power2.out" }}, 16.87);')
    J(f'tl.to("{h} svg", {{ scaleY: 1.22, scaleX: 0.88, duration: 0.12, ease: "power2.out" }}, 16.87);')
    J('tl.set("#herbert-mund-lachen", { opacity: 0 }, 16.87);')
    J('tl.set("#herbert-mund-schrei", { opacity: 1 }, 16.87);')
    J('tl.to("#herbert-augen", { scale: 1.4, duration: 0.1, ease: "back.out(3)" }, 16.87);')
    J('tl.to("#herbert-arm-l", { rotation: -70, duration: 0.12, ease: "back.out(2)" }, 16.87);')
    J('tl.to("#herbert-arm-r", { rotation: 70, duration: 0.12, ease: "back.out(2)" }, 16.9);')
    J(f'tl.to("{h}", {{ y: {h_door_t[1]:.1f}, duration: 0.3, ease: "power2.in" }}, 17.2);')
    J(f'tl.to("{h} svg", {{ scaleY: 0.86, scaleX: 1.08, duration: 0.08, ease: "power2.out" }}, 17.5);')
    J(f'tl.to("{h} svg", {{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "elastic.out(1, 0.5)" }}, 17.58);')
    J('tl.to("#herbert-augen", { scale: 1, duration: 0.2 }, 17.5);')
    J('tl.to(["#herbert-arm-l", "#herbert-arm-r"], { rotation: 0, duration: 0.3, ease: "power2.out" }, 17.55);')
    J('tl.set("#herbert-mund-schrei", { opacity: 0 }, 17.6);')
    J('tl.set("#herbert-mund-lachen", { opacity: 1 }, 17.6);')
    # beide lachen (kleines Hüpfen, versetzt)
    J(f'tl.to("{h} svg", {{ y: -14, duration: 0.14, ease: "power1.out", yoyo: true, repeat: 3 }}, 17.75);')
    J('tl.to("#kind svg", { y: -10, duration: 0.15, ease: "power1.out", yoyo: true, repeat: 3 }, 17.85);')
    # zurück zum ganzen Haus für „Der Spuk ist vorbei.“
    J(f'tl.to("#welt-kamera", {{ {cam_js("W")}, duration: 0.6, ease: "power2.inOut" }}, 18.2);')
    J(f'tl.to("{h}", {{ x: {door_world[0]}, y: {door_world[1]}, scale: 0.62, duration: 0.6, ease: "power2.inOut" }}, 18.2);')
    J(f'tl.to("#kind", {{ x: {kid_world[0]}, y: {kid_world[1]}, scale: 0.75, duration: 0.6, ease: "power2.inOut" }}, 18.2);')
    # Endkarte: Kamera tiefer, Figuren mit
    J(f'tl.to("{h}", {{ x: {h_door_e[0]:.1f}, y: {h_door_e[1]:.1f}, scale: {0.62 * CAM["E"][2]:.3f}, duration: 0.7, ease: "power2.inOut" }}, 22.0);')
    J(f'tl.to("#kind", {{ x: {kid_e[0]:.1f}, y: {kid_e[1]:.1f}, scale: {0.75 * CAM["E"][2]:.3f}, duration: 0.7, ease: "power2.inOut" }}, 22.0);')
    # Herbert zieht auch aus: Koffer, winken, davonschweben
    J('tl.to("#herbert-koffer", { opacity: 1, duration: 0.15 }, 25.4);')
    J('tl.to("#herbert-arm-l", { rotation: -60, duration: 0.15, ease: "power2.out" }, 25.55);')
    for i in range(4):
        J(f'tl.to("#herbert-arm-l", {{ rotation: {-30 if i % 2 == 0 else -65}, duration: 0.14, ease: "sine.inOut" }}, {25.72 + i * 0.15:.2f});')
    J(f'tl.to("{h}", {{ x: 1220, y: 760, scale: 0.42, duration: 1.4, ease: "power2.in" }}, 26.0);')
    J('tl.to("#kind-schuh-l", { y: -6, duration: 0.12, ease: "power1.out", yoyo: true, repeat: 5 }, 26.0);')

    # Nacht → Tag ---------------------------------------------------------
    T = 13.0
    order = ["himmel", "dach", "dachkante", "kamin", "wand", "fenster", "rahmen", "laden", "tuer", "knauf", "stufe",
             "huegel", "weg", "zaun", "baum"]
    svg_text = world_svg()
    for i, key in enumerate(order):
        night, day = PAL[key]
        t = T + 0.04 * i
        if f'class="t-{key}"' in svg_text:
            J(f'tl.fromTo(".t-{key}", {{ fill: "{night}" }}, {{ fill: "{day}", duration: 0.7, ease: "power2.inOut" }}, {t:.2f});')
        if f'class="t-{key}-s"' in svg_text:
            J(f'tl.fromTo(".t-{key}-s", {{ stroke: "{night}" }}, {{ stroke: "{day}", duration: 0.7, ease: "power2.inOut" }}, {t:.2f});')
    J(f'tl.to("#sterne", {{ opacity: 0, duration: 0.4, ease: "power1.in" }}, {T});')
    J(f'tl.to("#mond", {{ y: 120, opacity: 0, duration: 0.35, ease: "power2.in" }}, {T});')
    J(f'tl.fromTo("#sonne", {{ y: 480, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 1.1, ease: "power2.out" }}, {T + 0.35});')
    J(f'tl.to(["#spinnweben", "#risse", "#spuklicht"], {{ opacity: 0, duration: 0.35, ease: "power1.in" }}, {T + 0.1});')
    J(f'tl.to("#bretter", {{ y: 260, rotation: 25, opacity: 0, duration: 0.5, ease: "power2.in", transformOrigin: "50% 50%" }}, {T + 0.15});')
    J(f'tl.to("#laden-OL-l", {{ rotation: 0, duration: 0.6, ease: "elastic.out(1, 0.5)" }}, {T + 0.35});')
    J(f'tl.to(".latte", {{ rotation: 0, duration: 0.45, ease: "back.out(2)", stagger: 0.025 }}, {T + 0.3});')
    J(f'tl.to("#kuerbis-boese", {{ opacity: 0, duration: 0.2 }}, {T + 0.5});')
    J(f'tl.to("#kuerbis-froh", {{ opacity: 1, duration: 0.2 }}, {T + 0.6});')
    J(f'tl.fromTo(".blatt", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.35, ease: "back.out(2.2)", stagger: 0.05 }}, {T + 0.45});')
    J(f'tl.fromTo(".blume", {{ scale: 0, transformOrigin: "50% 100%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(2.4)", stagger: 0.035 }}, {T + 0.6});')
    # Schild: wächst nachts aus dem Rasen, tags klatscht VERKAUFT darauf
    J('tl.fromTo("#schild", { scaleY: 0, opacity: 0 }, { scaleY: 1, opacity: 1, duration: 0.36, ease: "back.out(2)" }, 12.0);')
    J('tl.fromTo("#schild-band", { scale: 1.7, rotation: -28, opacity: 0 }, { scale: 1, rotation: -10, opacity: 1, duration: 0.16, ease: "expo.out" }, 13.75);')
    # Familie und Kartons
    J('tl.fromTo("#familie", { y: 80 }, { y: 0, duration: 0.45, ease: "back.out(1.6)" }, 14.5);')
    J('tl.fromTo("#familie-arm", { rotation: 0 }, { rotation: -35, duration: 0.18, ease: "sine.inOut", yoyo: true, repeat: 5 }, 14.95);')
    J('tl.fromTo("#kartons", { scale: 0, transformOrigin: "50% 100%" }, { scale: 1, duration: 0.3, ease: "back.out(2.4)" }, 15.0);')
    files["compositions/welt.html"] = scene("welt", DURATION, css, body, js)

    # ---------------------------------------------------------------- s1: Spuk
    p, lines = "s1", TEXT["hook"]
    css = title_css(p, 128, CREAM) + f'''
        .s1-buh {{
          position: absolute;
          left: 0;
          right: 0;
          top: 560px;
          text-align: center;
          font-size: 230px;
          font-weight: 900;
          letter-spacing: -0.02em;
          line-height: 1;
          color: {CREAM};
          text-shadow: 10px 10px 0 {RED};
        }}'''
    body = title_html(p, lines) + f'\n        <div class="s1-buh" id="s1-buh">{TEXT["buh"]}</div>\n'
    js = [blur_out(word_ids(p, lines), 1.3, 0.2),
          'tl.fromTo("#s1-buh", { scale: 0.3, rotation: -14, opacity: 0 }, { scale: 1, rotation: -6, opacity: 1, duration: 0.2, ease: "back.out(2.6)" }, 2.2);',
          'tl.to("#s1-buh", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, 3.0);']
    files["compositions/s1-spuk.html"] = scene("s1-spuk", BY_ID["s1-spuk"]["dur"], css, body, js)

    # ---------------------------------------------------------------- s2: allein (Sprechblasen)
    p = "s2"
    b_left, b_top = 380, 646
    tail = (40, 300)  # Spitze relativ zur Blase: zu Herberts Kopf
    css = bubble_css(p)
    body = (bubble_html(p, "s2-b1", b_left, b_top, TEXT["blase1"], tail) + "\n"
            + bubble_html(p, "s2-b2", b_left, b_top, TEXT["blase2"], tail) + "\n")
    js = [pop_in("#s2-b1", 0.3, "15% 100%"),
          'tl.to("#s2-b1", { opacity: 0, scale: 0.92, duration: 0.14, ease: "power2.in" }, 2.5);',
          pop_in("#s2-b2", 2.7, "15% 100%"),
          'tl.to("#s2-b2", { opacity: 0, scale: 0.92, duration: 0.18, ease: "power2.in" }, 5.62);']
    files["compositions/s2-allein.html"] = scene("s2-allein", BY_ID["s2-allein"]["dur"], css, body, js)

    # ---------------------------------------------------------------- s3: viel zu viel Haus
    p, lines = "s3", TEXT["zu_gross"]
    size = 104
    while max(M.width(t, size, 900, -0.02) for t in lines) > W - 72 - 60:
        size -= 2
    css = title_css(p, size, CREAM)
    body = title_html(p, lines) + "\n"
    js = title_in(p, lines, 0.4) + [blur_out(word_ids(p, lines), 2.62)]
    files["compositions/s3-zu-gross.html"] = scene("s3-zu-gross", BY_ID["s3-zu-gross"]["dur"], css, body, js)

    # ---------------------------------------------------------------- s4: neues Leben
    p = "s4"
    neu, vorbei = TEXT["neu"], TEXT["vorbei"]
    css = (title_css(p, 120, INK) + "\n" + bubble_css(p) + f'''
        .s4-titel2 {{
          position: absolute;
          left: 72px;
          right: 60px;
          top: 226px;
          font-size: 120px;
          font-weight: 900;
          letter-spacing: -0.02em;
          line-height: 1.02;
          color: {INK};
        }}
        .s4-kind-blase {{
          color: {RED};
          font-size: 64px;
          font-weight: 900;
        }}
        .s4-aaah {{
          position: absolute;
          left: 500px;
          top: 452px;
          font-size: 84px;
          font-weight: 900;
          color: {INK};
          letter-spacing: -0.01em;
        }}''')
    zeilen2 = []
    for k, line in enumerate(vorbei):
        ws = " ".join('<span class="s4-w" id="s4-v%dw%d">%s</span>' % (k, i, w) for i, w in enumerate(line.split(" ")))
        zeilen2.append('<span class="s4-zeile%s">%s</span>' % (" rot" if k == 1 else "", ws))
    body = (title_html(p, neu, red=(1,)) + "\n"
            + '        <div class="s4-titel2">' + "".join(zeilen2) + "</div>\n"
            + bubble_html(p, "s4-kb", 650, 792, [TEXT["kind_buh"]], (80, 150), size=64, pad=(12, 30, 16), weight=900, color=RED) + "\n"
            + f'        <div class="s4-aaah" id="s4-aaah">{TEXT["aaah"]}</div>\n')
    js = title_in(p, neu, 0.05) + [blur_out(word_ids(p, neu), 2.25)]
    js += [pop_in("#s4-kb", 3.75, "30% 100%"),
           'tl.to("#s4-kb", { opacity: 0, duration: 0.15, ease: "power2.in" }, 4.75);',
           'tl.fromTo("#s4-aaah", { scale: 0.4, rotation: -20, opacity: 0 }, { scale: 1, rotation: -8, opacity: 1, duration: 0.16, ease: "back.out(2.6)" }, 3.9);',
           'tl.to("#s4-aaah", { opacity: 0, duration: 0.2, ease: "power2.in" }, 4.9);']
    vids = [f"#s4-v{k}w{i}" for k, line in enumerate(vorbei) for i, _ in enumerate(line.split(" "))]
    js += [blur_in(sel, 5.85 + 0.09 * i) for i, sel in enumerate(vids)]
    js.append(blur_out(vids, 8.7))
    files["compositions/s4-neues-leben.html"] = scene("s4-neues-leben", BY_ID["s4-neues-leben"]["dur"], css, body, js)

    # ---------------------------------------------------------------- s5: Ende (Leads)
    p, lines = "s5", TEXT["ende"]
    size5 = 96
    while max(M.width(t, size5, 900, -0.02) for t in lines) > W - 72 - 60:
        size5 -= 2
    cta_w = M.width(TEXT["cta"], 48, 800) + 2 * 34
    logo_w = 430
    k_logo = logo_w / 452
    mark = 100 * k_logo
    logo_top = 678
    facets = [
        ("A", [(0, 0), (79.5, 0), (0, 100)], (-90, -20, -16),
         ("0", "0", "48.9", "39.6", [("0", "#5e0f18"), ("0.56", "#a4222b"), ("0.8", "#c12a33"), ("0.93", "#ca2c35")])),
        ("R", [(79.5, 0), (100, 0), (100, 100), (47.5, 40.2)], (70, -60, 14),
         ("47.5", "40.2", "100", "0", [("0", "#4a0a13"), ("1", "#b0252e")])),
        ("B", [(0, 100), (47.5, 40.2), (100, 100)], (20, 80, 10),
         ("0", "100", "100", "100", [("0", "#480a12"), ("0.5", "#a2222b"), ("0.85", "#ca2c35")])),
    ]

    def centroid(pts):
        a = cx = cy = 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            c = x0 * y1 - x1 * y0
            a += c
            cx += (x0 + x1) * c
            cy += (y0 + y1) * c
        return cx / (3 * a), cy / (3 * a)

    facet_html, fjs = [], []
    for n, (key, pts, (dx, dy, rot), (x1, y1, x2, y2, stops)) in enumerate(facets):
        cx, cy = centroid(pts)
        st = "".join(f'<stop offset="{o}" stop-color="{c}" />' for o, c in stops)
        poly = " ".join(f"{x},{y}" for x, y in pts)
        facet_html.append(f'        <div class="s5-facet" id="s5-f{key}" style="left: 72px; top: {logo_top}px; width: {mark:.1f}px; height: {mark:.1f}px; '
                          f'transform-origin: {cx:.2f}% {cy:.2f}%"><svg viewBox="0 0 100 100" aria-hidden="true"><defs>'
                          f'<linearGradient id="s5-g{key}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient></defs>'
                          f'<polygon points="{poly}" fill="url(#s5-g{key})" /></svg></div>')
        fjs.append(f'tl.fromTo("#s5-f{key}", {{ x: {dx}, y: {dy}, rotation: {rot}, opacity: 0 }}, '
                   f'{{ x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.42, ease: "power3.out" }}, {2.58 + 0.04 * n:.2f});')
    css = title_css(p, size5, INK, top=212) + f'''
        .s5-cta {{
          position: absolute;
          left: 72px;
          top: 452px;
          width: {cta_w:.0f}px;
          height: 96px;
          border-radius: 22px;
          background: {RED};
          color: #ffffff;
          font-size: 48px;
          font-weight: 800;
          line-height: 96px;
          text-align: center;
          box-shadow: 0 12px 26px rgba(202, 44, 53, 0.3);
        }}
        .s5-url {{
          position: absolute;
          left: 72px;
          top: 574px;
          font-size: 46px;
          font-weight: 700;
          color: {INK};
          white-space: nowrap;
        }}
        .s5-facet {{
          position: absolute;
        }}
        .s5-facet svg,
        .s5-wort svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}
        .s5-wort {{
          position: absolute;
          left: {72 + 120 * k_logo:.1f}px;
          top: {logo_top}px;
          width: {340 * k_logo:.1f}px;
          height: {mark:.1f}px;
        }}
        .s5-wort text {{
          font-family: "Montserrat", sans-serif;
          fill: {INK};
        }}'''
    body = (title_html(p, lines, red=(1,)) + "\n"
            + f'        <div class="s5-cta" id="s5-cta">{TEXT["cta"]}</div>\n'
            + f'        <div class="s5-url" id="s5-url">{TEXT["url"]}</div>\n'
            + "\n".join(facet_html) + "\n"
            + f'        <div class="s5-wort" id="s5-wort"><svg viewBox="120 0 340 100" aria-hidden="true">'
            + '<text x="125.2" y="53" font-size="77" font-weight="700" textLength="328.5" lengthAdjust="spacing">KNIGGE</text>'
            + '<text x="125.5" y="100" font-size="44.3" font-weight="400" textLength="330.5" lengthAdjust="spacing">IMMOBILIEN</text></svg></div>\n')
    js = title_in(p, lines, 0.25, 0.07)
    js.append('tl.fromTo("#s5-cta", { clipPath: "inset(0% 100% 0% 0% round 22px)" }, { clipPath: "inset(0% 0% 0% 0% round 22px)", duration: 0.36, ease: "power3.out" }, 1.5);')
    js.append(blur_in("#s5-url", 1.95, 0.2))
    js += fjs
    js.append('tl.fromTo("#s5-wort", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }, 3.0);')
    files["compositions/s5-ende.html"] = scene("s5-ende", BY_ID["s5-ende"]["dur"], css, body, js)

    # ---------------------------------------------------------------- index.html
    hosts = [f'      <div id="welt" data-composition-id="welt" data-composition-src="compositions/welt.html" data-start="0" '
             f'data-duration="{DURATION}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>']
    hosts += [f'      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
              f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="1" data-track-kind="graphics" '
              f'data-width="{W}" data-height="{H}"></div>' for s in SCENES]
    # Geräusche: Spitze einen Frame nach dem Bild (Spitzen gemessen mit `hyperframes audio`)
    peaks = {"impact-bass-1": 0.073, "whoosh-short": 0.162, "pop": 0.12, "sparkle": 0.027}
    lengths = {"impact-bass-1": 2.116, "whoosh-short": 0.575, "pop": 0.72, "sparkle": 1.802}
    sfx = [("sfx-buh", "impact-bass-1", 2.2, 0.32), ("sfx-flug", "whoosh-short", 10.25, 0.5), ("sfx-schild", "pop", 12.12, 0.9),
           ("sfx-tag", "sparkle", 13.0, 0.4), ("sfx-verkauft", "whoosh-short", 13.8, 0.45), ("sfx-kind", "impact-bass-1", 16.75, 0.28),
           ("sfx-sprung", "whoosh-short", 16.95, 0.5), ("sfx-weg", "whoosh-short", 26.6, 0.35)]
    audio = ['      <audio id="musik" class="clip" src="assets/audio/musik.m4a" data-start="0" data-duration="28" data-track-index="2" data-volume="1"></audio>']
    ends = {}
    for aid, f, t, vol in sfx:
        start = t + 1 / FPS - peaks[f]
        track = next(tr for tr in (3, 4, 5) if ends.get(tr, -1) <= start)
        ends[track] = start + lengths[f]
        audio.append(f'      <audio id="{aid}" class="clip" src="assets/sfx/{f}.mp3" data-start="{start:.3f}" '
                     f'data-duration="{lengths[f]}" data-track-index="{track}" data-volume="{vol}"></audio>')
    files["index.html"] = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>KNIGGE Immobilien – Hausgeist Herbert (Halloween-Reel)</title>
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
        background: #26303a;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #26303a;
      }}
    </style>
  </head>
  <body>
    <!--
      KNIGGE Immobilien – Halloween-Reel „Hausgeist Herbert“ (1080×1920, 28 s, Musik + Geräusche)
      erzeugt von tools/build_reel.py – Texte dort in TEXT ändern
    -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="{W}" data-height="{H}" data-fps="{FPS}" data-motion-blur="on">
{chr(10).join(hosts)}
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    for rel, html in files.items():
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("geschrieben:", rel)
    print(f"  Herbert: Fenster OR bei P {h_pop0[0]:.0f},{h_pop0[1]:.0f}; Fenster OL bei Z {h_win_z[0]:.0f},{h_win_z[1]:.0f}; "
          f"Tür bei E {h_door_e[0]:.0f},{h_door_e[1]:.0f}; Kind bei E {kid_e[0]:.0f},{kid_e[1]:.0f}")
    print(f"  Titel s3 {size} px, s5 {size5} px, CTA {cta_w:.0f} px breit")


if __name__ == "__main__":
    build()
