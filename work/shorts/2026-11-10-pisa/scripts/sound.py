# Synthesised SFX + an original quirky march score, ducked under the voice -> public/whale/mix.wav (48 kHz)
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
WARP = json.load(open("voice/warp.json"))
def wp(o):  # old story time -> re-timed video time (voice/warp.json)
    for (a, b), (c, d) in zip(WARP, WARP[1:]):
        if o <= c: return b + (o - a) * (d - b) / (c - a)
    return WARP[-1][1]
SR = 48000; DUR = WARP[-1][1]; N = int(DUR * SR); rng = np.random.default_rng(7)
def T(n): return np.arange(n) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], "band", fs=SR, output="sos"), x)
def env(n, a, d):  # attack, exponential decay (s)
    t = T(n); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
sfx = np.zeros(N); mus = np.zeros(N)
def put(buf, t0, x, g=1.0):
    i = max(0, int(wp(t0) * SR)); j = min(N, i + len(x))
    if i < N and j > i: buf[i:j] += g * x[: j - i]
noise = lambda d: rng.standard_normal(int(d * SR))
# ---- ambience: surf swells + wind on beach shots (0-42.5, 50-61), softer on the lot
amb = lp(noise(DUR), 900) * 0.6 + hp(lp(noise(DUR), 3000), 400) * 0.15
sw = 0.55 + 0.45 * np.sin(2 * np.pi * T(N) / 7.5) ** 2
mask = np.ones(N) * 0.5
for a, b, g in [(42.6, 50.0, 0.18), (60.7, DUR, 0.22)]: mask[int(wp(a) * SR):int(wp(b) * SR)] = g
sfx += amb[:N] * sw * lp(mask, 3) * 0.05
# ---- gulls
def gull(d=0.45, f0=1700):
    t = T(int(d * SR)); f = f0 * (1 + 0.35 * np.sin(np.pi * t / d)) * (1 - 0.3 * t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR; x = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    return x * env(len(t), 0.03, d / 2.5) * (1 + 0.3 * np.sin(2 * np.pi * 28 * t))
for t0 in [5.0, 6.3, 8.1, 9.4, 17.5, 18.4, 19.0, 30.0, 31.6, 32.2, 55.7, 56.2, 56.6, 57.0]: put(sfx, t0, gull(0.35 + 0.2 * rng.random(), 1400 + 600 * rng.random()), 0.06)
# ---- whooshes: the flash and the big glides
def whoosh(d=0.6, f0=300, f1=2500):
    n = int(d * SR); x = noise(d); out = np.zeros(n); k = 64
    for s in range(0, n, n // k):
        u = s / n; fc = f0 + (f1 - f0) * u; seg = slice(s, min(n, s + n // k))
        out[seg] = bp(x, max(60, fc * 0.6), fc * 1.4)[seg]
    return out * np.sin(np.pi * T(n) / d) ** 2
for t0, g in [(3.9, 0.25), (7.2, 0.12), (53.1, 0.3), (53.8, 0.15)]: put(sfx, t0, whoosh(), g)
# ---- wave crash (bury), truck revs (tow), crates, countdown drums
put(sfx, 11.3, lp(noise(1.6), 1500) * env(int(1.6 * SR), 0.25, 0.5), 0.35)
t = T(int(1.5 * SR)); f = 55 + 25 * np.sin(np.pi * t / 1.5) ** 2; ph = 2 * np.pi * np.cumsum(f) / SR
put(sfx, 12.6, lp(np.sign(np.sin(ph)) * 0.5 + noise(1.5) * 0.3, 700) * env(len(t), 0.1, 0.9), 0.25)
def thud(d=0.25, f=90):
    t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t * (1 - 0.3 * t / d)) + lp(noise(d), 600) * 0.5) * env(len(t), 0.002, d / 4)
for t0 in [25.2, 25.55, 25.85, 26.2]: put(sfx, t0, thud(), 0.45)
for t0 in [29.35, 29.91, 30.42]: put(sfx, t0, thud(0.4, 70), 0.6)
put(sfx, 31.05, hp(noise(0.03), 2000) * env(int(0.03 * SR), 0.001, 0.008), 0.4)  # plunger click
# ---- BOOM
d = 3.0; t = T(int(d * SR))
boom = (np.sin(2 * np.pi * 42 * t * (1 - 0.15 * t / d)) * env(len(t), 0.005, 0.9) + lp(noise(d), 300) * env(len(t), 0.002, 0.7) * 1.4
        + lp(noise(d), 2500) * env(len(t), 0.001, 0.15) * 0.8)
put(sfx, 31.2, np.tanh(boom * 1.3), 0.9)
put(sfx, 31.5, lp(noise(4), 1200) * env(int(4 * SR), 0.3, 1.4), 0.15)  # rumble / sand settling
# ---- chunk falls: whistle down + wet splat
def splat(d=0.22):
    t = T(int(d * SR)); return bp(noise(d), 180, 1800) * env(len(t), 0.001, 0.05) + np.sin(2 * np.pi * 110 * t) * env(len(t), 0.001, 0.04)
def whistle(d=0.7):
    t = T(int(d * SR)); f = 1500 - 900 * t / d; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
for i in range(26):
    tl = 34.8 + 5.0 * rng.random()
    put(sfx, tl - 0.65, whistle(0.65), 0.03); put(sfx, tl, splat(), 0.22 + 0.1 * rng.random())
for tl in [-0.25, 0.4, 1.0, 1.6, 2.1, 2.7]: put(sfx, 1.2 + tl + 0.9, splat(), 0.2)  # hook
put(sfx, 40.62 - 0.6, whistle(0.6), 0.05); put(sfx, 40.62, splat(0.3), 0.55)
put(sfx, 40.62, np.sin(2 * np.pi * 520 * T(int(0.25 * SR))) * env(int(0.25 * SR), 0.001, 0.06), 0.15)  # bonk
# ---- ketchup
put(sfx, 45.9, bp(noise(0.2), 300, 2500) * env(int(0.2 * SR), 0.002, 0.05), 0.4)
put(sfx, 47.82, whoosh(0.55, 2500, 700) * 0.6 + bp(noise(0.55), 500, 3000) * env(int(0.55 * SR), 0.01, 0.2) * 0.4, 0.5)
put(sfx, 48.35, splat(0.25), 0.4)
# ---- physics "Up." small boom, bulldozer, burial
put(sfx, 53.22, np.tanh(boom[: int(1.5 * SR)] * 1.2), 0.45)
t = T(int(2.4 * SR)); put(sfx, 59.1, lp(np.sign(np.sin(2 * np.pi * 38 * t)) * 0.5 + noise(2.4) * 0.4, 500) * np.sin(np.pi * t / 2.4) ** 0.5, 0.18)
# ---- the car: whistle, crunch
put(sfx, 63.0, whistle(1.05), 0.08)
d = 1.0; t = T(int(d * SR))
crunch = (bp(noise(d), 800, 5000) * env(len(t), 0.001, 0.12) + sum(np.sin(2 * np.pi * f * t) * env(len(t), 0.001, 0.25) for f in [310, 530, 870]) * 0.25
          + np.sin(2 * np.pi * 60 * t) * env(len(t), 0.002, 0.2) + splat(1.0) * 0.8)
put(sfx, 64.05, np.tanh(crunch * 1.5), 0.7)
put(sfx, 64.6, np.sin(2 * np.pi * 1250 * T(int(0.6 * SR))) * env(int(0.6 * SR), 0.01, 0.2) * (1 + 0.5 * np.sin(2 * np.pi * 7 * T(int(0.6 * SR)))), 0.05)  # little tweet of the stars
# ---- music: original quirky march, 112 bpm, bass + pluck + soft kick; stops for the boom, gentle in the golden part
bpm = 112; beat = 60 / bpm
def pluck(f, d=0.28):
    t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t) + 0.15 * np.sin(6 * np.pi * f * t)) * env(len(t), 0.003, 0.09)
def bass(f, d=0.35):
    t = T(int(d * SR)); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env(len(t), 0.005, 0.18)
prog = [(130.81, [261.6, 329.6, 392.0]), (98.0, [246.9, 293.7, 392.0]), (110.0, [261.6, 329.6, 440.0]), (87.31, [261.6, 349.2, 440.0])]
mel = [523.3, 587.3, 659.3, 587.3, 523.3, 392.0, 440.0, 392.0, 659.3, 698.5, 784.0, 659.3, 587.3, 523.3, 587.3, 392.0]
sections = [(0.0, 29.2, 1.0), (32.2, 42.4, 1.0), (42.6, 54.7, 0.6), (54.8, 65.6, 1.0)]
for a, b, g in sections:
    k = 0; t0 = a
    while t0 < b - beat:
        bar = int(k // 4) % 4; root, ch = prog[bar]
        put(mus, t0, bass(root if k % 2 == 0 else root * 1.5), 0.35 * g)
        put(mus, t0 + beat / 2, pluck(ch[k % 3] , 0.2), 0.12 * g)
        if k % 2 == 0: put(mus, t0, np.sin(2 * np.pi * 55 * T(int(0.15 * SR)) * (1 - T(int(0.15 * SR)) * 3)) * env(int(0.15 * SR), 0.002, 0.04), 0.3 * g)
        if g == 1.0 and k % 2 == 1: put(mus, t0, pluck(mel[k % 16], 0.3), 0.14 * g)
        k += 1; t0 += beat
# tension roll before the boom
t = T(int(1.8 * SR)); put(mus, 29.3, lp(noise(1.8), 400) * (t / 1.8) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)), 0.25)
# ---- voice + ducking
v, vsr = sf.read("voice/voice_tight_proc.wav"); v = resample_poly(v, SR, vsr) if vsr != SR else v
voice = np.zeros(N); voice[: min(N, len(v))] = v[:N]
envv = np.abs(voice); envv = lp(envv, 4); envv /= envv.max() + 1e-9
duck = 1 - 0.75 * np.clip(envv * 4, 0, 1)
mix = voice * 1.0 + mus * duck * 0.17 + sfx * (1 - 0.4 * np.clip(envv * 4, 0, 1)) * 0.45
fade = int(0.6 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
peak = np.abs(mix).max(); mix = mix / peak * 0.93
sf.write("public/whale/mix.wav", mix.astype(np.float32), SR)
sf.write("audio/stem_sfx.wav", (sfx * 0.7 / peak).astype(np.float32), SR); sf.write("audio/stem_music.wav", (mus * duck * 0.55 / peak).astype(np.float32), SR)
print("mix", round(len(mix) / SR, 2), "s, peak", round(peak, 3))
