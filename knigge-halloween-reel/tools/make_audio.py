#!/usr/bin/env python3
"""Musik für das Halloween-Reel: Orgel-Intro + Schnitt aus der KNIGGE-Musik → assets/audio/musik.m4a.

0–4 s   Orgel: Anfang der Toccata d-Moll BWV 565 (J. S. Bach, gemeinfrei) in eigener Einspielung –
        Mordent, Lauf abwärts, dann der verminderte Akkord über dem Orgelpunkt D genau auf Herberts
        „BUH!“ (2,2 s); löst sich bei 3,0 s matt nach d-Moll auf, während Herbert in sich zusammensackt.
4–22 s  KNIGGE-Thema (../knigge-wohnen-im-ruhestand, 80 BPM) ab Takt 5 (12,0 s): leises Klavier in Moll
        („Stille“), Aufbau ab 10 s, Auflösung nach F-Dur bei 13 s („Zeit für neues Leben“).
22–28 s Takt 24–25 des Themas (69–75 s): Dominante, Schlussakkord bei 25 s (Logo).

Benötigt: fluidsynth, ffmpeg, Python mit numpy und mido, SoundFont GeneralUser GS
(https://github.com/mrbumpy409/GeneralUser-GS, Lizenz erlaubt kommerzielle Musikproduktion).

    python3 tools/make_audio.py --sf2 /pfad/GeneralUser-GS.sf2
"""
import argparse
import os
import subprocess
import tempfile
import wave

import mido
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.normpath(os.path.join(ROOT, "..", "knigge-wohnen-im-ruhestand", "assets", "audio", "knigge-theme.m4a"))
OUT = os.path.join(ROOT, "assets", "audio", "musik.m4a")
SR = 44100
ORGAN = 19  # GM Church Organ
NOTE = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "Bb": 10, "B": 11}


def n(name):
    return 12 * (int(name[-1]) + 1) + NOTE[name[:-1]]


# (Start in s, Dauer in s, Töne) – im Oktavabstand wie im Original
SCORE = [
    (0.20, 0.12, ["A4", "A5"]), (0.32, 0.10, ["G4", "G5"]), (0.42, 0.66, ["A4", "A5"]),
    (1.25, 0.11, ["G4", "G5"]), (1.36, 0.11, ["F4", "F5"]), (1.47, 0.11, ["E4", "E5"]),
    (1.58, 0.11, ["D4", "D5"]), (1.69, 0.30, ["C#4", "C#5"]), (1.99, 0.17, ["D4", "D5"]),
    # verminderter Septakkord über dem Orgelpunkt D – Herberts „BUH!“
    (2.20, 0.82, ["D2", "D3", "C#4", "E4", "G4", "Bb4"]),
    # matte Auflösung nach d-Moll, während er zusammensackt
    (3.02, 1.30, ["D2", "D3", "D4", "F4", "A4"]),
]


def organ_wav(sf2, tmp):
    tpb, bpm = 960, 60  # 1 Schlag = 1 s → Ticks direkt aus Sekunden
    mid = mido.MidiFile(type=0, ticks_per_beat=tpb)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    tr.append(mido.Message("program_change", channel=0, program=ORGAN, time=0))
    tr.append(mido.Message("control_change", channel=0, control=7, value=112, time=0))
    tr.append(mido.Message("control_change", channel=0, control=91, value=90, time=0))
    events = []
    for t, d, notes in SCORE:
        for name in notes:
            events.append((t, 1, n(name)))
            events.append((t + d, 0, n(name)))
    events.sort(key=lambda e: (e[0], e[1]))
    last = 0
    for t, on, key in events:
        tick = int(round(t * tpb))
        tr.append(mido.Message("note_on" if on else "note_off", channel=0, note=key, velocity=104 if on else 0,
                               time=tick - last))
        last = tick
    mid_path, wav_path = os.path.join(tmp, "orgel.mid"), os.path.join(tmp, "orgel.wav")
    mid.save(mid_path)
    subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.6", "-r", str(SR),
                    "-o", "synth.reverb.active=1", "-o", "synth.reverb.room-size=0.85",
                    "-o", "synth.reverb.damp=0.3", "-o", "synth.reverb.width=1.0", "-o", "synth.reverb.level=0.9",
                    "-o", "synth.chorus.active=0", "-F", wav_path, sf2, mid_path], check=True)
    return wav_path


def read_wav(path):
    with wave.open(path, "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, w.getnchannels())
        return data.astype(np.float64) / 32768.0


def decode(path, start, end, tmp, name):
    out = os.path.join(tmp, name)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-to", f"{end}", "-i", path,
                    "-ar", str(SR), "-ac", "2", out], check=True)
    return read_wav(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sf2", required=True)
    args = ap.parse_args()
    total = 28.0
    mix = np.zeros((int(total * SR), 2))
    with tempfile.TemporaryDirectory() as tmp:
        organ = read_wav(organ_wav(args.sf2, tmp))
        organ = organ / (np.abs(organ).max() or 1) * 0.8
        organ = organ[: int(4.5 * SR)]
        # Orgel klingt ab 3,6 s aus und ist bei 4,4 s weg
        k0, k1 = int(3.6 * SR), int(4.4 * SR)
        fade = np.ones(len(organ))
        fade[k0:k1] = np.linspace(1, 0, k1 - k0) ** 1.5
        fade[k1:] = 0
        organ *= fade[:, None]
        mix[: len(organ)] += organ
        # KNIGGE-Thema: Takte 5–10 (12–30 s) ab 4 s, dann Takte 24–25 (69–75 s) ab 22 s
        a = decode(THEME, 12.0, 30.04, tmp, "a.wav")
        b = decode(THEME, 68.96, 75.0, tmp, "b.wav")
        x = int(0.08 * SR)  # Überblendung auf der Taktgrenze bei 22 s
        a[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
        a[-x:] *= np.linspace(1, 0, x)[:, None]
        b[:x] *= np.linspace(0, 1, x)[:, None]
        s = int(4.0 * SR)
        mix[s: s + len(a)] += a[: len(mix) - s]
        s2 = int(21.96 * SR)
        mix[s2: s2 + len(b)] += b[: len(mix) - s2]
        mix = np.clip(mix, -1, 1)
        wav_path = os.path.join(tmp, "musik.wav")
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((mix * 32767).astype(np.int16).tobytes())
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", str(SR), "-c:a", "aac", "-b:a", "192k", OUT], check=True)
    print("geschrieben:", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
