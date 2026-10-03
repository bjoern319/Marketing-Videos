---
format: 1920x1080 (index.html) + 1080x1920 (formats/9x16.html)
duration: 75s
message: "Nicht weniger Zuhause – mehr Leben. KNIGGE Immobilien begleitet Sie von Anfang bis Ende."
arc: Nostalgie → Gegenwart (Last) → Reframe → Future Pacing → Autonomie → Einwand & Lösung → Vertrauen → CTA
audience: Eigentümer im Ruhestand mit großem Haus, Bergisch Gladbach / Köln-Ost
mode: autonomous
music: assets/audio/knigge-theme.m4a (80 BPM, 1 Takt = 3 s)
rhythm: slow-WARM · quiet-HOLD · LIFT · flowing · pause · steady · warm · resolve
---

Dieser Film sagt Eigentümern im Ruhestand, dass der Schritt vom großen Haus in eine Wohnung
kein Verlust ist, sondern mehr Leben bedeutet – und dass KNIGGE ihnen den Aufwand abnimmt.

Persistente Ebenen: `compositions/bg.html` (Hellgrau, Papierkorn, driftende K-Facetten, 0–75 s),
`compositions/chrome.html` (Logo-Bug 1–65 s, Brand-Wipes bei 45 s und 66 s).

| Frame | Beat | On screen | Why |
| --- | --- | --- | --- |
| 01 — Ihr Haus | hook + problem · 18 s | Haus zeichnet sich, Fenster leuchten; Erinnerungen. Dann gehen die Lichter aus, Lasten fallen aufs Haus. | Identifikation, dann empathisches Pacing der Gegenwart |
| 02 — Mehr Leben | reframe + benefits · 21 s | Frage, Haus verwandelt sich in Wohnung, Claim. Danach 5 konkrete Vorteile, Illustration reagiert. | Wert-Claim landet in Beat 2; Future Pacing |
| 03 — Zeitpunkt | autonomy · 6 s | „Solange Sie ihn selbst bestimmen können.“ – „selbst“ rot eingekreist, Sonne geht auf. | Autonomie + sanfte Dringlichkeit |
| 04 — Begleitung | objection + solution · 12 s | „Und der ganze Aufwand? Den nehmen wir Ihnen ab.“ 4-Stationen-Weg vom Haus zur Wohnung. | Einwand + Risikoreduktion, Kompetenz |
| 05 — Vor Ort | trust · 9 s | „Wir sind hier zu Hause.“ Stadtteile um Bergisch Gladbach, Zähler 1.600. | Sympathie (Ortsnähe) + Autorität |
| 06 — Kontakt | CTA · 9 s | Logo setzt sich zusammen, Kaffee-Einladung, kostenloses Gespräch, Telefon, Web, Claim. | Reziprozität, kleiner erster Schritt, Peak-End |

## Frame 1 — Ihr Haus

- status: animated
- src: compositions/s1-haus.html
- duration: 18s
- poster: 6.5s
- transition_in: fade from canvas
- scene: Linienhaus mit rotem Dach zeichnet sich; Erinnerungen; Lichter gehen aus; Lasten-Tags
- blueprint: kinetic-type-beats (statement build) + svg-path-draw, svg-icon-enrichment, sine-wave-loop, waterfall-entry (sanft), spring-pop-entrance (Tags)
- voiceover: "Erinnern Sie sich an den Tag, an dem Sie hier eingezogen sind? … Heute ist es still geworden."

0–9 s: „Erinnern Sie sich an den Tag, an dem Sie hier eingezogen sind?“ → „Kinderlachen im Flur.
Sommerfeste im Garten. Ein Haus voller Leben.“ Fenster gehen nacheinander warm an, Schaukel
schwingt, Rauch aus dem Kamin. 9–18 s: „Die Kinder sind längst aus dem Haus.“ / „Es ist still
geworden.“ Lichter gehen aus, Schaukel kommt zur Ruhe. Tags fallen: Treppen · Gartenarbeit ·
Heizkosten · Reparaturen · Schnee schippen – das Haus gibt jedes Mal leicht nach. Abschluss:
„Was früher Freude war, wird langsam zur Last.“ (Haus bleibt für den Übergang stehen.)

## Frame 2 — Mehr Leben

- status: animated
- src: compositions/s2-mehr-leben.html
- duration: 21s
- poster: 22.5s
- transition_in: continuous (Haus übernimmt Position aus Frame 1)
- scene: Frage → Haus wird Wohnung → Claim mit Unterstrich → 5 Vorteile mit Icons
- blueprint: kinetic-type-beats (Claim) + fixed-anchor-cycle (Illustration als Anker, Vorteile zyklisch), svg-path-draw, css-marker-patterns, spring-pop-entrance
- voiceover: "Was wäre, wenn weniger Haus mehr Leben bedeutet? Nicht weniger Zuhause. Mehr Leben."

18–24 s: „Was wäre, wenn weniger Haus mehr Leben bedeutet?“ Das Haus zeichnet sich zurück, die
Wohnung mit Balkon zeichnet sich auf, Licht geht an. Claim: „Nicht weniger Zuhause. / Mehr Leben.“
24–39 s: „Stellen Sie sich vor:“ – Aufzug statt Treppen. · Balkon statt Gartenarbeit. · Bäcker &
Arzt um die Ecke. · Tür zu – und sorgenfrei verreisen. · Freies Kapital für Enkel &
Herzenswünsche. Jeder Punkt aktiviert ein Detail der Illustration.

## Frame 3 — Zeitpunkt

- status: animated
- src: compositions/s3-zeitpunkt.html
- duration: 6s
- poster: 43s
- transition_in: fade from canvas
- scene: Ruhiger Typo-Moment mit aufgehender Sonne
- blueprint: kinetic-type-beats + css-marker-patterns (circle), ambient-glow-bloom
- voiceover: "Und der richtige Zeitpunkt? Solange Sie ihn selbst bestimmen können."

## Frame 4 — Begleitung

- status: animated
- src: compositions/s4-begleitung.html
- duration: 12s
- poster: 55s
- transition_in: brand wipe (K-Faltung, chrome.html)
- scene: Einwand → Antwort → 4 Stationen auf einem Weg vom Haus zur Wohnung
- blueprint: spatial-pan-stations (vereinfacht, Kamera fix) + svg-path-draw, spring-pop-entrance
- voiceover: "Und der ganze Aufwand? Den nehmen wir Ihnen ab: Wertermittlung, neue Wohnung, Verkauf – bis Sie angekommen sind."

Stationen: 1 Wertermittlung – kostenlos & unverbindlich · 2 Neue Wohnung finden – zur Miete oder
zum Kauf · 3 Haus verkaufen – diskret & zum fairen Preis · 4 Ankommen – persönlich begleitet.
Fuß: „Ein Ansprechpartner – von Anfang bis Ende.“

## Frame 5 — Vor Ort

- status: animated
- src: compositions/s5-vor-ort.html
- duration: 9s
- poster: 63s
- transition_in: fade from canvas
- scene: Pin „Bergisch Gladbach“, Stadtteile als Konstellation, Zähler 1.600
- blueprint: constellation-hub + counting-dynamic-scale
- voiceover: "Wir sind hier zu Hause – Ihr Immobilienmakler in Bergisch Gladbach."

## Frame 6 — Kontakt

- status: animated
- src: compositions/s6-kontakt.html
- duration: 9s
- poster: 73s
- transition_in: brand wipe (K-Faltung, chrome.html)
- scene: Logo-Lockup, Kaffee-Einladung, CTA-Pill, Telefon, Web, Claim
- blueprint: logo-assemble-lockup + cta-morph-press (ohne Cursor)
- voiceover: "Lassen Sie uns sprechen – gern bei einer Tasse Kaffee. Kostenlos und unverbindlich: KNIGGE Immobilien."

## Video direction

Hellgrauer Grund wie auf der Website, Linienillustration in Schiefergrau mit roten Akzenten,
Montserrat Regular als ruhige Stimme, Montserrat Bold als KNIGGE-Stimme. Bewegungen weich und lesefreundlich (Text steht
mindestens 2,5 s), Übergänge als Blende über den gemeinsamen Grund; zwei Brand-Wipes in
KNIGGE-Rot markieren „jetzt kommt KNIGGE“ (45 s) und den Abschluss (66 s).
