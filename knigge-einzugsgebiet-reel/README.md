# KNIGGE Immobilien – Instagram-Reel „Drei Standorte. Eine Region.“

**Version 2 „Drei Facetten“:** 18 Sekunden, 1080×1920, 30 fps, ohne Ton (Musik wird in Instagram
gewählt). Die drei Facetten der KNIGGE-Bildmarke werden die drei Standorte auf der Einzugsgebiet-Karte
aus den Standort-GIFs (`../knigge-standorte-gifs`) und setzen sich am Ende wieder zum Logo zusammen:

| Zeit | Szene | Inhalt |
| --- | --- | --- |
| 0–2,4 s | `s1-hook` | „Drei Standorte. Eine Region.“ mit Marker-Strich, das K springt auseinander, die Karte wächst, die Facetten fliegen zu den Standorten und werden Pins |
| 2,4–4 s | `s2-region` | „Zwischen Köln und Oberberg“ |
| 4–6,6 s | `s3-koeln` | Kamera auf Köln: Leverkusen, Pulheim, Frechen, Hürth |
| 6,6–9,2 s | `s4-bergisch-gladbach` | Hauptsitz Bergisch Gladbach: die übrigen Gemeinden des Rheinisch-Bergischen Kreises |
| 9,2–11,8 s | `s5-wipperfuerth` | Wipperfürth: Hückeswagen, Radevormwald, Marienheide, Lindlar, Engelskirchen |
| 11,8–14,6 s | `s6-zahl` | „19 Städte und Gemeinden“ – Zahlenrad, die Gemeinden leuchten nacheinander auf |
| 14,6–18 s | `s7-abschluss` | die Facetten fliegen zurück ins Logo, „Ein Ansprechpartner für Ihre Immobilie.“, knigge-immobilien.de |

Die Karte selbst (Gemeinden, Rhein, Pins, Kamera) ist die Komposition `karte`, die unter allen Szenen
läuft. Idee und weitere Varianten: `STORYLINES.md`, Gestaltung: `SPEC.md`, Prüfung: `REVIEW.md`.

Fertige Videos (im Repo bjoern319/Marketing-Videos): `renders/knigge-einzugsgebiet-reel-v2.mp4`
(Version 2) und `renders/knigge-einzugsgebiet-reel.mp4` (Version 1, 15 s; Quelltext in der
Git-Historie: personal-website 4b93cc2, Marketing-Videos 08783a5).

## Ändern & neu erzeugen

```bash
npm run build    # python3 tools/build_reel.py – schreibt index.html und compositions/*.html
npm run check    # Lint, Layout, Kontrast, Lesbarkeit
npm run render   # renders/knigge-einzugsgebiet-reel-v2.mp4
```

- Texte: oben in `tools/build_reel.py` (`TEXT`).
- Zeiten und Kamera: `SCENES` (Start, Dauer, Fahrzeit, Zoom-Faktor, Gemeinden im Bild, Namen).
- Gemeinden, Farben, Standorte und Logo kommen aus `../knigge-standorte-gifs/tools/build_maps.py`
  (Einzugsgebiet-Karte), die Flächen aus `../knigge-standorte-gifs/assets/geo/region.json`. Änderungen
  dort übernimmt das Reel beim nächsten `npm run build`.
- Jeder Ortsname wird mit der echten Schrift gemessen (`label_layout.py` aus dem GIF-Projekt) und so
  gesetzt, dass er mindestens 28 px groß mit Abstand in seine Fläche passt. Text bleibt im
  Instagram-Band 168–1330 px und nicht unter der Aktionsleiste rechts.
- Zahlenrad und Marker-Strich stammen aus der HyperFrames-Registry (`compositions/components/`).

Gemeindegrenzen sind schematisch (Quellen: README von `../knigge-standorte-gifs`).
