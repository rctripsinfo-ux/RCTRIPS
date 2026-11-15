# shared helpers for the week-1 plans (Day 2-7), approved Pilot 3 style + stronger hooks
import os, glob, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
DIRS = [f"{HERE}/week1/img", f"{HERE}/pilot3/img", f"{HERE}/pilot2/img"]
SLATE, SLATE_NUM = (75, 85, 104), (104, 116, 138)

def img(name):
    for d in DIRS:
        f = f"{d}/{name}.png"
        if os.path.exists(f): return f
    raise FileNotFoundError(name)

def full(name, at=0, w=0.82, y=0.58, **k):  # Codex picture on white, a little smaller than the frame: the top stays free for labels
    return dict(at=at, w=w, x=0.5, y=y, asset=img(name), **k)

def body(name, at=0, w=0.34, x=0.5, y=0.58, **k):  # cut-out figure for line-ups
    return dict(at=at, w=w, x=x, y=y, asset=img(name), **k)

def mini(name, side="r", until=None):  # Mini-H cameo from a bottom corner, everything behind blurs
    return dict(at=0, until=until, w=0.36, x=0.78 if side == "r" else 0.22, y=0.76, asset=img(name), enter=(f"corner_{side}", 0.4), z=3, focus=True)

def lab(at, text, x=0.5, y=0.14, until=None, **k): return dict(at=at, text=text, x=x, y=y, until=until, **k)

def stack(items, x=0.5, y0=0.1, dy=0.07):  # list of labels dropping one under the other
    return [lab(a, t, x, y0 + i * dy) for i, (a, t) in enumerate(items)]

def punch(at, z0, z1, f=(.5, .5)): return [(at, z0, *f), (f"{at}+0.1", z1, *f)]

def hook_keys(f=(.5, .5), end=1.05):  # frame 1 = 2x blurred close-up snapping out in 0.35 s, then a slow push-in
    return [(0, 1.9, *f), (0.35, 1.0, .5, .5), ("E", end, .5, .5)]

def card(text, num, label, tr):
    return dict(text=text, poses=[], tr=tr, d=0.3, set=SLATE, nocap=True, sfx=[(0, "whoosh_short", .3)],
                bgwords=[dict(text=num, at=-0.5, x=0.5, y=0.4, size=640, color=SLATE_NUM, cps=0.001)],
                labels=[dict(text=label, at=0.12, x=0.5, y=0.6, size=62)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .45)])

def plan(day, scenes):
    return dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/day{day:02d}_cut.words.json", voice=f"{HERE}/voice/day{day:02d}_cut.wav",
                music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=(255, 255, 255),
                scenes=scenes, cap_mode="build", cap_words=3, cap_size=62, cap_stroke=6, cap_y=0.8, cap_mini=(185, 168, 255),
                lead=0.06, tail=0.8, keywords=[], breathe=True)

# ---- v2: pose animation (owner 15 Nov: every scene acts with several poses) ----
A2 = f"{HERE}/week1/img2"
def G(name): return f"{A2}/{name}_al.png"          # aligned cut-out on its base canvas (gesture library / topic pairs)
def act(seq, at=0, until=None, w=0.82, x=0.5, y=0.58, **k):
    """one H layer that changes pose on the words: seq = [(pose, anchor), ...]; poses share one canvas so swaps stay in place"""
    return dict(at=at, until=until, w=w, x=x, y=y, poses=[(G(p) if not p.startswith("/") and "_" in p and not p.startswith("hero_") else p, a) for p, a in seq], **k)
