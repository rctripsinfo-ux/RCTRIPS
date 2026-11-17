# shared helpers for Shorts built with THE LONG METHOD engine in 9:16 (owner 18 Nov: "Day 4 v3 very good, make 5-8 the same way")
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D = [f"{HERE}/week1/img3", f"{HERE}/week1/img2", f"{HERE}/long03/img", f"{HERE}/week2/img", f"{HERE}/pilot3/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/long01/img"]
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)
def path(n):
    for d in D:
        for f in (f"{d}/{n}_al.png", f"{d}/{n}_c.png", f"{d}/{n}.png"):
            if os.path.exists(f): return f
    raise FileNotFoundError(n)
def wfor(n, h): im = Image.open(path(n)); return h * H * im.width / im.height / W
def act(seq, at=0, until=None, x=0.5, y=0.56, h=0.62, **k): return dict(at=at, until=until, w=wfor(seq[0][0], h), x=x, y=y, poses=[(path(p), a) for p, a in seq], **k)
def fig(n, at=0, until=None, x=0.5, y=0.56, h=0.62, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), **k)
def reps(a, b, n, step, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def loop(a, b, n=12, step=0.35, **k): return act(reps(a, b, n, step), pop=0.02, puppet=False, **k)
def world(n, **k): return dict(at=0, w=wfor(n, 1.0) if wfor(n, 1.0) > 1 else 1.0, x=0.5, y=0.5, asset=path(n), z=-1, puppet=False, breathe=False, **k)
def mini(n, side="r"): return dict(at=0, w=wfor(n, 0.3), x=0.8 if side == "r" else 0.2, y=0.74, asset=path(n), enter=(f"corner_{side}", 0.25), z=3)
def kin(at, text, x=0.5, y=0.12, size=120, color=INK, until=None, frm="l", **k): return dict(at=at, text=text, x=x, y=y, size=size, color=color, until=until, maxw=0.9, **{"from": frm}, **k)
DRIFT = [(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]
HOOK = [(0, 1.6, .5, .45), (0.35, 1.0, .5, .5), ("E", 1.05, .5, .5)]
def S_(text, layers, kinetic=(), tr="cut", **k): return dict(text=text, poses=[], tr=tr, layers=layers, kinetic=list(kinetic), keys=k.pop("keys", DRIFT), **k)
def M(text, base, m, side="r", **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m, side)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)], **k)
def plan(day, S, tag="v3"):
    return dict(dir=f"{HERE}/scenes_d{day:02d}{tag}", words=f"{HERE}/voice/day{day:02d}_cut.words.json", voice=f"{HERE}/voice/day{day:02d}_cut.wav",
                music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=TINT, scenes=S,
                cap_mode="build", cap_words=3, cap_size=58, cap_stroke=6, cap_y=0.9, cap_mini=(185, 168, 255),
                lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
