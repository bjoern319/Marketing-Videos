# KNIGGE Immobilien – „VIP-Suche“

Info- und Werbefilm (60 s) zur kostenfreien **VIP-Suche** von KNIGGE Immobilien: Immobiliensuchende
hinterlegen einmal ihr Suchprofil und bekommen passende Angebote aus der Region per E-Mail – bei
einem echten Treffer meldet sich KNIGGE persönlich. Gebaut mit [HyperFrames](https://github.com/heygen-com/hyperframes)
(HTML → Video), eine Szenenbasis für beide Formate. CI wie im Film „Nicht weniger Zuhause. Mehr Leben.“:
Montserrat, Rot #CA2C35, Bordeaux #6D131B, Schiefergrau #444F4F, Hellgrau #ECEEEA.

Gleicher Inhalt in beiden Formaten:

| Datei | Format | Einsatz |
| --- | --- | --- |
| `renders/knigge-vip-suche-9x16-4k.mp4` | 2160×3840 hochkant | YouTube Shorts · Fernseher mit Hochkant-Wiedergabe |
| `renders/knigge-vip-suche-9x16.mp4` | 1080×1920 hochkant | Instagram Reels/Stories, Facebook |
| `renders/knigge-vip-suche-tv-4k-gedreht-im-uhrzeigersinn.mp4` | 3840×2160, Inhalt 90° gedreht | Fernseher hochkant montiert, ohne Drehfunktion |
| `renders/knigge-vip-suche-tv-4k-gedreht-gegen-uhrzeigersinn.mp4` | 3840×2160, Inhalt 90° gedreht | dito – falls das Bild mit der anderen Datei auf dem Kopf steht |
| `renders/knigge-vip-suche-16x9-4k.mp4` | 3840×2160 quer | YouTube · Fernseher quer |
| `renders/knigge-vip-suche-16x9.mp4` | 1920×1080 quer | Website, Präsentationen, Social quer |

## Psychologischer Aufbau

| Zeit | Szene | Inhalt | Hebel |
| --- | --- | --- | --- |
| 0:00 | Die Suche | „Sie suchen eine Immobilie?“ Kaufen · Mieten · Kapitalanlage | Zielgruppe in 3 s ansprechen (Selbstselektion) |
| 0:03 | | Browser füllt sich: Abend für Abend Portale, vieles doppelt, das Passende „VERGEBEN“ | Problem-Pacing, milde Verlustaversion (kein Angstappell) |
| 0:12 | VIP-Suche | „Es geht auch einfacher: Die VIP-Suche“ – Inserate fallen in einen Filter, heraus kommt eine geordnete Trefferliste | Reframing, Erleichterung |
| 0:20 | So geht's | 1 Suchkriterien einmalig hinterlegen · 2 regelmäßiger Abgleich · 3 passende Angebote per E-Mail; „Jederzeit anpassen oder pausieren.“ | Einfachheit, Kontrolle |
| 0:32 | Ihr Vorteil | Drei Lasten werden durchgestrichen, ✓ gefilterte Marktübersicht; Claim der Website „Wir bündeln den Markt – Sie behalten den Überblick.“ | Kontrastprinzip, Wiedererkennung |
| 0:42 | Persönlich | „Mehr als ein Suchagent“ – KNIGGE ruft an, wenn ein Objekt besonders gut passt | Sympathie, Vertrauen, Abgrenzung zum Algorithmus |
| 0:50 | VIP-Zugang | „Jetzt VIP-Zugang sichern“, kostenfrei, unverbindlich, jederzeit pausierbar; QR-Code zur Anmeldung | Exklusivität, Risikoumkehr, kleiner erster Schritt, Peak-End |

Konzipiert für Ton-aus (Instagram): alle Aussagen stehen als Text im Bild. Ein optionaler
Sprechertext liegt in `SCRIPT.md`. Die Texte folgen der Seite „VIP-Suche“ auf knigge-immobilien.de.

## Projektstruktur

```
index.html              16:9-Host (YouTube)
formats/9x16.html       9:16-Host (Reels) – nutzt dieselben Szenen
compositions/           Szenen (Layout passt sich per Container-Queries an)
  bg.html  chrome.html  s1-suche.html … s6-zugang.html
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

Klavier, Marimba, Streicher in F-Dur, 96 BPM – jeder Szenenwechsel liegt auf einer Taktgrenze
(1 Takt = 2,5 s), kleine Akzente sitzen auf den Bild-Ereignissen. Im Abspann kehrt das Klavier-Motiv
aus „Nicht weniger Zuhause. Mehr Leben.“ als akustisches Markenzeichen wieder.
Neu erzeugen (benötigt `fluidsynth`, Python mit `numpy`, `mido`):

```bash
SF2=/pfad/GeneralUser-GS.sf2 npm run music
```

SoundFont: [GeneralUser GS](https://github.com/mrbumpy409/GeneralUser-GS) – Lizenz erlaubt kommerzielle Musikproduktion.

## Vor Veröffentlichung prüfen

- **QR-Code:** führt auf `https://www.knigge-immobilien.de/vip-suche.xhtml` (aus der Websuche,
  Seite war aus der Build-Umgebung nicht abrufbar) – einmal mit dem Handy scannen.
- **Formulierung:** „Der gesamte Immobilienmarkt der Region“ verdichtet die Website-Aussage
  „nahezu alle relevanten Kauf- oder Mietangebote aus der Region“ (wie die Website-Unterzeile
  „Der gesamte Immobilienmarkt – strukturiert für Sie gefiltert“).
- **Beispielwerte** im Suchprofil (Bergisch Gladbach, 3–4 Zimmer, ab 80 m²) sind Illustration.
- **Logo:** am Website-Logo vermessener SVG-Nachbau (wie im Ruhestand-Film).
- **Reels-Safe-Zone:** Pflichtinhalte liegen zwischen ca. 13 % und 78 % der Bildhöhe.
