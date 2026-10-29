---
workflow: hyperframes
flow: automation
storyboard: "no"
message: "Drei Standorte. Eine Region. – KNIGGE Immobilien ist zwischen Köln und Oberberg vor Ort, mit einem Ansprechpartner für Ihre Immobilie."
destination: instagram-reels
aspect: 1080x1920
language: de
length: 15s
narration: "no"
sound: "no"
---

## Intent

Instagram-Reel aus der Einzugsgebiet-Karte von KNIGGE Immobilien (`../knigge-standorte-gifs`,
Karte `formats/karte-einzugsgebiet.html`), Anfrage: „Mache mir daraus ein instagram reel“.

Vom Nutzer gewählt (Rückfragen vom 29.10.2026):

- **Länge:** 15 Sekunden
- **Botschaft:** Einstieg „Drei Standorte. Eine Region.“, Abschluss „Ein Ansprechpartner für Ihre
  Immobilie.“ + knigge-immobilien.de
- **Ton:** keiner – Musik wählt der Nutzer in Instagram selbst
- **Ablauf:** kein Storyboard vorab, direkt fertiges Reel, Feedback danach

## Inferred (nicht ausdrücklich gefragt)

- flow `automation` – „Mache mir daraus …“ ist ein Bauauftrag
- Ablauf: Übersicht der Region → Kamerafahrt zu Köln → Bergisch Gladbach (Hauptsitz) → Wipperfürth →
  zurück zur Übersicht mit Abschluss, Logo und Adresse. Die Kamera fährt, weil die Ortsnamen in der
  Gesamtansicht auf 1080 px Breite unter der Lesegrenze von 28 px lägen.
- Gemeinden wie in der Einzugsgebiet-Karte vom 14.10.2026: Köln, Leverkusen, Pulheim, Frechen, Hürth,
  die 8 Gemeinden des Rheinisch-Bergischen Kreises und aus dem Oberbergischen Kreis Wipperfürth,
  Hückeswagen, Radevormwald, Marienheide, Lindlar, Engelskirchen.
- Gestaltung: KNIGGE-CI wie in `../knigge-vip-suche/frame.md` (Montserrat, Schiefergrau #444F4F,
  KNIGGE-Rot #CA2C35), Kartenstil wie in den GIFs auf weißem Grund, neues Logo.
- 30 fps, H.264, kein Audiokanal.

## Assets

- Kartengrundlage und Beschriftungsprüfung aus `../knigge-standorte-gifs` (`assets/geo/region.json`,
  `tools/label_layout.py`).
- Logo (K-Bildmarke + Wortmarke) wie in `../knigge-standorte-gifs/tools/build_maps.py`.

## Notes

- Reels-Oberfläche: kein Text oberhalb 168 px, aller Text im Band 168–1330 px, nicht unter der
  Aktionsleiste rechts.
- Gemeindegrenzen sind schematisch (siehe Quellenhinweis der Karte).
