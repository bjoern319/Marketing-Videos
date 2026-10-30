# KNIGGE Immobilien – Katana-Reel „Wir verkaufen Zuhause.“

21,5 Sekunden, 1080×1920, 30 fps, mit Musik und Sounddesign. Beispiel-Werbung mit
[Higgsfield Katana](https://higgsfield.ai/blog/higgsfield-katana): fotoreale KI-Bilder und -Clips, geschnitten in der
Schnittsprache eines Trend-Reels, darüber die KNIGGE-Markenebene in Red Hat Display. Idee: Ein leeres Haus wird ein
Zuhause – leer → belebt, ein Jahr in vier Bildern, am Ende fährt die Kamera durch die rote Haustür zurück auf die Endkarte.

| Zeit | Bild | Text | Katana-Stärke |
| --- | --- | --- | --- |
| 0–1,7 s | FPV-Anflug auf das Haus, die Tür geht auf | „Bergisch Gladbach“ schreibt sich in den Himmel, die Kamera fliegt hindurch | KI-Video + Kinetic Type |
| 1,7–2,7 s | Leeres Wohnzimmer | „Quadratmeter.“ – Flug durchs Wort ins Weiß | Kamerafahrt auf Standbild |
| 2,7–5,0 s | Derselbe Raum, bewohnt | „Zuhause.“ | gleicher Raum leer und belebt |
| 5,0–7,9 s | Küche leer (gekippter Swoop) → Küche belebt | – | Blur-Übergänge im Takt |
| 7,9–13,2 s | Fassade aus derselben Position | HERBST · WINTER · FRÜHLING · SOMMER | ein Haus, vier Jahreszeiten |
| 13,2–16,6 s | Leere Terrasse → Terrasse am Abend, Anstoßen | – | Flash und Shake auf dem Drop |
| 16,6–17,4 s | Kamera fährt rückwärts aus der roten Haustür, warmes Licht | – | Portal-Pull-out |
| 17,4–21,5 s | Endkarte | Logo, „Wir verkaufen Zuhause.“, Kostenlose Wertermittlung, knigge-immobilien.de | Markenebene #CA2C35 / #444F4F |

Vorlage für Rhythmus und Schnittsprache: [„THE VILLA EDIT“](https://www.tiktok.com/@ae.visual.kevin/video/7560731974554455327).
Bilder sind neu generiert, die Musik kommt von Mixkit – aus der Vorlage ist nichts übernommen.

Fertiges Video (v2): Higgsfield-Bibliothek, Media-ID `ec273fb7-9656-45fd-969f-c070f992414f` (23,7 MB, AAC,
−13,1 LUFS, −1,7 dBTP). Nicht im Repo, weil die Claude-Umgebung das Higgsfield-CDN nicht erreicht – bitte dort laden.

## Technik

- **Bild:** 8 × Soul Cinematic (Fassade, leere Räume), 3 × GPT Image 2.5 (Winter, Frühling, Sommer aus der
  Herbst-Position), 4 × Seedance 2.5 Omni-Reference in 1080p, je 4 s (Anflug, Wohnzimmer, Küche, Terrasse).
- **Schnitt und Markenebene:** Katana-Compositor. Schnittliste mit Shots, Kamera, Übergängen und Texten:
  `comp/edl.json`; Effekte (Himmelstitel, Flugwort, Raum-Label, Jahreszeiten, Türlicht, Endkarte): `comp/fx.js`.
  Schrift Red Hat Display (SIL OFL 1.1); Logo aus der Original-SVG gerendert, unverändert.
- **Ton:** Mixkit Nr. 400 „Raising Me Higher“, zwei taktgenaue Ausschnitte (145 BPM); Geräusche CC0 von
  [Kenney](https://kenney.nl) und [OpenGameArt](https://opengameart.org).
- **Kosten:** 265,21 Higgsfield-Credits (4 × 64 Seedance, 3 × 2,75 GPT Image, 8 × 0,12 Soul Cinematic) aus dem
  Plus-Kontingent, kein Zusatzgeld.
- **Prüfung:** Energie-Kurve gegen die Vorlage bestanden, Clip-Bereiche ok, jedes Frame gesichtet. v2: dunkle Pille
  hinter den Jahreszeiten, damit FRÜHLING und SOMMER auf hellem Himmel lesbar sind.

## Ändern

Texte stehen in `comp/edl.json` im `fx` des jeweiligen Shots (Endkarte im letzten), die Gestaltung in `comp/fx.js`.
Gerendert wird im Katana-Arbeitsbereich in Higgsfield (Arbeitsstand v1 dort gesichert; v2 = v1 + dieses `fx.js`).
Quell-Generierungen:

| Clip | Modell | Job-ID |
| --- | --- | --- |
| loc_ext (Fassade Herbst) | Soul Cinematic | 69f215ca-1258-4d97-b8f6-c419012ed466, 430dc47f-081e-4fb6-b8ac-665aa5be6e54 |
| loc_liv (Wohnzimmer leer) | Soul Cinematic | e829fe37-bee8-4976-8152-48f985f338b8, a7b6968f-c856-462f-9dbb-1c07f4498f3a |
| loc_kit (Küche leer) | Soul Cinematic | fd5baa62-2225-4426-b05e-31e9a8a6315b, 00f57c65-3174-4443-bab6-b9d7a7646050 |
| loc_ter (Terrasse leer) | Soul Cinematic | 2a86c422-b099-4d51-a276-9bd950ed4b59, 2e277f74-66c2-43ad-a932-126982286db7 |
| st_winter / st_spring / st_summer | GPT Image 2.5 | b5459982-658d-49af-b8cf-84a079c61f72 / 82a41d42-6714-4b19-a249-dc26b32c62a8 / 78b48401-bf62-4153-9986-f5daaeae1a4b |
| v_ext (Anflug) | Seedance 2.5 | e800ec3e-da40-470d-a5fa-a531a1148fd8 |
| v_liv (Wohnzimmer belebt) | Seedance 2.5 | e4fd3d25-86ac-4320-982e-9518ec6247f0 |
| v_kit (Küche belebt) | Seedance 2.5 | 264eca3c-098a-4dc9-a80b-794b78991108 |
| v_ter (Terrasse, Anstoßen) | Seedance 2.5 | d5d12cf1-aac1-45eb-a50b-36f5c0a2c2c9 |

## Katana oder HyperFrames?

| | Katana | HyperFrames |
| --- | --- | --- |
| Stärke | fotoreale KI-Szenen, Schnitt nach Trend-Vorlage | exakte Marken-Layouts, Texte, Formate, Varianten |
| Kosten | Higgsfield-Credits (hier 265) | kostenlos, lokal |
| Ergebnis | jedes Mal neu generiert, Details prüfen | deterministisch, pixelgenau |

Am besten kombiniert: Katana liefert die Bilder, HyperFrames Markenebene und Varianten. In der Claude-Umgebung ging
das nicht, weil Uploads zu und Downloads von Higgsfield gesperrt sind (Proxy 403); lokal klappt es.

## Vor Veröffentlichung prüfen

- **„Kostenlose Wertermittlung“** als Angebot bestätigen.
- **KI-Kennzeichnung:** Haus, Räume und Menschen sind generiert – Label „Mit KI erstellt“ setzen, nicht als echtes
  Objekt bewerben.
- Anstoßen auf der Terrasse: Das Glas des Mädchens soll als Saft lesen – kurz ansehen.
- Musik: Lizenz auf der Mixkit-Trackseite bestätigen ([Lizenz](https://mixkit.co/license/)); einmal mit Ton anhören
  (bisher nur gemessen).
- Instagram: Text liegt zwischen 168 und 1330 px, nichts unter der Aktionsleiste rechts.
