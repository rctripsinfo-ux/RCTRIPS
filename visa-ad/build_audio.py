"""Voice (Kokoro), music and SFX for the visa ad. Writes out/voice.wav, out/audio.wav and timeline.js."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

HERE = Path(__file__).parent
OUT = HERE / 'out'; OUT.mkdir(exist_ok=True)
SR = 48000
VOICE, SPEED = 'af_heart', 1.06

# (id, lead-in before first cue, gap after scene) ; cues = (name, text, gap after)
SCENES = [
    ('hook', .25, [('h1', 'Your passport is ready.', .25), ('h2', 'But is your visa?', .0)], .45),
    ('nums', .0, [('n1', 'Eleven destinations.', .12), ('n2', 'Five visa types.', .12), ('n3', 'One expert team.', .0)], .4),
    ('stamps', .0, [('us', 'U.S.A.', .1), ('uk', 'U.K.', .1), ('ca', 'Canada.', .1),
                    ('sch', 'Schengen.', .08), ('sch2', 'Thirty countries, one visa.', .14),
                    ('jp', 'Japan.', .08), ('cn', 'China.', .08), ('tr', 'Turkey.', .08), ('tw', 'Taiwan.', .08),
                    ('sg', 'Singapore.', .08), ('au', 'Australia.', .08), ('nz', 'And New Zealand.', .0)], .55),
    ('types', .0, [('t0', 'Whatever the trip.', .1), ('t1', 'Tourist.', .04), ('t2', 'Business.', .04), ('t3', 'Family.', .04),
                   ('t4', 'E visa.', .04), ('t5', 'or M visa.', .0)], .45),
    ('proc', .0, [('p1', 'We check your documents,', .06), ('p2', 'fill every form,', .06), ('p3', 'and book your appointment.', .0)], .45),
    ('cta', .0, [('c1', 'Red Carpet Tours.', .15), ('c2', 'Your visa, sorted.', .15), ('c3', 'Apply today.', .0)], 2.0),
]


def trim(a, thr=.012):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a
    return a[max(0, idx[0] - 600): idx[-1] + 2400]


def tts():
    from kokoro_onnx import Kokoro
    k = Kokoro(str(HERE / 'models/kokoro.onnx'), str(HERE / 'models/voices.bin'))
    clips = {}
    for _, _, cues, _ in SCENES:
        for name, text, _ in cues:
            a, sr = k.create(text, voice=VOICE, speed=SPEED, lang='en-us')
            a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)  # 24k -> 48k
            clips[name] = trim(a.astype(np.float32))
    return clips


def layout(clips):
    t, tl, placed = 0.0, {'cues': {}, 'scenes': {}}, []
    for sid, lead, cues, tail in SCENES:
        start = t; t += lead
        for name, _, gap in cues:
            d = len(clips[name]) / SR
            tl['cues'][name] = [round(t, 3), round(d, 3)]
            placed.append((t, clips[name])); t += d + gap
        t += tail
        tl['scenes'][sid] = [round(start, 3), round(t, 3)]
    tl['total'] = round(t, 3)
    return tl, placed


# ---------------- synthesis helpers ----------------
def env(n, a=.002, r=.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)


def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
rng = np.random.default_rng(7)
def noise(n): return rng.standard_normal(n)


def sfx_stamp():  # rubber stamp: wooden thud + paper slap
    n = int(.45 * SR); t = np.arange(n) / SR
    thud = np.sin(2 * np.pi * (95 * t + 40 * (1 - np.exp(-t * 30)) / 30)) * env(n, .001, .07)
    slap = bp(noise(n), 900, 5000) * env(n, .0005, .018)
    body = lp(noise(n), 400) * env(n, .001, .05)
    return .9 * thud + .55 * slap + .5 * body


def sfx_whoosh(d=.45):
    n = int(d * SR); t = np.arange(n) / SR
    x = noise(n); e = np.sin(np.pi * t / d) ** 2
    lo = lp(x, 900) * e; hi = bp(x, 1500, 6000) * e * np.linspace(.2, 1, n)
    return .6 * lo + .35 * hi


def sfx_type():  # typewriter key
    n = int(.08 * SR)
    return bp(noise(n), 1800, 7000) * env(n, .0003, .006) + .4 * lp(noise(n), 500) * env(n, .0005, .012)


def sfx_ding():
    n = int(1.0 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * w for f, w in ((2093, .5), (4186, .2), (2637, .25))) * env(n, .001, .25)


def sfx_paper(d=.35):
    n = int(d * SR); t = np.arange(n) / SR
    crk = bp(noise(n), 2000, 8000) * (rng.random(n) > .985) * 3
    return (bp(noise(n), 700, 5000) * .4 + crk) * np.sin(np.pi * t / d)


def sfx_tick():
    n = int(.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1600 * t) * env(n, .0005, .02) * .6 + bp(noise(n), 3000, 9000) * env(n, .0003, .006)


def sfx_marker(d=.3):
    n = int(d * SR); t = np.arange(n) / SR
    return bp(noise(n), 2500, 9000) * (.6 + .4 * np.sin(2 * np.pi * 22 * t)) * np.sin(np.pi * t / d) * .5


def sfx_impact():
    n = int(1.4 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (48 * t + 60 * (1 - np.exp(-t * 18)) / 18)) * env(n, .001, .35)
    return boom + lp(noise(n), 2500) * env(n, .001, .08) * .5


def sfx_riser(d=1.2):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(bp(noise(n), 300 + 200 * k, 900 + 600 * k) for k in range(3))
    return x * (t / d) ** 2.2 * .5


# ---------------- music: warm travel pulse, 112 bpm ----------------
def music(total, bpm=112, intro_end=3.6, outro=None):
    n = int((total + 1) * SR); out = np.zeros((n, 2))
    beat = 60 / bpm; bar = beat * 4
    # Bb major-ish progression: I - V - vi - IV  (in A: A E F#m D)
    prog = [(57, [57, 61, 64]), (52, [52, 56, 59, 64]), (54, [54, 57, 61]), (50, [50, 54, 57, 62])]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def add(sig, t0, gain=1., pan=0.):
        i = int(t0 * SR)
        if i >= n: return
        s = sig[:n - i] * gain
        out[i:i + len(s), 0] += s * (1 - pan) ; out[i:i + len(s), 1] += s * (1 + pan)
    kick_n = int(.4 * SR); tk = np.arange(kick_n) / SR
    kick = np.sin(2 * np.pi * (50 * tk + 120 * (1 - np.exp(-tk * 35)) / 35)) * env(kick_n, .001, .16)
    hat = hp(noise(int(.05 * SR)), 7000) * env(int(.05 * SR), .0005, .012)
    shk = bp(noise(int(.09 * SR)), 5000, 11000) * np.sin(np.linspace(0, np.pi, int(.09 * SR)))
    clap = bp(noise(int(.2 * SR)), 1000, 4000) * env(int(.2 * SR), .001, .05)
    nb = int(total / bar) + 2
    for b in range(nb):
        t0 = b * bar; root, ch = prog[b % 4]
        intro = t0 < intro_end or (outro is not None and t0 >= outro)
        # pad
        dn = int(bar * SR) + 2400; tt = np.arange(dn) / SR
        pad = sum(np.sin(2 * np.pi * hz(m) * tt + .4 * np.sin(2 * np.pi * .3 * tt)) +
                  .5 * np.sin(2 * np.pi * hz(m) * 2.003 * tt) for m in ch)
        pad *= np.minimum(1, tt / .25) * np.minimum(1, (dn / SR - tt) / .3)
        add(lp(pad, 1800), t0, .035)
        for q in range(4):
            tb = t0 + q * beat
            if not intro or q == 0:
                add(kick, tb, .55)
            if not intro:
                add(hat, tb + beat / 2, .18, .3)
                for s in range(4): add(shk, tb + s * beat / 4, .07 if s % 2 else .04, -.3)
                if q in (1, 3): add(clap, tb, .18)
            # bass (offbeat pulse)
            bn = int(beat / 2 * SR); tb_ = np.arange(bn) / SR
            bass = np.tanh(1.5 * np.sin(2 * np.pi * hz(root - 12) * tb_)) * env(bn, .005, .18)
            add(lp(bass, 600), tb + beat / 2, .22 if not intro else .1)
        # pluck arpeggio (16ths) after the hook
        if not intro:
            arp = ch + [ch[0] + 12, ch[1] + 12]
            for s in range(16):
                m = arp[(s * 3) % len(arp)] + 12
                pn = int(.25 * SR); tp = np.arange(pn) / SR
                pl = (np.sin(2 * np.pi * hz(m) * tp) + .3 * np.sin(2 * np.pi * hz(m) * 2 * tp)) * env(pn, .001, .07)
                add(pl, t0 + s * beat / 4, .05, .4 if s % 2 else -.4)
    return out


BPM = 112
# music-only cut: cue start positions in beats (cuts land on the beat), duration in beats
BEATS = {'h1': (.5, 2), 'h2': (3, 2.4), 'n1': (6, 2.6), 'n2': (9, 2.6), 'n3': (12, 2.6),
         'us': (16, 1.6), 'uk': (18, 1.6), 'ca': (20, 1.6), 'sch': (22, 1), 'sch2': (23, 2.6), 'jp': (26, 1.6), 'cn': (28, 1.6),
         'tr': (30, 1.6), 'tw': (32, 1.6), 'sg': (34, 1.6), 'au': (36, 1.6), 'nz': (38, 1.6),
         't0': (40, 2), 't1': (42.5, 1.2), 't2': (44, 1.2), 't3': (45.5, 1.2), 't4': (47, 1.2), 't5': (48.5, 1.6),
         'p1': (52, 2), 'p2': (54.5, 2), 'p3': (57, 2), 'c1': (60, 2), 'c2': (62.5, 2.4), 'c3': (65.5, 2)}
BSCENES = {'hook': (0, 6), 'nums': (6, 16), 'stamps': (16, 40), 'types': (40, 52), 'proc': (52, 60), 'cta': (60, 72)}


def beat_timeline():
    b = 60 / BPM
    return {'cues': {k: [round(s * b, 3), round(d * b, 3)] for k, (s, d) in BEATS.items()},
            'scenes': {k: [round(s * b, 3), round(e * b, 3)] for k, (s, e) in BSCENES.items()},
            'total': round(72 * b, 3)}


def main():
    global OUT
    music_only = '--music' in sys.argv
    if music_only:
        OUT = HERE / 'out' / 'music'; OUT.mkdir(parents=True, exist_ok=True)
        tl, placed = beat_timeline(), []
    else:
        clips = tts()
        tl, placed = layout(clips)
    total = tl['total']; n = int(total * SR) + SR
    voice = np.zeros(n)
    for t0, a in placed:
        i = int(t0 * SR); voice[i:i + len(a)] += a
    voice = hp(voice, 80)
    voice /= np.abs(voice).max() + 1e-9 if placed else 1
    sf.write(OUT / 'voice.wav', voice, SR)

    C = tl['cues']; S = tl['scenes']; ev = []
    E = lambda t, f, g: ev.append((t, f, g))
    E(.0, sfx_whoosh, .55); E(.05, sfx_impact, .45)                  # globe + plane
    E(C['h2'][0] - .2, sfx_whoosh, .4)
    for j in range(5): E(C['h2'][0] + .1 + j * .09, sfx_type, .45)    # typing 'visa?'
    E(C['h2'][0] + C['h2'][1] - .15, sfx_stamp, .7)                  # ? badge
    E(S['nums'][0] - .2, sfx_whoosh, .6)
    for k in ('n1', 'n2', 'n3'):
        E(C[k][0] - .05, sfx_impact, .4)
        for j in range(3): E(C[k][0] + .06 * (j + 1), sfx_tick, .25)   # echo ghosts
    E(S['stamps'][0] - .35, sfx_whoosh, .6)
    for k in ('us', 'uk', 'ca', 'sch', 'jp', 'cn', 'tr', 'tw', 'sg', 'au', 'nz'):
        E(C[k][0] + .02, sfx_stamp, .85)
    E(C['sch2'][0] + .1, sfx_marker, .45)
    E(S['types'][0] - .35, sfx_whoosh, .6)
    for k in ('t1', 't2', 't3', 't4', 't5'): E(C[k][0], sfx_paper, .45); E(C[k][0], sfx_tick, .35)
    E(S['proc'][0] - .3, sfx_whoosh, .5)
    E(S['proc'][0], sfx_paper, .6)                                    # paper tear
    for k in ('p1', 'p2', 'p3'):
        E(C[k][0] + .15, sfx_marker, .5); E(C[k][0] + .6, sfx_tick, .4); E(C[k][0] + .62, sfx_ding, .1)
    E(S['cta'][0] - 1.3, sfx_riser, .5); E(S['cta'][0] - .42, sfx_whoosh, .7)
    E(C['c1'][0] - .05, sfx_impact, .5); E(C['c2'][0] + .6, sfx_marker, .4)
    for j in range(11): E(C['c2'][0] + .8 + j * .05, sfx_tick, .2)
    E(C['c3'][0], sfx_stamp, .7); E(C['c3'][0] + .05, sfx_ding, .25)

    sfx = np.zeros(n)
    for t0, f, g in ev:
        s = f(); i = int(max(0, t0) * SR); s = s[:n - i]
        sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * g

    if music_only:
        b = 60 / BPM
        mus = music(total, BPM, intro_end=6 * b - .01, outro=68 * b)[:n]
        # breakdown during the paperwork scene: low-pass sweep, then full drop on the end card
        lo = np.stack([lp(mus[:, 0], 700), lp(mus[:, 1], 700)], 1)
        tt = np.arange(n) / SR; a, z = S['proc'][0], S['cta'][0]
        w = np.clip((tt - a) / .4, 0, 1) * np.clip((z - .1 - tt) / .3, 0, 1)
        mus = mus * (1 - w)[:, None] + lo * 1.3 * w[:, None]
        end = int(total * SR); fo = int(2.2 * SR); fade = np.ones(n); fade[end - fo:end] = np.linspace(1, 0, fo) ** 1.5; fade[end:] = 0
        mix = (mus * fade[:, None] * 1.0 + (sfx * .3)[:, None])[:end]
        sf.write(OUT / 'mix_raw.wav', mix, SR)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'mix_raw.wav'),
                        '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', '48000', str(OUT / 'audio.wav')], check=True)
        (HERE / 'timeline-music.js').write_text('window.TL = ' + json.dumps(tl) + ';\n')
        print(json.dumps(tl['scenes']), 'total', total); return
    mus = music(total)[:n]
    # sidechain duck under voice
    envv = np.convolve(np.abs(voice), np.ones(2400) / 2400, 'same')
    duck = 1 - .55 * np.clip(envv / .08, 0, 1)
    duck = np.convolve(duck, np.ones(4800) / 4800, 'same')
    fade = np.ones(n); fo = int(1.6 * SR); end = int(total * SR)
    fade[end - fo:end] = np.linspace(1, 0, fo); fade[end:] = 0
    mus *= (duck * fade)[:, None]
    mix = mus * .9 + (voice * .95 + sfx * .32)[:, None]
    mix = mix[:end]
    sf.write(OUT / 'mix_raw.wav', mix, SR)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'mix_raw.wav'),
                    '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', '48000', str(OUT / 'audio.wav')], check=True)
    (HERE / 'timeline.js').write_text('window.TL = ' + json.dumps(tl) + ';\n')
    print(json.dumps(tl['scenes']), 'total', total)


if __name__ == '__main__':
    main()
