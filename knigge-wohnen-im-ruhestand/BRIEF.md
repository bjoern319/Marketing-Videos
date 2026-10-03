---
workflow: general-video
flow: automation
storyboard: "no"
message: "Nicht weniger Zuhause – mehr Leben: Der Umzug vom großen Haus in eine passende Wohnung ist ein Gewinn, und KNIGGE Immobilien begleitet Sie dabei von Anfang bis Ende."
destination: youtube + youtube-shorts + instagram-reels + tv (hochkant & quer)
aspect: 1080x1920 + 1920x1080 (Master je 4K)
language: de
audience: "Eigentümer im Ruhestand (ca. 65–85) mit großem Einfamilienhaus in Bergisch Gladbach / Köln-Ost; sekundär deren erwachsene Kinder"
length: 75s
angle: emotional-persuasive brand film (narrative, sound-off-first)
narration: "no"
---

## Intent

Info- und Werbefilm für KNIGGE Immobilien e.K. (Bergisch Gladbach). Ruheständler sollen Lust
bekommen, ihr zu groß gewordenes Haus zu verkaufen und in eine komfortable Wohnung zu ziehen –
vollständig begleitet durch KNIGGE. Ton laut Nutzer: „sympathisch“, „psychologisch aufgebaut für
maximale Überzeugung“. Sie-Ansprache, seriös, lokal-persönlich, keine Superlative ohne Beleg,
keine Wettbewerber-Nennung (KNIGGE-Tonalität).

Psychologischer Bogen (Reihenfolge ist Absicht):

1. **Nostalgie & Identifikation** – Erinnerungen ans Haus (Aufmerksamkeit, „das bin ich“).
2. **Pacing der Gegenwart** – Stille, Treppen, Garten, Heizkosten; empathisch, ohne Angstappell.
3. **Reframing** – Verlust wird Gewinn: „Nicht weniger Zuhause. Mehr Leben.“
4. **Future Pacing** – konkrete Bilder des neuen Alltags (Aufzug, Balkon, Bäcker, Reisen, Kapital).
5. **Autonomie + sanfte Dringlichkeit** – „Solange Sie ihn selbst bestimmen können.“
6. **Einwandbehandlung & Risikoreduktion** – „Und der ganze Aufwand? Den nehmen wir Ihnen ab.“ – 4 klare Schritte.
7. **Sympathie & Autorität** – lokal verwurzelt (Stadtteile), rund 1.600 verwaltete Wohneinheiten.
8. **Reziprozität & kleiner erster Schritt** – kostenloses, unverbindliches Gespräch „bei einer Tasse Kaffee“; Peak-End: warmer Abschluss mit Claim.

## Assets

- Logo — als SVG nachgebaut und am Website-Logo vermessen (Facetten-Geometrie, Verläufe, Wortmarke Montserrat in #444F4F); in compositions/chrome.html und compositions/s6-kontakt.html.
- assets/audio/knigge-theme.m4a — eigens komponierte Musik (Klavier/Streicher, 80 BPM, F-Dur), erzeugt mit tools/music/compose.py.
- Screenshots von knigge-immobilien.de (vom Nutzer) — Quelle für CI-Farben, Typografie, Buttons und Logo.

## Customizations

- Update Nutzerwunsch: „Für YouTube, Instagram und Fernseher hochkant (gleicher Inhalt wie Instagram)“ → 9:16 ist die Hauptfassung: 4K-Master (YouTube Shorts, TV), 1080×1920 (Instagram), gedrehte 3840×2160-Dateien für hochkant montierte TVs ohne Drehfunktion (tools/export.sh).
- Update Nutzerwunsch: „Querformat wird auch benötigt“ → zusätzlich 16:9 als 4K-Master (YouTube, TV quer) und 1920×1080. Die Szenen layouten per Container-Queries für beide Formate.
- Musik-Struktur folgt exakt den Szenengrenzen (1 Takt = 3 s).
- Optionaler Sprechertext in SCRIPT.md (für spätere Aufnahme, z. B. durch Inhaber/Makler).

## Notes

- Website knigge-immobilien.de war aus der Build-Umgebung nicht erreichbar (Netzwerk-Policy) → kein Website-Capture; CI aus Website-Screenshots des Nutzers vermessen (Rot #CA2C35, Bordeaux #6D131B, Schiefergrau #444F4F, Hellgrau #ECEEEA, nur Montserrat).
- Zu prüfende Fakten vor Veröffentlichung: Telefonnummer 02202 12 40 300, „kostenlose Wertermittlung“, „rund 1.600 verwaltete Wohneinheiten“.
- Reels-Safe-Zone: keine Pflichtinhalte im unteren ~20 % und oberen ~10 % des 9:16-Formats.
