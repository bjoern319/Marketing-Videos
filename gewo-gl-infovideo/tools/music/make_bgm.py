#!/usr/bin/env python3
"""Deterministic, warm music bed for the gewo-gl promo.

76.25 s, 96 BPM (1 bar = 2.5 s), C major. Sections follow the video:
  0.00 hook (curious, minor)      6.25 brand (resolve)        12.5 street (groove)
  25.0 build                      27.5 peak (bright)          32.5 new ways of living (calm)
  42.5 goals                      50.0 trust (lift)           57.5 "Ihre Entscheidung" (calm)
  66.25 call-out (build)          71.25 end card (final resolution)
Writes assets/audio/gewo-gl-theme.m4a (44.1 kHz stereo, AAC 256 kbit/s; needs ffmpeg).
"""
import os
import subprocess
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
DUR = 76.25
N = int(SR * DUR)
BEAT = 60 / 96
EIGHTH = BEAT / 2
SIXTEENTH = BEAT / 4
rng = np.random.default_rng(20260901)

dry = np.zeros((N, 2))
send = np.zeros((N, 2))


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def place(buf, sig, t0, pan=0.0, gain=1.0):
    i0 = int(round(t0 * SR))
    if i0 >= N:
        return
    sig = sig[: N - i0]
    left = np.cos((pan + 1) * np.pi / 4) * gain
    right = np.sin((pan + 1) * np.pi / 4) * gain
    buf[i0 : i0 + len(sig), 0] += sig * left
    buf[i0 : i0 + len(sig), 1] += sig * right


# chord = (bass midi, pad voicing, arp tones)
AM7 = (45, [57, 60, 64, 67], [69, 72, 76, 79])
FMAJ7 = (41, [53, 57, 60, 64], [65, 69, 72, 76])
GSUS = (43, [55, 60, 62, 67], [67, 72, 74, 79])
G = (43, [55, 59, 62, 67], [67, 71, 74, 79])
CADD9 = (48, [60, 64, 67, 74], [72, 76, 79, 74])
C = (48, [60, 64, 67, 72], [72, 76, 79, 84])
GB = (47, [59, 62, 67, 71], [67, 71, 74, 79])
AM = (45, [57, 60, 64, 69], [69, 72, 76, 81])
F = (41, [53, 57, 60, 65], [65, 69, 72, 77])

# (start, end, chord, brightness 0..1)
CHORDS = [
    (0.00, 2.50, AM7, 0.25), (2.50, 5.00, FMAJ7, 0.30), (5.00, 5.625, GSUS, 0.35), (5.625, 6.25, G, 0.40),
    (6.25, 8.75, CADD9, 0.60), (8.75, 11.25, GB, 0.55), (11.25, 12.50, FMAJ7, 0.55),
    (12.50, 15.00, C, 0.55), (15.00, 17.50, G, 0.55), (17.50, 20.00, AM, 0.55), (20.00, 22.50, F, 0.55),
    (22.50, 25.00, C, 0.60), (25.00, 26.25, F, 0.65), (26.25, 27.50, GSUS, 0.70),
    (27.50, 30.00, CADD9, 0.95), (30.00, 32.50, FMAJ7, 0.90),
    (32.50, 35.00, AM7, 0.45), (35.00, 37.50, FMAJ7, 0.50), (37.50, 40.00, C, 0.55), (40.00, 42.50, G, 0.55),
    (42.50, 45.00, AM, 0.55), (45.00, 47.50, F, 0.55), (47.50, 50.00, G, 0.60),
    (50.00, 52.50, C, 0.65), (52.50, 55.00, GB, 0.65), (55.00, 56.25, F, 0.70), (56.25, 57.50, G, 0.70),
    (57.50, 60.00, AM7, 0.50), (60.00, 62.50, FMAJ7, 0.55), (62.50, 65.00, C, 0.60), (65.00, 66.25, G, 0.60),
    (66.25, 68.75, AM7, 0.60), (68.75, 70.00, FMAJ7, 0.65), (70.00, 71.25, GSUS, 0.75),
    (71.25, 76.25, CADD9, 0.90),
]
PEAK = (27.5, 32.5)
FINALE = 71.25


def section_gain(t):
    for end, g in ((6.25, 0.45), (12.5, 0.55), (25.0, 0.5), (27.5, 0.6), (32.5, 0.75), (42.5, 0.5),
                   (57.5, 0.55), (66.25, 0.5), (71.25, 0.6)):
        if t < end:
            return g
    return 0.8


def arp_plan(t):
    """(step seconds, velocity) for the arpeggio at time t, or None."""
    if t < 6.25:
        return (BEAT, 0.28)
    if t < 12.5:
        return (EIGHTH, 0.34)
    if t < 25.0:
        return (EIGHTH, 0.40)
    if t < 27.5:
        return (SIXTEENTH, 0.30 + 0.25 * (t - 25.0) / 2.5)
    if t < 32.5:
        return (EIGHTH, 0.50)
    if t < 42.5:
        return (EIGHTH, 0.36)
    if t < 57.5:
        return (EIGHTH, 0.43)
    if t < 66.25:
        return (EIGHTH, 0.38)
    if t < 70.0:
        return (EIGHTH, 0.42)
    if t < FINALE:
        return (SIXTEENTH, 0.32 + 0.25 * (t - 70.0) / 1.25)
    return None


# --- pad: detuned additive saws, soft attack/release, slow tremolo ---
def pad_note(freq, length, bright, attack=0.45, release=0.9):
    total = length + release
    t = np.arange(int(total * SR)) / SR
    sig = np.zeros_like(t)
    rolloff = 2.1 - 1.0 * bright
    for cents in (-8, 0, 8):
        f = freq * 2 ** (cents / 1200)
        ph = rng.uniform(0, 2 * np.pi)
        for k in range(1, 11):
            if f * k > 9000:
                break
            sig += np.sin(2 * np.pi * f * k * t + ph * k) / k**rolloff
    env = np.ones_like(t)
    a = int(attack * SR)
    env[:a] = np.linspace(0, 1, a) ** 1.5
    r0 = int(length * SR)
    env[r0:] = np.linspace(1, 0, len(t) - r0) ** 2
    trem = 1 + 0.07 * np.sin(2 * np.pi * 0.23 * t + freq)
    return sig * env * trem / 3.0


for start, end, (bass, voicing, arp), bright in CHORDS:
    g = section_gain(start)
    for i, m in enumerate(voicing):
        note = pad_note(hz(m), end - start, bright)
        pan = (-0.45, 0.25, -0.15, 0.45)[i % 4]
        place(dry, note, start, pan, 0.055 * g)
        place(send, note, start, pan, 0.07 * g)
    if PEAK[0] <= start < PEAK[1] or start >= FINALE:
        for i, m in enumerate(voicing[1:]):
            note = pad_note(hz(m + 12), end - start, bright * 0.8, attack=0.8)
            place(send, note, start, (-0.6, 0.6, 0.0)[i % 3], 0.03)


# --- pluck: mallet / e-piano like additive tone with per-harmonic decay ---
def pluck(freq, vel, length=1.8):
    t = np.arange(int(length * SR)) / SR
    sig = np.zeros_like(t)
    for k, amp in ((1, 1.0), (2, 0.42), (3, 0.16), (4, 0.09), (6, 0.03)):
        tau = 0.75 / (1 + 0.9 * (k - 1))
        sig += amp * np.sin(2 * np.pi * freq * k * t) * np.exp(-t / tau)
    att = int(0.004 * SR)
    sig[:att] *= np.linspace(0, 1, att)
    return sig * vel


PATTERN = [0, 1, 2, 3, 2, 1, 2, 3]
step_i = 0
for start, end, (bass, voicing, arp), bright in CHORDS:
    t = start
    while t < end - 1e-6:
        plan = arp_plan(t)
        if plan is None:
            break
        step, vel = plan
        m = arp[PATTERN[step_i % len(PATTERN)]]
        v = vel * (1.0 if step_i % 4 == 0 else 0.78) * rng.uniform(0.92, 1.05)
        sig = pluck(hz(m), v)
        pan = 0.35 * np.sin(step_i * 0.9)
        place(dry, sig, t, pan, 0.07)
        place(send, sig, t, pan, 0.09)
        if PEAK[0] <= t < PEAK[1] and step_i % 2 == 0:
            place(send, pluck(hz(m + 12), v * 0.5), t, -pan, 0.05)
        step_i += 1
        t += step

# finale: one slow strum on the last chord, then two gentle bell notes
for i, m in enumerate([60, 64, 67, 72, 76, 79]):
    place(dry, pluck(hz(m), 0.55, 3.5), FINALE + i * 0.06, -0.5 + i * 0.2, 0.08)
    place(send, pluck(hz(m), 0.55, 3.5), FINALE + i * 0.06, -0.5 + i * 0.2, 0.12)
for t0, m in ((FINALE + 1.875, 84), (FINALE + 2.5, 79)):
    place(send, pluck(hz(m), 0.35, 3.0), t0, 0.3, 0.1)


# --- bass ---
def bass_note(freq, length):
    t = np.arange(int((length + 0.25) * SR)) / SR
    sig = np.sin(2 * np.pi * freq * t) + 0.22 * np.sin(4 * np.pi * freq * t) + 0.08 * np.sin(6 * np.pi * freq * t)
    env = 0.8 + 0.2 * np.exp(-t / 0.35)
    a = int(0.03 * SR)
    env[:a] *= np.linspace(0, 1, a)
    r0 = int(length * SR)
    env[r0:] *= np.linspace(1, 0, len(t) - r0)
    return sig * env


for start, end, (bass, voicing, arp), bright in CHORDS:
    if start < 6.25:
        continue
    calm = 32.5 <= start < 42.5 or 57.5 <= start < 66.25
    level = 0.05 if start < 12.5 else (0.06 if calm else 0.075)
    if start >= FINALE:
        level = 0.08
    place(dry, bass_note(hz(bass), end - start), start, 0.0, level)


# --- drums (soft) ---
def kick():
    t = np.arange(int(0.45 * SR)) / SR
    f = 46 + 75 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16)


hp = butter(4, 6500, "hp", fs=SR, output="sos")


def shaker():
    n = rng.standard_normal(int(0.09 * SR))
    t = np.arange(len(n)) / SR
    return sosfilt(hp, n) * np.exp(-t / 0.022)


def beats(a, b, every):
    t = a
    while t < b - 1e-6:
        yield t
        t += every


for a, b, every, lvl in ((17.5, 25.0, 2 * BEAT, 0.16), (27.5, 32.5, BEAT, 0.2), (37.5, 42.5, 2 * BEAT, 0.12),
                         (42.5, 57.5, 2 * BEAT, 0.16), (66.25, 71.25, 2 * BEAT, 0.14)):
    for t0 in beats(a, b, every):
        place(dry, kick(), t0, 0, lvl)
for t0 in (PEAK[0], FINALE):
    place(dry, kick(), t0, 0, 0.26)

for a, b, lvl in ((15.0, 25.0, 0.05), (27.5, 32.5, 0.06), (35.0, 66.25, 0.045), (66.25, 71.25, 0.05)):
    for t0 in beats(a + EIGHTH, b, BEAT):
        place(dry, shaker(), t0, 0.4, lvl)
        place(send, shaker(), t0, 0.4, lvl * 0.5)


# --- risers into the brand reveal, the peak and the end card ---
bp = butter(2, [900, 7000], "bandpass", fs=SR, output="sos")


def riser(length):
    n = rng.standard_normal(int(length * SR))
    t = np.arange(len(n)) / SR
    env = (t / length) ** 2.2
    sweep = np.sin(2 * np.pi * np.cumsum(300 + 900 * (t / length) ** 2) / SR) * 0.25
    return (sosfilt(bp, n) * 0.6 + sweep) * env


for t0, length, lvl in ((4.75, 1.5, 0.07), (25.0, 2.5, 0.09), (68.75, 2.5, 0.08)):
    place(send, riser(length), t0, 0.0, lvl)
    place(dry, riser(length), t0, 0.0, lvl * 0.5)


def swell():
    n = rng.standard_normal(int(3.0 * SR))
    t = np.arange(len(n)) / SR
    hp2 = butter(2, 4500, "hp", fs=SR, output="sos")
    return sosfilt(hp2, n) * np.exp(-t / 1.1) * np.minimum(1, t / 0.01)


for t0 in (PEAK[0], FINALE):
    place(send, swell(), t0, 0.0, 0.05)


# --- reverb (deterministic noise impulse response) ---
def impulse(seed):
    r = np.random.default_rng(seed)
    t = np.arange(int(2.6 * SR)) / SR
    ir = r.standard_normal(len(t)) * np.exp(-t / 0.62)
    ir = sosfilt(butter(2, 5200, "lp", fs=SR, output="sos"), ir)
    ir[: int(0.012 * SR)] = 0  # pre-delay
    return ir / np.sqrt(np.sum(ir**2))


wet = np.zeros_like(send)
for ch, seed in ((0, 11), (1, 12)):
    wet[:, ch] = fftconvolve(send[:, ch], impulse(seed))[:N]

mix = dry + 0.55 * wet + 0.18 * send
mix = sosfilt(butter(2, 32, "hp", fs=SR, output="sos"), mix, axis=0)

# fades
t = np.arange(N) / SR
mix *= np.clip(t / 0.4, 0, 1)[:, None]
fade_start = DUR - 2.4
fade_out = np.where(t > fade_start, np.cos(np.clip((t - fade_start) / 2.4, 0, 1) * np.pi / 2) ** 2, 1.0)
mix *= fade_out[:, None]

mix = mix / np.max(np.abs(mix)) * 0.92
mix = np.tanh(1.25 * mix) / np.tanh(1.25)
mix = mix / np.max(np.abs(mix)) * 0.89

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "audio")
wav = os.path.join(out_dir, "gewo-gl-theme.wav")
m4a = os.path.join(out_dir, "gewo-gl-theme.m4a")
pcm = (mix * 32767).astype("<i2")
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", wav, "-c:a", "aac", "-b:a", "256k", m4a], check=True)
os.remove(wav)
print("wrote", os.path.abspath(m4a), f"{DUR:.2f}s")
