# KNIGGE Immobilien – Instagram-Reel „Drei Standorte. Eine Region.“

15 Sekunden, 1080×1920, 30 fps, ohne Ton (Musik wird in Instagram gewählt). Die Einzugsgebiet-Karte aus
den Standort-GIFs (`../knigge-standorte-gifs`) als Kamerafahrt:

| Zeit | Szene | Inhalt |
| --- | --- | --- |
| 0–2,6 s | `b1-hook` | „Drei Standorte. Eine Region.“ über der ganzen Region, Rhein zeichnet sich, drei Standorte fallen und pulsen |
| 2,6–5,4 s | `b2-koeln` | Kamera auf Köln: Leverkusen, Pulheim, Frechen, Hürth |
| 5,4–8,2 s | `b3-bergisch-gladbach` | Hauptsitz Bergisch Gladbach: die übrigen Gemeinden des Rheinisch-Bergischen Kreises |
| 8,2–11 s | `b4-wipperfuerth` | Wipperfürth: Hückeswagen, Radevormwald, Marienheide, Lindlar, Engelskirchen |
| 11–15 s | `b5-abschluss` | zurück zur Übersicht, „Ein Ansprechpartner für Ihre Immobilie.“, Logo, knigge-immobilien.de |

Fertiges Video: `renders/knigge-einzugsgebiet-reel.mp4` (im Repo bjoern319/Marketing-Videos).

## Ändern & neu erzeugen

```bash
npm run build    # python3 tools/build_reel.py – schreibt index.html und compositions/*.html
npm run check    # Lint, Layout, Kontrast, Lesbarkeit
npm run render   # renders/knigge-einzugsgebiet-reel.mp4
```

- Texte: oben in `tools/build_reel.py` (`TEXT`) – oder in Studio über die Variablen der Szenen.
- Zeiten und Kamera: `BEATS` (Start, Dauer, Fahrzeit, Zoom-Faktor, Gemeinden im Bild, Namen).
- Gemeinden, Farben, Standorte und Logo kommen aus `../knigge-standorte-gifs/tools/build_maps.py`
  (Einzugsgebiet-Karte), die Flächen aus `../knigge-standorte-gifs/assets/geo/region.json`. Änderungen
  dort übernimmt das Reel beim nächsten `npm run build`.
- Jeder Ortsname wird mit der echten Schrift gemessen (`label_layout.py` aus dem GIF-Projekt) und so
  gesetzt, dass er mindestens 30 px groß mit Abstand in seine Fläche passt. Text bleibt im
  Instagram-Band 168–1330 px und nicht unter der Aktionsleiste rechts.

Gemeindegrenzen sind schematisch (Quellen: README von `../knigge-standorte-gifs`).
