# Red Hat Display – Hausschrift für alle Videos

Seit 29.10.2026 die Schrift für alle neuen KNIGGE-Videos (Titel, Texte, Etiketten). Das KNIGGE-Logo
bleibt, wie es ist – seine Wortmarke ist Teil des Logos, nicht der Videotypografie.

- **Quelle:** [Google Fonts](https://fonts.google.com/specimen/Red+Hat+Display), Dateien aus
  [google/fonts](https://github.com/google/fonts/tree/main/ofl/redhatdisplay), Gestaltung MCKL,
  © 2024 The Red Hat Project Authors
- **Lizenz:** SIL Open Font License 1.1 (`OFL.txt`) – frei nutzbar, auch kommerziell und in Videos;
  die Lizenzdatei liegt den Schriftdateien bei.

| Datei | Wofür |
| --- | --- |
| `red-hat-display.woff2`, `red-hat-display-italic.woff2` | HyperFrames / Web – variable Schrift, Stärken 300–900 |
| `red-hat-display.css` | fertige `@font-face`-Regeln für die beiden WOFF2-Dateien |
| `RedHatDisplay[wght].ttf`, `RedHatDisplay-Italic[wght].ttf` | Originale von Google Fonts (variabel) |
| `static/RedHatDisplay-*.ttf` | feste Schnitte Light bis Black – für Programme ohne variable Schriften (Canva, Office …) |

## In einem HyperFrames-Projekt

1. `red-hat-display.woff2` (bei Bedarf auch die Kursive) nach `<projekt>/assets/fonts/` kopieren.
2. In **jeder** Komposition, die die Schrift nutzt, im `<style>` einbinden – sonst meldet
   `hyperframes check` `font_family_without_font_face`:

   ```css
   @font-face {
     font-family: "Red Hat Display";
     src: url("assets/fonts/red-hat-display.woff2") format("woff2");
     font-weight: 300 900;
     font-style: normal;
     font-display: block;
   }
   ```

3. Verwenden: `font-family: "Red Hat Display", sans-serif;` und die Stärke über `font-weight`
   (z. B. 800 für Überschriften, 500 für Fließtext).
