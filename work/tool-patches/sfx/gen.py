# Original cartoon sound effects, synthesised (no third-party audio).
import numpy as np
from scipy.io import wavfile
SR = 44100


def env(n, a=0.01, r=0.08):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na); e[-nr:] = np.linspace(1, 0, nr)
    return e


def sweep(f0, f1, dur, vib=6.0, vibd=0.012, curve=1.0):
    n = int(dur * SR); k = np.linspace(0, 1, n) ** curve
    f = f0 + (f1 - f0) * k
    f = f * (1 + vibd * np.sin(2 * np.pi * vib * np.arange(n) / SR))
    ph = 2 * np.pi * np.cumsum(f) / SR
    # slide whistle: sine + a little 2nd harmonic + breath noise
    y = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.04 * np.random.randn(n)
    return y * env(n, 0.015, 0.06)


def tweet(f=2600, dur=0.32):
    n = int(dur * SR); t = np.arange(n) / SR
    fm = f * (1 + 0.05 * np.sign(np.sin(2 * np.pi * 34 * t)))      # pea-whistle trill
    y = np.sin(2 * np.pi * np.cumsum(fm) / SR) + 0.06 * np.random.randn(n)
    return y * env(n, 0.005, 0.05)


def boing(dur=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 + 140 * np.exp(-t * 6) * np.sin(2 * np.pi * 9 * t)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)
    return y * env(n, 0.003, 0.05)


def pop(dur=0.09):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 40) + 250
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)


def swoosh(dur=0.35, up=True):
    n = int(dur * SR); x = np.random.randn(n)
    # moving band-pass via simple one-pole filters with a sweeping cutoff
    y = np.zeros(n); lp = 0; hp_prev = 0; out_prev = 0
    for i in range(n):
        k = i / n; fc = (300 + 5000 * (k if up else 1 - k))
        a = np.exp(-2 * np.pi * fc / SR); lp = (1 - a) * x[i] + a * lp
        y[i] = lp
    y = y - np.convolve(y, np.ones(40) / 40, 'same')
    return y * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5


def save(name, y):
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.7
    wavfile.write(name + '.wav', SR, (y * 32767).astype(np.int16))


np.random.seed(7)
save('whistle_up', sweep(650, 1900, 0.42, curve=0.8))
save('whistle_down', sweep(1900, 520, 0.55, curve=1.3))
save('whistle_tweet', tweet())
save('boing', boing())
save('pop_soft', pop())
save('swoosh_up', swoosh(0.32, True))
