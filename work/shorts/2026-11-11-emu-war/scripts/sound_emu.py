# Emu War short: synthesised SFX + light march, music well under the voice -> public/emu/mix.wav
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
SR = 48000; DUR = 1445 / 30; N = int(DUR * SR); rng = np.random.default_rng(5)
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
def boom(d=0.5):  # emu drumming call: low pulsing hum
    t = T(int(d * SR)); return np.sin(2 * np.pi * 75 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * env(len(t), 0.05, d / 2)
def shot(): t = T(int(0.09 * SR)); return np.tanh((bp(noise(0.09), 300, 4000) * 2 + np.sin(2 * np.pi * 90 * t)) * env(len(t), 0.001, 0.025) * 3)
def thud(d=0.3, f=60): t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t) + lp(noise(d), 500) * 0.6) * env(len(t), 0.002, d / 3)
sfx += lp(noise(DUR), 600)[:N] * 0.015                              # warm wind over the wheat
for t0 in np.arange(0.4, 26, 1.7): put(sfx, t0 + rng.random(), boom(0.6), 0.12)   # emu calls
for t0 in np.arange(0, 3.5, 0.11): put(sfx, t0, thud(0.06, 120), 0.1)            # running feet (hook)
for t0 in np.arange(12.2, 14.2, 0.1): put(sfx, t0, thud(0.06, 120), 0.08)
for t0 in np.arange(16.9, 18.6, 0.075): put(sfx, t0, shot(), 0.35)              # the burst...
put(sfx, 18.6, bp(noise(0.25), 800, 3000) * env(int(0.25 * SR), 0.002, 0.05) + tone(1400, 0.25, 0.06), 0.5)  # ...and the jam
t = T(int(9 * SR)); put(sfx, 20.0, lp(np.sign(np.sin(2 * np.pi * np.cumsum(38 + 6 * np.sin(t * 2)) / SR)) * 0.5 + noise(9) * 0.3, 400) * np.minimum(1, t / 0.4) * np.minimum(1, (9 - t) / 0.6), 0.16)  # truck
for t0 in [21.5, 22.3, 23.1, 24.0, 24.9]: put(sfx, t0, thud(0.35, 55), 0.5)       # bumps
for t0 in np.arange(24.8, 25.9, 0.12): put(sfx, t0, shot(), 0.15)                 # wild shots
for t0 in np.arange(25.9, 34.3, 0.36): put(sfx, t0, bp(noise(0.05), 4200, 5200) * env(int(0.05 * SR), 0.002, 0.02), 0.08)  # crickets
for t0 in np.arange(32.4, 34.3, 0.21): put(sfx, t0 + 0.05 * rng.random(), bp(noise(0.04), 900, 3000) * env(int(0.04 * SR), 0.001, 0.01), 0.35)  # popcorn
t = T(int(3 * SR)); put(sfx, 34.4, lp(np.sign(np.sin(2 * np.pi * 36 * t)) * 0.5 + noise(3) * 0.3, 400) * np.minimum(1, (3 - t) / 1.5), 0.12)  # truck leaves
for t0 in np.arange(36.7, 40.6, 0.07): put(sfx, t0, shot(), 0.2)                 # ten thousand bullets
for t0 in np.arange(36.8, 40.6, 0.09): put(sfx, t0 + 0.03, tone(4200 + 400 * rng.random(), 0.05, 0.015), 0.05)  # shells tinkling
for t0 in [41.5, 42.4]: put(sfx, t0, boom(0.7), 0.25)
beat = 60 / 112
def pluck(f, d=0.3): t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t)) * env(len(t), 0.003, 0.09)
prog = [(130.8, [261.6, 329.6, 392.0]), (98.0, [246.9, 293.7, 392.0]), (110.0, [261.6, 329.6, 440.0]), (87.3, [261.6, 349.2, 440.0])]
for a, b, g in [(0.0, 16.8, 1.0), (19.0, 25.8, 1.0), (25.9, 34.3, 0.5), (34.4, 36.6, 1.0), (40.7, 48.1, 1.0)]:
    k = 0; t0 = a
    while t0 < b - beat:
        root, ch = prog[int(k // 4) % 4]; put(mus, t0, pluck(root, 0.35), 0.3 * g); put(mus, t0 + beat / 2, pluck(ch[k % 3], 0.22), 0.12 * g); k += 1; t0 += beat
v, vsr = sf.read("voice/voice_proc.wav"); v = resample_poly(v, SR, vsr) if vsr != SR else v
voice = np.zeros(N); voice[: min(N, len(v))] = v[:N]
ev = lp(np.abs(voice), 4); ev /= ev.max() + 1e-9; duck = 1 - 0.75 * np.clip(ev * 4, 0, 1)
mix = voice + mus * duck * 0.17 + sfx * (1 - 0.4 * np.clip(ev * 4, 0, 1)) * 0.5
fade = int(0.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade); mix = mix / np.abs(mix).max() * 0.93
sf.write("public/emu/mix.wav", mix.astype(np.float32), SR); print("mix", round(len(mix) / SR, 2))
