---
workflow: general-video
flow: automation
storyboard: no
mode: autonomous
message: "In Bergisch Gladbach schlummert Wohnraum im Bestand – gewo-gl macht ihn gemeinsam nutzbar. Machen Sie mit."
destination: website / YouTube / Präsentation
aspect: 1920x1080
length: 76s
language: de (Sie-Ansprache)
audience: Eigentümer:innen, Fachleute, engagierte Bürger:innen in Bergisch Gladbach
narration: no (Text-on-screen + Musik + SFX)
---

# gewo-gl – Info-Werbevideo

## Intent

Info-/Werbevideo für die **Gemeinschaft für Wohnen Bergisch Gladbach e.V. (gewo-gl)** im Stil der Webseite
(Lato, Dunkel-Grün-Anthrazit #2A3737, Oliv #5E742E, Logo-Grün #6BA221, dunkle Sektion #283434).
Quellen: Webseite gewo-gl.de (Screenshots/Texte vom Nutzer) und Bürgerportal in-gl.de (Gründung, Vorstand).

## Storyboard (76,25 s, 1 Takt Musik = 2,5 s)

| Zeit | Szene | Inhalt | Psychologie |
| --- | --- | --- | --- |
| 0–6,25 | Hook | „Wie wollen wir morgen in Bergisch Gladbach wohnen?" → „Vielleicht steckt in einer Immobilie mehr, als man auf den ersten Blick sieht." | Offene Frage + Wir-Gefühl, Neugier-Lücke |
| 6,25–12,5 | Marke | Logo zeichnet sich als eine Linie + Dreiklang der Webseite: „Mehr bedarfsgerechten Wohnraum schaffen. Vorhandene Flächen besser nutzen. Neue Formen des Zusammenlebens ermöglichen." | Wert vor Beweis, Dreier-Regel, Wiedererkennung |
| 12,5–27,5 | Drei Wege | Kamerafahrt: 01 Wohnraum besser nutzen · 02 Gewerbeflächen umnutzen · 03 Baulücken aktivieren | Dreier-Regel, Bildüberlegenheit |
| 27,5–32,5 | Höhepunkt | „Aus ungenutztem Raum wird Zuhause." | Peak-End-Regel |
| 32,5–42,5 | Wohnformen | Haus im Querschnitt, privat + gemeinsam; „Gemeinschaft bedeutet nicht, Privatsphäre aufzugeben." | Identifikation, Einwandbehandlung |
| 42,5–50 | Ziele | Zukunft bauen · Quartiere gestalten · Gemeinschaft leben | Werte-Übereinstimmung |
| 50–57,5 | Vertrauen | 10 Gründungsmitglieder, Vorstand, gemeinnützig & unabhängig | Social Proof, Autorität |
| 57,5–66,25 | Entscheidung | „Ihre Immobilie. Ihre Entscheidung." Eigentümer bleiben · Genossenschaft (geplant) · Stiftung (geplant) | Autonomie/Reaktanz vermeiden, Risiko senken |
| 66,25–76,25 | CTA | Dunkle Sektion: „Mit einem Hinweis kann es beginnen – Sie sind Eigentümer – oder kennen jemanden?" → Endkarte gewo-gl.de | Niedrigschwelliger CTA (Foot-in-the-door), Empfehlung, Peak-End |

## Assets

- Logo: vom Nutzer geliefert (96×72 px), als Vektor nachgezeichnet → `assets/logo/gewo-gl-logo.svg`
  (für den finalen Einsatz durch die Original-Vektordatei ersetzen).
- Farben und Schrift nach gewo-gl.de: siehe `frame.md` (Lato; #2A3737, #5E742E, Logo-Grün #6BA221, dunkle Sektion #283434).
- Musik: `tools/music/make_bgm.py` (deterministisch synthetisiert) → `assets/audio/gewo-gl-theme.m4a`.
- SFX: Pixabay (Content License) aus der HyperFrames-Mediathek, per `tools/fetch-sfx.sh` geholt, nicht eingecheckt.
