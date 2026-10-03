---
version: alpha
name: KNIGGE Immobilien — Frame (video / frame layer)
description: >
  Design-Wahrheit für das KNIGGE-Video. Farben nach der CI von knigge-immobilien.de (wie im Projekt knigge-wohnen-im-ruhestand):
  KNIGGE-Rot, Bordeaux, Schiefergrau und Hellgrau; dunkle Szenen in abgedunkeltem Schiefergrau. Typografie Montserrat
  (geometrisch, nah an der Wortmarke): 800 für Headlines, 300 als Kontrast, gesperrte Versalien für
  Kicker. Motiv: das KNIGGE-Quadrat als Aufzählungszeichen, die Facetten-Diagonalen als Flächen.
unit: the frame — 1920×1080
principle: eine Idee pro Frame · Rot nur als Akzent · Text kurz, hoher Kontrast

colors:
  canvas: "#ECEEEA"      # Hellgrau der Website-Sektionen – helle Szenen
  ink: "#444F4F"         # Schiefergrau – Text auf Hell, Wortmarke (Website)
  ink-muted: "#5E6A6A"   # Sekundärtext
  knigge-red: "#CA2C35"  # KNIGGE-Rot – Akzente, Bildmarke, Linien (Website)
  red-deep: "#6D131B"    # Bordeaux (Website)
  mark-dark: "#4A0A13"   # dunkelste Facette der Bildmarke
  slate-deep: "#2C3535"  # dunkle Szenen (Schiefergrau, abgedunkelt)
  slate-card: "#404B4B"  # Karten auf Dunkel
  red-on-dark: "#E8656B" # Rot-Tönung für Text auf Dunkel (Kontrast ≥ 3:1)
  white: "#FFFFFF"

typography:
  kicker:   { fontFamily: "Montserrat", px: 22, weight: 700, tracking: "0.24em", upper: true, color: "knigge-red" }
  h1:       { fontFamily: "Montserrat", px: 96, weight: 800, lineHeight: 1.04, tracking: "-0.02em", color: "ink" }
  h2:       { fontFamily: "Montserrat", px: 68, weight: 800, lineHeight: 1.08, tracking: "-0.015em", color: "ink" }
  body:     { fontFamily: "Montserrat", px: 34, weight: 500, lineHeight: 1.35, color: "ink" }
  muted:    { fontFamily: "Montserrat", px: 30, weight: 500, lineHeight: 1.35, color: "stone" }
  stat-num: { fontFamily: "Montserrat", px: 150, weight: 800, lineHeight: 1.0, tracking: "-0.03em", color: "knigge-red" }
  motto:    { fontFamily: "Montserrat", px: 104, weight: "300 / 800", tracking: "-0.02em", color: "white + red-on-dark" }

spacing:
  pad-x: "120px"
  pad-top: "110px"
  content-bottom: "≤ 900px (Keep-out unten)"

components:
  knigge-square:
    description: "Das Logo-Quadrat (drei Facetten) als Aufzählungszeichen, Bullet und Übergangsfläche."
  logo-lockup:
    description: "Bildmarke + KNIGGE (800) über IMMOBILIEN (600, gesperrt, gleiche Breite). Auf Dunkel weiß, auf Hell anthrazit."
  card-dark:
    backgroundColor: "{colors.graphite}"
    border-top: "6px solid {colors.knigge-red}"
    rounded: "6px"
    description: "Leistungs-Karten auf Anthrazit, kein Schatten."
  strike:
    description: "Rote 5px-Linie, die ein Klischee durchstreicht (zeichnet sich von links nach rechts)."
  check:
    description: "Checkbox 60px: Anthrazit-Kontur → rote Füllung mit weißem Haken."

motion:
  ease: "power3.out für Auftritte, power2.inOut für Linien/Wipes; kein Bounce"
  reveal: "Masken-Reveal (clip-path) für Headlines, Stagger für Listen, Count-up für Zahlen"
---

# KNIGGE Immobilien — Frame

Hell (Hellgrau #ECEEEA) und Dunkel (Schiefergrau #2C3535) wechseln sich Frame für Frame ab; Rot (#CA2C35)
bleibt Akzent — außer im Match-Cut vom Hook zur Logo-Enthüllung, wo das rote Quadrat einmal das ganze
Bild füllt (Von-Restorff-Effekt → Marke).
