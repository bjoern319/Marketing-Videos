# SPEC – KNIGGE Einzugsgebiet-Reel

```text
GOAL:    Wer das Reel sieht, weiß: KNIGGE ist zwischen Köln und Oberberg an drei Orten vor Ort –
         und hat die Adresse knigge-immobilien.de vor Augen.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, H.264, kein Ton
TIME:    15 s x 30 fps = 450 frames, keine Musik (Ton wählt der Nutzer in Instagram)
LOOK:    Grund Papierweiß #FFFFFF ohne Textur; Karte wie in den Standort-GIFs: Gemeinden #E0E3E1,
         Standort-Gemeinden #C9CECB, Grenzen weiß 3 px (bildschirmfest), Rhein #8ECDEB 7 px;
         Schrift Schiefergrau #444F4F, Nebenschrift #5E6A6A; Akzent KNIGGE-Rot #CA2C35 nur für eine
         Zeile oder ein Wort je Bild (Einstieg „Eine Region.“, Dachzeile über den Ortsnamen,
         Abschlusszeile „Ein Ansprechpartner“) und den Punkt im Marker.
         Montserrat: Einstieg 96 px/800/-0.03em, Ortsname 92 px/800/-0.03em, Dachzeile 40 px/700 Rot,
         Abschluss 66 px/800, Adresse 40 px/600, Gemeindenamen 30 px/500, Standortnamen 34 px/700.
         Medium: eine gezeichnete Landkarte (Flächen + weiße Grenzen) – kein Licht, kein Schatten.
OBJECTS: die Karte des Einzugsgebiets (19 Gemeinden, schematische Grenzen), der Rhein, drei
         Standort-Marker (weißer Kreis, Ring #444F4F, roter Punkt), das neue KNIGGE-Logo.
MOTION:  Kamera power2.inOut 24–27 Frames; Text-Ankunft wortweise blur 6→0 px + opacity in 4 Frames,
         2 Frames Versatz; Abgang blur-out 5 Frames power2.in; Marker fallen 14 Frames back.out(1.7),
         4 Frames Versatz; Puls-Ring 36 Frames, wird dünner statt zu verblassen; Namen auf der
         Karte erscheinen erst, wenn die Kamera steht, 5 Frames blur-in, 2 Frames Versatz.
SHOTS:   0–78     Einstieg: Bild 0 zeigt schon „Drei Standorte. / Eine Region.“ über der ganzen
                  Region. Rhein zeichnet sich (5–35), drei Marker fallen nacheinander (14/21/28) und
                  pulsen. Wörter gehen 70–78 mit Unschärfe ab.
         78–162   Köln: Kamera fährt 78–105 auf Köln mit Leverkusen, Pulheim, Frechen, Hürth. Dachzeile
                  „Standort“, Ortsname „Köln“ ab 96; Namen ab 105; Abgang 156–162.
         162–246  Bergisch Gladbach: Kamera 162–186 auf den Rheinisch-Bergischen Kreis; „Hauptsitz“ /
                  „Bergisch Gladbach“; 8 Gemeindenamen; Abgang 240–246.
         246–330  Wipperfürth: Kamera 246–270 auf Wipperfürth und Nachbarn; „Standort“ / „Wipperfürth“;
                  Hückeswagen, Radevormwald, Marienheide, Lindlar, Engelskirchen; Abgang 324–330.
         330–450  Abschluss: Kamera zieht 330–357 auf die ganze Region zurück (kleiner, Mitte oben);
                  „Ein Ansprechpartner / für Ihre Immobilie.“ ab 345; Marker pulsen 357; Logo landet
                  366 (Blur 8→0, 6 Frames), Adresse 375; Standbild bis 450 (2,5 s).
BANNED:  dunkler Grund, Leuchten/Glow, Verläufe außer in der Bildmarke, Logo in der Ecke, alles auf
         einmal einblenden, Text der sich beim Lesen bewegt (Namen nur bei stehender Kamera),
         langsames Nachschieben in Haltephasen, Federn/Bounce auf Text.
QA:      t=0 (Vorschaubild: Einstieg + Karte), 1.3 (drei Marker), 4.5 (Köln, alle Namen lesbar),
         7.3 (Rheinisch-Bergischer Kreis), 10.1 (Wipperfürth), 14.5 (Abschluss: Zeile, Karte, Logo,
         Adresse). Aller Text im Band 168–1330 px, rechts nicht unter der Aktionsleiste (x > 940 ab
         y 1000), keine Schrift unter 28 px.
```
