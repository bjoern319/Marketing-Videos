#!/usr/bin/env python3
"""Erzeugt die Karten-Animationen (Stil: graue Flächen, weiße Grenzen, blauer Rhein, Standort-Marker
und KNIGGE-Logo) als HyperFrames-Kompositionen mit transparentem Hintergrund.

Kartengrundlage: assets/geo/region.json (siehe tools/geo/prepare.py).
Karten ändern: MAPS unten anpassen, dann `python3 tools/build_maps.py` und `bash tools/export.sh`.
"""
import json
import math
import os

from shapely.geometry import shape, Point

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 25
DURATION = 7.8

# Standorte (lon, lat)
OFFICES = {
    "bgl": (7.1330, 50.9915),  # Laurentiusstraße, Bergisch Gladbach (Hauptsitz)
    "koeln": (6.9530, 50.9262),  # Sachsenring, Köln
    "wipperfuerth": (7.3990, 51.1166),  # Wipperfürth
}

COLORS = {"base": "#ebedeb", "area": "#e0e3e1", "focus": "#c9cecb", "stroke": "#ffffff", "rhein": "#8ecdeb",
          "label": "#5e6a6a", "label_focus": "#444f4f"}

MAPS = {
    "formats/karte-koeln.html": {
        "title": "Karte Köln",
        "W": 1200,
        "H": 800,
        "areas": [("Innenstadt", "focus"), ("Rodenkirchen", "area"), ("Lindenthal", "area"), ("Ehrenfeld", "area"),
                  ("Nippes", "area"), ("Chorweiler", "area"), ("Porz", "area"), ("Kalk", "area"), ("Mülheim", "area")],
        "kind": "koeln-bezirk",
        "labels": {"Innenstadt": None},
        "office_labels": {"koeln": "Innenstadt"},
        "markers": ["koeln"],
        "logo_at": "koeln",
        "logo": ("tr", 260),
        "rhein": True,
        "credit": "Kartengrundlage: © GeoBasis-DE / BKG 2023, Stadt Köln",
    },
    "formats/karte-einzugsgebiet.html": {
        "title": "Karte Einzugsgebiet",
        "W": 1920,
        "H": 1080,
        "areas": [("Köln", "area"), ("Leverkusen", "base"), ("Rheinisch-Bergischer Kreis", "area"),
                  ("Oberbergischer Kreis", "area")],
        "kind": "kreis",
        "labels": {"Köln": None, "Rheinisch-Bergischer Kreis": (60, -170)},
        "office_labels": {"koeln": "Köln", "bgl": "Bergisch Gladbach", "wipperfuerth": "Wipperfürth"},
        "markers": ["koeln", "bgl", "wipperfuerth"],
        "logo_at": "bgl",
        "logo": ("tl", 360),
        "rhein": True,
        "credit": "Kartengrundlage: © GeoBasis-DE / BKG 2023",
    },
}

LOGO_SVG = '''<svg viewBox="0 0 452 100" role="img" aria-label="KNIGGE Immobilien">
          <defs>
            <linearGradient id="k-a" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="48.9" y2="39.6">
              <stop offset="0" stop-color="#5e0f18" /><stop offset="0.56" stop-color="#a4222b" /><stop offset="0.8" stop-color="#c12a33" /><stop offset="0.93" stop-color="#ca2c35" />
            </linearGradient>
            <linearGradient id="k-r" gradientUnits="userSpaceOnUse" x1="47.5" y1="40.2" x2="100" y2="0">
              <stop offset="0" stop-color="#4a0a13" /><stop offset="1" stop-color="#b0252e" />
            </linearGradient>
            <linearGradient id="k-b" gradientUnits="userSpaceOnUse" x1="0" y1="100" x2="100" y2="100">
              <stop offset="0" stop-color="#480a12" /><stop offset="0.5" stop-color="#a2222b" /><stop offset="0.85" stop-color="#ca2c35" />
            </linearGradient>
          </defs>
          <path d="M0 0 H79.5 L0 100 Z" fill="url(#k-a)" />
          <path d="M79.5 0 H100 V100 L47.5 40.2 Z" fill="url(#k-r)" />
          <path d="M0 100 L47.5 40.2 L100 100 Z" fill="url(#k-b)" />
          <text class="word" x="125.2" y="53" font-size="77" font-weight="700" textLength="328.5" lengthAdjust="spacing">KNIGGE</text>
          <text class="word" x="125.5" y="100" font-size="44.3" font-weight="400" textLength="330.5" lengthAdjust="spacing">IMMOBILIEN</text>
        </svg>'''


class Projection:
    def __init__(self, bounds, W, H, margin):
        minx, miny, maxx, maxy = bounds
        self.lat0 = (miny + maxy) / 2
        self.k = math.cos(math.radians(self.lat0))
        w = (maxx - minx) * self.k
        h = maxy - miny
        self.s = min((W - 2 * margin) / w, (H - 2 * margin) / h)
        self.ox = (W - w * self.s) / 2 - minx * self.k * self.s
        self.oy = (H - h * self.s) / 2 + maxy * self.s

    def __call__(self, lon, lat):
        return (lon * self.k * self.s + self.ox, -lat * self.s + self.oy)


def ring_path(coords, proj):
    pts = [proj(x, y) for x, y in coords]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def geom_path(geom, proj):
    polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
    parts = []
    for p in polys:
        parts.append(ring_path(p.exterior.coords, proj))
        for hole in p.interiors:
            parts.append(ring_path(hole.coords, proj))
    return " ".join(parts)


def line_path(coords, proj):
    pts = [proj(x, y) for x, y in coords]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def build(rel, spec, region):
    W, H = spec["W"], spec["H"]
    by_name = {}
    for a in region["areas"]:
        if a["kind"] == spec["kind"] or (spec["kind"] == "kreis" and a["kind"] == "kreis"):
            by_name[a["name"]] = shape(a["geometry"])
    geoms = [(n, role, by_name[n]) for n, role in spec["areas"]]
    from shapely.ops import unary_union
    union = unary_union([g for _, _, g in geoms])
    margin = 30
    proj = Projection(union.bounds, W, H - 30, margin)  # unten Platz für den Quellenhinweis
    fx, fy = proj(*OFFICES[spec["logo_at"]])

    paths, labels = [], []
    for i, (name, role, g) in enumerate(geoms):
        c = g.centroid
        cx, cy = proj(c.x, c.y)
        dist = math.hypot(cx - fx, cy - fy)
        paths.append((i, name, role, geom_path(g, proj), cx, cy, dist))
        rp = g.representative_point()
        lx, ly = proj(rp.x, rp.y)
        off = spec["labels"].get(name, (0, 0))
        if off is not None:
            labels.append((i, name, role, lx + off[0], ly + off[1]))

    rhein = []
    if spec["rhein"]:
        for k, ln in enumerate(region["rhein"]):
            line = shape(ln).intersection(union.buffer(0.01))
            for seg in getattr(line, "geoms", [line]):
                if seg.geom_type == "LineString" and seg.length > 0.01:
                    rhein.append(line_path(seg.coords, proj))

    maxd = max(p[6] for p in paths) or 1
    area_svg = "\n".join(
        f'        <path class="area {role}" id="a{i}" data-d="{dist / maxd:.3f}" style="transform-origin: {cx:.1f}px {cy:.1f}px" d="{d}" />'
        for i, name, role, d, cx, cy, dist in paths
    )
    rhein_svg = "\n".join(f'        <path class="rhein" id="rh{k}" pathLength="1" d="{d}" />' for k, d in enumerate(rhein))
    label_html = "\n".join(
        f'      <div class="lpos" style="left: {x:.1f}px; top: {y:.1f}px"><span class="label" id="l{i}">{name}</span></div>'
        for i, name, role, x, y in labels
    )
    for k, (key, text) in enumerate(spec.get("office_labels", {}).items()):
        ox, oy = proj(*OFFICES[key])
        label_html += f'\n      <div class="lpos" style="left: {ox:.1f}px; top: {oy + 38:.1f}px"><span class="label lfocus" id="lo{k}">{text}</span></div>'

    markers = []
    for k, key in enumerate(spec["markers"]):
        mx, my = proj(*OFFICES[key])
        markers.append(f'      <svg class="marker" id="m{k}" style="left: {mx - 17:.1f}px; top: {my - 17:.1f}px" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="13" fill="#ffffff" stroke="#444f4f" stroke-width="4" /><circle cx="17" cy="17" r="5.5" fill="#ca2c35" /></svg>')
    rings = "\n".join(
        f'        <circle id="r{k}" cx="{proj(*OFFICES[key])[0]:.1f}" cy="{proj(*OFFICES[key])[1]:.1f}" r="14" stroke-width="0" />'
        for k, key in enumerate(spec["markers"])
    )
    corner, lw = spec["logo"]
    lh = lw * 100 / 452
    pad = 44
    lx = pad if corner in ("tl", "bl") else W - pad - lw
    ly = pad if corner in ("tl", "tr") else H - pad - lh - 30

    return f'''<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>KNIGGE Immobilien – {spec["title"]} (transparent)</title>
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
      .map {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        overflow: visible;
      }}
      .area {{
        fill: {COLORS["area"]};
        stroke: {COLORS["stroke"]};
        stroke-width: 3;
        stroke-linejoin: round;
        transform-box: view-box;
        transform: scale(var(--s, 1));
      }}
      .area.base {{
        fill: {COLORS["base"]};
      }}
      .area.focus {{
        fill: {COLORS["focus"]};
      }}
      .rhein {{
        fill: none;
        stroke: {COLORS["rhein"]};
        stroke-width: 7;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-dasharray: 1 2;
        stroke-dashoffset: 1.05;
      }}
      .rings circle {{
        fill: none;
        stroke: #ca2c35;
      }}
      .lpos {{
        position: absolute;
        transform: translate(-50%, -50%);
      }}
      .label {{
        display: block;
        white-space: nowrap;
        font-size: {22 if W <= 1400 else 24}px;
        font-weight: 500;
        line-height: 1.15;
        color: {COLORS["label"]};
        will-change: transform;
      }}
      .label.lfocus {{
        font-weight: 700;
        color: {COLORS["label_focus"]};
      }}
      .marker {{
        position: absolute;
        width: 34px;
        height: 34px;
        overflow: visible;
        will-change: transform;
      }}
      .logo {{
        position: absolute;
        will-change: transform;
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
      }}
      .credit {{
        position: absolute;
        right: 16px;
        bottom: 8px;
        font-size: 12px;
        font-weight: 500;
        color: #8a9393;
      }}
    </style>
  </head>
  <body>
    <!--
      KNIGGE Immobilien – {spec["title"]} (transparenter Hintergrund)
      erzeugt von tools/build_maps.py – nicht von Hand ändern
    -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <svg class="map" viewBox="0 0 {W} {H}" aria-hidden="true" data-layout-allow-overflow>
        <g id="areas">
{area_svg}
        </g>
        <g id="rhein">
{rhein_svg}
        </g>
        <g class="rings">
{rings}
        </g>
      </svg>
{label_html}
{chr(10).join(markers)}
      <div class="logo" id="logo" style="left: {lx:.1f}px; top: {ly:.1f}px; width: {lw}px; height: {lh:.1f}px">
        {LOGO_SVG}
      </div>
      <div class="credit" id="credit">{spec["credit"]}</div>
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const areas = Array.from(document.querySelectorAll(".area"));
        const labels = Array.from(document.querySelectorAll(".label"));
        const markers = Array.from(document.querySelectorAll(".marker"));
        const rings = Array.from(document.querySelectorAll(".rings circle"));

        // Flächen wachsen vom Standort aus nach außen auf
        areas.forEach((a) => {{
          const d = parseFloat(a.dataset.d);
          tl.fromTo(a, {{ "--s": 0 }}, {{ "--s": 1, duration: 0.55, ease: "back.out(1.3)" }}, 0.15 + d * 0.8);
        }});
        // Rhein fließt ein
        tl.fromTo(".rhein", {{ strokeDashoffset: 1.05 }}, {{ strokeDashoffset: 0, duration: 1.2, ease: "power1.inOut" }}, 1.0);
        // Namen
        labels.forEach((l, i) => tl.fromTo(l, {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, 1.5 + i * 0.06));
        // Standorte + Logo
        markers.forEach((m, i) => {{
          tl.fromTo(m, {{ y: -36, scale: 0 }}, {{ y: 0, scale: 1, duration: 0.6, ease: "bounce.out" }}, 2.0 + i * 0.18);
        }});
        rings.forEach((r, i) => {{
          tl.fromTo(r, {{ attr: {{ r: 14 }}, strokeWidth: 5 }}, {{ attr: {{ r: 110 }}, strokeWidth: 0, duration: 1.4, ease: "power2.out" }}, 2.45 + i * 0.18);
          tl.fromTo(r, {{ attr: {{ r: 14 }}, strokeWidth: 5 }}, {{ attr: {{ r: 110 }}, strokeWidth: 0, duration: 1.4, ease: "power2.out", immediateRender: false }}, 4.4 + i * 0.18);
        }});
        tl.fromTo("#logo", {{ scale: 0 }}, {{ scale: 1, duration: 0.55, ease: "back.out(1.6)", transformOrigin: "0% 100%" }}, 2.5);
        tl.fromTo("#credit", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "power2.out", transformOrigin: "100% 100%" }}, 2.6);

        // Abbau für die Schleife
        tl.to(["#logo", "#credit"], {{ scale: 0, duration: 0.3, ease: "back.in(1.5)" }}, 6.4);
        markers.forEach((m, i) => tl.to(m, {{ y: -30, scale: 0, duration: 0.3, ease: "back.in(1.4)" }}, 6.45 + i * 0.05));
        labels.forEach((l, i) => tl.to(l, {{ scale: 0, duration: 0.25, ease: "back.in(1.5)" }}, 6.5 + i * 0.02));
        tl.to(".rhein", {{ strokeDashoffset: 1.05, duration: 0.5, ease: "power1.in" }}, 6.55);
        areas.forEach((a) => {{
          const d = parseFloat(a.dataset.d);
          tl.to(a, {{ "--s": 0, duration: 0.35, ease: "back.in(1.3)" }}, 6.75 + (1 - d) * 0.5);
        }});

        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''


def main():
    with open(os.path.join(ROOT, "assets/geo/region.json"), encoding="utf-8") as f:
        region = json.load(f)
    for rel, spec in MAPS.items():
        html = build(rel, spec, region)
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(html)
        print("geschrieben:", rel)


if __name__ == "__main__":
    main()
