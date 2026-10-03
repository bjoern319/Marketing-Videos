# gewo-gl – „Wie wollen wir morgen in Bergisch Gladbach wohnen?“

Info- und Werbefilm (76 s, 16:9) für die Gemeinschaft für Wohnen Bergisch Gladbach e.V.: vom Leitgedanken
„Vorhandenes neu denken“ über die drei Wege zu mehr Wohnraum bis zum Aufruf an Eigentümer. Gebaut mit
[HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → Video). CI nach gewo-gl.de: Lato,
Dunkelgrün-Anthrazit #2A3737, Oliv #5E742E, Logo-Grün #6BA221, dunkle Sektion #283434.

| Datei | Format | Einsatz |
| --- | --- | --- |
| `renders/gewo-gl-infovideo-16x9.mp4` | 1920×1080 quer | Website, YouTube, Präsentationen |
| `renders/gewo-gl-infovideo-16x9-4k.mp4` | 3840×2160 quer | YouTube, Fernseher (optional) |

Renders entstehen lokal mit `npm run render` und werden nicht eingecheckt.

## Psychologischer Aufbau

| Zeit | Szene | Inhalt | Hebel |
| --- | --- | --- | --- |
| 0:00 | Hook | „Wie wollen wir morgen in Bergisch Gladbach wohnen?“ → „Vielleicht steckt in einer Immobilie mehr, als man auf den ersten Blick sieht.“ Häuserzeile mit gestrichelten Potenzialen | Offene Frage + Wir-Gefühl, Neugier-Lücke |
| 0:06 | Marke | Bildmarke zeichnet sich als eine Linie; „Mehr bedarfsgerechten Wohnraum schaffen. Vorhandene Flächen besser nutzen. Neue Formen des Zusammenlebens ermöglichen.“ | Wert vor Beweis, Dreier-Regel, Wiedererkennung |
| 0:12 | Drei Wege | Kamerafahrt durch eine Straße: 01 Wohnraum besser nutzen · 02 Gewerbeflächen umnutzen · 03 Baulücken aktivieren | Bildüberlegenheit, Chunking |
| 0:27 | Höhepunkt | Totale: alle Potenziale werden zu Licht – „Aus ungenutztem Raum wird Zuhause.“ | Peak-End-Regel, Zukunftsbild |
| 0:32 | Wohnformen | Haus im Querschnitt, private Wohnungen + Gästezimmer, Gemeinschaftsraum, Werkstatt, Garten; „Gemeinschaft bedeutet nicht, Privatsphäre aufzugeben.“ | Identifikation, Einwandbehandlung |
| 0:42 | Ziele | Zukunft bauen · Quartiere gestalten · Gemeinschaft leben | Werte-Übereinstimmung |
| 0:50 | Vertrauen | 10 Gründungsmitglieder (Count-up), Vorstand namentlich, gemeinnützig & unabhängig | Social Proof, Autorität |
| 0:57 | Entscheidung | „Ihre Immobilie. Ihre Entscheidung.“ Eigentümer bleiben · Genossenschaft (geplant) · Stiftung (geplant) | Autonomie statt Druck, Risiko senken |
| 1:06 | Aufruf | Dunkle Sektion „Mit einem Hinweis kann es beginnen: Sie sind Eigentümer – oder kennen jemanden?“ → Endkarte gewo-gl.de | Kleiner erster Schritt, Empfehlung, Peak-End |

Konzipiert für Ton-aus: alle Aussagen stehen als Text im Bild, Musik und Soundeffekte unterstützen nur.

## Projektstruktur

```
index.html            16:9-Host: Szenen, Musik, Soundeffekte
compositions/         hook · brand · street · wohnformen · ziele · trust · entscheidung · cta
assets/logo/          Bildmarke (Vektor-Nachbau, siehe unten)
assets/audio/         Musik (eigene Synthese, siehe tools/music) · sfx/ (wird geholt, siehe dort)
assets/vendor/        GSAP lokal, damit Renders offline funktionieren
tools/                fetch-sfx.sh · music/make_bgm.py
BRIEF.md · frame.md
```

## Vorschau & Rendern

Benötigt Node ≥ 22 und FFmpeg.

```bash
npm run dev            # Studio-Vorschau
npm run check          # Lint, Layout, Kontrast
npm run render         # 1080p-Master → renders/gewo-gl-infovideo-16x9.mp4
npm run render:4k      # optional 4K
```

Alle drei holen vorher die Soundeffekte (`npm run sfx`).

## Musik

Warmer Pad-/Mallet-Bed in C-Dur, 96 BPM. Jeder Szenenwechsel liegt auf einem ganzen oder halben Takt
(1 Takt = 2,5 s), der Höhepunkt bei 27,5 s, die Auflösung auf der Endkarte. Deterministisch neu
erzeugen (Python mit `numpy` und `scipy`, dazu FFmpeg):

```bash
npm run music
```

## Quellen

- Texte und Inhalte: Webseite gewo-gl.de (Hero, Ziele, Raum für neue Wohnformen, Drei Wege, Zusammenarbeit, Aufruf)
- Gründung am 1.9.2026, 10 Gründungsmitglieder, Vorstand, „gemeinnützig“ und „unabhängig“: Bürgerportal in-gl.de (24./25.9.2026)

## Vor Veröffentlichung prüfen

- **Logo:** `assets/logo/gewo-gl-logo.svg` (inline in `compositions/brand.html` und `compositions/cta.html`) ist
  ein Vektor-Nachbau des gelieferten 96×72-px-Logos – durch die Original-Vektordatei ersetzen.
- **Fakten aus der Presse:** Vorstand, 10 Gründungsmitglieder, „gemeinnützig“, „unabhängig“ (`compositions/trust.html`).
- **„geplant“:** Genossenschaft und Stiftung sind als geplant gekennzeichnet (`compositions/entscheidung.html`).
