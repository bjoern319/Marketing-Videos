# KNIGGE Immobilien – „Nicht weniger Zuhause. Mehr Leben.“

Info- und Werbefilm (75 s) für Eigentümer im Ruhestand: vom zu groß gewordenen Haus in eine
komfortable Wohnung – begleitet von KNIGGE Immobilien. Gebaut mit [HyperFrames](https://github.com/heygen-com/hyperframes)
(HTML → Video), eine Szenenbasis für beide Formate. CI nach knigge-immobilien.de: Montserrat,
Rot #CA2C35, Bordeaux #6D131B, Schiefergrau #444F4F, Hellgrau #ECEEEA.

Gleicher Inhalt in beiden Formaten:

| Datei | Format | Einsatz |
| --- | --- | --- |
| `renders/knigge-wohnen-im-ruhestand-9x16-4k.mp4` | 2160×3840 hochkant | YouTube Shorts · Fernseher mit Hochkant-Wiedergabe |
| `renders/knigge-wohnen-im-ruhestand-9x16.mp4` | 1080×1920 hochkant | Instagram Reels/Stories, Facebook |
| `renders/knigge-wohnen-im-ruhestand-tv-4k-gedreht-im-uhrzeigersinn.mp4` | 3840×2160, Inhalt 90° gedreht | Fernseher hochkant montiert, ohne Drehfunktion |
| `renders/knigge-wohnen-im-ruhestand-tv-4k-gedreht-gegen-uhrzeigersinn.mp4` | 3840×2160, Inhalt 90° gedreht | dito – falls das Bild mit der anderen Datei auf dem Kopf steht |
| `renders/knigge-wohnen-im-ruhestand-16x9-4k.mp4` | 3840×2160 quer | YouTube · Fernseher quer |
| `renders/knigge-wohnen-im-ruhestand-16x9.mp4` | 1920×1080 quer | Website, Präsentationen, Social quer |

## Psychologischer Aufbau

| Zeit | Szene | Inhalt | Hebel |
| --- | --- | --- | --- |
| 0:00 | Ihr Haus | „Erinnern Sie sich an den Tag, an dem Sie hier eingezogen sind?“ – Haus zeichnet sich, Lichter gehen an | Nostalgie, Identifikation („das bin ich“) |
| 0:09 | Stille | Lichter gehen aus; Treppen, Gartenarbeit, Heizkosten … fallen aufs Haus | Pacing der Gegenwart – empathisch, ohne Angstappell |
| 0:18 | Mehr Leben | Haus verwandelt sich in Wohnung: „Nicht weniger Zuhause. **Mehr Leben.**“ | Reframing: Verlust → Gewinn |
| 0:24 | Vorteile | Aufzug statt Treppen · Balkon statt Gartenarbeit · Bäcker & Arzt um die Ecke · sorgenfrei verreisen · freies Kapital | Future Pacing, Kontrastprinzip |
| 0:39 | Zeitpunkt | „Solange Sie ihn **selbst** bestimmen können.“ | Autonomie + sanfte Dringlichkeit |
| 0:45 | Begleitung | „Und der ganze Aufwand? Den nehmen **wir** Ihnen ab.“ – 4 Schritte | Einwandbehandlung, Risikoreduktion |
| 0:57 | Vor Ort | Stadtteile rund um Bergisch Gladbach, rund 1.600 verwaltete Wohneinheiten | Sympathie (Nähe), Autorität |
| 1:06 | Kontakt | „Lassen Sie uns sprechen – gern bei einer Tasse Kaffee.“ Kostenloses Beratungsgespräch | Reziprozität, kleiner erster Schritt, Peak-End |

Konzipiert für Ton-aus (Instagram): alle Aussagen stehen als Text im Bild. Ein optionaler
Sprechertext liegt in `SCRIPT.md`.

## Projektstruktur

```
index.html              16:9-Host (YouTube)
formats/9x16.html       9:16-Host (Reels) – nutzt dieselben Szenen
compositions/           Szenen (Layout passt sich per Container-Queries an)
  bg.html  chrome.html  s1-haus.html … s6-kontakt.html
assets/audio/           Musik (eigene Komposition, siehe tools/music)
assets/vendor/          GSAP (lokal, damit Renders offline funktionieren)
BRIEF.md · frame.md · STORYBOARD.md · SCRIPT.md
```

## Vorschau & Rendern

```bash
npm run dev            # Studio-Vorschau (16:9)
npm run check          # Lint, Layout, Kontrast
npm run render         # beide 4K-Master + abgeleitete Dateien (tools/export.sh)
```

## Musik

Klavier/Streicher in F-Dur, 80 BPM – jeder Szenenwechsel liegt auf einer Taktgrenze (1 Takt = 3 s).
Neu erzeugen (benötigt `fluidsynth`, Python mit `numpy`, `mido`, `tinysoundfont`):

```bash
SF2=/pfad/GeneralUser-GS.sf2 npm run music
```

SoundFont: [GeneralUser GS](https://github.com/mrbumpy409/GeneralUser-GS) – Lizenz erlaubt kommerzielle Musikproduktion.

## Vor Veröffentlichung prüfen

- **Logo:** `compositions/chrome.html` und `compositions/s6-kontakt.html` enthalten einen am
  Website-Logo vermessenen SVG-Nachbau (Original-Vektordatei lag nicht vor).
- **Fakten:** Telefonnummer 02202 12 40 300, „kostenlose Wertermittlung“,
  „rund 1.600 verwaltete Wohneinheiten“.
- **Reels-Safe-Zone:** Pflichtinhalte liegen zwischen ca. 14 % und 79 % der Bildhöhe.
