#!/usr/bin/env python3
"""Erzeugt das Instagram-Reel „Das Haus ist abbezahlt.“ (1080×1920, 27,75 s, 30 fps):
index.html und compositions/*.html.

Ein Film aus allen drei Storylines (STORYLINES.md): das rote „Aber“ trägt die Schnitte (Einstieg →
Match-Cut in „Aber die Kosten bleiben.“ → Andrea Gerhardus), ein Kassenbon druckt die Kosten, eine
Balkenwaage kippt unter den Aufgaben und kommt mit den vier Optionen zurück ins Gleichgewicht; am Ende
der Expertenbeitrag auf in-gl.de und das Logo. Alle Texte wörtlich aus dem Karussell.

Die Musik ist die Uhr (80 BPM, 1 Schlag = 0,75 s; Schnitt aus dem KNIGGE-Thema, tools/prepare_assets.py):
Auflösung nach F-Dur bei 12,75 s („Welche Optionen gibt es?“), Schlussakkord bei 24,75 s (Logo).

Schrift: Red Hat Display (Hausschrift, assets/fonts/red-hat-display.woff2); gemessen wird mit der
TTF-Fassung derselben Datei, damit Zeilen und Knöpfe passen.

Ändern: Texte in TEXT, Zeiten in SCENES bzw. den Zeitlisten der Szenen, dann
`python3 tools/build_reel.py` und `npm run check`. Fotos und Musik: tools/prepare_assets.py.
"""
import math
import os

from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF = os.path.join(ROOT, "assets", "fonts", "red-hat-display.ttf")

W, H, FPS, DURATION = 1080, 1920, 30, 27.75
INK, RED, PAPER_GREY, TOKEN_FILL = "#323c44", "#ca2c35", "#e4e7e9", "#f3f0eb"
X0, DASH_TOP, HEAD_TOP = 72, 208, 240  # linker Rand, roter Strich, erste Überschriftzeile
TRACK = -0.02  # Laufweite der Überschriften (em)

TEXT = {
    "einstieg": ["Das Haus", "ist abbezahlt.", "Aber können", "wir es uns", "noch leisten?"],
    "kosten": ["Keine", "Kreditrate mehr.", "Aber die Kosten", "bleiben."],
    "bon_kopf": "Kreditrate",
    "stempel": "ABBEZAHLT",
    "bon": [("heizung", ["Heizung und Energie"]), ("haus", ["Grundsteuer"]), ("schild", ["Versicherungen"]),
            ("werkzeug", ["Reparaturen und", "Instandhaltung"]), ("muenzen", ["Modernisierungen"])],
    "summe": "Summe",
    "aufgabe": ["Wenn das Haus", "zur Aufgabe wird."],
    "lasten": [("blatt", "Der große Garten macht viel Arbeit."), ("haus", "Viele Zimmer stehen leer."),
               ("treppe", "Treppen werden beschwerlicher."), ("uhr", "Pflege und Instandhaltung kosten Zeit und Kraft.")],
    "optionen_titel": ["Welche Optionen", "gibt es?"],
    "optionen": [("haus", "Im vertrauten Zuhause bleiben"), ("hammer", "Umbauen und altersgerecht gestalten"),
                 ("personen", "(Teil-)Vermietung in Betracht ziehen"), ("schluessel", "Ein neues, passendes Zuhause finden")],
    "zitat": ["Nicht jedes Haus muss", "verkauft werden.", "Aber jedes Zuhause", "sollte zum Leben passen."],
    "name": "Andrea Gerhardus",
    "funktion": ["Immobilienexpertin bei", "KNIGGE Immobilien"],
    "ende": ["Den ganzen", "Expertenbeitrag", "jetzt lesen."],
    "knopf": ["Zum Expertenbeitrag", "auf in-gl.de"],
}

SCENES = [
    {"id": "s1-einstieg", "start": 0.0, "dur": 3.75},
    {"id": "s2-kosten", "start": 3.75, "dur": 4.5},
    {"id": "s3-aufgabe", "start": 8.25, "dur": 4.5},
    {"id": "s4-optionen", "start": 12.75, "dur": 5.25},
    {"id": "s5-expertin", "start": 18.0, "dur": 5.25},
    {"id": "s6-ende", "start": 23.25, "dur": 4.5},
]
BY_ID = {s["id"]: s for s in SCENES}

# Strich-Icons (48er Raster, Kontur), wie die Icons des Karussells
ICONS = {
    "heizung": '<path d="M13 13v22M19 11v26M25 11v26M31 11v26M37 13v22"/><path d="M9.5 17h31M9.5 31h31"/><path d="M15 37v3.5M35 37v3.5"/>',
    "haus": '<path d="M7 23 24 9l17 14"/><path d="M11 20v19h26V20"/><path d="M20 39V29h8v10"/>',
    "schild": '<path d="M24 6 39 11.5V23c0 9.5-6.5 15.5-15 19-8.5-3.5-15-9.5-15-19V11.5Z"/><path d="m17 23.5 5 5 9.5-10"/>',
    "werkzeug": '<path d="M30.5 8.5a8.5 8.5 0 0 0-8.9 11.3L9.3 32.1a3.6 3.6 0 0 0 5.1 5.1L26.7 25a8.5 8.5 0 0 0 11.3-8.9l-5.3 5.3-4.6-1.3-1.3-4.6Z"/>',
    "muenzen": '<ellipse cx="24" cy="12" rx="12" ry="5"/><path d="M12 12v8c0 2.8 5.4 5 12 5s12-2.2 12-5v-8"/><path d="M12 20v8c0 2.8 5.4 5 12 5s12-2.2 12-5v-8"/><path d="M12 28v8c0 2.8 5.4 5 12 5s12-2.2 12-5v-8"/>',
    "blatt": '<path d="M24 40c-2-10 2-20 13-25 2 12-3 22-13 25Z"/><path d="M24 40c2-10-2-20-13-25-2 12 3 22 13 25Z"/>',
    "treppe": '<path d="M9 39V31h8v-8h8v-8h8V7h6v32Z"/>',
    "uhr": '<circle cx="24" cy="24" r="15.5"/><path d="M24 14v10l6.5 4"/>',
    "hammer": '<path d="M21 15 28 8l12 12-7 7Z"/><path d="M27 21 10 38"/>',
    "personen": '<circle cx="18" cy="16" r="6"/><path d="M7 38c0-7 5-11.5 11-11.5S29 31 29 38"/><circle cx="32.5" cy="18" r="5"/><path d="M31 27.5c6 0 10.5 3.8 10.5 10.5"/>',
    "schluessel": '<circle cx="16" cy="32" r="8"/><path d="m22 26 17-17"/><path d="m33.5 14.5 4.5 4.5"/><path d="m28.5 19.5 3.5 3.5"/>',
    "link": '<path d="M27 9h12v12"/><path d="M39 9 22 26"/><path d="M33 27v11H10V15h11"/>',
    "haken": '<path d="m10 25 9 9 19-20"/>',
}

# KNIGGE-Bildmarke: drei Facetten (Koordinaten 0–100) mit ihren Verläufen, Wortmarke wie im Logo
FACETS = [
    {"key": "A", "pts": [(0, 0), (79.5, 0), (0, 100)], "from": (-90, -20, -16),
     "grad": ("0", "0", "48.9", "39.6", [("0", "#5e0f18"), ("0.56", "#a4222b"), ("0.8", "#c12a33"), ("0.93", "#ca2c35")])},
    {"key": "R", "pts": [(79.5, 0), (100, 0), (100, 100), (47.5, 40.2)], "from": (70, -60, 14),
     "grad": ("47.5", "40.2", "100", "0", [("0", "#4a0a13"), ("1", "#b0252e")])},
    {"key": "B", "pts": [(0, 100), (47.5, 40.2), (100, 100)], "from": (20, 80, 10),
     "grad": ("0", "100", "100", "100", [("0", "#480a12"), ("0.5", "#a2222b"), ("0.85", "#ca2c35")])},
]
WORDMARK = ('<text x="125.2" y="53" font-size="77" font-weight="700" textLength="328.5" lengthAdjust="spacing">KNIGGE</text>'
            '<text x="125.5" y="100" font-size="44.3" font-weight="400" textLength="330.5" lengthAdjust="spacing">IMMOBILIEN</text>')

# Waage (Bildkoordinaten): Drehpunkt, halbe Balkenlänge, Schnurlänge bis zur Schale
PIVOT = (540, 930)
ARM, DROP = 320, 262


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

    def fit(self, lines, max_w, weight, start, track=TRACK):
        size = start
        while max(self.width(t, size, weight, track) for t in lines) > max_w:
            size -= 1
        return size


M = Measure()


# ------------------------------------------------------------------------------------------------
# HTML-Bausteine
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
          background: #ffffff;
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


def scene(sid, css, body, js):
    s = BY_ID[sid]
    return (SCENE_HEAD.format(id=sid, font=FONT_FACE, ink=INK, css=css, W=W, H=H, dur=s["dur"]) + body
            + SCENE_TAIL.format(js="\n".join("          " + j for j in js), id=sid))


def icon(name, size, stroke=INK, width=2.6):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def head_css(p, size, top=HEAD_TOP):
    return f'''        .{p}-strich {{
          position: absolute;
          left: {X0}px;
          top: {DASH_TOP}px;
          width: 100px;
          height: 9px;
          background: {RED};
          transform-origin: 0 50%;
        }}
        .{p}-kopf {{
          position: absolute;
          left: {X0}px;
          top: {top}px;
          font-size: {size}px;
          font-weight: 800;
          letter-spacing: {TRACK}em;
          line-height: 1;
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


def head_html(p, lines, red_from):
    """Überschrift: je Zeile ein Block, je Wort ein Span (id p-l{k}w{i}); ab Zeile red_from rot."""
    out = [f'        <div class="{p}-kopf">']
    for k, line in enumerate(lines):
        words = " ".join(f'<span class="{p}-w" id="{p}-l{k}w{i}">{w}</span>' for i, w in enumerate(line.split(" ")))
        out.append(f'          <span class="{p}-zeile{" rot" if k >= red_from else ""}">{words}</span>')
    out.append("        </div>")
    return "\n".join(out)


def word_ids(p, lines, skip=()):
    return [f"#{p}-l{k}w{i}" for k, line in enumerate(lines) for i, _ in enumerate(line.split(" ")) if (k, i) not in skip]


def blur_in(sel, t, dur=0.16):
    return (f'tl.fromTo("{sel}", {{ opacity: 0, filter: "blur(10px)" }}, '
            f'{{ opacity: 1, filter: "blur(0px)", duration: {dur}, ease: "power4.out" }}, {t:.3f});')


def blur_out(sels, t, dur=0.2):
    arr = ", ".join(f'"{s}"' for s in sels)
    return f'tl.to([{arr}], {{ opacity: 0, filter: "blur(10px)", duration: {dur}, ease: "power2.in" }}, {t:.3f});'


def slam(sel, t):
    """Das rote „Aber“: schlägt mit Unschärfe und Übergröße ein."""
    return (f'tl.fromTo("{sel}", {{ opacity: 0, scale: 1.3, filter: "blur(10px)" }}, '
            f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.16, ease: "expo.out" }}, {t:.3f});')


def photo_css(p, img_w, img_h, left, top, veils, origin="50% 50%"):
    """Foto in einem Kasten (für die langsame Fahrt) plus weiße Lichtschleier (x, y, w, h, Richtung, Deckung)."""
    css = f'''        .{p}-foto {{
          position: absolute;
          left: {left}px;
          top: {top}px;
          width: {min(img_w, W - left)}px;
          height: {min(img_h, H - top)}px;
          overflow: hidden;
        }}
        .{p}-foto img {{
          position: absolute;
          left: 0;
          top: 0;
          width: {img_w}px;
          height: {img_h}px;
          transform-origin: {origin};
        }}'''
    for k, (x, y, w, h, direction, solid) in enumerate(veils):
        css += f'''
        .{p}-schleier{k} {{
          position: absolute;
          left: {x}px;
          top: {y}px;
          width: {w}px;
          height: {h}px;
          background: linear-gradient({direction}, #ffffff 0%, #ffffff {solid}%, rgba(255, 255, 255, 0) 100%);
        }}'''
    return css


def photo_html(p, src, veils):
    return (f'        <div class="{p}-foto"><img id="{p}-bild" src="assets/img/{src}" alt="" /></div>\n'
            + "\n".join(f'        <div class="{p}-schleier{k}"></div>' for k in range(len(veils))))


def push_in(p, dur, scale=1.05):
    return f'tl.fromTo("#{p}-bild", {{ scale: 1 }}, {{ scale: {scale}, duration: {dur}, ease: "power1.inOut" }}, 0);'


def zigzag(w, h, tooth=16, depth=9, top=True):
    """clip-path-Polygon für eine gezackte Papierkante (oben oder unten)."""
    n = max(2, round(w / tooth))
    pts = []
    if top:
        for i in range(n + 1):
            pts.append(f"{100 * i / n:.2f}% {0 if i % 2 == 0 else depth}px")
        pts += ["100% 100%", "0% 100%"]
    else:
        pts += ["0% 0%", "100% 0%"]
        for i in range(n, -1, -1):
            pts.append(f"{100 * i / n:.2f}% calc(100% - {0 if i % 2 == 0 else depth}px)")
    return "polygon(" + ", ".join(pts) + ")"


def centroid(pts):
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    return cx / (3 * a), cy / (3 * a)


def facet_svg(f, gid):
    x1, y1, x2, y2, stops = f["grad"]
    st = "".join(f'<stop offset="{o}" stop-color="{c}" />' for o, c in stops)
    pts = " ".join(f"{x},{y}" for x, y in f["pts"])
    return (f'<svg viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient></defs>'
            f'<polygon points="{pts}" fill="url(#{gid})" /></svg>')


# ------------------------------------------------------------------------------------------------
# Waage: gemeinsamer Aufbau für s3 und s4 (gleiche Lage, Zustand wird übergeben)
# ------------------------------------------------------------------------------------------------
RIGHT_LOAD = [  # rechte Schale: Bon + Aufgaben (Mitte relativ zum Balkenende, Gewichte 100 px)
    ("bon", (-70, 217)), ("blatt", (68, 212)), ("haus", (-52, 123)), ("treppe", (58, 117)), ("uhr", (4, 26)),
]
LEFT_LOAD = [("haus", (-128, 212)), ("hammer", (128, 212)), ("personen", (-50, 46)), ("schluessel", (50, 46))]
ANGLES_S3 = [5, 9, 12.5, 15.5, 18]  # nach Bon, Garten, Zimmer, Treppen, Pflege
ANGLES_S4 = [13, 8.5, 4, 0]  # nach den vier Optionen


def scale_css(p, angle0):
    px, py = PIVOT
    return f'''        .{p}-buehne {{
          position: absolute;
          inset: 0;
        }}
        .{p}-buehne div {{
          box-sizing: border-box;
        }}
        .{p}-geruest,
        .{p}-balken {{
          position: absolute;
          left: 0;
          top: 0;
          width: {W}px;
          height: {H}px;
          overflow: visible;
        }}
        #{p}-balken-g {{
          transform-box: view-box;
          transform-origin: {px}px {py}px;
          transform: rotate(calc(var(--a) * 1deg));
        }}
        .{p}-schale {{
          position: absolute;
          left: 0;
          top: 0;
          width: 0;
          height: 0;
        }}
        #{p}-schale-l {{
          transform: translate(calc({px}px - {ARM}px * cos(calc(var(--a) * 1deg))), calc({py}px - {ARM}px * sin(calc(var(--a) * 1deg))));
        }}
        #{p}-schale-r {{
          transform: translate(calc({px}px + {ARM}px * cos(calc(var(--a) * 1deg))), calc({py}px + {ARM}px * sin(calc(var(--a) * 1deg))));
        }}
        .{p}-schale svg.{p}-korb {{
          position: absolute;
          left: -200px;
          top: -20px;
          width: 400px;
          height: 330px;
          overflow: visible;
        }}
        .{p}-plakette {{
          position: absolute;
          left: -85px;
          top: {DROP - 172}px;
          width: 170px;
          height: 170px;
          border-radius: 50%;
          overflow: hidden;
          border: 6px solid #ffffff;
          box-shadow: 0 10px 26px rgba(30, 40, 48, 0.22);
        }}
        .{p}-plakette img {{
          display: block;
          width: 100%;
          height: 100%;
        }}
        .{p}-last {{
          position: absolute;
          width: 100px;
          height: 100px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 8px 18px rgba(30, 40, 48, 0.16);
        }}
        .{p}-last.rund {{
          border-radius: 50%;
          background: #ffffff;
          border: 3px solid {INK};
        }}
        .{p}-last.eckig {{
          border-radius: 18px;
          background: {TOKEN_FILL};
          border: 2px solid #ded8ce;
        }}
        .{p}-zettel {{
          position: absolute;
          width: 136px;
          height: 90px;
          background: #ffffff;
          clip-path: {zigzag(136, 90, 12, 6)};
          box-shadow: 0 6px 14px rgba(30, 40, 48, 0.16);
        }}
        .{p}-zettel i {{
          position: absolute;
          left: 16px;
          height: 5px;
          border-radius: 3px;
          background: {PAPER_GREY};
        }}
        .{p}-zettel b {{
          position: absolute;
          right: 12px;
          top: 30px;
          width: 46px;
          height: 22px;
          border: 3px solid {RED};
          border-radius: 4px;
          transform: rotate(-8deg);
        }}'''


def scale_html(p, angle0, right, left):
    """right/left: Liste (art, (x, y), sichtbar_von_anfang)."""
    px, py = PIVOT
    ink = INK
    geruest = f'''        <svg class="{p}-geruest" viewBox="0 0 {W} {H}" aria-hidden="true">
          <path d="M{px} {py} V1322" stroke="{ink}" stroke-width="14" stroke-linecap="round" fill="none" />
          <rect x="430" y="1316" width="220" height="30" rx="15" fill="{ink}" />
          <rect id="{p}-lot" x="{px - 3}" y="832" width="6" height="26" rx="3" fill="{RED}" />
        </svg>'''

    def pan(side, loads):
        dish = (f'<svg class="{p}-korb" viewBox="-200 -20 400 330" aria-hidden="true">'
                f'<path d="M0 0 L-168 {DROP} M0 0 L168 {DROP}" stroke="{ink}" stroke-width="3" fill="none" />'
                f'<path d="M-178 {DROP} H178 Q162 {DROP + 34} 0 {DROP + 36} Q-162 {DROP + 34} -178 {DROP} Z" fill="{ink}" /></svg>')
        items = [dish]
        if side == "l":
            items.append(f'<div class="{p}-plakette"><img src="assets/img/haus-rund.jpg" alt="" /></div>')
        for k, (kind, (x, y)) in enumerate(loads):
            if kind == "bon":
                items.append(f'<div class="{p}-zettel" id="{p}-{side}{k}" style="left: {x - 68}px; top: {y - 45}px">'
                             f'<i style="top: 22px; width: 70px"></i><i style="top: 38px; width: 52px"></i>'
                             f'<i style="top: 54px; width: 62px"></i><b></b></div>')
            else:
                shape = "rund" if side == "r" else "eckig"
                items.append(f'<div class="{p}-last {shape}" id="{p}-{side}{k}" style="left: {x - 50}px; top: {y - 50}px">'
                             f'{icon(kind, 54)}</div>')
        return (f'        <div class="{p}-schale" id="{p}-schale-{side}">\n          '
                + "\n          ".join(items) + "\n        </div>")

    balken = f'''        <svg class="{p}-balken" viewBox="0 0 {W} {H}" aria-hidden="true">
          <g id="{p}-balken-g">
            <rect x="{px - ARM}" y="{py - 6}" width="{2 * ARM}" height="12" rx="6" fill="{ink}" />
            <circle cx="{px - ARM}" cy="{py}" r="10" fill="{ink}" />
            <circle cx="{px + ARM}" cy="{py}" r="10" fill="{ink}" />
            <path d="M{px} {py - 58} L{px - 13} {py - 16} H{px + 13} Z" fill="{ink}" />
            <circle cx="{px}" cy="{py}" r="19" fill="{ink}" />
            <circle cx="{px}" cy="{py}" r="7" fill="#ffffff" />
          </g>
        </svg>'''
    return (f'        <div class="{p}-buehne" id="{p}-buehne" style="--a: {angle0}">\n{geruest}\n'
            + pan("l", left) + "\n" + pan("r", right) + f"\n{balken}\n        </div>")


def drop(p, side, k, t_land, fall=0.3):
    """Gewicht fällt von oberhalb des Bildes in seine Lage auf der Schale."""
    return (f'tl.fromTo("#{p}-{side}{k}", {{ y: -1500 }}, {{ y: 0, duration: {fall}, ease: "power2.in" }}, '
            f'{t_land - fall:.3f});')


def tip(p, angle, t, dur):
    return (f'tl.to("#{p}-buehne", {{ "--a": {angle}, duration: {dur:.2f}, ease: "elastic.out(1, 0.5)" }}, {t:.3f});')


def list_css(p, top0, pitch, shape):
    radius = "50%" if shape == "rund" else "14px"
    fill = "#ffffff" if shape == "rund" else TOKEN_FILL
    border = f"2.5px solid {INK}" if shape == "rund" else "2px solid #ded8ce"
    return f'''        .{p}-zeile2 {{
          position: absolute;
          left: {X0}px;
          height: 60px;
          display: flex;
          align-items: center;
          gap: 22px;
        }}
        .{p}-ikon {{
          box-sizing: border-box;
          flex: none;
          width: 60px;
          height: 60px;
          border-radius: {radius};
          background: {fill};
          border: {border};
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .{p}-text {{
          display: block;
          white-space: nowrap;
          font-size: 40px;
          font-weight: 500;
          line-height: 1.2;
        }}'''


def list_html(p, items, top0, pitch, with_marker=False):
    out = []
    for k, (ic, text) in enumerate(items):
        marker = ""
        if with_marker:
            w = 60 + 22 + M.width(text, 40, 500) + 18
            marker = f'<span class="{p}-marker" id="{p}-m{k}" style="width: {w:.0f}px"></span>'
        out.append(f'        <div class="{p}-zeile2" id="{p}-z{k}" style="top: {top0 + k * pitch}px">{marker}'
                   f'<span class="{p}-ikon" id="{p}-i{k}">{icon(ic, 36)}</span>'
                   f'<span class="{p}-text" id="{p}-t{k}">{text}</span></div>')
    return "\n".join(out)


LIST_TOP, LIST_PITCH = 488, 80


# ------------------------------------------------------------------------------------------------
# Szenen
# ------------------------------------------------------------------------------------------------
def build():
    files = {}
    report = []

    # ---------------------------------------------------------------- s1: Einstieg
    p, lines = "s1", TEXT["einstieg"]
    size1 = min(124, M.fit(lines, W - X0 - 72, 800, 124))
    foto_top = HEAD_TOP + len(lines) * size1 + 20
    veils = [(0, foto_top - 10, W, 260, "180deg", 18), (0, foto_top, 560, H - foto_top, "90deg", 32)]
    css = head_css(p, size1) + "\n" + photo_css(p, 1080, 1452, 0, foto_top, veils, "70% 45%") + f'''
        #s1-l2w0 {{
          transform-origin: 0% 60%;
        }}'''
    body = photo_html(p, "haus.jpg", veils) + f'\n        <div class="{p}-strich"></div>\n' + head_html(p, lines, 2) + "\n"
    js = [push_in(p, BY_ID["s1-einstieg"]["dur"])]
    js.append(slam("#s1-l2w0", 0.75))  # Taktanfang (d-Moll)
    for (k, i), t in zip([(2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)], [0.9, 1.02, 1.09, 1.16, 1.26, 1.33]):
        js.append(blur_in(f"#s1-l{k}w{i}", t))
    js.append(blur_out(word_ids(p, lines, skip={(2, 0)}), 3.3))
    files["compositions/s1-einstieg.html"] = scene("s1-einstieg", css, body, js)
    report.append(f"s1: Einstieg {size1} px, Foto ab y {foto_top}")

    # ---------------------------------------------------------------- s2: Kosten (Kassenbon)
    p, lines = "s2", TEXT["kosten"]
    size2 = min(112, M.fit(lines, W - X0 - 72, 800, 112))
    aber_dy = (HEAD_TOP + 2 * size1) - (HEAD_TOP + 2 * size2)  # Match-Cut: „Aber“ von s1 nach s2
    aber_scale = size1 / size2
    slot = 1290  # Druckerschlitz
    bon_x, bon_w = 340, 560
    rows = []  # (art, y, h, inhalt)
    y = 34
    rows.append(("kopf", y, 70))
    y += 70
    rows.append(("linie", y + 8, 2))
    y += 18
    for ic, txt in TEXT["bon"]:
        h = 60 if len(txt) == 1 else 98
        rows.append(("posten", y, h, ic, txt))
        y += h
    rows.append(("linie", y + 8, 2))
    y += 18
    rows.append(("summe", y, 82))
    y += 82 + 24
    bon_h = y
    steps = [(0.75, 34 + 70 + 18)]  # (Zeit, sichtbare Höhe): Kopf
    vis = 34 + 70 + 18
    t = 1.5
    for r in rows:
        if r[0] == "posten":
            vis = r[1] + r[2]
            steps.append((t, vis))
            t += 0.375
    steps.append((t, bon_h))  # Linie, Summe, Rand
    t_sum = t + 0.18
    report.append(f"s2: Überschrift {size2} px, Bon {bon_w}×{bon_h} (oben bei y {slot - bon_h})")
    css = head_css(p, size2) + "\n" + photo_css(p, 714, 1330, 0, 600, [(0, 590, 714, 240, "180deg", 20), (430, 600, 290, 1320, "270deg", 8)], "40% 60%") + f'''
        #s2-l2w0 {{
          transform-origin: 0 0;
        }}
        .s2-fenster {{
          position: absolute;
          left: 0;
          top: 0;
          width: {W}px;
          height: {slot}px;
          overflow: hidden;
        }}
        .s2-bon {{
          position: absolute;
          left: {bon_x}px;
          top: {slot - bon_h}px;
          width: {bon_w}px;
          height: {bon_h}px;
          background: #ffffff;
          clip-path: {zigzag(bon_w, bon_h, 16, 9)};
        }}
        .s2-schatten {{
          position: absolute;
          left: {bon_x}px;
          top: {slot - bon_h + 12}px;
          width: {bon_w}px;
          height: {bon_h - 12}px;
          box-shadow: 0 18px 40px rgba(30, 40, 48, 0.2);
        }}
        .s2-reihe {{
          position: absolute;
          left: 34px;
          right: 34px;
          display: flex;
          align-items: center;
          gap: 18px;
          font-size: 36px;
          font-weight: 600;
          line-height: 1.12;
        }}
        .s2-reihe .s2-txt {{
          display: block;
          white-space: nowrap;
        }}
        .s2-reihe.kopf {{
          font-weight: 700;
          justify-content: space-between;
        }}
        .s2-reihe.summe {{
          font-size: 40px;
          font-weight: 800;
          justify-content: space-between;
        }}
        .s2-frage {{
          display: inline-block;
          color: {RED};
          font-size: 66px;
          font-weight: 900;
          line-height: 1;
        }}
        .s2-trenn {{
          position: absolute;
          left: 34px;
          right: 34px;
          height: 0;
          border-top: 3px dashed #c9ced2;
        }}
        .s2-fein {{
          position: absolute;
          left: 34px;
          right: 34px;
          height: 0;
          border-top: 1.5px solid {PAPER_GREY};
        }}
        .s2-stempel {{
          position: absolute;
          left: 236px;
          top: 30px;
          padding: 4px 16px 6px;
          border: 5px solid {RED};
          border-radius: 10px;
          color: {RED};
          font-size: 44px;
          font-weight: 900;
          letter-spacing: 0.06em;
          line-height: 1.1;
          opacity: 0.92;
        }}
        .s2-drucker {{
          position: absolute;
          left: 290px;
          top: {slot - 10}px;
          width: 660px;
          height: 190px;
        }}'''
    bon_rows = []
    n_posten = 0
    for r in rows:
        if r[0] == "kopf":
            bon_rows.append(f'<div class="s2-reihe kopf" style="top: {r[1]}px; height: {r[2]}px"><span class="s2-txt">{TEXT["bon_kopf"]}</span></div>')
            bon_rows.append(f'<div class="s2-stempel" id="s2-stempel">{TEXT["stempel"]}</div>')
        elif r[0] == "linie":
            bon_rows.append(f'<div class="s2-trenn" style="top: {r[1]}px"></div>')
        elif r[0] == "posten":
            txt = "<br />".join(r[4])
            if n_posten:
                bon_rows.append(f'<div class="s2-fein" style="top: {r[1]}px"></div>')
            bon_rows.append(f'<div class="s2-reihe" style="top: {r[1]}px; height: {r[2]}px">{icon(r[3], 42)}<span class="s2-txt">{txt}</span></div>')
            n_posten += 1
        elif r[0] == "summe":
            bon_rows.append(f'<div class="s2-reihe summe" style="top: {r[1]}px; height: {r[2]}px"><span class="s2-txt">{TEXT["summe"]}</span><span class="s2-frage" id="s2-frage">?</span></div>')
    drucker = (f'<svg class="s2-drucker" id="s2-drucker" viewBox="0 0 660 190" aria-hidden="true">'
               f'<rect x="0" y="10" width="660" height="180" rx="28" fill="{INK}" />'
               f'<rect x="22" y="0" width="616" height="26" rx="13" fill="#20282e" />'
               f'<rect x="44" y="11" width="572" height="5" rx="2.5" fill="#0f1417" /></svg>')
    body = (photo_html(p, "kosten.jpg", [0, 1]) + f'\n        <div class="{p}-strich"></div>\n' + head_html(p, lines, 2) + "\n"
            + f'        <div class="s2-fenster">\n          <div class="s2-bonflug" id="s2-bonflug" style="position: absolute; inset: 0">\n'
            + f'            <div class="s2-schatten" id="s2-schatten"></div>\n'
            + f'            <div class="s2-bon" id="s2-bon">\n              ' + "\n              ".join(bon_rows) + "\n            </div>\n"
            + "          </div>\n        </div>\n        " + drucker + "\n")
    js = [push_in(p, BY_ID["s2-kosten"]["dur"], 1.04)]
    js.append(f'tl.fromTo("#s2-l2w0", {{ y: {aber_dy}, scale: {aber_scale:.4f} }}, {{ y: 0, scale: 1, duration: 0.45, ease: "power3.inOut" }}, 0);')
    for k, sel in enumerate(["#s2-l0w0", "#s2-l1w0", "#s2-l1w1"]):
        js.append(blur_in(sel, 0.1 + 0.07 * k))
    for k, sel in enumerate(["#s2-l2w1", "#s2-l2w2", "#s2-l3w0"]):
        js.append(blur_in(sel, 0.5 + 0.07 * k))
    js.append('tl.fromTo("#s2-drucker", { y: 700 }, { y: 0, duration: 0.4, ease: "power3.out" }, 0.15);')
    # Bon: Papier und Schatten rücken gemeinsam vor
    js.append(f'tl.set(["#s2-bon", "#s2-schatten"], {{ y: {bon_h} }}, 0);')
    for k, (ts, v) in enumerate(steps):
        js.append(f'tl.to(["#s2-bon", "#s2-schatten"], {{ y: {bon_h - v}, duration: 0.13, ease: "power2.out" }}, {ts:.3f});')
        if k == 0:
            js.append('tl.fromTo("#s2-stempel", { opacity: 0, scale: 1.6, rotation: -16, filter: "blur(6px)" }, '
                      '{ opacity: 0.92, scale: 1, rotation: -8, filter: "blur(0px)", duration: 0.16, ease: "expo.out" }, 1.125);')
    js.append(f'tl.fromTo("#s2-frage", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.2)" }}, {t_sum:.3f});')
    # Abgang: Bon reißt ab und fliegt nach oben weg
    js.append('tl.to("#s2-bonflug", { y: -16, duration: 0.06, ease: "power2.out" }, 4.2);')
    js.append('tl.to("#s2-bonflug", { y: -1500, x: 240, rotation: 14, duration: 0.26, ease: "power2.in" }, 4.26);')
    js.append('tl.to("#s2-drucker", { y: 320, duration: 0.22, ease: "power2.in" }, 4.26);')
    js.append(blur_out(word_ids(p, lines), 4.22))
    files["compositions/s2-kosten.html"] = scene("s2-kosten", css, body, js)

    # ---------------------------------------------------------------- s3: Aufgabe (Waage kippt)
    p, lines = "s3", TEXT["aufgabe"]
    size3 = min(104, M.fit(lines, W - X0 - 72, 800, 104))
    widest = max(M.width(t, 40, 500) for _, t in TEXT["lasten"] + TEXT["optionen"]) + 60 + 22
    report.append(f"s3/s4: Überschrift {size3} px, längste Listenzeile {widest:.0f} px (bis x {X0 + widest:.0f})")
    css = head_css(p, size3) + "\n" + scale_css(p, 0) + "\n" + list_css(p, LIST_TOP, LIST_PITCH, "rund")
    body = (f'        <div class="{p}-strich"></div>\n' + head_html(p, lines, 1) + "\n"
            + list_html(p, TEXT["lasten"], LIST_TOP, LIST_PITCH) + "\n"
            + scale_html(p, 0, RIGHT_LOAD, []) + "\n")
    js = []
    js.append('tl.fromTo(".s3-strich", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, 0);')
    t = 0.05
    for sel in word_ids(p, lines):
        js.append(f'tl.fromTo("{sel}", {{ y: -44, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.24, ease: "power3.out" }}, {t:.3f});')
        t += 0.06
    lands = [0.3, 0.75, 1.5, 2.25, 3.0]
    for k, (tl_, ang) in enumerate(zip(lands, ANGLES_S3)):
        js.append(drop(p, "r", k, tl_, 0.26 if k == 0 else 0.3))
        nxt = lands[k + 1] if k + 1 < len(lands) else tl_ + 0.9
        js.append(tip(p, ang, tl_, min(0.85, nxt - tl_ - 0.01)))
        if k >= 1:
            j = k - 1
            js.append(f'tl.fromTo("#{p}-i{j}", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {tl_:.3f});')
            js.append(f'tl.fromTo("#{p}-t{j}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.32, ease: "power3.out" }}, {tl_ + 0.04:.3f});')
    js.append(blur_out(word_ids(p, lines) + [f"#{p}-z{k}" for k in range(4)], 4.2, 0.22))
    files["compositions/s3-aufgabe.html"] = scene("s3-aufgabe", css, body, js)

    # ---------------------------------------------------------------- s4: Optionen (Waage kommt ins Gleichgewicht)
    p, lines = "s4", TEXT["optionen_titel"]
    size4 = min(104, M.fit(lines, W - X0 - 72, 800, 104))
    css = head_css(p, size4) + f'''
        .s4-maske {{
          display: block;
          overflow: hidden;
          padding: 0.06em 0 0.24em;
          margin: -0.06em 0 -0.24em;
        }}
        .s4-ch {{
          display: inline-block;
        }}
        .s4-marker {{
          position: absolute;
          left: -10px;
          top: 2px;
          height: 56px;
          background: {RED};
          border-radius: 6px;
        }}
''' + scale_css(p, ANGLES_S3[-1]) + "\n" + list_css(p, LIST_TOP, LIST_PITCH, "eckig")
    title = [f'        <div class="{p}-kopf">']
    for k, line in enumerate(lines):
        chars = "".join(f'<span class="s4-ch" id="s4-l{k}c{i}">{"&nbsp;" if ch == " " else ch}</span>' for i, ch in enumerate(line))
        title.append(f'          <span class="{p}-zeile s4-maske{" rot" if k == 1 else ""}">{chars}</span>')
    title.append("        </div>")
    body = (f'        <div class="{p}-strich"></div>\n' + "\n".join(title) + "\n"
            + list_html(p, TEXT["optionen"], LIST_TOP, LIST_PITCH, with_marker=True) + "\n"
            + scale_html(p, ANGLES_S3[-1], RIGHT_LOAD, LEFT_LOAD) + "\n")
    js = []
    t = 0.05
    for k, line in enumerate(lines):
        for i, _ in enumerate(line):
            js.append(f'tl.fromTo("#s4-l{k}c{i}", {{ yPercent: 112 }}, {{ yPercent: 0, duration: 0.42, ease: "expo.out" }}, {t:.3f});')
            t += 0.022
    lands = [0.75, 1.5, 2.25, 3.0]
    for k, (tl_, ang) in enumerate(zip(lands, ANGLES_S4)):
        js.append(drop(p, "l", k, tl_))
        nxt = lands[k + 1] if k + 1 < len(lands) else tl_ + 0.9
        js.append(tip(p, ang, tl_, min(0.85, nxt - tl_ - 0.01)))
        # roter Marker wischt über die Zeile und gibt sie frei
        js.append(f'tl.fromTo("#s4-m{k}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.16, ease: "power2.in" }}, {tl_:.3f});')
        js.append(f'tl.to("#s4-m{k}", {{ clipPath: "inset(0% 0% 0% 100%)", duration: 0.2, ease: "power2.out" }}, {tl_ + 0.17:.3f});')
        js.append(f'tl.fromTo(["#s4-i{k}", "#s4-t{k}"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.04, ease: "none" }}, {tl_ + 0.15:.3f});')
    # Gleichgewicht: das Lot pulst, wenn der Zeiger es trifft
    js.append('tl.fromTo("#s4-lot", { scaleY: 1 }, { scaleY: 1.9, duration: 0.14, ease: "power2.out", transformOrigin: "50% 100%" }, 3.6);')
    js.append('tl.to("#s4-lot", { scaleY: 1, duration: 0.3, ease: "power2.inOut" }, 3.75);')
    js.append(blur_out([f"#s4-l{k}c{i}" for k, line in enumerate(lines) for i, _ in enumerate(line)] + [f"#s4-z{k}" for k in range(4)], 4.95, 0.22))
    files["compositions/s4-optionen.html"] = scene("s4-optionen", css, body, js)

    # ---------------------------------------------------------------- s5: Expertin
    p, lines = "s5", TEXT["zitat"]
    size5 = min(86, M.fit(lines, W - X0 - 72, 800, 86))
    q_lh = 1.04
    name_top = 1036
    veils = [(434, 600, 646, 250, "180deg", 10), (430, 610, 250, 1310, "90deg", 12)]
    css = head_css(p, size5) + f'''
        .s5-kopf {{
          line-height: {q_lh};
        }}
        #s5-l2w0 {{
          transform-origin: 0% 60%;
        }}
        .s5-strich2 {{
          position: absolute;
          left: {X0}px;
          top: {name_top - 30}px;
          width: 70px;
          height: 7px;
          background: {RED};
          transform-origin: 0 50%;
        }}
        .s5-name {{
          position: absolute;
          left: {X0}px;
          top: {name_top}px;
          font-size: 46px;
          font-weight: 800;
          line-height: 1.15;
          white-space: nowrap;
        }}
        .s5-funktion {{
          position: absolute;
          left: {X0}px;
          top: {name_top + 64}px;
          font-size: 32px;
          font-weight: 500;
          line-height: 1.3;
        }}
        .s5-funktion span {{
          display: block;
          white-space: nowrap;
        }}
''' + photo_css(p, 646, 1310, 434, 610, veils, "50% 35%")
    body = (photo_html(p, "andrea.jpg", veils) + f'\n        <div class="{p}-strich"></div>\n' + head_html(p, lines, 2) + "\n"
            + f'        <div class="s5-strich2" id="s5-strich2"></div>\n'
            + f'        <div class="s5-name" id="s5-name">{TEXT["name"]}</div>\n'
            + '        <div class="s5-funktion">' + "".join(f'<span id="s5-f{k}">{t}</span>' for k, t in enumerate(TEXT["funktion"])) + "</div>\n")
    js = [push_in(p, BY_ID["s5-expertin"]["dur"], 1.04)]
    js.append('tl.fromTo(".s5-strich", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, 0);')
    t = 0.2
    for sel in word_ids(p, lines[:2]):
        js.append(blur_in(sel, t))
        t += 0.07
    js.append(slam("#s5-l2w0", 1.5))  # auf dem Schlag
    t = 1.64
    for k in (2, 3):
        for i, _ in enumerate(lines[k].split(" ")):
            if (k, i) != (2, 0):
                js.append(blur_in(f"#s5-l{k}w{i}", t))
                t += 0.07
    js.append('tl.fromTo("#s5-strich2", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, 2.4);')
    js.append(blur_in("#s5-name", 2.5, 0.2))
    js.append(blur_in("#s5-f0", 2.64))
    js.append(blur_in("#s5-f1", 2.72))
    js.append(blur_out(word_ids(p, lines) + ["#s5-strich2", "#s5-name", "#s5-f0", "#s5-f1"], 5.0))
    files["compositions/s5-expertin.html"] = scene("s5-expertin", css, body, js)
    report.append(f"s5: Zitat {size5} px")

    # ---------------------------------------------------------------- s6: Ende
    p, lines = "s6", TEXT["ende"]
    size6 = min(112, M.fit(lines, W - X0 - 72, 800, 112))
    head_bottom = HEAD_TOP + len(lines) * size6
    knopf_top = head_bottom + 50
    tw = max(M.width(t, 42, 800) for t in TEXT["knopf"])
    knopf_w = 36 + 56 + 24 + tw + 44
    knopf_h = 150
    logo_w = 560
    k_logo = logo_w / 452
    mark = 100 * k_logo
    logo_top = knopf_top + knopf_h + 70
    veils = [(113, 550, 967, 260, "180deg", 14), (110, 560, 430, 1360, "90deg", 30)]
    css = head_css(p, size6) + f'''
        .s6-maske {{
          display: block;
          overflow: hidden;
          padding: 0.06em 0 0.24em;
          margin: -0.06em 0 -0.24em;
        }}
        .s6-innen {{
          display: inline-block;
        }}
        .s6-knopf {{
          position: absolute;
          left: {X0}px;
          top: {knopf_top}px;
          width: {knopf_w:.0f}px;
          height: {knopf_h}px;
          border-radius: 26px;
          background: {RED};
          color: #ffffff;
          display: flex;
          align-items: center;
          gap: 24px;
          padding-left: 36px;
          box-shadow: 0 14px 30px rgba(202, 44, 53, 0.28);
        }}
        .s6-knopf span {{
          display: block;
          white-space: nowrap;
          font-size: 42px;
          font-weight: 800;
          line-height: 1.14;
        }}
        .s6-facet {{
          position: absolute;
        }}
        .s6-facet svg,
        .s6-wort svg {{
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }}
        .s6-wort {{
          position: absolute;
          left: {X0 + 120 * k_logo:.1f}px;
          top: {logo_top}px;
          width: {340 * k_logo:.1f}px;
          height: {mark:.1f}px;
        }}
        .s6-wort text {{
          font-family: "Montserrat", sans-serif;
          fill: {INK};
        }}
''' + photo_css(p, 967, 1360, 113, 560, veils, "60% 55%")
    title = [f'        <div class="{p}-kopf">']
    for k, line in enumerate(lines):
        title.append(f'          <span class="{p}-zeile s6-maske{" rot" if k == 2 else ""}"><span class="s6-innen" id="s6-z{k}">{line}</span></span>')
    title.append("        </div>")
    facets = []
    fjs = []
    for n, f in enumerate(FACETS):
        cx, cy = centroid(f["pts"])
        facets.append(f'        <div class="s6-facet" id="s6-f{f["key"]}" style="left: {X0}px; top: {logo_top}px; width: {mark:.1f}px; '
                      f'height: {mark:.1f}px; transform-origin: {cx:.2f}% {cy:.2f}%">{facet_svg(f, "s6-g" + f["key"])}</div>')
        dx, dy, rot = f["from"]
        fjs.append(f'tl.fromTo("#s6-f{f["key"]}", {{ x: {dx}, y: {dy}, rotation: {rot}, opacity: 0 }}, '
                   f'{{ x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.42, ease: "power3.out" }}, {1.08 + 0.04 * n:.3f});')
    body = (photo_html(p, "tisch.jpg", veils) + f'\n        <div class="{p}-strich"></div>\n' + "\n".join(title) + "\n"
            + f'        <div class="s6-knopf" id="s6-knopf">{icon("link", 56, "#ffffff", 3.4)}<div>'
            + "".join(f"<span>{t}</span>" for t in TEXT["knopf"]) + "</div></div>\n"
            + "\n".join(facets) + "\n"
            + f'        <div class="s6-wort" id="s6-wort"><svg viewBox="120 0 340 100" aria-hidden="true">{WORDMARK}</svg></div>\n')
    js = [push_in(p, BY_ID["s6-ende"]["dur"], 1.04)]
    js.append('tl.fromTo(".s6-strich", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, 0);')
    for k in range(len(lines)):
        js.append(f'tl.fromTo("#s6-z{k}", {{ yPercent: 112 }}, {{ yPercent: 0, duration: 0.45, ease: "expo.out" }}, {0.05 + 0.08 * k:.3f});')
    js.append('tl.fromTo("#s6-knopf", { clipPath: "inset(0% 100% 0% 0% round 26px)" }, { clipPath: "inset(0% 0% 0% 0% round 26px)", duration: 0.36, ease: "power3.out" }, 0.62);')
    js += fjs
    js.append('tl.fromTo("#s6-wort", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }, 1.5);')
    files["compositions/s6-ende.html"] = scene("s6-ende", css, body, js)
    report.append(f"s6: Überschrift {size6} px, Knopf {knopf_w:.0f}×{knopf_h} bei y {knopf_top}, Logo bei y {logo_top:.0f}")

    # ---------------------------------------------------------------- index.html
    hosts = [f'      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
             f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="1" data-track-kind="graphics" '
             f'data-width="{W}" data-height="{H}"></div>' for s in SCENES]
    files["index.html"] = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>KNIGGE Immobilien – Das Haus ist abbezahlt. (Instagram-Reel)</title>
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
      KNIGGE Immobilien – Instagram-Reel „Das Haus ist abbezahlt.“ (1080×1920, 27,75 s, KNIGGE-Musik)
      erzeugt von tools/build_reel.py – Texte dort in TEXT ändern
    -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="{W}" data-height="{H}" data-fps="{FPS}" data-motion-blur="on">
{chr(10).join(hosts)}
      <audio id="musik" class="clip" src="assets/audio/knigge-theme-reel.m4a" data-start="0" data-duration="{DURATION}" data-track-index="2" data-volume="1"></audio>
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
    for line in report:
        print(" ", line)


if __name__ == "__main__":
    build()
