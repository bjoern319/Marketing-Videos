---
format: 1920x1080 (index.html) + 1080x1920 (formats/9x16.html)
duration: 60s
message: "Mit der kostenfreien VIP-Suche behalten Sie den regionalen Immobilienmarkt im Blick – ohne selbst alle Portale durchsuchen zu müssen."
arc: Zielgruppe → Problem (Überforderung) → Lösung → So einfach → Kontrast/Vorteil → Persönlich → CTA
audience: Immobiliensuchende in Bergisch Gladbach und Region (Kauf, Miete, Kapitalanlage)
mode: autonomous
music: assets/audio/knigge-vip-theme.m4a (96 BPM, 1 Takt = 2,5 s)
rhythm: restless-BUILD · RELIEF · steady-flow · lift-STRIKE · warm-hold · resolve
---

Dieser Film sagt Immobiliensuchenden: Sie müssen nicht mehr Abend für Abend Portale durchsuchen –
die VIP-Suche von KNIGGE bündelt den Markt, schickt passende Angebote per E-Mail, und bei einem
echten Treffer meldet sich KNIGGE persönlich. Registrierung kostenfrei und unverbindlich.

Persistente Ebenen: `compositions/bg.html` (Hellgrau, Papierkorn, driftende K-Facetten, 0–60 s),
`compositions/chrome.html` (Logo-Bug 0,8–49,6 s, Brand-Wipes bei 12,5 s und 50 s).

| Frame | Beat | On screen | Why |
| --- | --- | --- | --- |
| 01 — Die Suche | hook + problem · 12,5 s | „Sie suchen eine Immobilie?“ Kaufen · Mieten · Kapitalanlage. Browserfenster: Tabs vermehren sich, Inserate doppelt, das Passende wird „vergeben“. | Selbstselektion, Pacing der Überforderung, milde Verlustaversion |
| 02 — VIP-Suche | solution · 7,5 s | „Es geht auch einfacher.“ VIP-Suche; Inserate fallen in einen Filter, heraus kommt eine geordnete Trefferliste. | Reframing, Erleichterung, Produkt-Name |
| 03 — So geht's | how it works · 12,5 s | 3 Schritte im App-Fenster: Suchprofil → Abgleich mit dem Markt → passende Angebote per E-Mail; „Jederzeit anpassen oder pausieren.“ | Einfachheit, Kontrolle |
| 04 — Ihr Vorteil | benefits · 10 s | Drei Lasten werden durchgestrichen, ✓ gefilterte Marktübersicht; Claim „Wir bündeln den Markt – Sie behalten den Überblick.“ | Kontrastprinzip, Claim |
| 05 — Persönlich | trust · 7,5 s | „Mehr als ein Suchagent.“ Telefon klingelt: KNIGGE Immobilien. „Passt ein Objekt besonders gut, melden wir uns persönlich.“ | Sympathie, Vertrauen, Differenzierung |
| 06 — VIP-Zugang | CTA · 10 s | Logo setzt sich zusammen, „Jetzt VIP-Zugang sichern“, Button „Kostenfrei registrieren“, URL, QR-Code, Claim. | Exklusivität, Risikoumkehr, kleiner erster Schritt, Peak-End |

## Frame 1 — Die Suche

- status: animated
- src: compositions/s1-suche.html
- duration: 12.5s
- poster: 10.8s
- transition_in: fade from canvas
- scene: Zielgruppen-Frage mit Chips, dann Browserfenster, das sich mit Tabs und Inseraten füllt
- blueprint: overwhelm-surround (adapted: Tabs + Inseratskarten akkumulieren) + kinetic-type-beats (3 Pain-Statements) · rules: spring-pop-entrance, waterfall-entry, svg-path-draw, physics-press-reaction (Stempel), sine-wave-loop (Uhr)
- voiceover: "Sie suchen eine Immobilie? Dann kennen Sie das: Abend für Abend Portale durchsuchen. Vieles ist doppelt inseriert. Und das Passende? Schon wieder weg."

0–3 s: „Sie suchen eine Immobilie?“ + Chips Kaufen · Mieten · Kapitalanlage. 3–12,5 s: „Kennen Sie
das?“ – Browser zeichnet sich; „Abend für Abend Portale durchsuchen.“ (Tabs vermehren sich, Uhr
läuft) · „Vieles ist doppelt inseriert.“ (2×/3×-Badges, Kopien) · „Und das Passende? Schon wieder
weg.“ (Herz, Stempel „VERGEBEN“).

## Frame 2 — VIP-Suche

- status: animated
- src: compositions/s2-vip-suche.html
- duration: 7.5s
- poster: 18.5s
- transition_in: brand wipe (K-Faltung, chrome.html)
- scene: Kicker, Produktname mit VIP-Badge, Unterzeile; Filter-Trichter ordnet Inserate zu Trefferliste
- blueprint: kinetic-type-beats (Product_Intro name-drop) + depth-scatter-assemble (2D, Karten → Trichter) · rules: spring-pop-entrance, svg-path-draw, waterfall-entry
- voiceover: "Es geht auch einfacher: die VIP-Suche von KNIGGE. Der gesamte Immobilienmarkt der Region – strukturiert für Sie gefiltert."

## Frame 3 — So geht's

- status: animated
- src: compositions/s3-so-gehts.html
- duration: 12.5s
- poster: 29.5s
- transition_in: fade from canvas
- scene: Schrittliste links (quer) bzw. unten (hoch); App-Fenster wechselt Suchprofil → Abgleich (Scan) → Posteingang
- blueprint: device-surface-showcase (static tour, cursorless) + grid-card-assemble (Schrittliste) · rules: discrete-text-sequence (Eingabe), ai-tracking-box (Scan, als Linie), spring-pop-entrance, svg-icon-enrichment
- voiceover: "So funktioniert's: Sie hinterlegen einmalig Ihre Suchkriterien. Wir gleichen sie regelmäßig mit dem aktuellen Markt ab. Und Sie erhalten passende Angebote per E-Mail – jederzeit anpassbar oder pausierbar."

Schritte: 1 „Sie hinterlegen einmalig Ihre Suchkriterien.“ · 2 „Wir gleichen sie regelmäßig mit dem
aktuellen Markt ab.“ · 3 „Sie erhalten passende Angebote per E-Mail.“ · Hinweis „Jederzeit anpassen
oder pausieren.“

## Frame 4 — Ihr Vorteil

- status: animated
- src: compositions/s4-vorteil.html
- duration: 10s
- poster: 40s
- transition_in: fade from canvas
- scene: „Das bedeutet für Sie:“ – drei Lasten werden rot durchgestrichen, ✓ gefilterte Marktübersicht; Karte mit Pins; dann Claim
- blueprint: grid-card-assemble (vertical benefit list clearing to a payoff line) · rules: css-marker-patterns (strike-through, underline), spring-pop-entrance, waterfall-entry
- voiceover: "Das bedeutet für Sie: keine parallele Suche, keine doppelte Dateneingabe, kein tägliches Prüfen – sondern eine strukturierte Marktübersicht. Wir bündeln den Markt – Sie behalten den Überblick."

## Frame 5 — Persönlich

- status: animated
- src: compositions/s5-persoenlich.html
- duration: 7.5s
- poster: 47s
- transition_in: fade from canvas
- scene: Smartphone mit eingehendem Anruf „KNIGGE Immobilien“, Ringwellen; Treffer-Karte „passt besonders gut“
- blueprint: titlecard-reveal (calm breather) + device-surface-showcase (phone hero) · rules: sine-wave-loop (Ringwellen), spring-pop-entrance, svg-path-draw
- voiceover: "Mehr als ein Suchagent: Passt ein Objekt besonders gut, melden wir uns persönlich."

## Frame 6 — VIP-Zugang

- status: animated
- src: compositions/s6-zugang.html
- duration: 10s
- poster: 58s
- transition_in: brand wipe (K-Faltung, chrome.html)
- scene: Logo-Lockup, Headline wie auf der Website, Bordeaux-Button mit Glanz, URL, QR-Code, Claim
- blueprint: logo-assemble-lockup + cta-morph-press (ohne Cursor) · rules: physics-press-reaction, spring-pop-entrance
- voiceover: "Jetzt VIP-Zugang sichern – kostenfrei und unverbindlich auf knigge-immobilien.de."

## Video direction

Gleiche Welt wie „Nicht weniger Zuhause. Mehr Leben.“: hellgrauer Grund, Linienzeichnung in
Schiefergrau mit roten Akzenten, Montserrat 400 als Stimme des Zuschauers (Fragen, Gefühle),
Montserrat 700 als KNIGGE-Stimme. UI wird als ruhige Linien-Mockups gezeigt (keine echten
Portale, keine Markennamen). Tempo etwas zügiger (jüngere, beschäftigte Zielgruppe), Text steht
trotzdem ≥ 2 s. Zwei Brand-Wipes markieren „jetzt kommt KNIGGE“ (12,5 s) und den Abschluss (50 s).
