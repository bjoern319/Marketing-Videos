---
workflow: general-video
flow: automation
storyboard: "no"
message: "Mit der kostenfreien VIP-Suche von KNIGGE Immobilien behalten Sie den regionalen Immobilienmarkt im Blick – ohne selbst alle Portale durchsuchen zu müssen."
destination: youtube + youtube-shorts + instagram-reels + tv (hochkant & quer)
aspect: 1080x1920 + 1920x1080 (Master je 4K)
language: de
audience: "Immobiliensuchende in Bergisch Gladbach und Region: Kaufinteressenten, Kapitalanleger, Mieter, Vielbeschäftigte mit wenig Zeit für Recherche"
length: 60s
angle: info-/werbefilm, psychologisch aufgebaut (problem → lösung → so einfach → vorteil → persönlich → CTA), sound-off-first
narration: "no"
---

## Intent

Info- und Werbefilm zur **VIP-Suche** von KNIGGE Immobilien e.K. (Bergisch Gladbach) – „so ein
info-werbe video“ wie der Film „Nicht weniger Zuhause. Mehr Leben.“, gleiche CI, Hoch- und
Querformat. Ziel: Registrierungen für die kostenfreie VIP-Suche. Sie-Ansprache, seriös,
lokal-persönlich, keine Superlative ohne Beleg, keine Wettbewerber- oder Portalnamen.

Psychologischer Bogen (Reihenfolge ist Absicht):

1. **Zielgruppe ansprechen + Identifikation** – „Sie suchen eine Immobilie?“ Kaufen · Mieten · Kapitalanlage (Selbstselektion in den ersten 3 s).
2. **Pacing des Problems** – Abend für Abend Portale, vieles doppelt, das Passende schnell weg (Verlustaversion, mild – kein Angstappell).
3. **Lösung / Reframing** – „Es geht auch einfacher.“ VIP-Suche: der gesamte Markt der Region, strukturiert gefiltert.
4. **Einfachheit (kognitive Leichtigkeit)** – 3 Schritte: Suchkriterien einmal hinterlegen → regelmäßiger Abgleich → passende Angebote per E-Mail.
5. **Kontrastprinzip** – Lasten werden durchgestrichen; Claim der Website: „Wir bündeln den Markt – Sie behalten den Überblick.“
6. **Sympathie & Vertrauen** – „Mehr als ein Suchagent“: Passt ein Objekt besonders gut, meldet sich KNIGGE persönlich.
7. **Exklusivität + Risikoumkehr + kleiner erster Schritt** – „Jetzt VIP-Zugang sichern“, kostenfrei, unverbindlich, jederzeit anpassbar oder pausierbar; QR-Code direkt zur Anmeldung.

## Assets

- Screenshots der Seite „VIP-Suche“ auf knigge-immobilien.de (vom Nutzer) — Quelle aller Aussagen im Film.
- Logo-SVG und CI-Tokens aus `../knigge-wohnen-im-ruhestand` (am Website-Logo vermessen) — `frame.md`, `compositions/chrome.html`, `compositions/s6-zugang.html`.
- assets/audio/knigge-vip-theme.m4a — eigens komponierte Musik (96 BPM, 1 Takt = 2,5 s), erzeugt mit tools/music/compose.py.

## Customizations

- Formate wie beim Ruhestand-Film: 9:16 als 4K-Master (YouTube Shorts, TV hochkant), 1080×1920 (Instagram), gedrehte 3840×2160-Dateien für hochkant montierte TVs ohne Drehfunktion; 16:9 als 4K-Master (YouTube, TV quer) und 1920×1080 (tools/export.sh).
- QR-Code im Abspann → https://www.knigge-immobilien.de/vip-suche.xhtml (für TV/Schaufenster).
- Musik-Struktur folgt exakt den Szenengrenzen (1 Takt = 2,5 s); das Klavier-Motiv aus dem Ruhestand-Film kehrt im Abspann als akustisches Markenzeichen wieder.
- Optionaler Sprechertext in SCRIPT.md.

## Notes

- knigge-immobilien.de ist aus der Build-Umgebung nicht erreichbar (Netzwerk-Policy); Texte aus den Screenshots, URL der Anmeldeseite aus der Websuche (Seitentitel „Welche Immobilie suchen Sie?“).
- Vor Veröffentlichung prüfen: QR-Code/URL (…/vip-suche.xhtml), „nahezu alle relevanten Kauf- oder Mietangebote aus der Region“ (Website-Formulierung, im Film als „der gesamte Immobilienmarkt der Region“ verdichtet – wie die Website-Unterzeile).
- Beispielwerte im Suchprofil (Bergisch Gladbach, 3–4 Zimmer, ab 80 m²) sind Illustration, keine Angebote.
- Reels-Safe-Zone: keine Pflichtinhalte im unteren ~21 % und oberen ~12 % des 9:16-Formats.
