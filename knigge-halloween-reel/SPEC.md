# SPEC – Halloween-Reel „Hausgeist Herbert“

```text
GOAL:    Lachen, sich wiedererkennen (das zu große, stille Haus) und mitnehmen: KNIGGE bringt neues
         Leben ins Haus – erster Schritt ist die kostenlose Wertermittlung auf knigge-immobilien.de.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, H.264 + AAC
TIME:    28 s x 30 = 840 Frames. Ton ist die Uhr: Orgel frei bis 4,0 s, danach KNIGGE-Thema 80 BPM
         (1 Schlag = 0,75 s, 1 Takt = 3 s); Taktanfänge 4 · 7 · 10 · 13 (Auflösung F-Dur) · 16 · 19 ·
         22 · 25 (Schlussakkord).
LOOK:    Flache Illustration, keine Verläufe außer Himmel-Wechsel als Flächenfarbe. NACHT: Himmel
         #26303A, Hügel #1B2328, Wand #3B474F, Dach #1C2329, Fenster #161C20, Spuklicht #D8C27A,
         Mond #EFE6C8, Schrift Creme #F3ECD8. TAG: Himmel #E6F1F6, Sonne #FFD166, Hügel #8CBF6E, Wand
         #F4EDE1, Dach #A9443C, Fenster #FFD98A, Haustür KNIGGE-Rot #CA2C35, Läden #3F6E5B, Laub
         #E9A23B/#D9622B/#F2C14E, Schrift Schiefer #323C44 + Rot #CA2C35 für ein Wort.
         Red Hat Display: Titel 900, 104–112 px, -0,02em; Sprechblasen 46 px/700 Schiefer auf Weiß,
         Ecken 30 px; BUH 220 px/900. Herbert: Bettlaken #F8F5EE, Schatten #E5DFD1, Augen #1D2328.
OBJECTS: das Haus (Satteldach, Schornstein, Rundfenster, 4 Fenster mit Läden, Tür, Kürbis, Zaun,
         Baum, Weg) – nachts schief, vernagelt, Spinnweben; tags gerade, geputzt, Blumen, Laub.
         Herbert (Bettlaken-Geist, Ärmchen, Augen, Mund o/flach/Lächeln/Schrei), Spinne am Faden,
         Kind im Bettlaken mit roten Turnschuhen, zwei Eltern-Silhouetten im Fenster, Umzugskartons,
         Gartenschild mit KNIGGE-Logo und rotem VERKAUFT-Band, KNIGGE-Logo.
MOTION:  Figuren: Vorbereitung → Aktion → Überschwingen, Stauchen/Strecken, Teile versetzt (Kopf
         führt, Arme folgen); Schweben ±12 px, 2,4 s. Kamera power2.inOut. Titel wortweise 5 Frames
         (Unschärfe 10→0), Blasen: Skalierung 0,6→1 back.out(1.8), 8 Frames, vom Schwanz aus.
         Verwandlung Nacht→Tag: 36 Frames, Teile gestaffelt 1–2 Frames.
SHOTS:   0–120    Hook: Bild 0 Spukhaus + „Dieses Haus spukt.“; Orgel-Mordent (6–33), Fledermäuse;
                  Lauf (38–63) mit Kamerafahrt ans Fenster; 66: Herbert springt heraus „BUH!“ (Orgel-
                  Akkord + Bass-Schlag); 80–114 er sucht links/rechts – niemand da – und sackt zusammen.
         120–300  Allein: Kamera zurück, Herbert groß vorn. Blase „Seit die Kinder ausgezogen sind …“
                  (129–195), „… erschreck ich nur noch Spinnen.“ (201–291); Spinne fällt (219),
                  Herbert „buh“ (232), Spinne zuckt mit den Schultern (249), klettert weg (279).
         300–390  Zu groß: Herbert schwebt winzig ins Fenster, Kamera zieht auf; „Viel zu viel Haus /
                  für einen Geist.“ (312–378); KNIGGE-Schild wächst aus dem Rasen (360, Pop).
         390–660  Neues Leben: Auflösung bei 390 – Nacht wird Tag (390–426, Funkeln), „Zeit für neues
                  Leben.“ (392–468); VERKAUFT-Band klatscht aufs Schild (412); Eltern winken (435);
                  Kartons (450); Kind läuft herein (480–501); „BUH!“ (502) – Herbert springt (505–
                  528, „AAAH!“); Lachen (530); „Der Spuk ist vorbei.“ (552–651).
         660–840  Ende: Kamera tiefer, „Jedes Haus verdient / ein zweites Leben.“ (666–684),
                  „Kostenlose Wertermittlung“ (705), knigge-immobilien.de (720), Logo auf dem
                  Schlussakkord (750), Herbert schwebt mit Koffer winkend davon (768–816); Stand bis 840.
BANNED:  dunkle Leere mit kleinen Dingen (die Nacht ist eine ganze Szene), Leuchten/Glühen, Partikel,
         Verläufe, Logo in der Ecke, alles gleichzeitig einblenden, Text, der sich beim Lesen bewegt,
         Gruselbilder, die Angst machen (Blut, Fratzen), Spott über ältere Eigentümer, erfundene Zahlen.
QA:      0 (Vorschaubild), 2,4 (BUH), 7,8 (Spinne), 11,5 (zu groß), 14,0 (Tag), 17,2 (Kind erschreckt
         Herbert), 19,5 (Spuk vorbei), 26,5 (Endkarte). Text im Band 168–1330 px, nicht unter der
         Aktionsleiste, ≥ 28 px. Ton -16…-14 LUFS, Spitze ≤ -1 dBTP.
```
