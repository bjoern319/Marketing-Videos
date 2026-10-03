#!/usr/bin/env python3
"""Erzeugt das Musikbett für das KNIGGE-Video (lizenzfrei, rein synthetisch).

D-Dur, 96 BPM, Piano-Arpeggien + Pad + Bass + dezente Percussion.
Die Form folgt den Szenen des Videos:
  0–6 s    Hook: monotoner Ton (Gleichförmigkeit), bei 3,25 s ein heller Glockenton
           (das „andere" Feld), danach Crescendo in den Logo-Downbeat
  6 s      Logo: voller Akkord, Arpeggien setzen ein
  11–46 s  Groove (Kick/Shaker), ab 26 s zusätzliche Melodie
  46–53,5  Breakdown (Wir sind von hier)
  53,5–63,5 Groove + Melodie (Selbst-Check)
  63,5–    Kadenz ii–IV–V–I, Schlussakkord auf dem Motto (≈ 67,9 s), Ausklang bis 72,5 s

Aufruf:  python3 scripts/make-music.py  → assets/audio/knigge-bgm.wav
"""
import os
import wave

import numpy as np

SR = 44100
DUR = 73.0
N = int(SR * DUR)
BEAT = 60.0 / 96.0
BAR = 4 * BEAT
T0 = 6.0  # erster Takt = Logo-Downbeat

L = np.zeros(N)
R = np.zeros(N)
REV_L = np.zeros(N)  # Hall-Send
REV_R = np.zeros(N)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def add(sig, start, pan=0.0, gain=1.0, send=0.25):
    i0 = int(round(start * SR))
    if i0 >= N or i0 < 0:
        return
    n = min(len(sig), N - i0)
    lg = gain * np.cos((pan + 1) * np.pi / 4)
    rg = gain * np.sin((pan + 1) * np.pi / 4)
    L[i0 : i0 + n] += sig[:n] * lg
    R[i0 : i0 + n] += sig[:n] * rg
    REV_L[i0 : i0 + n] += sig[:n] * lg * send
    REV_R[i0 : i0 + n] += sig[:n] * rg * send


def piano(m, dur, vel=0.8):
    f = hz(m)
    t = np.arange(int((dur + 1.4) * SR)) / SR
    out = np.zeros_like(t)
    for k in range(1, 14):
        fk = f * k * np.sqrt(1 + 0.00025 * k * k)
        if fk > 15000:
            break
        amp = 1.0 / k**1.35
        decay = 0.9 + 0.45 * k * (f / 440.0) ** 0.5
        out += amp * np.sin(2 * np.pi * fk * t + 0.37 * k) * np.exp(-t * decay)
    att = np.minimum(1.0, t / 0.004)
    rel = np.where(t < dur, 1.0, np.exp(-(t - dur) * 5.0))
    rng = np.random.default_rng(int(m * 1000 + dur * 100))
    hammer = rng.standard_normal(len(t)) * np.exp(-t * 80.0) * 0.015
    return (out * att * rel + hammer) * vel * 0.22


def pad(notes, dur, gain=0.05):
    t = np.arange(int((dur + 2.5) * SR)) / SR
    out = np.zeros_like(t)
    for m in notes:
        for det in (-0.09, 0.0, 0.08):
            fd = hz(m) * 2 ** (det / 12.0)
            for k in range(1, 7):
                out += np.sin(2 * np.pi * fd * k * t + 3.1 * det + 0.7 * k) / k**1.7
    env = np.minimum(1.0, t / 1.1) * np.where(t < dur, 1.0, np.exp(-(t - dur) * 1.8))
    return out * env * gain / len(notes)


def bass(m, dur, gain=0.32):
    f = hz(m)
    t = np.arange(int((dur + 0.4) * SR)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1.0, t / 0.008) * np.exp(-t * 0.8) * np.where(t < dur, 1.0, np.exp(-(t - dur) * 14.0))
    return s * env * gain


def kick(gain=0.42):
    t = np.arange(int(0.45 * SR)) / SR
    f = 46.0 + 80.0 * np.exp(-t * 32.0)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8.5) * gain


def noise_hit(seed, length, decay, gain, hp=True):
    t = np.arange(int(length * SR)) / SR
    n = np.random.default_rng(seed).standard_normal(len(t))
    if hp:
        n = np.diff(np.concatenate([[0.0], n]))
    return n * np.minimum(1.0, t / 0.003) * np.exp(-t * decay) * gain


def bell(m, gain=0.16):
    f = hz(m)
    t = np.arange(int(3.5 * SR)) / SR
    s = (
        np.sin(2 * np.pi * f * t) * np.exp(-t * 1.3)
        + 0.45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 2.8)
        + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 5.5)
    )
    return s * np.minimum(1.0, t / 0.002) * gain


# ---------- Harmonie (D-Dur) ----------
CH = {
    #       Arpeggio (tief→hoch)   Pad            Bass
    "D": ([62, 69, 74, 78], [62, 66, 69], 50),
    "A/C#": ([61, 69, 73, 76], [61, 64, 69], 49),
    "Bm": ([59, 66, 71, 74], [59, 62, 66], 47),
    "G": ([59, 67, 71, 74], [59, 62, 67], 43),
    "A": ([61, 69, 73, 76], [61, 64, 69], 45),
    "Em": ([64, 67, 71, 76], [59, 64, 67], 52),
}
PROG = (
    ["D", "A/C#", "Bm", "G", "D", "A/C#", "Bm", "G"]  # Takt 0–7
    + ["D", "A/C#", "Bm", "G", "D", "A", "G", "A"]  # Takt 8–15
    + ["Bm", "G", "A"]  # Takt 16–18 Breakdown
    + ["D", "A/C#", "Bm", "Em"]  # Takt 19–22
    + ["G", "A"]  # Takt 23–24 Kadenz
)
MELODY = {  # Halbe Noten, Takt → (Ton 1, Ton 2)
    8: (78, 76), 9: (76, 73), 10: (74, 78), 11: (79, 78),
    12: (78, 81), 13: (81, 76), 14: (79, 74), 15: (76, 73),
    19: (78, 76), 20: (76, 73), 21: (74, 78), 22: (79, 76),
}
ARP = [0, 1, 2, 1, 3, 1, 2, 1]
FINAL = T0 + 24 * BAR + 0.75 * BAR  # ≈ 67,9 s – Motto

# ---------- Intro / Hook ----------
add(pad([62, 69, 74], 6.0, gain=0.035), 0.0, send=0.5)
for i in range(5):  # monotoner Ton = „alle gleich"
    add(piano(69, 0.18, vel=0.45), 0.3 + i * BEAT, pan=-0.1, send=0.35)
add(bell(81, 0.13), 3.25, pan=0.25, send=0.6)  # das „andere" Feld
add(bell(78, 0.08), 3.25, pan=-0.2, send=0.6)
for i in range(4):  # leises Arpeggio wächst in den Downbeat
    for j, idx in enumerate(ARP):
        tt = 3.75 + i * BEAT * 2 + j * BEAT / 4
        if tt >= T0 - 0.05:
            break
        vel = 0.18 + 0.5 * (tt - 3.75) / (T0 - 3.75)
        add(piano(CH["D"][0][idx], 0.25, vel=vel), tt, pan=0.15 * (idx - 1.5), send=0.35)

# ---------- Hauptteil ----------
for b, name in enumerate(PROG):
    start = T0 + b * BAR
    arp, padn, bn = CH[name]
    breakdown = 16 <= b <= 18
    final_bar = b == 24
    groove = (2 <= b <= 15) or (19 <= b <= 22)

    add(pad(padn, BAR * (0.75 if final_bar else 1.0), gain=0.05 if not breakdown else 0.06), start, send=0.5)
    add(bass(bn, BAR * (0.75 if final_bar else 0.95)), start, send=0.05)

    steps = 6 if final_bar else 8
    for j in range(steps):
        if breakdown and j % 2 == 1:
            continue
        idx = ARP[j]
        vel = 0.55 + (0.12 if j in (0, 4) else 0.0)
        add(piano(arp[idx], BEAT * 0.9, vel=vel), start + j * BEAT / 2, pan=0.18 * (idx - 1.5), send=0.3)

    if b in MELODY:
        for k, m in enumerate(MELODY[b]):
            add(piano(m, BEAT * 1.8, vel=0.5), start + k * 2 * BEAT, pan=0.3, send=0.45)

    if groove:
        for q in (0, 2):
            add(kick(), start + q * BEAT, send=0.02)
        for q in (1, 3):
            add(noise_hit(100 + b * 4 + q, 0.18, 26.0, 0.07), start + q * BEAT, pan=0.1, send=0.3)
        for e in range(8):
            g = 0.035 if e % 2 else 0.018
            add(noise_hit(500 + b * 8 + e, 0.08, 55.0, g), start + e * BEAT / 2, pan=0.35, send=0.1)

# Logo-Downbeat: Akkord + weicher Becken-Swell
add(pad([50, 57, 62, 66, 69], 2.5, gain=0.05), T0, send=0.6)
for m in (50, 57, 62, 66, 69):
    add(piano(m, 1.6, vel=0.5), T0, send=0.45)
add(noise_hit(31, 2.5, 1.6, 0.05), T0, send=0.5)

# Schlussakkord auf dem Motto
for m in (38, 50, 57, 62, 66, 69, 74):
    add(piano(m, 3.4, vel=0.55), FINAL, send=0.5)
add(pad([50, 57, 62, 66, 69], 3.0, gain=0.06), FINAL, send=0.6)
add(bell(81, 0.1), FINAL + 0.02, pan=0.2, send=0.7)

# ---------- Hall (Faltung mit synthetischer Impulsantwort) ----------
ir_len = int(2.6 * SR)
tt = np.arange(ir_len) / SR
rng = np.random.default_rng(2006)
ir_l = rng.standard_normal(ir_len) * np.exp(-tt / 0.55)
ir_r = rng.standard_normal(ir_len) * np.exp(-tt / 0.55)
for ir in (ir_l, ir_r):
    ir[: int(0.012 * SR)] = 0.0  # Pre-Delay
    ir /= np.sqrt(np.sum(ir**2))


def fftconv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[: len(x)]


L += 0.55 * fftconv(REV_L, ir_l)
R += 0.55 * fftconv(REV_R, ir_r)

# ---------- Master ----------
t = np.arange(N) / SR
fade = np.minimum(1.0, t / 0.25) * np.clip((72.5 - t) / 2.0, 0.0, 1.0)
L *= fade
R *= fade
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = np.tanh(1.1 * L / peak) / np.tanh(1.1)
R = np.tanh(1.1 * R / peak) / np.tanh(1.1)
L *= 0.89
R *= 0.89

out = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "knigge-bgm.wav")
os.makedirs(os.path.dirname(out), exist_ok=True)
data = (np.stack([L, R], axis=1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", os.path.abspath(out), f"{DUR:.1f}s")
