# KNIGGE Immobilien – Halloween-Reel „Hausgeist Herbert“

28 Sekunden, 1080×1920, 30 fps, mit Ton. Ein Spukhaus bekommt neues Leben: Hausgeist Herbert erschreckt
seit Jahren niemanden mehr – bis KNIGGE kommt, eine Familie einzieht und ein Kind im Bettlaken ihn
selbst erschreckt. Endkarte mit kostenloser Wertermittlung als Lead.

| Zeit | Szene | Inhalt | Psychologischer Hebel |
| --- | --- | --- | --- |
| 0–4 s | `s1-spuk` | Spukhaus bei Vollmond, „Dieses Haus spukt.“ – Orgel (Toccata d-Moll), Herbert springt aus dem Fenster: „BUH!“ … niemand da | Neugier + Halloween-Relevanz, Pattern Interrupt |
| 4–10 s | `s2-allein` | „Seit die Kinder ausgezogen sind … erschreck ich nur noch Spinnen.“ – die Spinne zuckt mit den Schultern | Identifikation ohne Scham (leeres Nest), harmlose Pointe |
| 10–13 s | `s3-zu-gross` | Herbert winzig im Fenster: „Viel zu viel Haus für einen Geist.“ – das KNIGGE-Schild wächst aus dem Rasen | Problem benennen, Marke als Wendepunkt |
| 13–22 s | `s4-neues-leben` | Nacht wird Tag, Musik nach Dur: „Zeit für neues Leben.“ – VERKAUFT, Familie winkt, ein Kind erschreckt Herbert, „Der Spuk ist vorbei.“ | Reframing Verlust → Gewinn, Social Proof, Rollentausch als Höhepunkt |
| 22–28 s | `s5-ende` | „Jedes Haus verdient ein zweites Leben.“ – Kostenlose Wertermittlung, knigge-immobilien.de, Logo; Herbert zieht mit Koffer aus | Reziprozität, kleiner erster Schritt, Peak-End |

Die Welt (Haus, Garten, Himmel, Kamera, Figuren) ist die Komposition `welt` unter allen Szenen.
Idee und Varianten: `STORYLINES.md`, Gestaltung: `SPEC.md`, Auftrag und Psychologie: `BRIEF.md`,
Prüfung: `REVIEW.md`. Fertiges Video: `renders/knigge-halloween-reel.mp4` (im Repo bjoern319/Marketing-Videos).

## Ändern & neu erzeugen

```bash
SF2=/pfad/GeneralUser-GS.sf2 npm run audio   # Musik: Orgel-Intro + Schnitt aus der KNIGGE-Musik
npm run build    # python3 tools/build_reel.py – schreibt index.html und compositions/*.html
npm run check    # Lint, Layout, Kontrast, Lesbarkeit, Ton
npm run render   # renders/knigge-halloween-reel.mp4
```

- Texte: oben in `tools/build_reel.py` (`TEXT`); Farben Nacht/Tag in `PAL`; Kamera in `CAM`.
- Ton: Orgel = Anfang der Toccata d-Moll BWV 565 (J. S. Bach, gemeinfrei) in eigener Einspielung mit dem
  SoundFont [GeneralUser GS](https://github.com/mrbumpy409/GeneralUser-GS); danach die KNIGGE-Musik aus
  `../knigge-wohnen-im-ruhestand`. Geräusche: Pixabay (kommerziell frei, `assets/sfx/CREDITS.md`).
- Schrift: Red Hat Display (Hausschrift, `assets/fonts/`, SIL OFL 1.1). Logo-Wortmarke unverändert.

## Vor Veröffentlichung prüfen

- **„Kostenlose Wertermittlung“** – Angebot wie im Film `../knigge-wohnen-im-ruhestand`; bitte bestätigen.
- Instagram: kein Text oberhalb 168 px oder unter 1330 px, nichts unter der Aktionsleiste rechts.
