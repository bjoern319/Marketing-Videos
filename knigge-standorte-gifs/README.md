# KNIGGE Immobilien – Standort-Animationen (transparent)

Die Orts-Konstellation aus dem Film „Nicht weniger Zuhause. Mehr Leben.“ als freigestellte
Animation für die KNIGGE-Standorte und das gesamte Einzugsgebiet – zum Einsetzen auf Website, in
Präsentationen oder über eigene Hintergründe. 25 fps, Endlosschleife (Aufbau → Halten → Abbau).

| Datei | Mitte | Orte (im Uhrzeigersinn ab Norden) |
| --- | --- | --- |
| `renders/knigge-standort-bergisch-gladbach.gif` | Bergisch Gladbach (Hauptsitz) | Paffrath, Herkenrath, Moitzfeld, Bensberg, Frankenforst, Refrath, Köln-Ost, Schildgen |
| `renders/knigge-standort-koeln.gif` | Köln (Standort Sachsenring) | Stadtbezirke Nippes, Mülheim, Kalk, Porz, Rodenkirchen, Lindenthal, Ehrenfeld, Chorweiler |
| `renders/knigge-standort-wipperfuerth.gif` | Wipperfürth (Oberbergischer Kreis) | Radevormwald, Marienheide, Bergneustadt, Gummersbach, Wiehl, Engelskirchen, Lindlar, Hückeswagen |
| `renders/knigge-standort-rheinisch-bergischer-kreis.gif` | Rheinisch-Bergischer Kreis | Burscheid, Wermelskirchen, Kürten, Overath, Rösrath, Bergisch Gladbach, Odenthal, Leichlingen |
| `renders/knigge-standort-einzugsgebiet.gif` | KNIGGE-Logo – gesamtes Einzugsgebiet | Köln (W), Rheinisch-Bergischer Kreis (N), Wipperfürth/Oberbergischer Kreis (O), Bergisch Gladbach – Hauptsitz (S), jeweils mit ihren Orten |

Einzelne Gebiete: 1200×680 px, 7,2 s. Einzugsgebiet: 1920×1080 px, 10,2 s – am besten groß zeigen
(Präsentation, TV, Website in voller Breite).

Zu jedem GIF gibt es eine gleichnamige **`.webp`**: GIF kennt nur „ganz sichtbar oder ganz
transparent“, das animierte WebP hat weiche Kanten und ist kleiner – für Websites die bessere Wahl,
für PowerPoint/Keynote das GIF. Die Animation nutzt deshalb keine Blenden, nur Skalieren und Zeichnen.

## Orte ändern & neu erzeugen

Namen in `tools/build.py` (Abschnitte `REGIONS` und `COMBINED`) tauschen, dann:

```bash
npm run build    # schreibt index.html und formats/*.html
npm run check    # Lint, Layout, Kontrast
npm run export   # rendert PNG-Sequenzen (RGBA) und baut GIF + WebP (ffmpeg mit libwebp, optional gifsicle)
```

Die Orte stehen in der richtigen Reihenfolge rund um ihre Mitte, aber nicht maßstabs- oder
richtungsgenau (Wipperfürth liegt z. B. am Nordrand des Oberbergischen Kreises). In der
Gesamtgrafik fehlt „Köln-Ost“ bei Bergisch Gladbach, weil Köln dort eine eigene Gruppe hat.

## Karten im Stil der Gebietskarte

Dieselben Standorte als echte Karte: hellgraue Flächen, weiße Grenzen, blauer Rhein, rot-weiße
Standort-Marker und das neue KNIGGE-Logo. Die Flächen wachsen von innen nach außen auf, der Rhein
wird gezeichnet, dann erscheinen Namen, Marker und Logo. 25 fps, 7,8 s, Endlosschleife.

| Datei | Inhalt | Größe |
| --- | --- | --- |
| `renders/knigge-standort-karte-koeln.gif` | Köln mit den 9 Stadtbezirken, Standort Innenstadt (Sachsenring) hervorgehoben | 1200×800 px |
| `renders/knigge-standort-karte-einzugsgebiet.gif` | Köln, Rheinisch-Bergischer Kreis und Oberbergischer Kreis mit den Standorten Köln, Bergisch Gladbach und Wipperfürth (Leverkusen heller als Lückenschluss) | 1920×1080 px |

Auch hier gibt es jeweils eine `.webp` mit weichen Kanten.

```bash
npm run build:maps                    # schreibt formats/karte-*.html (braucht Python mit shapely)
bash tools/export.sh karte-koeln      # nur eine Animation exportieren
```

Kartengrundlage ist `assets/geo/region.json`, erzeugt mit `tools/geo/prepare.py` (Quellen im
Kopf der Datei). Die Kölner Stadtbezirke sind aus den 86 Stadtteilen zusammengesetzt und an der
amtlichen Stadtgrenze ausgerichtet; der Rhein ist die gemeinsame Grenze der links- und
rechtsrheinischen Gebiete. Karten auf Gemeindeebene (Bergisch Gladbach mit Nachbarn,
Rheinisch-Bergischer Kreis, Oberbergischer Kreis) folgen, sobald Gemeindegrenzen vorliegen
(`prepare.py --gemeinden`).

Quellen und Lizenzen (Nennung steht klein unten rechts in jeder Karte):

- Kreisgrenzen: © GeoBasis-DE / BKG 2023 (VG250), [Datenlizenz Deutschland – Namensnennung 2.0](https://www.govdata.de/dl-de/by-2-0),
  bezogen über [geoBoundaries](https://www.geoboundaries.org/)
- Kölner Stadtteile: Stadt Köln (Offene Daten Köln), bezogen über
  [click_that_hood](https://github.com/codeforgermany/click_that_hood)
