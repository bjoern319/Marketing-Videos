# REVIEW – Einzugsgebiet-Reel (29.10.2026)

## Entscheidungen

- **Kamerafahrt statt Gesamtkarte mit allen Namen.** Auf 1080 px Breite wären die Gemeindenamen der
  ganzen Region unter der Lesegrenze von 28 px geblieben. Die Kamera fährt deshalb nacheinander zu
  Köln, Bergisch Gladbach und Wipperfürth (Zoom ≈ 2,2) und zeigt dort die Namen in 30 px; Übersicht
  am Anfang und am Ende ohne Gemeindenamen, im Abschluss mit den drei Standortnamen.
- **Namen nur bei stehender Kamera**, Überschriften fest im Bild – nichts bewegt sich, während man es
  liest. Die Überschrift einer Station darf schon während der Fahrt kommen.
- **Karte wie in den GIFs** (Vektor-Gemeinden statt Satellitenbild), weil der Nutzer genau diese Karte
  als Reel wollte; die drei Standort-Gemeinden sind dunkler.
- **Kein Ton** (Wahl des Nutzers – Musik kommt in Instagram dazu). Kein Storyboard vorab (Wahl des
  Nutzers); alternative Erzählweisen wurden nicht gebaut.
- Botschaft nach Wahl des Nutzers: „Drei Standorte. Eine Region.“ → „Ein Ansprechpartner für Ihre
  Immobilie.“ + knigge-immobilien.de.

## Gemessen und angesehen

- `hyperframes check`: 0 Fehler, 0 Warnungen (Lint, Laufzeit, Layout, Bewegung, Kontrast, Lesbarkeit);
  Hinweis `audio_none` ist gewollt.
- Beschriftung über `label_layout.py`: jeder Gemeindename 30 px, Standortnamen 32 px, jeweils mit
  mindestens 4 px Abstand in seiner Fläche, keine Überlappung mit Markern, Rhein, Überschrift, Logo;
  alles im Instagram-Band 168–1330 px und links der Aktionsleiste. Im Abschluss ragen „Bergisch
  Gladbach“ und „Wipperfürth“ als Standortnamen über ihre kleinen Flächen (berühren nichts).
- Angesehen: Prüfbilder bei 0 / 1,3 / 4,5 / 7,3 / 10,1 / 14,5 s, Beat-Bogen, die vier Übergänge
  (−0,2 bis +0,2 s), Handy-Bogen bei 360 px Breite.
- Nicht geprüft: wie die Instagram-Oberfläche (Profilname, Beschreibung, Knöpfe) auf einem echten
  Gerät darüber liegt – nur nach den Maßen der Plattform freigehalten.

## Schwächste Stelle

Während der drei Kamerafahrten steht jeweils rund eine halbe Sekunde kein Name im Bild; das ist
gewollt (nichts wird beim Lesen bewegt), wirkt aber kurz leer. Mit mehr Zeit: die Fahrten auf
0,6 s kürzen oder die Länge auf 20 s erhöhen und jede Station 0,5 s länger halten.
