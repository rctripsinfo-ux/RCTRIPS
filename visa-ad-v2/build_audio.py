"""Music + SFX for visa ad v2 (no voice). Uses the synth helpers from ../visa-ad/build_audio.py."""
import sys, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / 'visa-ad'))
import build_audio as L

SR, BPM, TOTAL = L.SR, 112, 37.5
B = 60 / BPM
OUT = HERE / 'out'; OUT.mkdir(exist_ok=True)
ev = []
E = lambda t, f, g: ev.append((t, f, g))
# S1 hook: flag flashes + VISA? stamp
for j in range(20): E(j * .13, L.sfx_tick, .22 if j % 2 else .3)
E(1.3, L.sfx_whoosh, .3); E(1.52, L.sfx_stamp, 1.0); E(1.52, L.sfx_impact, .55)
E(2.85, lambda: L.sfx_whoosh(.6), .6)                       # zoom-through
# S2 problem
for t in (3.35, 3.6): E(t, L.sfx_tick, .22)
E(3.7, L.sfx_paper, .45); E(4.05, L.sfx_marker, .45)
for i in range(4): E(4.15 + i * .42, L.sfx_paper, .4); E(4.15 + i * .42, L.sfx_tick, .3)
E(5.3, lambda: L.sfx_riser(1.1), .45)
E(6.43, L.sfx_stamp, 1.0); E(6.43, L.sfx_impact, .6)
E(6.6, lambda: L.sfx_whoosh(.5), .55)                       # circle reveal
# S3 solution
E(6.95, L.sfx_tick, .35)
for t in (7.2, 7.45, 7.8): E(t, L.sfx_tick, .2)
E(9.0, lambda: L.sfx_whoosh(.5), .5); E(9.35, lambda: L.sfx_whoosh(.6), .6)
# S4 stamps on the beat
E(9.9, L.sfx_tick, .3); E(10.05, L.sfx_tick, .25)
s0 = 10.514
durs = [2.5 if i == 3 else 1.5 for i in range(11)]
for i in range(11):
    st = s0 + sum(durs[:i]) * B; E(st - .02, L.sfx_stamp, .8); E(st - .02, L.sfx_impact, .18)
    if i == 3:
        for j in range(10): E(st + .25 + j * .055, L.sfx_type, .3)
E(19.95, L.sfx_paper, .7); E(19.95, lambda: L.sfx_whoosh(.5), .4)   # page turn
# S5 cards
for i in range(5): E(20.9 + i * .55, lambda: L.sfx_whoosh(.3), .3); E(21.25 + i * .55, L.sfx_ding, .1)
E(25.4, lambda: L.sfx_whoosh(.5), .65)                      # whip
# S6 steps
for i in range(3): E(26.7 + i * 1.25, L.sfx_tick, .4); E(26.75 + i * 1.25, L.sfx_ding, .1)
E(29.6, lambda: L.sfx_riser(1.0), .4); E(30.6, lambda: L.sfx_whoosh(.55), .6)
# S7 CTA
E(30.95, L.sfx_impact, .55); E(31.95, L.sfx_marker, .4)
for i in range(11): E(32.2 + i * .06, L.sfx_tick, .16)
E(33.1, L.sfx_stamp, .5); E(33.15, L.sfx_ding, .2)

n = int(TOTAL * SR) + SR
sfx = np.zeros(n)
for t0, f, g in ev:
    s = f(); i = int(max(0, t0) * SR); s = s[:n - i]; sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * g
mus = L.music(TOTAL, BPM, intro_end=6.4, outro=34.2)[:n]
end = int(TOTAL * SR); fo = int(2.6 * SR); fade = np.ones(n); fade[end - fo:end] = np.linspace(1, 0, fo) ** 1.5; fade[end:] = 0
mix = (mus * fade[:, None] + (sfx * .3)[:, None])[:end]
sf.write(OUT / 'mix_raw.wav', mix, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', '48000', str(OUT / 'audio.wav')], check=True)
print('audio ok')
