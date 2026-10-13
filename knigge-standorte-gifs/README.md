# KNIGGE Immobilien – Standort-Animationen (transparent)

Die Orts-Konstellation aus dem Film „Nicht weniger Zuhause. Mehr Leben.“ als freigestellte
Animation für die drei KNIGGE-Standorte – zum Einsetzen auf Website, in Präsentationen oder
über eigene Hintergründe. 1200×680 px, 25 fps, 7,2 s, Endlosschleife (Aufbau → Halten → Abbau).

| Datei | Mitte | Orte (im Uhrzeigersinn ab Norden) |
| --- | --- | --- |
| `renders/knigge-standort-bergisch-gladbach.gif` | Bergisch Gladbach (Hauptsitz) | Paffrath, Herkenrath, Moitzfeld, Bensberg, Frankenforst, Refrath, Köln-Ost, Schildgen |
| `renders/knigge-standort-koeln.gif` | Köln (Standort Sachsenring) | Stadtbezirke Nippes, Mülheim, Kalk, Porz, Rodenkirchen, Lindenthal, Ehrenfeld, Chorweiler |
| `renders/knigge-standort-wipperfuerth.gif` | Wipperfürth (Oberbergischer Kreis) | Radevormwald, Marienheide, Bergneustadt, Gummersbach, Wiehl, Engelskirchen, Lindlar, Hückeswagen |

Zu jedem GIF gibt es eine gleichnamige **`.webp`**: GIF kennt nur „ganz sichtbar oder ganz
transparent“, das animierte WebP hat weiche Kanten und ist kleiner – für Websites die bessere Wahl,
für PowerPoint/Keynote das GIF. Die Animation nutzt deshalb keine Blenden, nur Skalieren und Zeichnen.

## Orte ändern & neu erzeugen

Namen in `tools/build.py` (Abschnitt `REGIONS`) tauschen, dann:

```bash
npm run build    # schreibt index.html, formats/koeln.html, formats/wipperfuerth.html
npm run check    # Lint, Layout, Kontrast
npm run export   # rendert PNG-Sequenzen (RGBA) und baut GIF + WebP (benötigt ffmpeg mit libwebp)
```

Wipperfürth liegt am Nordrand des Kreises; die Nachbarorte stehen deshalb in der richtigen
Reihenfolge rund um die Mitte, aber nicht maßstabs- oder richtungsgenau.
