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
