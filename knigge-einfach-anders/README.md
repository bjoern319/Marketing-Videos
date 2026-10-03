# KNIGGE Immobilien – „einfach anders." (Info-/Werbevideo)

Ein ca. 72 Sekunden langes Video (1920×1080, 30 fps), gebaut mit [HyperFrames](https://hyperframes.heygen.com)
(HTML + GSAP → MP4). Es zeigt, warum KNIGGE Immobilien aus Bergisch Gladbach „einfach anders" ist,
und lässt den Zuschauer selbst prüfen, ob KNIGGE der passende Makler für ihn ist.

**Video:** `renders/knigge-einfach-anders.mp4` (wird beim Rendern erzeugt, liegt nicht im Repo) – 1920×1080, 30 fps, 72,5 s.

## Ablauf und Psychologie

| # | Szene | Zeit | Inhalt | Psychologisches Prinzip |
|---|-------|------|--------|-------------------------|
| 1 | Hook | 0–6 s | „Makler gibt es viele. Hausverwaltungen auch. Einer ist anders." – ein Raster gleicher Häuser, ein Feld wird zum roten KNIGGE-Quadrat und zoomt bildfüllend | Pattern Interrupt, Neugierlücke, **Von-Restorff-Effekt** (das eine Andere fällt auf) |
| 2 | Marke | 6–11,5 s | Rote Fläche → Bildmarke → „KNIGGE IMMOBILIEN – einfach anders." | Auflösung der Neugierlücke, Marken-Anker (Mere-Exposure) |
| 3 | Klischees | 11,5–27,5 s | Vier Makler-Klischees werden rot durchgestrichen und durch die KNIGGE-Antwort ersetzt (Bewertung, Betreuung, Diskretion, Langfristigkeit) | **Kontrastprinzip** (ohne Wettbewerber zu nennen) |
| 4 | Ein Dach | 27,5–36 s | Vermitteln · Verwalten · Gestalten – Verkauf, Vermietung, Verwaltung, Entwicklung aus einer Hand | Dreierregel (Chunking), Reibungsreduktion |
| 5 | Zahlen | 36–46 s | 20 Jahre · rund 1.600 Wohneinheiten · 17 Menschen · Inhaber = zertifizierter Gutachter · „Service eines großen Unternehmens, Persönlichkeit eines Familienbetriebs" | **Social Proof**, **Autorität**, Anker-Zahlen |
| 6 | Heimat | 46–54 s | „Wir sind von hier." – Stadtteile rund um die Stadtmitte (Laurentiusstraße 98) | **Sympathie/Ähnlichkeit** (lokale In-Group), Spezifität |
| 7 | Selbst-Check | 54–63,5 s | „Ist KNIGGE der richtige Makler für Sie?" – vier Häkchen → „Dann sind wir Ihr Makler." | **Commitment & Konsistenz** (Ja-Leiter), Selbstreferenz, Verlustaversion („nicht unter Wert verkaufen") |
| 8 | Kontakt | 63,5–72,5 s | „Lernen wir uns kennen. Persönlich. Unverbindlich." + Telefon, Web, YouTube (KNIGGE.Immobilien), Instagram (@kniggeimmobilien), Adresse, Motto | Reziprozität/Reibungsreduktion („unverbindlich"), **Peak-End-Regel** (Motto als letzter Eindruck) |

Durchgehend: eine Idee pro Szene, kurze Texte mit hohem Kontrast (Processing Fluency), Rot nur als Akzent
(Logo-Rot als Wiedererkennungsanker). Kein Voiceover – das Video funktioniert auch stumm (Social Media).

## Marke

- CI wie knigge-immobilien.de (und das Projekt `knigge-wohnen-im-ruhestand`): KNIGGE-Rot `#CA2C35`, Bordeaux `#6D131B`,
  Schiefergrau `#444F4F`, Hellgrau `#ECEEEA`. Dunkle Szenen in abgedunkeltem Schiefergrau `#2C3535`, rote Schrift auf
  Dunkel als lesbare Tönung `#E8656B`.
- Schrift: Montserrat (OFL, liegt in `assets/fonts/`); Wortmarke KNIGGE 700, IMMOBILIEN 400 gesperrt.
- **Logo:** Bildmarke (K-Faltung) als SVG nachgebaut – Geometrie und Verläufe wie in `knigge-wohnen-im-ruhestand`
  (am Website-Logo vermessen), inline in den Szenen und als `assets/brand/knigge-icon.svg`. Für den offiziellen
  Einsatz die Original-Vektordatei verwenden.

## Fakten – bitte vor Veröffentlichung prüfen

knigge-immobilien.de war aus der Build-Umgebung nicht erreichbar; die Inhalte stammen aus Suchergebnissen zur
Webseite und aus Artikeln auf in-gl.de: seit 2006, Motto „einfach anders", Inhaber Oliver Knigge (Kaufmann der
Grundstücks- und Wohnungswirtschaft, zertifizierter Immobiliengutachter), 17 Mitarbeitende, rund 1.600 verwaltete
Wohneinheiten, Laurentiusstraße 98, Büros in Köln und Wipperfürth, „Verkauf unter vier Augen", Tel. 02202 1240300,
YouTube-Kanal „KNIGGE.Immobilien", Instagram @kniggeimmobilien.
Alle Texte stehen direkt in `compositions/frames/*.html`.

## Projektstruktur

```
BRIEF.md            Auftrag, Zielgruppe, Kernbotschaft
STORYBOARD.md       Szenenplan (Dauer, Übergänge, Psychologie je Szene)
frame.md            Designsystem (Farben, Typo, Komponenten)
compositions/frames/ die 8 Szenen (je eine HyperFrames-Sub-Komposition)
index.html          Gesamt-Timeline (aus STORYBOARD + audio_meta.json gebaut)
audio_meta.json     Musik + Soundeffekte (Zeitpunkte je Szene)
assets/             Schrift, GSAP (lokal), Logo, Musik, SFX
scripts/            make-music.py (Musikbett), build-index.sh (index.html neu bauen)
```

## Vorschau und Rendern

```bash
cd knigge-einfach-anders
npx hyperframes browser ensure          # einmalig: Chrome für den Renderer
npm run dev                             # Studio-Vorschau im Browser
npm run check                           # Lint + Layout + Kontrast
npx hyperframes render --quality high --output renders/knigge-einfach-anders.mp4
```

Nach Änderungen an Storyboard-Dauern oder Sounds: `./scripts/build-index.sh` (benötigt die installierten
HyperFrames-Skills, `npx hyperframes skills update product-launch-video`).
Musik neu erzeugen: `python3 scripts/make-music.py` (numpy), danach als MP3 nach `assets/audio/knigge-bgm.mp3`.

## Audio

- Musikbett: eigens synthetisiert (`scripts/make-music.py`), keine Fremdrechte.
- Soundeffekte: aus der HyperFrames-SFX-Bibliothek (Pixabay Content License, siehe `assets/sfx/CREDITS.md`).
