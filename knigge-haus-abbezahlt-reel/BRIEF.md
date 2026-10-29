---
workflow: hyperframes
flow: automation
storyboard: "no"
message: "Das Haus ist abbezahlt – aber die Kosten bleiben. Es gibt mehrere Wege; welche, zeigt der Expertenbeitrag von Andrea Gerhardus auf in-gl.de."
destination: instagram-reels
aspect: 1080x1920
language: de
length: 27.75s
narration: "no"
sound: music
font: Red Hat Display
---

## Intent

Instagram-Reel zum Karussell „Das Haus ist abbezahlt. Aber können wir es uns noch leisten?“ (6 Folien,
Expertenbeitrag von Andrea Gerhardus auf in-gl.de). Anfrage: „Auch dafür brauche ich ein cooles Reel!“

Vom Nutzer gewählt (Rückfragen vom 29.10.2026):

- **Idee:** „Entscheide selbst – vielleicht schaffst du alles in einem unterzubringen“ → ein Film aus
  allen drei Storylines (`STORYLINES.md`): das rote „Aber“ als Schnitt (A), der Kassenbon für die
  Kosten (C), die Waage für Aufgaben und Optionen (B).
- **Fotos:** keine Originale – die freien Bildteile der Screenshots werden genutzt.
- **Ton:** die KNIGGE-Musik aus `../knigge-wohnen-im-ruhestand` (eigene Komposition, lizenzfrei).
- **Bildunterschrift:** „Andrea Gerhardus, Immobilienexpertin bei KNIGGE Immobilien“.
- **Schrift:** Red Hat Display – ab jetzt die Schrift für alle Videos (Nachricht vom 29.10.2026,
  abgelegt in bjoern319/Marketing-Videos `fonts/red-hat-display/`).

## Inferred (nicht ausdrücklich gefragt)

- Länge 27,75 s: die Musik (80 BPM, 1 Takt = 3 s) ist die Uhr. Schnitt aus dem Stück: 8,25–30 s und
  69–75 s; die Auflösung (F-Dur) liegt auf „Welche Optionen gibt es?“, der Schlussakkord auf dem Logo.
- Texte wörtlich aus dem Karussell. „Pflege und Instandhaltung kosten Zeit und Kraft.“ ist im
  Screenshot halb verdeckt – „kosten“ angenommen.
- Fotos: Haus (Folie 1), Schreibtisch (Folie 2), Andrea Gerhardus (Folie 5), Kaffeetisch (Folie 6).
  Eingebrannte Schrift und Instagram-Oberfläche liegen außerhalb des Ausschnitts oder werden entfernt
  und liegen unter dem weißen Lichtschleier des Karussells. Paar (Folie 3) und Wohnzimmer (Folie 4)
  bleiben ungenutzt: die Waage steht auf Weiß, damit sie klar liest.
- Kein Sprecher, keine Untertitel – alle Aussagen stehen als Text im Bild.
- Farben aus dem Karussell gemessen: Schiefer #323C44 (Überschriften), KNIGGE-Rot #CA2C35.

## Assets

- Screenshots der sechs Folien (`assets/source/`), daraus die Fotos in `assets/img/`.
- Musik: `../knigge-wohnen-im-ruhestand/assets/audio/knigge-theme.m4a` → `assets/audio/`.
- Logo (Bildmarke + Wortmarke) wie in `../knigge-standorte-gifs/tools/build_maps.py`.
- Schrift: `assets/fonts/red-hat-display.woff2` (SIL OFL 1.1).

## Notes

- Reels-Oberfläche: kein Text oberhalb 168 px, aller Text im Band 168–1330 px, kein Text unter der
  Aktionsleiste rechts (x > 940 ab y 1000).
