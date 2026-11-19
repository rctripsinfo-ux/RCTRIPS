"""Make English VO in several Kokoro voices, synced to the final video, mixed over the music."""
import sys, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from kokoro_onnx import Kokoro
HERE = Path(__file__).parent; OUT = HERE / 'out' / 'vo'; OUT.mkdir(parents=True, exist_ok=True)
M = HERE.parent / 'visa-ad' / 'models'
SR = 48000; B = 60 / 112; S0 = 10.514
durs = [2.5 if i == 3 else 1.5 for i in range(11)]
CS = [S0 + sum(durs[:i]) * B for i in range(11)] + [19.95]
names = ['U.S.A.', 'U.K.', 'Canada.', 'Schengen, thirty countries.', 'Japan.', 'China.', 'Turkey.', 'Taiwan.', 'Singapore.', 'Australia.', 'And New Zealand.']
CUES = [(.3, 3.0, 'Planning a trip abroad?'), (3.35, 5.0, 'But first comes the visa stress.'), (5.0, 6.3, 'Documents, slots, rejections.'),
        (6.43, 6.95, 'Relax.'), (6.95, 8.95, 'Red Carpet Tours handles your visa.'), (9.0, 10.5, 'Visas for your dream destinations.')]
CUES += [(CS[i] + .02, CS[i + 1] - .04, names[i]) for i in range(11)]
CUES += [(20.9, 23.4, 'Tourist, business, family, e-visa, or m-visa.'), (23.5, 25.3, 'Every visa, one expert team.'),
         (25.7, 26.65, 'Three simple steps.'), (26.7, 27.9, 'Share your documents.'), (27.95, 29.15, 'We file and book.'), (29.2, 30.5, 'You get your visa.'),
         (31.0, 32.0, 'Red Carpet Tours.'), (32.05, 33.15, 'Your visa, sorted.'), (33.2, 35.2, 'Call or WhatsApp today.')]
VOICES = sys.argv[1:] or ['af_heart', 'am_michael', 'bf_emma', 'bm_george']
k = Kokoro(str(M / 'kokoro.onnx'), str(M / 'voices.bin'))
def trim(a, thr=.012):
    i = np.where(np.abs(a) > thr)[0]; return a[max(0, i[0] - 400): i[-1] + 1800] if len(i) else a
def say(text, v, sp):
    a, sr = k.create(text, voice=v, speed=sp, lang='en-gb' if v[0] == 'b' else 'en-us')
    return trim(np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32))
music, msr = sf.read(HERE / 'out' / 'audio.wav'); assert msr == SR
n = len(music)
for v in VOICES:
    base = 1.1 if v[1] == 'm' else 1.08
    vo = np.zeros(n)
    for s, e, text in CUES:
        a = say(text, v, base); d = len(a) / SR
        if d > e - s: a = say(text, v, min(1.5, base * d / (e - s) * 1.04))
        i = int(s * SR); a = a[:n - i]; vo[i:i + len(a)] += a
    vo = sosfilt(butter(2, 90, 'high', fs=SR, output='sos'), vo); vo /= np.abs(vo).max()
    env = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - .6 * np.clip(env / .06, 0, 1)
    duck = np.convolve(duck, np.ones(4800) / 4800, 'same')
    mix = music * duck[:, None] * .75 + vo[:, None] * .9
    sf.write(OUT / f'raw_{v}.wav', mix, SR)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / f'raw_{v}.wav'), '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', '48000', str(OUT / f'mix_{v}.wav')], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(HERE / 'out' / 'RedCarpet-Visa-Ad-Final.mp4'), '-i', str(OUT / f'mix_{v}.wav'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(OUT / f'RedCarpet-Visa-VO-{v}.mp4')], check=True)
    print('done', v)
