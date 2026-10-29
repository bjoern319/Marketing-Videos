# SPEC – Reel „Das Haus ist abbezahlt.“

```text
GOAL:    Eigentümer erkennen sich wieder („abbezahlt – aber die Kosten bleiben“), sehen, dass es
         Wege gibt, und wollen den Expertenbeitrag von Andrea Gerhardus auf in-gl.de lesen.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, H.264 + AAC
TIME:    27,75 s x 30 = 833 Frames. Musik ist die Uhr: KNIGGE-Thema, 80 BPM, 1 Schlag = 0,75 s
         (22,5 Frames), 1 Takt = 3 s. Taktanfänge im Reel: 0,75 · 3,75 · 6,75 · 9,75 · 12,75 ·
         15,75 · 18,75 · 21,75 (Schnitt im Stück) · 24,75 (Schlussakkord F-Dur).
LOOK:    Grund Weiß #FFFFFF. Fotos aus dem Karussell mit dem weißen Lichtschleier des Karussells
         (Verlauf Weiß → transparent über 220–260 px, links bzw. oben). Schrift: Schiefer #323C44,
         Rot #CA2C35 nur für das „Aber“-Satzende je Bild, Stempel, Summe „?“, Knopf, Lot der Waage.
         Red Hat Display: Überschriften 800, -0,02em, Zeilenhöhe 1,0 (Einstieg 124 px, Kosten 112,
         Waage 104, Ende 112), Zitat 84 px/800, Listen 36 px/500, Bon 34 px/600, Name 46/800,
         Funktion 32/500, Knopf 42/800. Roter Strich über jeder Überschrift: 100 x 9 px.
         Licht und Tiefe: nur der Bon und die Pins der Waage werfen Schatten (0 18px 40px, 18 %).
OBJECTS: das abbezahlte Haus (Foto, Folie 1) – auch als runde Plakette auf der Waage (Ø 180);
         ein Kassenbon aus weißem Papier mit Zackenkante, der aus einem schiefergrauen Drucker steigt,
         roter Stempel „ABBEZAHLT“; eine Balkenwaage als Strichzeichnung (Schiefer, 12 px): Säule,
         Balken 720 px, Schnüre, zwei Schalen, Fuß, Zeiger über dem Drehpunkt; Gewichte: Aufgaben als
         Kreise Ø 92 (weiß, Rand 3 px, Icon), Optionen als abgerundete Quadrate 92 px (#F2EFEA, Icon);
         Andrea Gerhardus (Foto, Folie 5); Kaffeetisch mit Zeitschrift (Foto, Folie 6); KNIGGE-Logo.
MOTION:  Wörter: Unschärfe 10→0 px + Deckkraft, 5 Frames, power4.out, 2 Frames Versatz. „Aber“
         schlägt ein: Skalierung 1,3→1 + Unschärfe, 5 Frames expo.out. Waage: Winkel als Feder
         elastic.out(1, 0.5), 24 Frames; Gewichte fallen 9 Frames power2.in. Bon: Papier rückt je
         Zeile 4 Frames power2.out vor. Fotos: langsame Fahrt Skalierung 1,00→1,05 über die Szene.
         Abgänge: Unschärfe-Abgang 6 Frames power2.in. Nichts bewegt sich, während es gelesen wird.
SHOTS:   0–112    Einstieg: Bild 0 zeigt Strich + „Das Haus / ist abbezahlt.“ über dem Haus. 22:
                  „Aber“ schlägt rot ein (Taktanfang Dm), 27–45 „können / wir es uns / noch
                  leisten?“ wortweise. Text außer „Aber“ geht 99–108 ab.
         112–247  Kosten: Match-Cut – „Aber“ bleibt stehen, das Bild dahinter wird der Schreibtisch;
                  „Aber“ gleitet in „Aber die Kosten bleiben.“ (112–126), „Keine Kreditrate mehr.“
                  kommt (115–124). Drucker fährt hoch (120–130), Bon druckt: Kreditrate (135),
                  Stempel ABBEZAHLT (146), fünf Kosten im Achtel-Takt (157–202), Summe „?“ (219).
                  238–247 der Bon reißt ab und fliegt nach oben weg.
         247–382  Aufgabe: weiße Bühne, Waage im Gleichgewicht, Haus-Plakette links. „Wenn das Haus /
                  zur Aufgabe wird.“ fällt wortweise ein. Der Bon fällt auf die rechte Schale (252–
                  261), dann vier Aufgaben im Takt (270 · 292 · 315 · 337); die Waage kippt je Gewicht
                  weiter bis 18°; je Gewicht wischt seine Zeile in die Liste.
         382–540  Optionen: Auflösung F-Dur bei 382. „Welche Optionen / gibt es?“ steigt
                  buchstabenweise aus der Maske; vier Optionen fallen auf die linke Schale (405 · 427
                  · 450 · 472), die Waage kommt zurück bis 0° (472 = Taktanfang); der Zeiger trifft
                  das rote Lot (480). Zeilen mit rotem Marker-Wisch.
         540–697  Expertin: Andrea rechts unten, Satz oben: „Nicht jedes Haus muss / verkauft
                  werden.“ (545–566), „Aber jedes Zuhause / sollte zum Leben passen.“ rot (581–602),
                  Name und Funktion (612–630).
         697–832  Ende: Kaffeetisch; „Den ganzen / Expertenbeitrag / jetzt lesen.“ steigt zeilenweise
                  (699–714), roter Knopf „Zum Expertenbeitrag auf in-gl.de“ wischt ein (717–729),
                  Logo-Facetten setzen sich auf den Schlussakkord zusammen (731–742), Wortmarke
                  (742–756); Stand bis 832.
BANNED:  dunkler Grund, Leuchten, Partikel, Verläufe außer dem Lichtschleier des Karussells, Logo in
         der Ecke, alles gleichzeitig einblenden, jede Szene gleich auftreten lassen, Text, der sich
         beim Lesen bewegt, Federn auf Text (Feder nur auf der Waage), Beträge oder Zahlen, die das
         Karussell nicht nennt, Monospace-Bon-Schrift.
QA:      0 (Vorschaubild), 1,6 (Einstieg ganz), 4,3 (Match-Cut „Aber“), 7,6 (Bon fertig), 11,9
         (Waage gekippt, 4 Zeilen), 16,5 (Waage im Gleichgewicht, 4 Optionen), 21,5 (Zitat + Name),
         26,5 (Endkarte). Text im Band 168–1330 px, rechts nicht unter der Aktionsleiste (x > 940 ab
         y 1000), keine Schrift unter 28 px. Ton: Musik vorhanden, Pegel -16…-14 LUFS.
```
