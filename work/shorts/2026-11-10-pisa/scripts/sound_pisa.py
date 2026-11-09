# Pisa short: synthesised SFX + light original lute-ish march, music well under the voice -> public/pisa/mix.wav
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
SR = 48000; DUR = 1755 / 30; N = int(DUR * SR); rng = np.random.default_rng(3)
def T(n): return np.arange(n) / SR
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
def env(n, a, d): t = T(n); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
noise = lambda d: rng.standard_normal(int(d * SR))
sfx = np.zeros(N); mus = np.zeros(N)
def put(buf, t0, x, g=1.0):
    i = max(0, int(t0 * SR)); j = min(N, i + len(x))
    if j > i: buf[i:j] += g * x[: j - i]
def tone(f, d, dec=0.15): t = T(int(d * SR)); return np.sin(2 * np.pi * f * t) * env(len(t), 0.002, dec)
def clink(): return bp(noise(0.12), 2500, 7000) * env(int(0.12 * SR), 0.001, 0.02) + tone(2300, 0.12, 0.03) * 0.4
def thud(d=0.4, f=60): t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t) + lp(noise(d), 500) * 0.6) * env(len(t), 0.002, d / 3)
# ambience: birds + soft air on the square (day), crickets at night (26.6-34)
amb = lp(noise(DUR), 700)[:N] * 0.02
for t0 in np.arange(1, 26, 2.3): put(sfx, t0 + rng.random(), tone(3200 + 600 * rng.random(), 0.08, 0.03), 0.04)
for t0 in np.arange(26.7, 34, 0.37): put(sfx, t0, bp(noise(0.05), 4200, 5200) * env(int(0.05 * SR), 0.002, 0.02), 0.08)
sfx += amb
# hammers while building (5.2-12.5), the marble chisel (8.9-9.7)
for t0 in np.arange(5.4, 12.4, 0.45): put(sfx, t0 + 0.05 * rng.random(), clink(), 0.18)
for t0 in np.arange(8.95, 9.7, 0.45): put(sfx, t0, clink(), 0.35)
# the lean: long creak + thud + kick
t = T(int(1.6 * SR)); put(sfx, 11.6, np.sin(2 * np.pi * np.cumsum(90 + 40 * np.sin(t * 3)) / SR) * env(len(t), 0.3, 0.8) * 0.5, 0.3)
put(sfx, 13.0, thud(0.6, 50), 0.7)
# war: drums + distant shouts (14.3-17.3)
for t0 in np.arange(14.3, 17.3, 0.5): put(sfx, t0, thud(0.25, 85), 0.35)
# time-lapse building: fast ticks (21.2-25)
for t0 in np.arange(21.2, 25, 0.12): put(sfx, t0, clink(), 0.06)
# banana boing (25.2)
t = T(int(0.5 * SR)); put(sfx, 25.15, np.sin(2 * np.pi * np.cumsum(220 + 160 * np.sin(t * 40) * np.exp(-t * 4)) / SR) * env(len(t), 0.005, 0.2), 0.3)
# mattress squeak (30.3), sinking rumble (32.2)
t = T(int(0.3 * SR)); put(sfx, 30.35, np.sin(2 * np.pi * np.cumsum(600 - 300 * t) / SR) * env(len(t), 0.01, 0.1), 0.15)
put(sfx, 32.2, lp(noise(1.6), 140) * env(int(1.6 * SR), 0.2, 0.6), 0.6)
# closed: clang (36.9); drill (39-44); works chime (44); stop (47)
put(sfx, 36.9, tone(520, 0.8, 0.3) + tone(780, 0.8, 0.25) * 0.5, 0.25)
t = T(int(4.5 * SR)); put(sfx, 39.3, bp(noise(4.5), 300, 1600) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * t)) * np.minimum(1, t / 0.3) * np.minimum(1, (4.5 - t) / 0.4), 0.09)
for k, f in enumerate([660, 880, 1320]): put(sfx, 44.0 + k * 0.09, tone(f, 0.6, 0.25), 0.12)
put(sfx, 46.95, thud(0.2, 120), 0.3)
# quake: rumble + hits
put(sfx, 51.8, lp(noise(5.8), 120) * np.sin(np.pi * T(int(5.8 * SR)) / 5.8), 1.0)
for t0 in [51.85, 52.6, 53.4, 54.5, 55.9]: put(sfx, t0, thud(0.5, 45), 0.6)
# music: light plucked march, 104 bpm, pauses under the night explanation and the quake
beat = 60 / 104
def pluck(f, d=0.3): t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t)) * env(len(t), 0.003, 0.09)
prog = [(146.8, [293.7, 370.0, 440.0]), (110.0, [277.2, 329.6, 440.0]), (123.5, [246.9, 293.7, 370.0]), (98.0, [246.9, 293.7, 392.0])]
for a, b, g in [(0.0, 26.4, 1.0), (26.6, 34.0, 0.5), (34.1, 51.6, 1.0), (57.6, 58.4, 1.0)]:
    k = 0; t0 = a
    while t0 < b - beat:
        root, ch = prog[int(k // 4) % 4]
        put(mus, t0, pluck(root, 0.35), 0.3 * g); put(mus, t0 + beat / 2, pluck(ch[k % 3], 0.22), 0.12 * g)
        k += 1; t0 += beat
v, vsr = sf.read("voice/voice_proc.wav"); v = resample_poly(v, SR, vsr) if vsr != SR else v
voice = np.zeros(N); voice[: min(N, len(v))] = v[:N]
ev = lp(np.abs(voice), 4); ev /= ev.max() + 1e-9; duck = 1 - 0.75 * np.clip(ev * 4, 0, 1)
mix = voice + mus * duck * 0.17 + sfx * (1 - 0.4 * np.clip(ev * 4, 0, 1)) * 0.5
fade = int(0.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade); mix = mix / np.abs(mix).max() * 0.93
sf.write("public/pisa/mix.wav", mix.astype(np.float32), SR); print("mix", round(len(mix) / SR, 2))
