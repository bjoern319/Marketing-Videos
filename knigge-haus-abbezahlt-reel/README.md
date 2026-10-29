# KNIGGE Immobilien – Instagram-Reel „Das Haus ist abbezahlt.“

27,75 Sekunden, 1080×1920, 30 fps, mit der KNIGGE-Musik. Das Reel zum Instagram-Karussell (6 Folien)
über den Expertenbeitrag von Andrea Gerhardus auf in-gl.de – alle drei Ideen aus `STORYLINES.md` in
einem Film: das rote „Aber“ trägt die Schnitte, ein Kassenbon druckt die Kosten, eine Waage kippt unter
den Aufgaben und kommt mit den vier Optionen zurück ins Gleichgewicht.

| Zeit | Szene | Inhalt |
| --- | --- | --- |
| 0–3,75 s | `s1-einstieg` | „Das Haus ist abbezahlt.“ über dem Haus – das rote „Aber“ schlägt auf dem Takt ein: „… können wir es uns noch leisten?“ |
| 3,75–8,25 s | `s2-kosten` | Match-Cut: „Aber“ bleibt stehen, „Keine Kreditrate mehr. Aber die Kosten bleiben.“ – ein Bon mit Stempel ABBEZAHLT druckt die fünf Kosten, Summe „?“ |
| 8,25–12,75 s | `s3-aufgabe` | „Wenn das Haus zur Aufgabe wird.“ – der Bon und vier Aufgaben fallen auf die Waage, sie kippt |
| 12,75–18 s | `s4-optionen` | „Welche Optionen gibt es?“ (auf der Auflösung der Musik) – vier Optionen bringen die Waage ins Gleichgewicht |
| 18–23,25 s | `s5-expertin` | Andrea Gerhardus: „Nicht jedes Haus muss verkauft werden. Aber jedes Zuhause sollte zum Leben passen.“ |
| 23,25–27,75 s | `s6-ende` | „Den ganzen Expertenbeitrag jetzt lesen.“, Knopf „Zum Expertenbeitrag auf in-gl.de“, Logo auf dem Schlussakkord |

Fertiges Video: `renders/knigge-haus-abbezahlt-reel.mp4` (im Repo bjoern319/Marketing-Videos).
Gestaltung und Zeiten: `SPEC.md`, Prüfung: `REVIEW.md`, Auftrag: `BRIEF.md`.

## Ändern & neu erzeugen

```bash
npm run assets   # python3 tools/prepare_assets.py – Fotos aus den Screenshots, Musikschnitt
npm run build    # python3 tools/build_reel.py – schreibt index.html und compositions/*.html
npm run check    # Lint, Layout, Kontrast, Lesbarkeit, Ton
npm run render   # renders/knigge-haus-abbezahlt-reel.mp4
```

- Texte: oben in `tools/build_reel.py` (`TEXT`), Zeiten in `SCENES` und den Zeitlisten der Szenen.
- Fotos: die Screenshots der Folien liegen in `assets/source/`. `tools/prepare_assets.py` schneidet die
  freien Bildteile aus und übermalt eingebrannte Schrift. **Mit den Originalfotos wird das Reel
  schärfer:** Datei in `assets/source/` ersetzen, Ausschnitt in `PHOTOS` anpassen, `npm run assets`.
- Musik: Schnitt aus `../knigge-wohnen-im-ruhestand/assets/audio/knigge-theme.m4a` (eigene Komposition)
  auf Taktgrenzen; Einzelheiten in `tools/prepare_assets.py`.
- Schrift: Red Hat Display (`assets/fonts/`, SIL OFL 1.1) – Hausschrift für alle neuen Videos.
  `prepare_assets.py` braucht `opencv-python-headless`, `pillow`, `numpy` und ffmpeg.
