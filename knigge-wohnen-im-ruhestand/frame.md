---
version: alpha
name: KNIGGE Immobilien — Frame (video layer)
description: >
  Video-Designsystem für KNIGGE Immobilien e.K., abgeleitet von knigge-immobilien.de:
  gefaltetes K-Quadrat als Bildmarke, Wortmarke in Montserrat (KNIGGE fett, IMMOBILIEN gesperrt)
  in Schiefergrau, Überschriften in Montserrat Regular (Rot oder Schiefergrau), Bordeaux-Buttons
  auf hellgrauen Flächen. Für die Zielgruppe Ruhestand: ruhig, gut lesbar, große Schrift.
unit: the frame — 1920×1080 (YouTube) und 1080×1920 (Reels); Szenen skalieren über cqmin
principle: CI-Atome sind fix · Komposition ist frei · Fakten nur aus dem Brief

colors:
  canvas: "#ECEEEA"        # Hellgrau der Website-Sektionen – Grundfläche aller Szenen
  paper: "#FFFFFF"         # Weiß – Hauswände, Labels
  ink: "#444F4F"           # Schiefergrau – Text, Wortmarke, Linienzeichnung (Website)
  ink-muted: "#5E6A6A"     # Sekundärtext
  red: "#CA2C35"           # KNIGGE-Rot – Überschriften, Akzente, Dach (Website)
  red-deep: "#6D131B"      # Bordeaux – Buttons/Toggles auf grauen Flächen (Website)
  mark-dark: "#4A0A13"     # dunkelste Facette der Bildmarke
  warm-light: "#F2C36B"    # Fensterlicht = Leben/Erinnerung (funktional, nicht dekorativ)
  night: "#AEB6BF"         # Fenster ohne Licht (Szene „Stille“)
  leaf: "#B9C2A0"          # Laub (nur Illustration)

radii:
  button: "1cqmin"         # leicht gerundete Rechtecke wie auf der Website
  label: "0.9cqmin"
  mark: "0"                # Bildmarke ist streng quadratisch

typography:
  voice:        { fontFamily: "Montserrat", weight: 400, cqmin: 5.6, lineHeight: 1.2, color: "ink" }   # ruhige Stimme (wie Website-Überschriften)
  headline:     { fontFamily: "Montserrat", weight: 700, cqmin: 6.4, lineHeight: 1.12, tracking: "-0.02em", color: "ink" }
  tagline:      { fontFamily: "Montserrat", weight: 900, cqmin: 11.5, lineHeight: 1.0, tracking: "-0.035em", color: "red" }
  body:         { fontFamily: "Montserrat", weight: 400, cqmin: 4.2, lineHeight: 1.3, color: "ink-muted" }
  list:         { fontFamily: "Montserrat", weight: 700, cqmin: 4.3, lineHeight: 1.2, color: "ink" }
  wordmark:     { fontFamily: "Montserrat", weight: 700, upper: true, color: "ink" }      # KNIGGE
  wordmark-sub: { fontFamily: "Montserrat", weight: 400, upper: true, color: "ink" }      # IMMOBILIEN, gesperrt

spacing:
  pad-landscape: "6.5cqw"
  pad-portrait-x: "8cqw"
  pad-portrait-top: "12cqh"     # Reels-UI oben
  pad-portrait-bottom: "20cqh"  # Reels-UI unten
  stroke-illustration: "3.2"    # in SVG-Einheiten (viewBox 800×600)

components:
  k-mark:
    description: "Quadrat aus drei Facetten (K-Faltung), vermessen am Website-Logo: A (0,0)-(79.5,0)-(0,100), R (79.5,0)-(100,0)-(100,100)-(47.5,40.2), B (0,100)-(47.5,40.2)-(100,100); Verläufe von Dunkelrot zu #CA2C35."
  label:
    backgroundColor: "{colors.paper}"
    border: "0.3cqmin solid {colors.ink}"
    rounded: "{radii.label}"
    typography: "Montserrat 700"
  step-tile:
    backgroundColor: "{colors.red}"
    textColor: "{colors.paper}"
    rounded: "{radii.button}"
  icon-tile:
    backgroundColor: "{colors.red-deep}"
    textColor: "{colors.paper}"
    rounded: "{radii.button}"
  cta-button:
    backgroundColor: "{colors.red-deep}"
    textColor: "{colors.paper}"
    rounded: "{radii.button}"
    typography: "Montserrat 700"
  illustration:
    description: "Linienzeichnung in {colors.ink}, Flächen in paper/canvas-deep, Dächer und Akzente in {colors.red}; zeichnet sich per Strich auf (svg-path-draw)."
---

## Overview

Vertrauensvoll, regional, klar – wie die Website. Das Rot ist Signal, nicht Fläche: Bildmarke,
Schlüsselwörter, Dach des Hauses. Buttons und Icon-Kacheln in Bordeaux, Text in Schiefergrau
auf Hellgrau. Wärme entsteht über die Illustration (Fensterlicht, Sonne), nicht über die Palette.

## Voices

- **Montserrat 400** = ruhige, nachdenkliche Stimme (Fragen, Gefühle) – wie die Website-Überschriften.
- **Montserrat 700/900** = KNIGGE spricht: klar, strukturiert, verlässlich.

## Do

- Große Schrift (≥ 4 cqmin Fließtext), kurze Zeilen, lange Standzeiten.
- Sanfte Ease-Kurven (power2/power3.out, sine.inOut), keine harten Slams.
- Diagonale K-Faltung als Übergangsmotiv (Brand-Wipe) – sparsam.

## Don't

- Keine Angstappelle, keine Superlative, keine Wettbewerber.
- Keine zusätzliche Schriftfamilie, kein reines Schwarz, kein Rot als Vollfläche außer im Brand-Wipe.
