#!/usr/bin/env python3
"""Bereitet die Kartengrundlagen für die Karten-Animationen auf (einmalig, Ergebnis liegt in assets/geo/).

Quellen (vor dem Lauf herunterladen, Pfade als Argumente übergeben):
  --kreise  geoBoundaries DEU ADM3 (BKG VG250, Kreise; Datenlizenz Deutschland – Namensnennung 2.0)
            https://github.com/wmgeolab/geoBoundaries/ → releaseData/gbOpen/DEU/ADM3/geoBoundaries-DEU-ADM3.geojson
  --koeln   Kölner Stadtteile (Stadt Köln, Offene Daten Köln) aus
            https://github.com/codeforgermany/click_that_hood → public/data/cologne.geojson
  --gemeinden (optional) Gemeindegrenzen NRW als GeoJSON (z. B. DVG NRW von opengeodata.nrw.de)

Ausgabe: assets/geo/region.json  – Flächen (lon/lat, vereinfacht) + daraus abgeleiteter Rheinverlauf
"""
import argparse
import json
import os

from shapely.geometry import shape, mapping, MultiLineString, LineString
from shapely.ops import unary_union, linemerge

KREISE = [
    "Köln, Kreisfreie Stadt", "Leverkusen, Kreisfreie Stadt", "Rheinisch-Bergischer Kreis", "Oberbergischer Kreis",
    "Rhein-Erft-Kreis", "Rhein-Sieg-Kreis", "Rhein-Kreis Neuss", "Mettmann", "Solingen, Kreisfreie Stadt",
    "Remscheid, Kreisfreie Stadt", "Wuppertal, Kreisfreie Stadt", "Märkischer Kreis", "Olpe", "Bonn, Kreisfreie Stadt",
    "Düsseldorf, Kreisfreie Stadt", "Ennepe-Ruhr-Kreis", "Altenkirchen (Westerwald)", "Siegen-Wittgenstein", "Hagen, Kreisfreie Stadt",
]

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

SIMPLIFY = 0.0006  # Grad (~45-65 m) – glatte, aber formtreue Linien


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kreise", required=True)
    ap.add_argument("--koeln", required=True)
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

    out = {"areas": [], "rhein": []}
    for name, geom in bez.items():
        out["areas"].append({"name": name, "kind": "koeln-bezirk", "geometry": mapping(geom.simplify(SIMPLIFY, preserve_topology=True))})
    for name, geom in kreise.items():
        out["areas"].append({"name": name.replace(", Kreisfreie Stadt", ""), "kind": "kreis",
                             "geometry": mapping(geom.simplify(SIMPLIFY, preserve_topology=True))})
    if a.gemeinden:
        for f in load(a.gemeinden)["features"]:
            p = f["properties"]
            name = p.get("GN") or p.get("gen") or p.get("GEN") or p.get("name")
            out["areas"].append({"name": name, "kind": "gemeinde",
                                 "geometry": mapping(shape(f["geometry"]).buffer(0).simplify(SIMPLIFY, preserve_topology=True))})
    for p in parts:
        out["rhein"].append(mapping(p.simplify(SIMPLIFY / 2)))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("Flächen:", len(out["areas"]), "Rhein-Abschnitte:", len(out["rhein"]), [round(p.length, 3) for p in parts])


if __name__ == "__main__":
    main()
