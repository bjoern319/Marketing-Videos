#!/usr/bin/env python3
"""Bereitet die Kartengrundlagen für die Karten-Animationen auf (einmalig, Ergebnis liegt in assets/geo/).

Quellen (vor dem Lauf herunterladen, Pfade als Argumente übergeben):
  --kreise        geoBoundaries DEU ADM3 (BKG VG250, Kreise; Datenlizenz Deutschland – Namensnennung 2.0)
                  https://github.com/wmgeolab/geoBoundaries/ → releaseData/gbOpen/DEU/ADM3/geoBoundaries-DEU-ADM3.geojson
  --koeln         Kölner Stadtteile (Stadt Köln, Offene Daten Köln) aus
                  https://github.com/codeforgermany/click_that_hood → public/data/cologne.geojson
  --haltestellen  Zentrales Haltestellenverzeichnis (DELFI e.V.) aus dem npm-Paket zhv-json
                  → refineddata/stations.json
  --gv            Gemeindeverzeichnis (Statistisches Bundesamt, GV100; Datenlizenz Deutschland – Namensnennung 2.0)
                  aus dem npm-Paket gemeindeverzeichnis → Ordner mit gemeinden.ndjson und gemeindeverbaende.ndjson
  --gemeinden     (optional) amtliche Gemeindegrenzen als GeoJSON mit 8-stelligem Gemeindeschlüssel (KN/AGS),
                  z. B. DVG NRW von opengeodata.nrw.de – ersetzt die angenäherten Grenzen

Gemeindegrenzen ohne --gemeinden: Innerhalb der amtlichen Kreisgrenze gehört jede Stelle zur Gemeinde der
nächstgelegenen Haltestelle. Gewichte gleichen die Flächen an die amtlichen Gemeindeflächen an, danach wird
geglättet. Das ergibt schematische Grenzen in der richtigen Lage und Größe, keine amtlichen.

Ausgabe: assets/geo/region.json – Flächen (lon/lat) für Kölner Stadtbezirke, Gemeinden und Kreise
(alle aus einem gemeinsamen Netz vereinfacht, damit Nachbarn lückenlos aneinanderpassen) + Rheinverlauf
"""
import argparse
import json
import math
import os
import re

import numpy as np
import shapely
from shapely.geometry import shape, mapping, MultiLineString, Polygon
from shapely.ops import unary_union, linemerge

# BKG-Name -> (Kreisschlüssel, Unterteilung: None = kreisfreie Stadt, "gemeinde", "verband" = Verbandsgemeinden)
KREISE = {
    "Köln, Kreisfreie Stadt": ("05315", None),
    "Leverkusen, Kreisfreie Stadt": ("05316", None),
    "Rheinisch-Bergischer Kreis": ("05378", "gemeinde"),
    "Oberbergischer Kreis": ("05374", "gemeinde"),
    "Rhein-Erft-Kreis": ("05362", "gemeinde"),
    "Rhein-Sieg-Kreis": ("05382", "gemeinde"),
    "Rhein-Kreis Neuss": ("05162", "gemeinde"),
    "Mettmann": ("05158", "gemeinde"),
    "Solingen, Kreisfreie Stadt": ("05122", None),
    "Remscheid, Kreisfreie Stadt": ("05120", None),
    "Wuppertal, Kreisfreie Stadt": ("05124", None),
    "Märkischer Kreis": ("05962", "gemeinde"),
    "Olpe": ("05966", "gemeinde"),
    "Bonn, Kreisfreie Stadt": ("05314", None),
    "Düsseldorf, Kreisfreie Stadt": ("05111", None),
    "Ennepe-Ruhr-Kreis": ("05954", "gemeinde"),
    "Altenkirchen (Westerwald)": ("07132", "verband"),
    "Siegen-Wittgenstein": ("05970", "gemeinde"),
    "Hagen, Kreisfreie Stadt": ("05914", None),
}

# Kölner Stadtteile -> Stadtbezirke (amtliche Gliederung)
BEZIRKE = {
    "Innenstadt": ["Altstadt/Nord", "Altstadt/Süd", "Neustadt/Nord", "Neustadt/Süd", "Deutz"],
    "Rodenkirchen": ["Bayenthal", "Godorf", "Hahnwald", "Immendorf", "Marienburg", "Meschenich", "Raderberg", "Raderthal",
                     "Rodenkirchen", "Rondorf", "Sürth", "Weiß", "Zollstock"],
    "Lindenthal": ["Braunsfeld", "Junkersdorf", "Klettenberg", "Lindenthal", "Lövenich", "Müngersdorf", "Sülz", "Weiden", "Widdersdorf"],
    "Ehrenfeld": ["Bickendorf", "Bocklemünd/Mengenich", "Ehrenfeld", "Neuehrenfeld", "Ossendorf", "Vogelsang"],
    "Nippes": ["Bilderstöckchen", "Longerich", "Mauenheim", "Niehl", "Nippes", "Riehl", "Weidenpesch"],
    "Chorweiler": ["Blumenberg", "Chorweiler", "Esch/Auweiler", "Fühlingen", "Heimersdorf", "Lindweiler", "Merkenich", "Pesch",
                   "Roggendorf/Thenhoven", "Seeberg", "Volkhoven/Weiler", "Worringen"],
    "Porz": ["Eil", "Elsdorf", "Ensen", "Finkenberg", "Gremberghoven", "Grengel", "Langel", "Libur", "Lind", "Poll", "Porz",
             "Urbach", "Wahn", "Wahnheide", "Westhoven", "Zündorf"],
    "Kalk": ["Brück", "Höhenberg", "Humboldt/Gremberg", "Kalk", "Merheim", "Neubrück", "Ostheim", "Rath/Heumar", "Vingst"],
    "Mülheim": ["Buchforst", "Buchheim", "Dellbrück", "Dünnwald", "Flittard", "Höhenhaus", "Holweide", "Mülheim", "Stammheim"],
}
RECHTS_RHEIN_KOELN = {"Porz", "Kalk", "Mülheim"}  # plus Deutz (Innenstadt)

SIMPLIFY = 0.0006  # Grad (~45-65 m) – nur noch für den Rhein
TOL_EXACT = 0.04  # km – Vereinfachung amtlicher Grenzen
TOL_APPROX = 0.12  # km – Vereinfachung angenäherter Grenzen, danach Chaikin-Glättung
RES = 0.07  # km – Rasterweite für die Annäherung
MODE_R = 3  # Zellen – Glättungsfenster (2r+1)²

# lokale, längentreue Projektion in km
LAT0, LON0 = 51.0, 7.0
KX = 111.32 * math.cos(math.radians(LAT0))
KY = 111.13


def to_km(g):
    return shapely.transform(g, lambda c: np.column_stack(((c[:, 0] - LON0) * KX, (c[:, 1] - LAT0) * KY)))


def to_deg(g):
    return shapely.transform(g, lambda c: np.column_stack((np.round(c[:, 0] / KX + LON0, 5), np.round(c[:, 1] / KY + LAT0, 5))))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_ndjson(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def clean_name(name):
    name = re.split(r",", name)[0]  # „Bergisch Gladbach, Stadt“
    return re.sub(r"\s*\(.*?\)", "", name).strip()  # „Leichlingen (Rheinland)“


def mode_filter(lab, n, r):
    """Mehrheitsfilter: jede Zelle bekommt die häufigste Klasse ihres (2r+1)²-Fensters."""
    best_s = np.full(lab.shape, -1, dtype=np.int32)
    best_c = lab.copy()
    cur_s = np.zeros(lab.shape, dtype=np.int32)
    k = 2 * r + 1
    for c in range(n):
        m = np.pad((lab == c).astype(np.int32), r)
        ii = np.zeros((m.shape[0] + 1, m.shape[1] + 1), dtype=np.int32)
        ii[1:, 1:] = m.cumsum(0).cumsum(1)
        s = ii[k:, k:] - ii[:-k, k:] - ii[k:, :-k] + ii[:-k, :-k]
        cur_s = np.where(lab == c, s, cur_s)
        better = s > best_s
        best_s = np.where(better, s, best_s)
        best_c = np.where(better, c, best_c)
    return np.where(best_s > cur_s, best_c, lab)


def approx_partition(P, units):
    """Teilt die Kreisfläche P (km) auf. units: [(stops (n,2) km, Zielfläche km²)] -> [Polygon (km)]."""
    n = len(units)
    minx, miny, maxx, maxy = P.bounds
    pad = 4 * RES
    x0, y0 = minx - pad, miny - pad
    nx = int(math.ceil((maxx + pad - x0) / RES))
    ny = int(math.ceil((maxy + pad - y0) / RES))
    cx = (x0 + (np.arange(nx) + 0.5) * RES).astype(np.float32)
    cy = (y0 + (np.arange(ny) + 0.5) * RES).astype(np.float32)
    gx, gy = np.meshgrid(cx, cy)
    gx, gy = gx.ravel(), gy.ravel()
    inside = shapely.contains_xy(P, gx, gy)

    # Abstand jeder Zelle zur nächsten Haltestelle jeder Gemeinde
    D = np.empty((n, gx.size), dtype=np.float32)
    for i, (pts, _) in enumerate(units):
        best = np.full(gx.size, np.inf, dtype=np.float32)
        pts = pts.astype(np.float32)
        for s in range(0, len(pts), 16):
            ch = pts[s:s + 16]
            d2 = (gx[None, :] - ch[:, 0:1]) ** 2 + (gy[None, :] - ch[:, 1:2]) ** 2
            best = np.minimum(best, d2.min(axis=0))
        D[i] = np.sqrt(best)

    # Gewichte so einstellen, dass die Flächen den amtlichen entsprechen
    target = np.array([t for _, t in units], dtype=np.float64)
    target *= P.area / target.sum()
    w = np.zeros(n, dtype=np.float32)
    Din = D[:, inside]
    cell = RES * RES
    for _ in range(400):
        lab = np.argmin(Din - w[:, None], axis=0)
        A = np.bincount(lab, minlength=n) * cell
        if np.abs((A - target) / target).max() < 0.01:
            break
        step = 0.5 * (target - A) / (4 * np.sqrt(target))
        w += np.clip(step, -0.3, 0.3).astype(np.float32)
    lab = np.argmin(D - w[:, None], axis=0).reshape(ny, nx)
    for _ in range(2):
        lab = mode_filter(lab, n, MODE_R)

    # Raster -> Polygone (Zeilenläufe als Rechtecke, gemeinsame Kanten liegen exakt aufeinander)
    boxes = [[] for _ in range(n)]
    for j in range(ny):
        row = lab[j]
        cut = np.flatnonzero(np.diff(row)) + 1
        starts = np.concatenate(([0], cut))
        ends = np.concatenate((cut, [nx]))
        for s, e in zip(starts, ends):
            boxes[row[s]].append((x0 + s * RES, y0 + j * RES, x0 + e * RES, y0 + (j + 1) * RES))
    pieces = []
    for c in range(n):
        if boxes[c]:
            b = np.array(boxes[c])
            pieces.append(shapely.union_all(shapely.box(b[:, 0], b[:, 1], b[:, 2], b[:, 3])).intersection(P))
        else:
            pieces.append(Polygon())

    # abgesprengte Splitter (z. B. einzelne falsch zugeordnete Haltestellen) dem Nachbarn mit der längsten Grenze geben
    loose = []
    for c in range(n):
        parts = sorted((p for p in getattr(pieces[c], "geoms", [pieces[c]]) if p.geom_type == "Polygon" and not p.is_empty),
                       key=lambda p: p.area, reverse=True)
        pieces[c] = parts[0] if parts else Polygon()
        loose.extend(parts[1:])
    for p in sorted(loose, key=lambda p: p.area, reverse=True):
        ring = p.buffer(RES * 0.2)
        best = max(range(n), key=lambda c: pieces[c].intersection(ring).area)
        pieces[best] = pieces[best].union(p)
    return pieces


def chaikin(coords, iters=3):
    pts = np.asarray(coords, dtype=float)
    closed = len(pts) > 3 and np.allclose(pts[0], pts[-1])
    for _ in range(iters):
        if closed:
            p = pts[:-1]
            q = np.roll(p, -1, axis=0)
            new = np.empty((2 * len(p), 2))
            new[0::2] = 0.75 * p + 0.25 * q
            new[1::2] = 0.25 * p + 0.75 * q
            pts = np.vstack([new, new[:1]])
        else:
            p, q = pts[:-1], pts[1:]
            new = np.empty((2 * len(p), 2))
            new[0::2] = 0.75 * p + 0.25 * q
            new[1::2] = 0.25 * p + 0.75 * q
            pts = np.vstack([pts[:1], new, pts[-1:]])
    return pts


def simplify_coverage(geoms, approx_zone):
    """Vereinfacht alle Flächen über ein gemeinsames Kantennetz: jede Grenze nur einmal, Nachbarn passen lückenlos."""
    geoms = [shapely.set_precision(g, 0.002) for g in geoms]
    net = shapely.union_all([shapely.boundary(g) for g in geoms])
    merged = linemerge(net)
    arcs = []
    for arc in getattr(merged, "geoms", [merged]):
        if arc.is_empty:
            continue
        approx = arc.intersection(approx_zone).length > 0.5 * arc.length
        if approx:
            s = arc.simplify(TOL_APPROX)
            arcs.append(shapely.LineString(chaikin(s.coords)) if len(s.coords) > 2 else s)
        else:
            arcs.append(arc.simplify(TOL_EXACT))
    faces = list(shapely.get_parts(shapely.polygonize(shapely.get_parts(shapely.union_all(arcs)))))
    tree = shapely.STRtree(geoms)
    owned = [[] for _ in geoms]
    for f in faces:
        rp = f.representative_point()
        hit = tree.query(rp, predicate="within")
        if len(hit):
            owned[int(hit[0])].append(f)
            continue
        cand = tree.query(f, predicate="intersects")
        if len(cand):
            best = max(cand, key=lambda i: geoms[i].intersection(f).area)
            if geoms[best].intersection(f).area > 0.3 * f.area:
                owned[int(best)].append(f)
    return [shapely.union_all(o) if o else Polygon() for o in owned]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kreise", required=True)
    ap.add_argument("--koeln", required=True)
    ap.add_argument("--haltestellen", required=True)
    ap.add_argument("--gv", required=True)
    ap.add_argument("--gemeinden")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    kreise = {f["properties"]["shapeName"]: shape(f["geometry"]).buffer(0) for f in load(a.kreise)["features"]
              if f["properties"]["shapeName"] in KREISE}
    missing = [k for k in KREISE if k not in kreise]
    if missing:
        raise SystemExit("fehlt: %s" % missing)

    # Kölner Stadtbezirke aus Stadtteilen, auf den amtlichen Stadtumriss (BKG) zugeschnitten
    teile = {f["properties"]["name"]: shape(f["geometry"]).buffer(0) for f in load(a.koeln)["features"]}
    koeln = kreise["Köln, Kreisfreie Stadt"]
    bez = {}
    for name, members in BEZIRKE.items():
        bez[name] = unary_union([teile[m] for m in members]).buffer(0.0002).buffer(-0.0002).intersection(koeln)
    # Reste (Abweichungen zwischen den Datenquellen) dem längsten Nachbarn zuschlagen
    rest = koeln.difference(unary_union(list(bez.values())))
    pieces = list(rest.geoms) if rest.geom_type == "MultiPolygon" else [rest] if not rest.is_empty else []
    for p in pieces:
        if p.area < 1e-9:
            continue
        best = max(bez, key=lambda n: bez[n].buffer(0.0005).intersection(p.buffer(0.0005)).area)
        bez[best] = unary_union([bez[best], p])

    # Rhein: gemeinsame Grenze zwischen linkem und rechtem Ufer (Kölner Stadtteile + Nachbarkreise)
    left = unary_union([bez[n] for n in BEZIRKE if n not in RECHTS_RHEIN_KOELN and n != "Innenstadt"]
                       + [unary_union([teile[m] for m in BEZIRKE["Innenstadt"] if m != "Deutz"]).intersection(koeln),
                          kreise["Rhein-Kreis Neuss"], kreise["Rhein-Erft-Kreis"]])
    right = unary_union([bez[n] for n in RECHTS_RHEIN_KOELN] + [teile["Deutz"].intersection(koeln),
                         kreise["Leverkusen, Kreisfreie Stadt"], kreise["Mettmann"], kreise["Rhein-Sieg-Kreis"]])
    shared = left.boundary.intersection(right.buffer(0.0012))
    lines = []
    for g in getattr(shared, "geoms", [shared]):
        if g.geom_type == "LineString" and g.length > 0.002:
            lines.append(g)
        elif g.geom_type == "MultiLineString":
            lines.extend(x for x in g.geoms if x.length > 0.002)
    rhein = linemerge(MultiLineString(lines))
    # nur der zusammenhängende Hauptlauf (Süd -> Nord), kurze Splitter verwerfen
    parts = list(rhein.geoms) if rhein.geom_type == "MultiLineString" else [rhein]
    parts = [p for p in parts if p.length > 0.01]

    # Gemeindeverzeichnis: Namen, amtliche Flächen, Verbandsgemeinden
    gv = load_ndjson(os.path.join(a.gv, "gemeinden.ndjson"))
    verbaende = {v["schlüssel"]["nummer"]: v["name"] for v in load_ndjson(os.path.join(a.gv, "gemeindeverbaende.ndjson"))}
    gem = {}
    for g in gv:
        s = g["schlüssel"]
        kreis = s["land"] + s["regierungsbezirk"] + s["kreis"]
        gem[kreis + s["gemeinde"]] = {"name": clean_name(g["name"]), "flaeche": g["fläche"] / 100.0, "kreis": kreis,
                                      "verband": kreis + s["gemeindeverband"]}

    # Haltestellen je Gemeinde (km)
    stops = {}
    for v in load(a.haltestellen).values():
        m = v.get("m")
        if not m or "c" not in v:
            continue
        ags = "%08d" % m
        if ags in gem:
            stops.setdefault(ags, []).append((v["c"][1], v["c"][0]))

    amtlich = {}
    if a.gemeinden:
        for f in load(a.gemeinden)["features"]:
            p = f["properties"]
            key = next((str(p[k]) for k in ("KN", "AGS", "ags", "AGS_0", "GKZ") if p.get(k)), None)
            if key:
                amtlich[key[:8]] = to_km(shape(f["geometry"]).buffer(0))

    # Feinste Einheiten: Kölner Stadtbezirke, kreisfreie Städte, Gemeinden bzw. Verbandsgemeinden
    units = []  # dict(name, kind, kreis, geom km)
    approx_zone = []
    for bkg_name, (kkey, mode) in KREISE.items():
        P = to_km(kreise[bkg_name])
        kname = bkg_name.replace(", Kreisfreie Stadt", "")
        if kkey == "05315":
            for name, g in bez.items():
                units.append({"name": name, "kind": "koeln-bezirk", "kreis": kname, "geom": to_km(g)})
            continue
        if mode is None:
            units.append({"name": kname, "kind": "gemeinde", "kreis": kname, "geom": P})
            continue
        members = sorted(k for k, g in gem.items() if g["kreis"] == kkey)
        if mode == "verband":
            groups = {}
            for k in members:
                groups.setdefault(gem[k]["verband"], []).append(k)
            entries = [(clean_name(verbaende.get(vk, vk)), ks) for vk, ks in sorted(groups.items())]
        else:
            entries = [(gem[k]["name"], [k]) for k in members]
        if all(k in amtlich for _, ks in entries for k in ks):
            for name, ks in entries:
                units.append({"name": name, "kind": "gemeinde", "kreis": kname,
                              "geom": unary_union([amtlich[k] for k in ks]).intersection(P)})
            continue
        Pb = P.buffer(0.3)
        spec = []
        for name, ks in entries:
            ll = np.array([xy for k in ks for xy in stops.get(k, [])]).reshape(-1, 2)
            pts = np.column_stack(((ll[:, 0] - LON0) * KX, (ll[:, 1] - LAT0) * KY))
            pts = pts[shapely.contains_xy(Pb, pts[:, 0], pts[:, 1])]  # Haltestellen außerhalb des Kreises verwerfen
            if len(pts) == 0:
                raise SystemExit("keine Haltestellen: %s" % name)
            spec.append((np.unique(pts, axis=0), sum(gem[k]["flaeche"] for k in ks)))
        pieces = approx_partition(P, spec)
        print(f"{kname}:")
        for (name, _), (_, target), g in zip(entries, spec, pieces):
            print(f"  {name:28s} {g.area:7.1f} km²  amtlich {target:7.1f}  ({(g.area / target - 1) * 100:+.1f} %)")
            units.append({"name": name, "kind": "gemeinde", "kreis": kname, "geom": g})
        approx_zone.append(P.buffer(-0.01))

    final = simplify_coverage([u["geom"] for u in units], unary_union(approx_zone))
    for u, g in zip(units, final):
        u["final"] = g

    out = {"areas": [], "rhein": []}
    names = set()

    def add(name, kind, g_km):
        if (name, kind) in names:
            raise SystemExit("doppelter Name: %s (%s)" % (name, kind))
        names.add((name, kind))
        out["areas"].append({"name": name, "kind": kind, "geometry": mapping(to_deg(g_km))})

    for u in units:
        add(u["name"], u["kind"], u["final"])
    add("Köln", "gemeinde", shapely.union_all([u["final"] for u in units if u["kind"] == "koeln-bezirk"]))
    for bkg_name in KREISE:
        kname = bkg_name.replace(", Kreisfreie Stadt", "")
        add(kname, "kreis", shapely.union_all([u["final"] for u in units if u["kreis"] == kname]))
    for p in parts:
        out["rhein"].append(mapping(p.simplify(SIMPLIFY / 2)))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("Flächen:", len(out["areas"]), "Rhein-Abschnitte:", len(out["rhein"]), [round(p.length, 3) for p in parts])


if __name__ == "__main__":
    main()
