---
version: alpha
name: gewo-gl — Frame (video layer)
description: >
  Video-Designsystem für die Gemeinschaft für Wohnen Bergisch Gladbach e.V., abgeleitet von gewo-gl.de:
  Bildmarke aus einer durchgehenden Linie (zwei Häuser, zwei Menschen mit verbundener Schlaufe),
  Wortmarke „gewo-gl“ in Lato Black, Überschriften in Lato Bold in Dunkelgrün-Anthrazit, Labels in Oliv,
  helle, leicht grünstichige Flächen, eine dunkle Sektion für den Aufruf.
unit: the frame — 1920×1080
principle: CI-Atome sind fix · Komposition ist frei · Fakten nur aus Webseite und Brief

colors:
  canvas: "#F4F8F4"        # helle Sektionsfläche der Webseite – Grundfläche aller Szenen
  card: "#FCFCFC"          # Karten (Webseite)
  card-border: "#DEE3DB"   # Kartenrand (Webseite)
  ink: "#2A3737"           # Überschriften und Text (Webseite)
  ink-muted: "#5A6462"     # Fließtext (Webseite)
  olive: "#5E742E"         # Labels, Nummern, Akzentwörter (Webseite)
  logo-green: "#6BA221"    # grüner Teil der Bildmarke, Grafikakzente, gestrichelte „Potenziale“
  logo-gray: "#3F3F3F"     # grauer Teil der Bildmarke
  tint: "#E6F2DD"          # Icon-Kreise (Webseite #F0F8EC, fürs Video etwas kräftiger)
  dark: "#283434"          # dunkle Sektion „Mit einem Hinweis kann es beginnen“ (Webseite)
  on-dark-label: "#BFD39A" # Label auf dunkler Sektion (Webseite)
  window-light: "#F4B24E"  # Fensterlicht = bewohnt (nur Illustration, funktional)

typography:
  label:    { fontFamily: "Lato", weight: 700, px: 24, upper: true, tracking: "0.12em", color: "olive" }
  headline: { fontFamily: "Lato", weight: 700, px: "88–116", lineHeight: 1.06, tracking: "-0.015em", color: "ink" }
  body:     { fontFamily: "Lato", weight: 400, px: "30–46", lineHeight: 1.3, color: "ink-muted" }
  wordmark: { fontFamily: "Lato", weight: 900, color: "ink", hyphen: "logo-green" }

components:
  logo:
    description: >
      assets/logo/gewo-gl-logo.svg – Vektor-Nachbau des gelieferten 96×72-px-Logos (Strich 22 im viewBox
      24 12 738 546). Grüner Pfad: Tal zwischen den Dächern → linkes Haus → linke Figur → Schlaufe;
      grauer Pfad: Schlaufe → rechte Figur → rechtes Haus → Tal. Köpfe als Ringe. In brand.html und
      cta.html inline, damit sich die Linie in beide Richtungen zeichnet.
  card:      { backgroundColor: "{colors.card}", border: "3px solid {colors.card-border}", rounded: "26px" }
  icon-disc: { backgroundColor: "{colors.tint}", strokes: "5–6 px, logo-green + ink (wie Webseiten-Icons)" }
  potential: { stroke: "{colors.logo-green}", dash: "16 11", meaning: "ungenutztes Potenzial, wird im Höhepunkt zu Fensterlicht" }
  dark-callout: { backgroundColor: "{colors.dark}", label: "{colors.on-dark-label}", headline: "#FCFCFC" }
---

## Bildsprache

Linienillustration im Stil der Bildmarke: dunkle Konturen, helle Flächen, Grün nur für Potenziale,
Bildmarke und Icons. Fensterlicht (warm) steht für „bewohnt“: dunkle Fenster sind ungenutzter Raum,
gestrichelte grüne Rahmen markieren Potenzial, im Höhepunkt werden sie zu Licht.
