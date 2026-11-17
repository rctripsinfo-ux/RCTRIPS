# DAY 4 v3 "Which Arm Level Are You?" rebuilt with THE LONG METHOD engine in 9:16:
# the character explains with poses (5 arm-level poses on one canvas, curl reps, triceps flex + red, doorframe pair, level-up montage, mirror),
# kinetic italic words instead of label boxes, pose pop swaps, puppet sway, Mini-H in front, small build captions kept (Shorts).
# usage: LUFS=-14 python3 week1/day04v3_plan.py
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D = [f"{HERE}/week1/img3", f"{HERE}/week1/img2", f"{HERE}/long03/img", f"{HERE}/pilot3/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img"]
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
def mini(n, side="r"): return dict(at=0, w=wfor(n, 0.3), x=0.8 if side == "r" else 0.2, y=0.74, asset=path(n), enter=(f"corner_{side}", 0.25), z=3)
def kin(at, text, x=0.5, y=0.12, size=120, color=INK, until=None, frm="l", **k): return dict(at=at, text=text, x=x, y=y, size=size, color=color, until=until, maxw=0.9, **{"from": frm}, **k)
DRIFT = [(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]
def S_(text, layers, kinetic=(), tr="cut", **k): return dict(text=text, poses=[], tr=tr, layers=layers, kinetic=list(kinetic), keys=k.pop("keys", DRIFT), **k)
def M(text, base, m, **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)], **k)
def level(text, n, name, pose, extra=()):
    return S_(text, [act([(pose, 0)] + list(extra))], [kin(0, f"LEVEL {n}", 0.5, 0.09, 90, TEAL), kin("the", name, 0.5, 0.16, 110, RED if n in (1, 5) else INK)],
              sfx=[(0, "pop", .3)])

S = [
 S_("Every arm on Earth fits one of five levels.", [act([("lv1", 0), ("lv2", "arm"), ("lv3", "Earth"), ("lv4", "fits"), ("lv5", "five")])],
    [kin("five", "5 LEVELS", 0.5, 0.12, 150, RED)], keys=[(0, 1.6, .5, .45), (0.35, 1.0, .5, .5), ("E", 1.05, .5, .5)], shake=[("levels.", .04)],
    sfx=[(0, "whoosh_big", .2), ("five", "pop", .3)]),
 S_("Find yours.", [act([("g_point", 0)])], [kin(0, "FIND YOURS.", 0.5, 0.12, 130)], keys=DRIFT + [("yours.", 1.04, .5, .45), ("yours.+0.1", 1.1, .5, .4)]),
 M("Can we skip the first one?", [act([("lv1", 0)], x=0.4)], "mini_shy_cut"),
 level("Level one, the noodle.", 1, "THE NOODLE", "lv1"),
 level("Level two, the beginner bump.", 2, "BEGINNER BUMP", "lv2"),
 level("Level three, the sleeve-filler.", 3, "SLEEVE-FILLER", "lv3"),
 level("Level four, the shirt-stretcher.", 4, "SHIRT-STRETCHER", "lv4"),
 S_("Level five, the doorframe problem.", [act([("lv5", 0), ("d4_door", "doorframe"), ("d4_door_b", "problem.")], h=0.72, y=0.55)],
    [kin(0, "LEVEL 5", 0.5, 0.06, 90, TEAL), kin("the", "DOORFRAME PROBLEM", 0.5, 0.12, 100, RED, stroke=8)], shake=[("problem.", .03)], sfx=[(0, "pop", .3), ("problem.", "whoosh_short", .3)]),
 M("I'm at one point five.", [act([("lv1", 0), ("lv2", "point"), ("lv1", "five.")], x=0.4)], "mini_laugh_cut", kinetic=[kin("one", "1.5", 0.5, 0.12, 160, RED)]),
 S_("Most guys get stuck at three because they only curl.", [act([("lv3", 0)] + reps("curl_a", "curl_b", 6, 0.35, 1.6), h=0.6)],
    [kin("stuck", "STUCK AT 3", 0.5, 0.1, 120, INK, until="only"), kin("only", "ONLY CURLS", 0.5, 0.1, 120, RED)], sfx=[("only", "pop", .3)]),
 S_("The back of the arm is two-thirds of the size.", [act([("tri", 0)], highlight=dict(base=path("tri"), asset=path("tri_red"), at="back"))],
    [kin("back", "THE BACK", 0.5, 0.1, 120, INK, until="two-thirds"), kin("two-thirds", "2/3 OF YOUR ARM", 0.5, 0.1, 110, RED)],
    keys=DRIFT + [("two-thirds", 1.04, .5, .5), ("two-thirds+0.1", 1.12, .45, .42)], sfx=[("back", "pop", .3), ("two-thirds", "pop", .3)]),
 S_("Train both, and add one rep a week.", [act([("g_two", 0), ("curl_b", "and"), ("tri_red", "add"), ("g_thumbs", "week.")])],
    [kin("both,", "TRAIN BOTH", 0.5, 0.1, 120, TEAL, until="add"), kin("add", "+1 REP / WEEK", 0.5, 0.1, 120, RED)], particles=[dict(at="week.", x=0.5, y=0.2, spread=0.4)],
    sfx=[("both,", "pop", .3), ("add", "pop", .3)]),
 S_("Levels change.", [act([("lv1", 0), ("lv2", 0.15), ("lv3", 0.3), ("lv4", 0.45), ("lv5", 0.6)])], [kin(0, "LEVELS CHANGE", 0.5, 0.12, 120, TEAL)],
    sfx=[(0, "whoosh_short", .3)]),
 S_("Mirrors don't lie, but they do update.", [fig("prop_mirror", x=0.68, y=0.5, h=0.62, puppet=False, breathe=False), act([("g_cross", 0), ("g_flex", "update.")], x=0.3, h=0.55),
    dict(at=0, w=wfor("lv1", 0.42), x=0.68, y=0.5, poses=[(path("lv1"), 0), (path("lv5"), "update.")], flip=True, alpha=0.5, puppet=False)],
    [kin("lie,", "MIRRORS DON'T LIE", 0.5, 0.1, 100, INK, until="update."), kin("update.", "THEY UPDATE", 0.5, 0.1, 120, TEAL)], particles=[dict(at="update.", x=0.68, y=0.2, spread=0.25)],
    sfx=[("update.", "chime", .4)]),
 M("What level are you right now? Comment the number.", [act([("g_point", 0)], x=0.4)], "s9_mini_point_cut",
   kinetic=[kin("level", "YOUR LEVEL?", 0.5, 0.1, 130, INK, until="Comment"), kin("Comment", "COMMENT 1-5", 0.5, 0.1, 130, RED)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d04v3", words=f"{HERE}/voice/day04_cut.words.json", voice=f"{HERE}/voice/day04_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=TINT, scenes=S,
            cap_mode="build", cap_words=3, cap_size=58, cap_stroke=6, cap_y=0.9, cap_mini=(185, 168, 255),
            lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/day04_v3.mp4")
