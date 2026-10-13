#!/usr/bin/env python3
"""Erzeugt die Standort-Animationen (transparenter Hintergrund) als HyperFrames-Kompositionen.

    index.html                              Bergisch Gladbach (Hauptsitz)          1200×680
    formats/koeln.html                      Köln (Standort Sachsenring)            1200×680
    formats/wipperfuerth.html               Wipperfürth (Oberbergischer Kreis)     1200×680
    formats/rheinisch-bergischer-kreis.html Rheinisch-Bergischer Kreis             1200×680
    formats/einzugsgebiet.html              alles zusammen um das KNIGGE-Logo      1920×1080

Orte ändern: in REGIONS bzw. COMBINED die Namen tauschen (Reihenfolge im Uhrzeigersinn, Winkel in
Grad ab Norden), dann `python3 tools/build.py` und `bash tools/export.sh`.

Die Animation nutzt nur Skalieren, Verschieben und Strich-Zeichnen – keine Deckkraft-Blenden –,
damit das GIF (nur „sichtbar“ oder „transparent“ je Pixel) sauber bleibt.
"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 25
EIGHT = [0, 45, 90, 135, 180, 225, 270, 315]
EIGHT_TURNED = [337.5, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5]

# ---------------------------------------------------------------------------------------------
# Einzel-Animationen (1200×680)
# ---------------------------------------------------------------------------------------------
SINGLE = {"W": 1200, "H": 680, "CX": 600, "CY": 340, "RX": 425, "RY": 250, "duration": 7.2}

REGIONS = {
    "index.html": {
        "title": "Bergisch Gladbach",
        "hub": "Bergisch Gladbach",
        "places": ["Paffrath", "Herkenrath", "Moitzfeld", "Bensberg", "Frankenforst", "Refrath", "Köln-Ost", "Schildgen"],
        "angles": EIGHT,
    },
    "formats/koeln.html": {
        "title": "Köln",
        "hub": "Köln",
        "places": ["Nippes", "Mülheim", "Kalk", "Porz", "Rodenkirchen", "Lindenthal", "Ehrenfeld", "Chorweiler"],
        "angles": EIGHT,
    },
    "formats/wipperfuerth.html": {
        "title": "Wipperfürth · Oberbergischer Kreis",
        "hub": "Wipperfürth",
        "places": ["Radevormwald", "Marienheide", "Bergneustadt", "Gummersbach", "Wiehl", "Engelskirchen", "Lindlar", "Hückeswagen"],
        "angles": EIGHT,
    },
    # Kreisstadt Bergisch Gladbach + die sieben übrigen Kreis-Kommunen; Ring um 22,5° gedreht,
    # damit die Himmelsrichtungen gut passen (kein Ort genau im Osten)
    "formats/rheinisch-bergischer-kreis.html": {
        "title": "Rheinisch-Bergischer Kreis",
        "hub": "Rheinisch-Bergischer Kreis",
        "hub_size": 32,
        "places": ["Burscheid", "Wermelskirchen", "Kürten", "Overath", "Rösrath", "Bergisch Gladbach", "Odenthal", "Leichlingen"],
        "angles": EIGHT_TURNED,
    },
}

# ---------------------------------------------------------------------------------------------
# Gesamtes Einzugsgebiet (1920×1080): KNIGGE-Logo in der Mitte, vier Gruppen rundherum
# W Köln · N Rheinisch-Bergischer Kreis · O Oberbergischer Kreis (Wipperfürth) · S Bergisch Gladbach
# ---------------------------------------------------------------------------------------------
COMBINED = {
    "file": "formats/einzugsgebiet.html",
    "title": "Einzugsgebiet",
    "W": 1920,
    "H": 1080,
    "duration": 10.2,
    "logo": (960, 540, 370),  # Mitte x, y, Breite (Logo sitzt auf einer weißen Karte)
    "clusters": [
        {
            "hub": "Köln",
            "c": (390, 560),
            "rx": 245,
            "ry": 165,
            "places": ["Chorweiler", "Nippes", "Mülheim", "Kalk", "Porz", "Rodenkirchen", "Lindenthal", "Ehrenfeld"],
            "angles": EIGHT_TURNED,
        },
        {
            "hub": "Rheinisch-Bergischer Kreis",
            "c": (960, 205),
            "rx": 345,
            "ry": 118,
            "places": ["Burscheid", "Wermelskirchen", "Kürten", "Overath", "Rösrath", "Odenthal", "Leichlingen"],
            "angles": [335, 18, 68, 122, 160, 245, 292],
        },
        {
            "hub": "Wipperfürth",
            "caption": "Oberbergischer Kreis",
            "c": (1535, 560),
            "rx": 265,
            "ry": 165,
            "places": ["Hückeswagen", "Radevormwald", "Marienheide", "Bergneustadt", "Gummersbach", "Wiehl", "Engelskirchen", "Lindlar"],
            "angles": [292.5, 330, 30, 67.5, 112.5, 157.5, 202.5, 247.5],
        },
        {
            "hub": "Bergisch Gladbach",
            "caption": "Hauptsitz",
            "c": (960, 860),
            "rx": 345,
            "ry": 118,
            "places": ["Schildgen", "Paffrath", "Herkenrath", "Moitzfeld", "Bensberg", "Frankenforst", "Refrath"],
            "angles": [292.5, 337.5, 67.5, 112.5, 157.5, 202.5, 247.5],
        },
    ],
}


def ring_points(cx, cy, rx, ry, angles):
    pts = []
    for deg in angles:
        a = math.radians(deg)
        pts.append((round(cx + rx * math.sin(a), 1), round(cy - ry * math.cos(a), 1)))
    return pts


PIN_PATH = '<path d="M12 29 C12 29 2 17.5 2 11 A10 10 0 0 1 22 11 C22 17.5 12 29 12 29 Z" fill="#ca2c35" stroke="#6d131b" stroke-width="1.2" /><circle cx="12" cy="11" r="4" fill="#ffffff" />'

LOGO_SVG = '''<svg viewBox="0 0 452 100" role="img" aria-label="KNIGGE Immobilien">
          <defs>
            <linearGradient id="k-a" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="48.9" y2="39.6">
              <stop offset="0" stop-color="#5e0f18" />
              <stop offset="0.56" stop-color="#a4222b" />
              <stop offset="0.8" stop-color="#c12a33" />
              <stop offset="0.93" stop-color="#ca2c35" />
            </linearGradient>
            <linearGradient id="k-r" gradientUnits="userSpaceOnUse" x1="47.5" y1="40.2" x2="100" y2="0">
              <stop offset="0" stop-color="#4a0a13" />
              <stop offset="1" stop-color="#b0252e" />
            </linearGradient>
            <linearGradient id="k-b" gradientUnits="userSpaceOnUse" x1="0" y1="100" x2="100" y2="100">
              <stop offset="0" stop-color="#480a12" />
              <stop offset="0.5" stop-color="#a2222b" />
              <stop offset="0.85" stop-color="#ca2c35" />
            </linearGradient>
          </defs>
          <path id="lf-a" d="M0 0 H79.5 L0 100 Z" fill="url(#k-a)" />
          <path id="lf-r" d="M79.5 0 H100 V100 L47.5 40.2 Z" fill="url(#k-r)" />
          <path id="lf-b" d="M0 100 L47.5 40.2 L100 100 Z" fill="url(#k-b)" />
          <text class="word" x="125.2" y="53" font-size="77" font-weight="700" textLength="328.5" lengthAdjust="spacing">KNIGGE</text>
          <text class="word" x="125.5" y="100" font-size="44.3" font-weight="400" textLength="330.5" lengthAdjust="spacing">IMMOBILIEN</text>
        </svg>'''


def css(W, H, s):
    """Gemeinsame Gestaltung; s = Größen (pill, hub, pin, line)."""
    return f'''      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: {W}px;
        height: {H}px;
        overflow: hidden;
        background: transparent;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: transparent;
        font-family: "Montserrat", sans-serif;
        color: #444f4f;
      }}
      .lines,
      .rings {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        overflow: visible;
      }}
      .lines path {{
        fill: none;
        stroke: #aab3b0;
        stroke-width: {s["line"]};
        stroke-linecap: round;
        stroke-dasharray: 1 2;
        stroke-dashoffset: 1.05;
      }}
      .lines path.cn {{
        stroke: #ca2c35;
        stroke-width: {s["line"] + 1.5};
      }}
      .rings circle {{
        fill: none;
        stroke: #ca2c35;
      }}
      .pos {{
        position: absolute;
        transform: translate(-50%, -50%);
      }}
      .pill,
      .hub,
      .logo {{
        will-change: transform; /* eigene Ebene: Graustufen-Kantenglättung statt farbiger Subpixel-Ränder */
      }}
      .pill {{
        display: block;
        white-space: nowrap;
        font-size: {s["pill"]}px;
        font-weight: 700;
        line-height: 1.2;
        color: #444f4f;
        background: #ffffff;
        border: {s["border"]}px solid #444f4f;
        border-radius: {s["radius"]}px;
        padding: {s["pad_v"]}px {s["pad_h"]}px {s["pad_v"] + 1}px;
      }}
      .pin {{
        position: absolute;
        width: {s["pin_w"]}px;
        height: {s["pin_h"]}px;
        overflow: visible;
      }}
      .hubpos {{
        position: absolute;
        transform: translateX(-50%);
        display: flex;
        flex-direction: column;
        align-items: center;
      }}
      .hub {{
        display: block;
        white-space: nowrap;
        font-size: {s["hub"]}px;
        font-weight: 700;
        line-height: 1.2;
        color: #ffffff;
        background: #ca2c35;
        border-radius: {s["radius"]}px;
        padding: {s["hub_pad_v"]}px {s["hub_pad_h"]}px {s["hub_pad_v"] + 1}px;
      }}
      .cap {{
        display: block;
        margin-top: 4px;
        white-space: nowrap;
        font-size: {s.get("cap", 16)}px;
        font-weight: 700;
        line-height: 1.2;
        color: #444f4f;
        background: #ffffff;
        border-radius: 6px;
        padding: 2px 8px 3px;
        will-change: transform;
      }}
      .logo {{
        position: absolute;
        background: #ffffff;
        border: {s["border"]}px solid #444f4f;
        border-radius: 14px;
      }}
      .logo svg {{
        display: block;
        width: 100%;
        height: 100%;
        overflow: visible;
      }}
      .word {{
        font-family: "Montserrat", sans-serif;
        fill: #444f4f;
      }}'''


def pin_markup(pid, cx, cy, s):
    left = cx - s["pin_w"] / 2
    top = cy - s["pin_h"] * 29 / 30
    return f'<svg class="pin" id="{pid}" style="left: {left:.1f}px; top: {top:.1f}px" viewBox="0 0 24 30" aria-hidden="true">{PIN_PATH}</svg>'


def head(W, H, title, s):
    return f'''<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>KNIGGE Immobilien – {title} (transparent)</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{css(W, H, s)}
    </style>
  </head>
  <body>
    <!--
      KNIGGE Immobilien – {title} (transparenter Hintergrund)
      erzeugt von tools/build.py – Namen dort ändern, nicht hier
    -->'''


SINGLE_SIZES = {"pill": 30, "border": 3, "radius": 10, "pad_v": 8, "pad_h": 21, "hub": 34, "hub_pad_v": 9,
                "hub_pad_h": 27, "pin_w": 86, "pin_h": 106, "line": 3}
COMBINED_SIZES = {"pill": 22, "border": 2.5, "radius": 8, "pad_v": 6, "pad_h": 15, "hub": 26, "hub_pad_v": 7,
                  "hub_pad_h": 20, "pin_w": 58, "pin_h": 72, "line": 2.5, "cap": 16}


def single_page(region):
    g = SINGLE
    s = dict(SINGLE_SIZES)
    if region.get("hub_size"):
        s["hub"] = region["hub_size"]
    W, H, CX, CY = g["W"], g["H"], g["CX"], g["CY"]
    pts = ring_points(CX, CY, g["RX"], g["RY"], region["angles"])
    lines = "\n".join(f'        <path id="ln{k}" pathLength="1" d="M{CX} {CY} L{x} {y}" />' for k, (x, y) in enumerate(pts))
    pills = "\n".join(
        f'      <div class="pos" style="left: {x}px; top: {y}px"><span class="pill" id="p{k}">{name}</span></div>'
        for k, ((x, y), name) in enumerate(zip(pts, region["places"]))
    )
    n = len(pts)
    return f'''{head(W, H, region["title"], s)}
    <div id="root" data-composition-id="main" data-start="0" data-duration="{g["duration"]}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <svg class="lines" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
{lines}
      </svg>
      <svg class="rings" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
        <circle id="r1" cx="{CX}" cy="{CY}" r="20" stroke-width="0" />
        <circle id="r2" cx="{CX}" cy="{CY}" r="20" stroke-width="0" />
        <circle id="r3" cx="{CX}" cy="{CY}" r="20" stroke-width="0" />
      </svg>
{pills}
      {pin_markup("pin", CX, CY, s)}
      <div class="hubpos" style="left: {CX}px; top: {CY + 14}px"><span class="hub" id="hub">{region["hub"]}</span></div>
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});

        // Pin landet, Ortsname erscheint
        tl.fromTo("#pin", {{ y: -70, scale: 0 }}, {{ y: 0, scale: 1, duration: 0.7, ease: "bounce.out", transformOrigin: "50% 100%" }}, 0.15);
        tl.fromTo("#hub", {{ scale: 0 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)", transformOrigin: "50% 0%" }}, 0.55);

        // Ringwellen: erst beim Start sichtbar (vorher Strichstärke 0), wachsen und werden dünner (statt auszublenden)
        [["#r1", 0.65], ["#r2", 1.2], ["#r3", 3.9]].forEach(([r, t]) => {{
          tl.fromTo(r, {{ attr: {{ r: 20 }}, strokeWidth: 0 }}, {{ strokeWidth: 6, duration: 0.04, ease: "none" }}, t);
          tl.to(r, {{ attr: {{ r: 190 }}, strokeWidth: 0, duration: 1.6, ease: "power2.out" }}, t + 0.04);
        }});

        // Orte erscheinen reihum, Verbindungen zeichnen sich
        for (let k = 0; k < {n}; k++) {{
          const t = 0.8 + k * 0.17;
          tl.fromTo("#ln" + k, {{ strokeDashoffset: 1.05 }}, {{ strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }}, t);
          tl.fromTo("#p" + k, {{ scale: 0 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2.2)" }}, t + 0.22);
        }}

        // Abbau für die Schleife (umgekehrte Reihenfolge)
        for (let k = {n - 1}; k >= 0; k--) {{
          const t = 5.9 + ({n - 1} - k) * 0.05;
          tl.to("#p" + k, {{ scale: 0, duration: 0.3, ease: "back.in(1.6)" }}, t);
          tl.to("#ln" + k, {{ strokeDashoffset: 1.05, duration: 0.35, ease: "power2.in" }}, t + 0.1);
        }}
        tl.to("#hub", {{ scale: 0, duration: 0.3, ease: "back.in(1.6)" }}, 6.45);
        tl.to("#pin", {{ y: -40, scale: 0, duration: 0.35, ease: "back.in(1.4)" }}, 6.5);

        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''


def combined_page(spec):
    s = COMBINED_SIZES
    W, H = spec["W"], spec["H"]
    lx, ly, lw = spec["logo"]
    lh = lw * 100 / 452
    lines, rings, pills, pins, hubs = [], [], [], [], []
    counts = []
    for i, cl in enumerate(spec["clusters"]):
        cx, cy = cl["c"]
        lines.append(f'        <path class="cn" id="cn{i}" pathLength="1" d="M{lx} {ly} L{cx} {cy}" />')
        pts = ring_points(cx, cy, cl["rx"], cl["ry"], cl["angles"])
        counts.append(len(pts))
        for k, ((x, y), name) in enumerate(zip(pts, cl["places"])):
            lines.append(f'        <path id="l{i}_{k}" pathLength="1" d="M{cx} {cy} L{x} {y}" />')
            pills.append(f'      <div class="pos" style="left: {x}px; top: {y}px"><span class="pill" id="p{i}_{k}">{name}</span></div>')
        rings.append(f'        <circle id="r{i}" cx="{cx}" cy="{cy}" r="14" stroke-width="0" />')
        pins.append("      " + pin_markup(f"pin{i}", cx, cy, s))
        cap = f'<span class="cap" id="cap{i}">{cl["caption"]}</span>' if cl.get("caption") else ""
        hubs.append(f'      <div class="hubpos" style="left: {cx}px; top: {cy + 10}px"><span class="hub" id="hub{i}">{cl["hub"]}</span>{cap}</div>')
    caps = [i for i, cl in enumerate(spec["clusters"]) if cl.get("caption")]
    nl = "\n"
    return f'''{head(W, H, spec["title"], s)}
    <div id="root" data-composition-id="main" data-start="0" data-duration="{spec["duration"]}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <svg class="lines" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
{nl.join(lines)}
      </svg>
      <svg class="rings" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
{nl.join(rings)}
      </svg>
{nl.join(pills)}
{nl.join(pins)}
{nl.join(hubs)}
      <div class="logo" id="logo" style="left: {lx - lw / 2 - 28:.1f}px; top: {ly - lh / 2 - 24:.1f}px; padding: 22px 26px; width: {lw + 56}px; height: {lh + 48:.1f}px">
        {LOGO_SVG}
      </div>
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const counts = {counts};
        const caps = {caps};

        // KNIGGE in der Mitte
        tl.fromTo("#logo", {{ scale: 0 }}, {{ scale: 1, duration: 0.6, ease: "back.out(1.8)" }}, 0.15);

        // Verbindung zu den vier Gebieten, Pins landen (W, N, O, S)
        counts.forEach((n, i) => {{
          const t = 0.6 + i * 0.14;
          tl.fromTo("#cn" + i, {{ strokeDashoffset: 1.05 }}, {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }}, t);
          tl.fromTo("#pin" + i, {{ y: -50, scale: 0 }}, {{ y: 0, scale: 1, duration: 0.6, ease: "bounce.out", transformOrigin: "50% 100%" }}, t + 0.35);
          tl.fromTo("#hub" + i, {{ scale: 0 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2)", transformOrigin: "50% 0%" }}, t + 0.6);
          tl.fromTo("#r" + i, {{ attr: {{ r: 14 }}, strokeWidth: 0 }}, {{ strokeWidth: 5, duration: 0.04, ease: "none" }}, t + 0.65);
          tl.to("#r" + i, {{ attr: {{ r: 130 }}, strokeWidth: 0, duration: 1.4, ease: "power2.out" }}, t + 0.69);
        }});
        caps.forEach((i) => tl.fromTo("#cap" + i, {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)", transformOrigin: "50% 0%" }}, 0.6 + i * 0.14 + 0.8));

        // Orte je Gebiet
        counts.forEach((n, i) => {{
          const base = 1.5 + i * 0.5;
          for (let k = 0; k < n; k++) {{
            const t = base + k * 0.08;
            tl.fromTo("#l" + i + "_" + k, {{ strokeDashoffset: 1.05 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, t);
            tl.fromTo("#p" + i + "_" + k, {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2.2)" }}, t + 0.18);
          }}
        }});
        // Halten ohne Bewegung: hält das GIF klein und ruhig zum Lesen

        // Abbau für die Schleife
        counts.forEach((n, i) => {{
          for (let k = 0; k < n; k++) {{
            const t = 8.6 + i * 0.08 + k * 0.03;
            tl.to("#p" + i + "_" + k, {{ scale: 0, duration: 0.28, ease: "back.in(1.6)" }}, t);
            tl.to("#l" + i + "_" + k, {{ strokeDashoffset: 1.05, duration: 0.3, ease: "power2.in" }}, t + 0.08);
          }}
          tl.to("#hub" + i, {{ scale: 0, duration: 0.28, ease: "back.in(1.6)" }}, 9.15 + i * 0.05);
          tl.to("#pin" + i, {{ y: -30, scale: 0, duration: 0.3, ease: "back.in(1.4)" }}, 9.2 + i * 0.05);
          tl.to("#cn" + i, {{ strokeDashoffset: 1.05, duration: 0.35, ease: "power2.in" }}, 9.3 + i * 0.05);
        }});
        caps.forEach((i) => tl.to("#cap" + i, {{ scale: 0, duration: 0.25, ease: "back.in(1.6)" }}, 9.1 + i * 0.05));
        tl.to("#logo", {{ scale: 0, duration: 0.35, ease: "back.in(1.4)" }}, 9.6);

        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("geschrieben:", rel)


def main():
    for rel, region in REGIONS.items():
        write(rel, single_page(region))
    write(COMBINED["file"], combined_page(COMBINED))


if __name__ == "__main__":
    main()
