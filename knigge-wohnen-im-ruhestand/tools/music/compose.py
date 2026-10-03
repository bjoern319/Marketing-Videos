#!/usr/bin/env python3
"""Komponiert und rendert die Hintergrundmusik fuer den KNIGGE-Film.

Warmes Klavier + Streicher in F-Dur, 80 BPM (1 Takt = 3 s), 25 Takte = 75 s.
Die Abschnitte liegen exakt auf den Szenengrenzen des Films:

  Takt  1-3   (0-9 s)    Erinnerung   - Klavier allein, nostalgisch
  Takt  4-6   (9-18 s)   Stille       - sparsam, Moll-Farben
  Takt  7-8   (18-24 s)  Wendepunkt   - Aufbau, Aufloesung auf "Mehr Leben" (21 s)
  Takt  9-13  (24-39 s)  Neues Leben  - fliessend, Streicher
  Takt 14-15  (39-45 s)  Zeitpunkt    - nachdenklich, Vorhalt
  Takt 16-19  (45-57 s)  Begleitung   - ruhiger, zuversichtlicher Puls
  Takt 20-22  (57-66 s)  Vor Ort      - voll, warm
  Takt 23-25  (66-75 s)  Kontakt      - Schluss, F-Dur klingt aus

Benoetigt: pip install tinysoundfont numpy; ffmpeg im PATH;
SoundFont "GeneralUser GS" (https://github.com/mrbumpy409/GeneralUser-GS,
Lizenz erlaubt kommerzielle Musikproduktion).

    python3 compose.py --sf2 /pfad/GeneralUser-GS.sf2 --out ../../assets/audio/knigge-theme.m4a
"""
import argparse
import os
import subprocess
import tempfile
import wave

import numpy as np
import tinysoundfont

SR = 44100
BPM = 80
BEAT = 60.0 / BPM  # 0.75 s
BAR = 4 * BEAT  # 3.0 s
BARS = 25
TAIL = 0.0  # Film endet bei 75 s; Ausklang liegt im letzten Takt

# --- Instrumente (GM-Programme) -------------------------------------------
PIANO, STRINGS, CELLO, CELESTA, HARP = 0, 1, 2, 3, 4
PROGRAMS = {PIANO: 0, STRINGS: 49, CELLO: 42, CELESTA: 8, HARP: 46}

# --- Hilfen -----------------------------------------------------------------
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


rng = Rng(1959)
events = []  # (zeit, typ, kanal, taste, velocity)


def note(ch, t, key, dur, vel, human=True):
    if human:
        t += (rng() - 0.5) * 0.016
        vel += int((rng() - 0.5) * 10)
    vel = max(1, min(127, vel))
    t = max(0.0, t)
    events.append((t, 1, ch, key, vel))
    events.append((t + dur, 0, ch, key, 0))


def bar_t(bar, beat=0.0):
    """Startzeit von Takt (1-basiert) plus Schlag (0-basiert, darf Bruch sein)."""
    return (bar - 1) * BAR + beat * BEAT


# --- Harmonik: ein Akkord pro Takt (bzw. zwei halbe) -------------------------
# Jeder Eintrag: (bass, [akkordtoene fuer arpeggio]) oder Liste zweier Haelften
CH = {
    "F": ("F2", ["F3", "C4", "A4", "C5"]),
    "Fmaj7": ("F2", ["F3", "C4", "E4", "A4"]),
    "F/A": ("A2", ["F3", "C4", "A4", "C5"]),
    "F/C": ("C3", ["F3", "C4", "A4", "C5"]),
    "Am": ("A2", ["E3", "C4", "E4", "A4"]),
    "Am7": ("A2", ["E3", "G3", "C4", "E4"]),
    "C/E": ("E2", ["C3", "G3", "C4", "E4"]),
    "C": ("C3", ["E3", "G3", "C4", "E4"]),
    "Csus": ("C3", ["F3", "G3", "C4", "F4"]),
    "C7sus": ("C3", ["F3", "Bb3", "C4", "F4"]),
    "Dm": ("D2", ["A3", "D4", "F4", "A4"]),
    "Dm7": ("D2", ["A3", "C4", "F4", "A4"]),
    "Bb": ("Bb1", ["F3", "Bb3", "D4", "F4"]),
    "Bbmaj7": ("Bb1", ["F3", "A3", "D4", "F4"]),
    "Bbadd9": ("Bb1", ["F3", "C4", "D4", "F4"]),
    "Gm7": ("G2", ["F3", "Bb3", "D4", "F4"]),
}

# Takt -> Akkord(e)
PROG = {
    1: ["Fmaj7"], 2: ["Am7"], 3: ["Bbadd9", "Csus"],
    4: ["Dm"], 5: ["Bbmaj7"], 6: ["Gm7", "C7sus"],
    7: ["Gm7", "C"], 8: ["F"],
    9: ["F"], 10: ["C/E"], 11: ["Dm7"], 12: ["Bbmaj7"], 13: ["Gm7", "C"],
    14: ["Dm7"], 15: ["Bbmaj7", "Csus"],
    16: ["F"], 17: ["Am"], 18: ["Bb"], 19: ["Csus", "C"],
    20: ["Dm7"], 21: ["Bbmaj7"], 22: ["F/C", "C"],
    23: ["F/A"], 24: ["Bb", "C"], 25: ["Fmaj7"],
}


def chord_slices(bar):
    names = PROG[bar]
    span = 4.0 / len(names)
    return [(i * span, span, CH[name]) for i, name in enumerate(names)]


# --- Stimmen -----------------------------------------------------------------
def piano_arpeggio(bar, vel=58, pattern=(0, 1, 2, 3, 2, 1, 2, 3), density=1.0, bass_vel=62):
    for start, span, (bass, tones) in chord_slices(bar):
        note(PIANO, bar_t(bar, start), n(bass), span * BEAT * 0.98, bass_vel)
        steps = int(span * 2)  # Achtel
        for i in range(steps):
            if density < 1.0 and (i % 2 == 1) and rng() > density:
                continue
            key = n(tones[pattern[i % len(pattern)]])
            accent = 6 if i % 4 == 0 else 0
            note(PIANO, bar_t(bar, start + i * 0.5), key, BEAT * 1.6, vel + accent)


def piano_sparse(bar, vel=50):
    """Stille: nur Bass + liegender Akkord, ein Nachschlag."""
    for start, span, (bass, tones) in chord_slices(bar):
        note(PIANO, bar_t(bar, start), n(bass), span * BEAT, vel + 4)
        for k, tone in enumerate(tones[1:]):
            note(PIANO, bar_t(bar, start + 0.02 * k), n(tone), span * BEAT * 0.95, vel - 6)
        note(PIANO, bar_t(bar, start + min(2.5, span - 0.5)), n(tones[-1]) + 12, BEAT * 1.5, vel - 12)


def melody(notes_beats, bar0, vel=72, ch=PIANO):
    """notes_beats: Liste (schlag_ab_bar0, notenname, dauer_in_schlaegen)."""
    for beat, name, dur in notes_beats:
        note(ch, bar_t(bar0, beat), n(name), dur * BEAT * 0.98, vel)


def strings_pad(bar, vel=46, octave_up=False):
    for start, span, (bass, tones) in chord_slices(bar):
        voicing = tones[:3]
        for tone in voicing:
            k = n(tone) + (12 if octave_up else 0)
            note(STRINGS, bar_t(bar, start), k, span * BEAT * 1.02, vel, human=False)


def cello_bass(bar, vel=50, pulse=False):
    for start, span, (bass, tones) in chord_slices(bar):
        k = n(bass)
        if k > n("E3"):
            k -= 12
        if pulse:
            beats = int(span)
            for b in range(beats):
                note(CELLO, bar_t(bar, start + b), k, BEAT * 0.9, vel - (0 if b == 0 else 8))
        else:
            note(CELLO, bar_t(bar, start), k, span * BEAT * 1.0, vel)


def celesta_sparkle(bar, beat, names, vel=58, step=0.25):
    for i, name in enumerate(names):
        note(CELESTA, bar_t(bar, beat + i * step), n(name), BEAT * 2, vel)


def harp_gliss(bar, beat, names, vel=55, step=0.125):
    for i, name in enumerate(names):
        note(HARP, bar_t(bar, beat + i * step), n(name), BEAT * 3, vel)


# --- Partitur ----------------------------------------------------------------
# 1-3 Erinnerung
for b in (1, 2, 3):
    piano_arpeggio(b, vel=54, density=0.85, bass_vel=56)
melody([(0.5, "A4", 1), (1.5, "C5", 1), (2.5, "F5", 1.5)], 1, vel=64)
melody([(0.5, "E5", 1), (1.5, "C5", 1), (2.5, "A4", 1.5)], 2, vel=62)
melody([(0.5, "D5", 1), (1.5, "F5", 0.5), (2.0, "E5", 0.5), (2.5, "C5", 1.5)], 3, vel=60)

# 4-6 Stille
for b in (4, 5, 6):
    piano_sparse(b, vel=46)
melody([(1.0, "A4", 2), (3.0, "F4", 1)], 4, vel=48)
melody([(1.0, "D5", 2), (3.0, "A4", 1)], 5, vel=46)
melody([(1.0, "Bb4", 1.5), (3.0, "C5", 1)], 6, vel=46)
strings_pad(6, vel=30)

# 7-8 Wendepunkt: Aufbau -> "Mehr Leben" (Takt 8 = 21 s)
piano_arpeggio(7, vel=56, pattern=(0, 1, 2, 3, 1, 2, 3, 2), bass_vel=60)
strings_pad(7, vel=40)
cello_bass(7, vel=44)
melody([(2.0, "F4", 0.5), (2.5, "G4", 0.5), (3.0, "A4", 0.5), (3.5, "Bb4", 0.5)], 7, vel=60)
piano_arpeggio(8, vel=64, bass_vel=70)
strings_pad(8, vel=60, octave_up=True)
cello_bass(8, vel=58)
melody([(0.0, "C5", 1.5), (1.5, "A4", 0.5), (2.0, "F5", 2)], 8, vel=78)
harp_gliss(7, 3.0, ["F4", "A4", "C5", "F5", "A5", "C6", "F6"], vel=48)
celesta_sparkle(8, 0.0, ["C6", "F6", "A6", "C7"], vel=54)

# 9-13 Neues Leben
for b in range(9, 14):
    piano_arpeggio(b, vel=58, bass_vel=62)
    strings_pad(b, vel=44)
    cello_bass(b, vel=46)
melody([(0.0, "A4", 1), (1.0, "C5", 1), (2.0, "F5", 1), (3.0, "E5", 1)], 9, vel=70)
melody([(0.0, "E5", 1.5), (1.5, "D5", 0.5), (2.0, "C5", 2)], 10, vel=68)
melody([(0.0, "D5", 1), (1.0, "F5", 1), (2.0, "A5", 1), (3.0, "G5", 1)], 11, vel=70)
melody([(0.0, "F5", 1.5), (1.5, "E5", 0.5), (2.0, "D5", 2)], 12, vel=66)
melody([(0.0, "D5", 1), (1.0, "Bb4", 1), (2.0, "C5", 1), (3.0, "E5", 1)], 13, vel=66)

# 14-15 Zeitpunkt
piano_sparse(14, vel=50)
piano_sparse(15, vel=48)
strings_pad(14, vel=40)
strings_pad(15, vel=36)
melody([(1.0, "F5", 1.5), (2.5, "E5", 0.5), (3.0, "D5", 1)], 14, vel=58)
melody([(0.0, "D5", 1.5), (2.0, "C5", 2)], 15, vel=54)

# 16-19 Begleitung: ruhiger Puls
for b in range(16, 20):
    piano_arpeggio(b, vel=56, pattern=(0, 2, 1, 3, 0, 2, 1, 3), bass_vel=58)
    strings_pad(b, vel=42)
    cello_bass(b, vel=52, pulse=True)
melody([(0.0, "C5", 1), (1.0, "A4", 1), (2.0, "C5", 1), (3.0, "F5", 1)], 16, vel=66)
melody([(0.0, "E5", 2), (2.0, "C5", 2)], 17, vel=62)
melody([(0.0, "D5", 1), (1.0, "F5", 1), (2.0, "Bb5", 2)], 18, vel=66)
melody([(0.0, "A5", 1.5), (1.5, "G5", 0.5), (2.0, "G5", 2)], 19, vel=64)
celesta_sparkle(16, 1.75, ["F6"], vel=40)
celesta_sparkle(17, 1.75, ["E6"], vel=40)
celesta_sparkle(18, 1.75, ["D6"], vel=40)
celesta_sparkle(19, 1.75, ["C6"], vel=40)

# 20-22 Vor Ort: voll, warm
for b in (20, 21, 22):
    piano_arpeggio(b, vel=60, bass_vel=64)
    strings_pad(b, vel=52, octave_up=(b != 20))
    cello_bass(b, vel=54)
melody([(0.0, "F5", 1), (1.0, "A5", 1), (2.0, "G5", 1), (3.0, "F5", 1)], 20, vel=72)
melody([(0.0, "D5", 1.5), (1.5, "F5", 0.5), (2.0, "F5", 2)], 21, vel=70)
melody([(0.0, "E5", 1), (1.0, "F5", 1), (2.0, "G5", 2)], 22, vel=70)

# 23-25 Kontakt: Schluss
piano_arpeggio(23, vel=60, bass_vel=64)
strings_pad(23, vel=50, octave_up=True)
cello_bass(23, vel=52)
melody([(0.0, "C6", 1.5), (1.5, "A5", 0.5), (2.0, "F5", 2)], 23, vel=72)
piano_arpeggio(24, vel=56, density=0.8, bass_vel=60)
strings_pad(24, vel=46)
cello_bass(24, vel=48)
melody([(0.0, "D5", 1), (1.0, "F5", 1), (2.0, "E5", 1), (3.0, "G5", 1)], 24, vel=64)
# Schlussakkord, lang
for k, name in enumerate(["F2", "C3", "F3", "A3", "C4", "E4", "A4", "F5"]):
    note(PIANO, bar_t(25, 0.0) + 0.03 * k, n(name), BAR * 0.98, 60 - k, human=False)
strings_pad(25, vel=42)
note(CELLO, bar_t(25, 0.0), n("F2"), BAR * 0.95, 46, human=False)
celesta_sparkle(25, 0.5, ["A5", "C6", "F6"], vel=44, step=0.5)


# --- Rendering ---------------------------------------------------------------
def render(sf2_path):
    synth = tinysoundfont.Synth(samplerate=SR, gain=-6.0)
    sfid = synth.sfload(sf2_path)
    for ch, prog in PROGRAMS.items():
        synth.program_select(ch, sfid, 0, prog)
    # Kanal-Lautstaerke (CC7) und Panorama (CC10)
    mix = {PIANO: (110, 64), STRINGS: (82, 54), CELLO: (78, 70), CELESTA: (62, 80), HARP: (66, 44)}
    for ch, (vol, pan) in mix.items():
        synth.control_change(ch, 7, vol)
        synth.control_change(ch, 10, pan)
    synth.control_change(PIANO, 64, 0)

    total = BARS * BAR + TAIL
    n_total = int(total * SR)
    out = np.zeros((n_total, 2), dtype=np.float32)
    evs = sorted(events, key=lambda e: (e[0], e[1]))
    pos = 0
    i = 0
    while pos < n_total:
        nxt = evs[i][0] if i < len(evs) else total
        target = min(n_total, int(round(nxt * SR)))
        if target > pos:
            buf = synth.generate(target - pos)
            arr = np.frombuffer(buf, dtype=np.float32).reshape(-1, 2)
            out[pos:target] = arr[: target - pos]
            pos = target
        while i < len(evs) and int(round(evs[i][0] * SR)) <= pos:
            t, typ, ch, key, vel = evs[i]
            if typ == 1:
                synth.noteon(ch, key, vel)
            else:
                synth.noteoff(ch, key)
            i += 1
        if i >= len(evs) and pos >= n_total:
            break
    return out


def reverb(dry, seconds=2.4, wet=0.22):
    """Einfacher Faltungshall mit synthetischer Impulsantwort (deterministisch)."""
    length = int(seconds * SR)
    t = np.arange(length) / SR
    r = np.random.default_rng(42)
    ir = np.zeros((length, 2), dtype=np.float64)
    env = np.exp(-6.9 * t / seconds)
    for c in range(2):
        noise = r.standard_normal(length)
        # sanfter Tiefpass fuer warmen Hall
        k = np.exp(-np.arange(32) / 6.0)
        noise = np.convolve(noise, k / k.sum(), mode="same")
        ir[:, c] = noise * env
    ir[: int(0.012 * SR)] = 0  # Pre-Delay
    ir /= np.sqrt((ir ** 2).sum(axis=0))
    nfft = 1 << int(np.ceil(np.log2(len(dry) + length)))
    wet_sig = np.zeros_like(dry, dtype=np.float64)
    for c in range(2):
        spec = np.fft.rfft(dry[:, c], nfft) * np.fft.rfft(ir[:, c], nfft)
        wet_sig[:, c] = np.fft.irfft(spec, nfft)[: len(dry)]
    return (1 - wet) * dry + wet * wet_sig * 0.9


MIX = {PIANO: (110, 64, 46), STRINGS: (84, 52, 72), CELLO: (80, 72, 52), CELESTA: (64, 82, 80), HARP: (68, 42, 70)}


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
        "fluidsynth", "-ni", "-q", "-g", "0.55", "-r", str(SR),
        "-o", "synth.reverb.active=1", "-o", "synth.reverb.room-size=0.62",
        "-o", "synth.reverb.damp=0.35", "-o", "synth.reverb.width=0.9",
        "-o", "synth.reverb.level=0.75", "-o", "synth.chorus.active=0",
        "-F", raw_path, sf2_path, mid_path,
    ], check=True)
    with wave.open(raw_path, "rb") as w:
        frames = w.readframes(w.getnframes())
        width = w.getsampwidth()
    dtype = {2: np.int16, 4: np.int32}[width]
    arr = np.frombuffer(frames, dtype=dtype).reshape(-1, 2).astype(np.float64)
    arr /= float(np.iinfo(dtype).max)
    total = int((BARS * BAR + TAIL) * SR)
    if len(arr) < total:
        arr = np.vstack([arr, np.zeros((total - len(arr), 2))])
    return arr[:total]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sf2", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--engine", choices=["fluidsynth", "tsf"], default="fluidsynth",
                    help="fluidsynth (Referenz, inkl. Hall) oder tsf (TinySoundFont + eigener Hall)")
    ap.add_argument("--midi", help="optional: Partitur zusaetzlich als .mid speichern")
    args = ap.parse_args()

    if args.midi:
        write_midi(args.midi)
    if args.engine == "fluidsynth":
        with tempfile.TemporaryDirectory() as tmp:
            mixed = render_fluidsynth(args.sf2, tmp)
    else:
        dry = render(args.sf2).astype(np.float64)
        mixed = reverb(dry)
    # sanftes Ein-/Ausblenden
    fade_in = int(0.25 * SR)
    mixed[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    fade_out = int(2.6 * SR)
    mixed[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None] ** 1.6
    peak = np.abs(mixed).max()
    mixed = mixed / peak * 0.89

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
    print(f"wrote {args.out} ({BARS * BAR + TAIL:.1f}s)")


if __name__ == "__main__":
    main()
