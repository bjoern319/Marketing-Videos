# REVIEW – Einzugsgebiet-Reel

## Version 2 „Drei Facetten“ (29.10.2026, 18 s)

### Entscheidungen

- **Erzählidee A aus `STORYLINES.md`** gebaut, ohne Zwischenstopp (wie vom Nutzer für v1 gewählt): Die
  drei Facetten der KNIGGE-Bildmarke werden die drei Standort-Pins und setzen sich am Ende wieder zum
  Logo zusammen – „drei Standorte → ein Ansprechpartner“ erzählt die Marke selbst.
- **18 s statt 15 s**, damit die zusätzlichen Texte (Region, Ortstitel, Zähler) lesbar stehen bleiben.
- **Jede Szene hat ihren eigenen Auftritt:** Wort-Einschlag mit Marker-Strich (Einstieg), Einfärben
  (Region), Etikett-Wisch und Buchstaben aus der Maske (Standorte), Zahlenrad aus der Registry
  (`number-wheel`) mit Gemeinde-Welle, Facetten-Montage (Abschluss).
- Ortstitel liegen direkt über der Karte (Schiefergrau auf Hellgrau, gut lesbar) – kein Kasten, kein
  Verlauf. Die aktive Standort-Gemeinde färbt sich hellrot, ihr Pin pulst, wenn die Kamera steht.
- **Kein Ton** (Wahl des Nutzers – Musik kommt in Instagram dazu).

### Gemessen und angesehen

- `hyperframes check`: 0 Fehler. Warnungen, bewusst behalten:
  - `film_silent` – ohne Ton gewählt.
  - `line_unread` für „Gladbach“ und „Wipperfürth“: Der Prüfer zählt die einzeln animierten Buchstaben
    als Wörter („G l a d b a c h“ = 8 Wörter). Tatsächlich stehen die Titel 2,0 bzw. 2,2 s; für ein bis
    zwei Wörter verlangt die Regel 0,4 s.
  - `contrast_aa_failure` (1:1) bei vier Buchstaben von „Bergisch Gladbach“ bei 9 s: Gemessen wird
    zwischen den eng gesetzten Nachbarbuchstaben; im Bild steht Schiefergrau #444F4F auf Hellgrau
    #E0E3E1 bzw. Weiß.
  - Das Zahlenrad ist `data-layout-ignore` – die durchrollenden Ziffern sollen nicht gelesen werden.
- Beschriftung über `label_layout.py`: alle 16 Gemeindenamen passen mit Abstand in ihre Fläche, 30 px
  (Wermelskirchen 28 px), unter dem Titel, im Band 168–1330 px, links der Aktionsleiste.
- Angesehen: Prüfbilder von 0 bis 17,9 s (u. a. 0 / 1,15 / 1,9 / 2,25 / 3,4 / 5,6 / 8,2 / 10,8 / 13,4 /
  14,6–15,5 / 17,5 s), Beat-Bogen, die sechs Übergänge (−0,2 bis +0,2 s), Handy-Bogen bei 360 px.
- Nach dem Ansehen behoben: Die Karte zog im Abschluss erst seitlich weg, bevor sie schrumpfte
  (Kameramitte und Zoom getrennt interpoliert) – jetzt schrumpft sie um ihren Schwerpunkt in die
  Bildmarke. Die Facetten blendeten während des Rückflugs erst ein und waren kaum zu sehen – jetzt lösen
  sie die Pins sichtbar ab und fliegen nacheinander. Die Adresse stand unter 2 s – kommt jetzt früher.
- Nicht geprüft: die echte Instagram-Oberfläche auf einem Gerät und die Wirkung mit Musik.

### Schwächste Stelle

Zu Beginn jeder Kamerafahrt (4,0 / 6,6 / 9,2 / 11,8 s) steht 0,2–0,3 s kein Text, während die Kamera
anläuft. Mit mehr Zeit: Titel schon in der Fahrt beginnen lassen oder die Fahrten auf 0,6 s kürzen.

## Version 1 (15 s, ruhige Kamerafahrt)

### Entscheidungen

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

### Gemessen und angesehen

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

### Schwächste Stelle

Während der drei Kamerafahrten steht jeweils rund eine halbe Sekunde kein Name im Bild; das ist
gewollt (nichts wird beim Lesen bewegt), wirkt aber kurz leer. Mit mehr Zeit: die Fahrten auf
0,6 s kürzen oder die Länge auf 20 s erhöhen und jede Station 0,5 s länger halten.
