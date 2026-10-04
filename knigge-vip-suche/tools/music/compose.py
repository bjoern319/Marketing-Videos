#!/usr/bin/env python3
"""Komponiert und rendert die Hintergrundmusik fuer den KNIGGE-Film "VIP-Suche".

96 BPM, 4/4 (1 Takt = 2,5 s), 24 Takte = 60 s. Die Abschnitte liegen exakt auf den
Szenengrenzen, kleine Akzente sitzen auf den Bild-Ereignissen (Sekunden aus den Kompositionen):

  Takt  1-5   (0-12,5 s)   Die Suche   - d-Moll-Farbe, tickende Uhr, unruhige Pizzicati
  Takt  6-8   (12,5-20 s)  VIP-Suche   - Aufloesung nach F-Dur (Brand-Wipe), Erleichterung
  Takt  9-13  (20-32,5 s)  So geht's   - gleichmaessiger Puls, Marimba, Akzente auf den 3 Schritten
  Takt 14-17  (32,5-42,5 s) Ihr Vorteil - Steigerung, Akzente auf dem Durchstreichen, Claim
  Takt 18-20  (42,5-50 s)  Persoenlich - warm, Marimba-"Klingeln" zum Telefon
  Takt 21-24  (50-60 s)    VIP-Zugang  - Klavier-Motiv aus "Nicht weniger Zuhause. Mehr Leben." als
                                         akustisches Markenzeichen, Schluss in F-Dur

Benoetigt: fluidsynth, ffmpeg, Python mit numpy + mido;
SoundFont "GeneralUser GS" (https://github.com/mrbumpy409/GeneralUser-GS,
Lizenz erlaubt kommerzielle Musikproduktion).

    python3 compose.py --sf2 /pfad/GeneralUser-GS.sf2 --out ../../assets/audio/knigge-vip-theme.m4a
"""
import argparse
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100
BPM = 96
BEAT = 60.0 / BPM  # 0.625 s
BAR = 4 * BEAT  # 2.5 s
BARS = 24

# --- Kanaele / GM-Programme --------------------------------------------------
PIANO, PAD, PIZZ, MARIMBA, CELESTA, BASS, HARP, FX, DRUMS = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROGRAMS = {PIANO: 0, PAD: 49, PIZZ: 45, MARIMBA: 12, CELESTA: 8, BASS: 32, HARP: 46, FX: 119, DRUMS: 0}
# Lautstaerke (CC7), Panorama (CC10), Hall (CC91)
MIX = {PIANO: (108, 60, 44), PAD: (70, 50, 70), PIZZ: (82, 74, 40), MARIMBA: (80, 40, 46),
       CELESTA: (66, 84, 72), BASS: (84, 64, 20), HARP: (66, 46, 68), FX: (56, 64, 60), DRUMS: (78, 64, 24)}

# GM-Schlagzeug
KICK, RIM, SNARE, HAT, TOM_LO, CRASH, SHAKER, TAMB = 36, 37, 38, 42, 41, 49, 70, 54

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
        "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def n(name):
    """'A4' -> MIDI-Nummer."""
    pitch, octave = name[:-1], int(name[-1])
    return 12 * (octave + 1) + NOTE[pitch]


class Rng:
    """Deterministischer LCG fuer leichte Humanisierung."""

    def __init__(self, seed=7):
        self.s = seed

    def __call__(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


rng = Rng(2026)
events = []  # (zeit, typ, kanal, taste, velocity)


def note(ch, t, key, dur, vel, human=True):
    if human and ch != DRUMS:
        t += (rng() - 0.5) * 0.012
        vel += int((rng() - 0.5) * 8)
    vel = max(1, min(127, int(vel)))
    t = max(0.0, t)
    events.append((t, 1, ch, key, vel))
    events.append((t + max(0.03, dur), 0, ch, key, 0))


def bt(bar, beat=0.0):
    """Startzeit von Takt (1-basiert) plus Schlag (0-basiert)."""
    return (bar - 1) * BAR + beat * BEAT


def drum(t, key, vel, dur=0.1):
    note(DRUMS, t, key, dur, vel, human=False)


# --- Harmonik -----------------------------------------------------------------
CH = {
    "Dm": ("D2", ["A3", "D4", "F4", "A4"]),
    "Dm7": ("D2", ["A3", "C4", "D4", "F4"]),
    "Bb": ("Bb1", ["F3", "Bb3", "D4", "F4"]),
    "Bbmaj7": ("Bb1", ["F3", "A3", "D4", "F4"]),
    "Bb/F": ("F2", ["F3", "Bb3", "D4", "F4"]),
    "Gm7": ("G2", ["F3", "Bb3", "D4", "G4"]),
    "C7sus": ("C3", ["G3", "Bb3", "C4", "F4"]),
    "C7": ("C3", ["G3", "Bb3", "C4", "E4"]),
    "C": ("C3", ["G3", "C4", "E4", "G4"]),
    "Csus": ("C3", ["F3", "G3", "C4", "F4"]),
    "C/E": ("E2", ["G3", "C4", "E4", "G4"]),
    "F": ("F2", ["F3", "A3", "C4", "F4"]),
    "F/A": ("A2", ["F3", "A3", "C4", "F4"]),
    "Am7": ("A2", ["G3", "A3", "C4", "E4"]),
}

PROG = {
    1: ["Dm"], 2: ["Bb"], 3: ["Gm7"], 4: ["Dm", "Bb"], 5: ["C7sus", "C7"],
    6: ["F"], 7: ["C/E"], 8: ["Bbmaj7", "Csus"],
    9: ["F"], 10: ["Am7"], 11: ["Bbmaj7"], 12: ["Gm7", "C"], 13: ["Bbmaj7", "C7sus"],
    14: ["Dm7"], 15: ["Bbmaj7", "C"], 16: ["F"], 17: ["Bb", "C7sus"],
    18: ["F"], 19: ["Bb/F", "F"], 20: ["Gm7", "C7sus"],
    21: ["F"], 22: ["Bbmaj7"], 23: ["Gm7", "C"], 24: ["F"],
}


def slices(bar):
    names = PROG[bar]
    span = 4.0 / len(names)
    return [(i * span, span, CH[name]) for i, name in enumerate(names)]


# --- Stimmen -------------------------------------------------------------------
def pad(bar, vel=40, up=False):
    for start, span, (bass, tones) in slices(bar):
        for tone in tones[:3]:
            note(PAD, bt(bar, start), n(tone) + (12 if up else 0), span * BEAT * 1.02, vel, human=False)


def bass(bar, vel=56, pattern="half"):
    for start, span, (b, tones) in slices(bar):
        k = n(b)
        if k > n("E3"):
            k -= 12
        if pattern == "half":
            note(BASS, bt(bar, start), k, span * BEAT * 0.95, vel)
        elif pattern == "quarter":
            for q in range(int(span)):
                kk = k if q % 2 == 0 else k + 7
                note(BASS, bt(bar, start + q), kk, BEAT * 0.85, vel - (0 if q == 0 else 8))
        elif pattern == "pulse8":
            for e in range(int(span * 2)):
                note(BASS, bt(bar, start + e * 0.5), k, BEAT * 0.4, vel - (0 if e % 2 == 0 else 10))


def piano_arp(bar, vel=52, pattern=(0, 1, 2, 3, 2, 1, 2, 3), bass_vel=54):
    for start, span, (b, tones) in slices(bar):
        note(PIANO, bt(bar, start), n(b) + 12, span * BEAT * 0.98, bass_vel)
        for i in range(int(span * 2)):
            key = n(tones[pattern[i % len(pattern)]]) + 12
            note(PIANO, bt(bar, start + i * 0.5), key, BEAT * 1.4, vel + (5 if i % 4 == 0 else 0))


def piano_stabs(bar, vel=46, beats=(0.5, 1.5, 2.5, 3.5)):
    """Kurze, unruhige Nachschlag-Akkorde (Szene 'Suche')."""
    for start, span, (b, tones) in slices(bar):
        for bb in beats:
            if start <= bb < start + span:
                for k, tone in enumerate(tones[1:]):
                    note(PIANO, bt(bar, bb) + 0.004 * k, n(tone), BEAT * 0.28, vel - 3 * k)


def pizz_ostinato(bar, vel=50, pattern=(0, 2, 1, 2, 3, 2, 1, 2)):
    for start, span, (b, tones) in slices(bar):
        for i in range(int(span * 2)):
            note(PIZZ, bt(bar, start + i * 0.5), n(tones[pattern[i % len(pattern)]]), BEAT * 0.45, vel + (6 if i % 2 == 0 else 0))


def marimba_ostinato(bar, vel=44, pattern=(0, 2, 3, 2, 1, 2, 3, 2)):
    for start, span, (b, tones) in slices(bar):
        for i in range(int(span * 2)):
            note(MARIMBA, bt(bar, start + i * 0.5), n(tones[pattern[i % len(pattern)]]) + 12, BEAT * 0.5, vel + (5 if i % 4 == 0 else 0))


def melody(spec, bar0, vel=66, ch=PIANO):
    for beat, name, dur in spec:
        note(ch, bt(bar0, beat), n(name), dur * BEAT * 0.98, vel)


def chime(t, names, vel=56, ch=CELESTA, step=0.06, dur=1.2):
    for i, name in enumerate(names):
        note(ch, t + i * step, n(name), dur, vel)


def gliss(t, names, total, vel=48, ch=HARP):
    step = total / max(1, len(names) - 1)
    for i, name in enumerate(names):
        note(ch, t + i * step, n(name), 1.6, vel)


# --- Partitur ------------------------------------------------------------------
# Takt 1-5 · Die Suche (0-12,5 s)
for b in (1, 2, 3, 4, 5):
    bass(b, vel=50 if b < 5 else 56, pattern="half")
    pad(b, vel=26 + 3 * b)
for b in (2, 3, 4, 5):
    pizz_ostinato(b, vel=40 + 3 * b)
for b in (1, 2, 3, 4, 5):
    piano_stabs(b, vel=34 + 2 * b, beats=(0.5, 1.5, 2.5, 3.5) if b > 1 else (2.5, 3.5))
# Uhr tickt, sobald sie im Bild laeuft (3,4 s)
t = bt(2, 1.5)
k = 0
while t < 12.3:
    drum(t, HAT, 30 + (8 if k % 2 == 0 else 0) + int(t), 0.05)
    t += BEAT / 2
    k += 1
# Tabs ploppen auf (steigend)
for tt, nm in zip([3.95, 4.3, 4.6, 4.85, 5.05], ["A4", "C5", "D5", "F5", "A5"]):
    note(MARIMBA, tt, n(nm), 0.3, 50)
# "doppelt" = zwei Schlaege, "3x" = drei
for tt, reps, nm in [(6.95, 2, "D6"), (7.3, 2, "F6"), (7.8, 3, "A6")]:
    for r in range(reps):
        note(MARIMBA, tt + r * 0.09, n(nm), 0.2, 54)
note(CELESTA, 9.4, n("A6"), 1.0, 50)  # Herz
# Stempel "VERGEBEN"
drum(10.25 + 0.2, TOM_LO, 76, 0.3)
for k2, nm in enumerate(["D2", "A2", "D3", "F3"]):
    note(PIANO, 10.47 + 0.003 * k2, n(nm), 0.35, 74 - 4 * k2, human=False)
# Aufbau in den Brand-Wipe (12,5 s)
note(FX, 12.5 - 1.95, n("C4"), 1.95, 64, human=False)
for i in range(8):
    drum(bt(5, 2.0 + i * 0.25), SNARE, 18 + i * 6, 0.08)

# Takt 6-8 · VIP-Suche (12,5-20 s)
drum(12.5, CRASH, 50, 2.0)
for b in (6, 7, 8):
    piano_arp(b, vel=50, bass_vel=56)
    pad(b, vel=40, up=(b == 6))
    bass(b, vel=56, pattern="half")
melody([(1.0, "A4", 0.5), (1.5, "C5", 0.5), (2.0, "F5", 1.5), (3.5, "E5", 0.5)], 6, vel=70)
melody([(0.0, "D5", 1.0), (1.0, "C5", 1.0), (2.0, "A4", 2.0)], 7, vel=64)
melody([(0.0, "Bb4", 1.0), (1.0, "D5", 1.0), (2.0, "C5", 2.0)], 8, vel=64)
chime(13.82, ["C6", "F6", "A6"], vel=52, step=0.07)  # "VIP-Suche"
gliss(13.6, ["C7", "A6", "F6", "C6", "A5", "F5", "C5", "A4", "F4"], 1.5, vel=40)  # Inserate fallen in den Trichter
chime(15.8, ["F5", "C6"], vel=50)  # Trefferliste kommt heraus
for tt, nm in zip([16.45, 16.65, 16.85], ["C6", "D6", "F6"]):
    note(MARIMBA, tt, n(nm), 0.3, 56)
for i in range(16):
    drum(bt(7, i * 0.5), SHAKER, 22 + (6 if i % 2 == 0 else 0), 0.06)
    drum(bt(8, i * 0.5), SHAKER, 24 + (6 if i % 2 == 0 else 0), 0.06)

# Takt 9-13 · So geht's (20-32,5 s)
for b in range(9, 14):
    marimba_ostinato(b, vel=40)
    pad(b, vel=34)
    bass(b, vel=58, pattern="quarter")
    for q in range(4):
        if q in (0, 2):
            drum(bt(b, q), KICK, 54)
        else:
            drum(bt(b, q), RIM, 30)
    for e in range(8):
        drum(bt(b, e * 0.5), SHAKER, 26 + (8 if e % 2 == 1 else 0), 0.06)
for tt in (21.0, 24.5, 28.0):  # die drei Schritte
    chime(tt, ["F5", "C6"], vel=58, ch=MARIMBA, step=0.08, dur=0.6)
note(CELESTA, 23.62, n("C6"), 0.8, 50)  # gespeichert
gliss(25.35, ["F4", "A4", "C5", "F5", "A5", "C6", "F6"], 1.4, vel=42)  # Scan
note(CELESTA, 25.93, n("A6"), 0.8, 52)  # Treffer
note(CELESTA, 26.63, n("C7"), 0.8, 52)
chime(28.85, ["A5", "F6"], vel=52)  # neue E-Mail
note(CELESTA, 30.3, n("F6"), 1.0, 46)  # Hinweis
melody([(2.0, "A4", 1.0), (3.0, "C5", 1.0)], 11, vel=54)
melody([(0.0, "D5", 2.0), (2.0, "E5", 2.0)], 12, vel=54)
melody([(0.0, "F5", 2.0), (2.0, "G5", 2.0)], 13, vel=56)

# Takt 14-17 · Ihr Vorteil (32,5-42,5 s)
drum(32.5, CRASH, 44, 1.6)
for b in range(14, 18):
    piano_arp(b, vel=52, pattern=(0, 2, 1, 3, 0, 2, 1, 3), bass_vel=56)
    pad(b, vel=44, up=(b >= 16))
    bass(b, vel=60, pattern="pulse8")
    for q in range(4):
        drum(bt(b, q), KICK, 50 if q % 2 == 0 else 40)
        if q % 2 == 1:
            drum(bt(b, q), RIM, 36)
    for e in range(8):
        drum(bt(b, e * 0.5), SHAKER, 28 + (8 if e % 2 == 1 else 0), 0.06)
for tt in (34.0, 35.0, 36.0):  # durchgestrichen
    for k2, nm in enumerate(["D4", "F4", "A4"]):
        note(PIZZ, tt + 0.004 * k2, n(nm), 0.25, 66)
    drum(tt, TAMB, 34, 0.1)
chime(36.35, ["C6", "E6", "G6"], vel=56, step=0.05)  # gefilterte Uebersicht
melody([(0.0, "F5", 1.0), (1.0, "E5", 0.5), (1.5, "D5", 0.5), (2.0, "A4", 2.0)], 14, vel=62)
melody([(0.0, "D5", 1.0), (1.0, "F5", 1.0), (2.0, "E5", 1.0), (3.0, "G5", 1.0)], 15, vel=64)
melody([(1.5, "A5", 0.5), (2.0, "G5", 0.5), (2.5, "A5", 0.5), (3.0, "F5", 1.0)], 16, vel=72)  # Claim
melody([(0.0, "F5", 1.5), (1.5, "D5", 0.5), (2.0, "E5", 2.0)], 17, vel=62)
chime(39.5, ["F6"], vel=48)  # "Ueberblick"

# Takt 18-20 · Persoenlich (42,5-50 s)
for b in (18, 19, 20):
    piano_arp(b, vel=48, pattern=(0, 1, 2, 3, 2, 1, 2, 3), bass_vel=52)
    pad(b, vel=44)
    bass(b, vel=52, pattern="half")
    drum(bt(b, 0), KICK, 44)
    drum(bt(b, 2), KICK, 40)
    for e in range(8):
        drum(bt(b, e * 0.5), SHAKER, 20 + (6 if e % 2 == 1 else 0), 0.06)
melody([(0.5, "A4", 0.5), (1.0, "C5", 1.0), (2.0, "D5", 0.5), (2.5, "C5", 1.5)], 18, vel=60)
melody([(0.0, "F5", 1.5), (1.5, "E5", 0.5), (2.0, "D5", 2.0)], 19, vel=60)
melody([(0.0, "D5", 1.0), (1.0, "C5", 1.0), (2.0, "Bb4", 1.0), (3.0, "C5", 1.0)], 20, vel=58)
for tt in (44.2, 45.7, 47.2, 48.7):  # Telefon klingelt
    for r in range(6):
        note(MARIMBA, tt + r * 0.06, n("A5" if r % 2 == 0 else "F5"), 0.08, 40 + (4 if r == 0 else 0))
note(FX, 50.0 - 1.95, n("C4"), 1.95, 60, human=False)

# Takt 21-24 · VIP-Zugang (50-60 s)
drum(50.0, CRASH, 52, 2.2)
for b in (21, 22, 23):
    piano_arp(b, vel=54, bass_vel=58)
    pad(b, vel=48, up=True)
    bass(b, vel=58, pattern="half")
    drum(bt(b, 0), KICK, 46)
    drum(bt(b, 2), KICK, 40)
# Markenmotiv (aus dem Ruhestand-Film: C - A - F)
melody([(0.5, "C5", 1.5), (2.0, "A4", 0.5), (2.5, "F5", 1.5)], 21, vel=78)
melody([(0.5, "C6", 1.5), (2.0, "A5", 0.5), (2.5, "F6", 1.5)], 21, vel=54, ch=CELESTA)
melody([(0.0, "D5", 1.0), (1.0, "F5", 1.0), (2.0, "A5", 2.0)], 22, vel=66)
melody([(0.0, "G5", 1.0), (1.0, "F5", 1.0), (2.0, "E5", 1.0), (3.0, "G5", 1.0)], 23, vel=64)
gliss(54.05, ["F5", "A5", "C6", "F6", "A6"], 0.8, vel=40)  # QR-Scan
chime(54.5, ["A6", "C7"], vel=44, step=0.1)  # Button-Glanz
# Schlussakkord
for k2, nm in enumerate(["F2", "C3", "F3", "A3", "C4", "F4", "A4", "C5", "F5"]):
    note(PIANO, bt(24, 0.0) + 0.025 * k2, n(nm), BAR * 0.98, 66 - 2 * k2, human=False)
for tone in ["F3", "A3", "C4", "F4"]:
    note(PAD, bt(24, 0.0), n(tone), BAR * 0.95, 44, human=False)
note(BASS, bt(24, 0.0), n("F1"), BAR * 0.9, 56, human=False)
chime(bt(24, 0.5), ["A5", "C6", "F6"], vel=44, step=0.31)


# --- MIDI + Rendering -------------------------------------------------------------
def write_midi(path):
    """Partitur als Standard-MIDI-Datei (Typ 1) schreiben."""
    import mido

    tpb = 480
    mid = mido.MidiFile(type=1, ticks_per_beat=tpb)
    meta = mido.MidiTrack()
    meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM), time=0))
    meta.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    mid.tracks.append(meta)
    for ch, prog in PROGRAMS.items():
        tr = mido.MidiTrack()
        vol, pan, rev = MIX[ch]
        tr.append(mido.Message("program_change", channel=ch, program=prog, time=0))
        tr.append(mido.Message("control_change", channel=ch, control=7, value=vol, time=0))
        tr.append(mido.Message("control_change", channel=ch, control=10, value=pan, time=0))
        tr.append(mido.Message("control_change", channel=ch, control=91, value=rev, time=0))
        tr.append(mido.Message("control_change", channel=ch, control=93, value=0, time=0))
        evs = sorted((e for e in events if e[2] == ch), key=lambda e: (e[0], e[1]))
        last = 0
        for t, typ, _, key, vel in evs:
            tick = int(round(t / BEAT * tpb))
            msg = "note_on" if typ == 1 else "note_off"
            tr.append(mido.Message(msg, channel=ch, note=key, velocity=vel, time=tick - last))
            last = tick
        mid.tracks.append(tr)
    mid.save(path)


def render_fluidsynth(sf2_path, tmp):
    mid_path = os.path.join(tmp, "theme.mid")
    raw_path = os.path.join(tmp, "theme-raw.wav")
    write_midi(mid_path)
    subprocess.run([
        "fluidsynth", "-ni", "-q", "-g", "0.5", "-r", str(SR),
        "-o", "synth.reverb.active=1", "-o", "synth.reverb.room-size=0.55",
        "-o", "synth.reverb.damp=0.4", "-o", "synth.reverb.width=0.9",
        "-o", "synth.reverb.level=0.7", "-o", "synth.chorus.active=0",
        "-F", raw_path, sf2_path, mid_path,
    ], check=True)
    with wave.open(raw_path, "rb") as w:
        frames = w.readframes(w.getnframes())
        width = w.getsampwidth()
    dtype = {2: np.int16, 4: np.int32}[width]
    arr = np.frombuffer(frames, dtype=dtype).reshape(-1, 2).astype(np.float64)
    arr /= float(np.iinfo(dtype).max)
    total = int(BARS * BAR * SR)
    if len(arr) < total:
        arr = np.vstack([arr, np.zeros((total - len(arr), 2))])
    return arr[:total]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sf2", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--midi", help="optional: Partitur zusaetzlich als .mid speichern")
    args = ap.parse_args()

    if args.midi:
        write_midi(args.midi)
    with tempfile.TemporaryDirectory() as tmp:
        mixed = render_fluidsynth(args.sf2, tmp)
    fade_in = int(0.2 * SR)
    mixed[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    fade_out = int(2.2 * SR)
    mixed[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None] ** 1.5
    mixed = mixed / np.abs(mixed).max() * 0.89

    with tempfile.TemporaryDirectory() as tmp:
        wav_path = os.path.join(tmp, "theme.wav")
        pcm = (np.clip(mixed, -1, 1) * 32767).astype(np.int16)
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", wav_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", str(SR), "-c:a", "aac", "-b:a", "192k", args.out,
        ], check=True)
    print(f"wrote {args.out} ({BARS * BAR:.1f}s)")


if __name__ == "__main__":
    main()
