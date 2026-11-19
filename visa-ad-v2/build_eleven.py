"""Re-time the video to the ElevenLabs VO (word times from the SRT): writes eleven/warp.json and eleven/audio.wav."""
import json, re, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
HERE = Path(__file__).parent; D = HERE / 'eleven'
OFF = .6                      # voice starts 0.6 s into the video
words = []
for blk in D.joinpath('vo.srt').read_text(encoding='utf-8').strip().split('\n\n'):
    ln = blk.splitlines(); a = re.findall(r'(\d+):(\d+):(\d+),(\d+)', ln[1])
    ts = [int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000 for h, m, s, ms in a]
    words.append((ts[0] + OFF, ts[1] + OFF, ln[2].split()[-1].strip('.,?')))
def w(word, n=1):   # start time of the n-th occurrence of a word
    k = 0
    for s, e, x in words:
        if x.lower() == word.lower():
            k += 1
            if k == n: return s
    raise KeyError(word)
def we(word, n=1):
    k = 0
    for s, e, x in words:
        if x.lower() == word.lower():
            k += 1
            if k == n: return e
B = 60 / 112; S0 = 10.514; durs = [2.5 if i == 3 else 1.5 for i in range(11)]
CS = [S0 + sum(durs[:i]) * B for i in range(11)]
A = [(0, 0), (.55, w('Planning')), (3.35, w('But')), (4.15, w('Documents')), (6.43, w('Relax')), (7.2, w('Red')),
     (9.0, we('visa', 2) + .1), (9.6, w('Visas') - .05)]
cw = ['USA', 'UK', 'Canada', 'Schengen', 'Japan', 'China', 'Turkey', 'Taiwan', 'Singapore', 'Australia']
A += [(CS[i] - .02, w(c) - .06) for i, c in enumerate(cw)] + [(CS[10] - .02, w('New') - .15)]
A += [(19.95, w('Tourist') - .5)] + [(20.9 + i * .55, w(x) - .05) for i, x in enumerate(['Tourist', 'business', 'family', 'E', 'M'])]
A += [(25.4, w('Three') - .45), (25.85, w('Three')), (26.7, w('Share')), (27.95, w('We')), (29.2, w('You')),
      (30.6, w('Red', 2) - .5), (30.95, w('Red', 2)), (31.35, w('Your', 5)), (31.6, w('sorted')), (33.1, w('Call')), (37.5, we('today') + 1.5)]
orig, out = [a for a, b in A], [b for a, b in A]
assert all(x < y for x, y in zip(out, out[1:])) and all(x < y for x, y in zip(orig, orig[1:])), A
TOTAL = out[-1]
json.dump({'orig': orig, 'out': out, 'total': TOTAL}, open(D / 'warp.json', 'w'))
WARP = lambda t: float(np.interp(t, orig, out))
print('total', round(TOTAL, 2), 'speed range', min((orig[i+1]-orig[i])/(out[i+1]-out[i]) for i in range(len(A)-1)), max((orig[i+1]-orig[i])/(out[i+1]-out[i]) for i in range(len(A)-1)))

# SFX events from build_audio.py, moved onto the new timeline
src = (HERE / 'build_audio.py').read_text()
head = src[:src.index('n = int(TOTAL')].replace('E = lambda t, f, g: ev.append((t, f, g))', 'E = lambda t, f, g: ev.append((WARP(t), f, g))')
ns = {'WARP': WARP, '__file__': str(HERE / 'build_audio.py')}; exec(head, ns)
L, SR, ev = ns['L'], ns['SR'], ns['ev']
n = int(TOTAL * SR) + SR
sfx = np.zeros(n)
for t0, f, g in ev:
    s = f(); i = int(max(0, t0) * SR); s = s[:n - i]; sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * g
mus = L.music(TOTAL, 112, intro_end=WARP(6.4), outro=TOTAL - 4)[:n]
# voice
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(D / 'vo.mp3'), '-ar', str(SR), '-ac', '1', str(D / 'vo48.wav')], check=True)
v, _ = sf.read(D / 'vo48.wav'); voice = np.zeros(n); i = int(OFF * SR); voice[i:i + len(v)] = v[:n - i]
voice /= np.abs(voice).max()
env = np.convolve(np.abs(voice), np.ones(2400) / 2400, 'same')
duck = np.convolve(1 - .5 * np.clip(env / .05, 0, 1), np.ones(4800) / 4800, 'same')
end = int(TOTAL * SR); fade = np.ones(n); fo = int(1.8 * SR); fade[end - fo:end] = np.linspace(1, 0, fo) ** 1.5; fade[end:] = 0
bed = mus * (duck * fade * .32)[:, None] + (sfx * duck * .16)[:, None]      # music well under the voice
mix = (bed + voice[:, None] * 1.0)[:end]
sf.write(D / 'mix_raw.wav', mix, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(D / 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.2:LRA=11', '-ar', '48000', str(D / 'audio.wav')], check=True)
# loudness check: voice vs music bed
for nm, x in (('voice', voice[:end] * 1.0), ('music+sfx', bed[:end].mean(1))):
    sf.write(D / f'chk_{nm}.wav', x, SR)
print('ok')
