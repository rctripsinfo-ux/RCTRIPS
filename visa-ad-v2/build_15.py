"""15 s cut-down with the ElevenLabs voice: picks phrases from the SRT and maps video segments. Writes eleven/warp15.json, eleven/audio15.wav."""
import json, re, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
HERE = Path(__file__).parent; D = HERE / 'eleven'
words = []
for blk in D.joinpath('vo.srt').read_text(encoding='utf-8').strip().split('\n\n'):
    ln = blk.splitlines(); a = re.findall(r'(\d+):(\d+):(\d+),(\d+)', ln[1])
    ts = [int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000 for h, m, s, ms in a]
    words.append((ts[0], ts[1], ln[2].split()[-1].strip('.,?-')))
def span(first, last, n1=1, n2=1):
    def find(wd, n):
        k = 0
        for i, (s, e, x) in enumerate(words):
            if x.lower() == wd.lower():
                k += 1
                if k == n: return i
    i, j = find(first, n1), find(last, n2); return words[i][0], words[j][1], [(words[q][0] - words[i][0], words[q][2]) for q in range(i, j + 1)]
# phrases (start in output, srt span)
P = [(0.15, span('Planning', 'abroad')), (2.25, span('Red', 'visa', 1, 2)), (4.4, span('Visas', 'destinations')),
     (8.55, span('Tourist', 'visa', 1, 4)), (12.3, span('Your', 'sorted', 5, 1)), (13.75, span('Call', 'today'))]
for st, (a, b, w) in P: print(round(st, 2), round(b - a, 2), ' '.join(x for _, x in w))
mt = {x.lower(): st + o for st, (a, b, w) in P[3:4] for o, x in w}
SEGS = [dict(out=[0, 2.1], orig=[0, 2.6]),
        dict(out=[2.1, 4.3], orig=[7.05, 9.2]),
        dict(out=[4.3, 8.4], orig=[10.494, 19.9]),
        dict(out=[8.4, 8.55, mt['business'], mt['family'], mt['e'], mt['m'], 12.1], orig=[20.6, 20.9, 21.45, 22.0, 22.55, 23.1, 23.8]),
        dict(out=[12.1, 12.3, 12.55, 13.65, 15.3], orig=[30.95, 31.35, 31.6, 33.1, 34.4])]
TOTAL = 15.3
json.dump({'segs': SEGS, 'total': TOTAL, 'name': 'visa-ad-15s', 'audio': 'audio15.wav'}, open(D / 'warp15.json', 'w'))
def o2out(t):
    for g in SEGS:
        if g['orig'][0] <= t <= g['orig'][-1]: return float(np.interp(t, g['orig'], g['out']))
    return None
src = (HERE / 'build_audio.py').read_text()
head = src[:src.index('n = int(TOTAL')].replace('E = lambda t, f, g: ev.append((t, f, g))', 'E = lambda t, f, g: (o2out(t) is not None) and ev.append((o2out(t), f, g))')
ns = {'o2out': o2out, '__file__': str(HERE / 'build_audio.py')}; exec(head, ns)
L, SR, ev = ns['L'], ns['SR'], ns['ev']
for g in SEGS[1:]: ev.append((g['out'][0] - .12, lambda: L.sfx_whoosh(.35), .5))
n = int(TOTAL * SR) + SR
sfx = np.zeros(n)
for t0, f, g in ev:
    s = f(); i = int(max(0, t0) * SR); s = s[:n - i]; sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * g
mus = L.music(TOTAL, 112, intro_end=1.2, outro=TOTAL - 1.0)[:n]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(D / 'vo.mp3'), '-ar', str(SR), '-ac', '1', str(D / 'vo48.wav')], check=True)
v, _ = sf.read(D / 'vo48.wav'); voice = np.zeros(n)
for st, (a, b, w) in P:
    c = v[int(a * SR): int((b + .08) * SR)].copy(); fz = int(.01 * SR); c[:fz] *= np.linspace(0, 1, fz); c[-fz:] *= np.linspace(1, 0, fz)
    i = int(st * SR); voice[i:i + len(c)] += c[:n - i]
voice /= np.abs(voice).max()
env = np.convolve(np.abs(voice), np.ones(2400) / 2400, 'same')
duck = np.convolve(1 - .5 * np.clip(env / .05, 0, 1), np.ones(4800) / 4800, 'same')
end = int(TOTAL * SR); fade = np.ones(n); fo = int(1.0 * SR); fade[end - fo:end] = np.linspace(1, 0, fo) ** 1.5; fade[end:] = 0
bed = mus * (duck * fade * .32)[:, None] + (sfx * duck * .16)[:, None]
mix = (bed + voice[:, None])[:end]
sf.write(D / 'mix15_raw.wav', mix, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(D / 'mix15_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.2:LRA=11', '-ar', '48000', str(D / 'audio15.wav')], check=True)
print('ok total', TOTAL)
