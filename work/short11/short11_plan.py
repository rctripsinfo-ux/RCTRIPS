# SHORT 11 "The Sit-Down Stand-Up Test" 9:16 (self-test, engagement beats: challenge, pause-and-try, score, comment/like)
# the character explains with poses (5 arm-level poses on one canvas, curl reps, triceps flex + red, doorframe pair, level-up montage, mirror),
# kinetic italic words instead of label boxes, pose pop swaps, puppet sway, Mini-H in front, small build captions kept (Shorts).
# usage: LUFS=-14 python3 short11/short11_plan.py
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D = [f"{HERE}/short11/img", f"{HERE}/short10/img", f"{HERE}/long11/img", f"{HERE}/long03/img", f"{HERE}/long09/img", f"{HERE}/week1/img2", f"{HERE}/long03/img", f"{HERE}/pilot3/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img"]
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

NAVY, LTEAL = (30, 42, 72), (15, 139, 133)
def IC(n, at=0, x=0.75, y=0.4, h=0.18, until=None, **k):  # icon pop (one picture per phrase)
    return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), puppet=False, breathe=False, enter=k.pop("enter", ("pop", 0.22)), **k)
def N(at, text, x=0.5, y=0.14, size=150, color=NAVY, until=None, **k): return kin(at, text, x, y, size, color, until=until, stroke=8, stroke_fill=WHITE, **k)
POP = lambda *a: [(t, "pop", .3) for t in a]
PU = lambda n, step=0.28, t0=0.0, **k: act([("pu_top", 0)] + reps("pu_bot", "pu_top", n, step, t0), **{"h": 0.3, "y": 0.6, **k})
BIG = dict(x=0.5, y=0.6, h=0.62)
def M(text, base, m, **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], **{"sfx": [(0, "pop_soft", .3)], **k})
SC = lambda at, a, b, dur, y=0.16, col=NAVY: dict(at=at, a=a, b=b, dur=dur, x=0.5, y=y, size=230, color=col, label="POINTS", stroke=8)
S = [
 S_("Sit on the floor, then stand back up.", [act([("stand_done", 0), ("sit_cross", "floor,"), ("rise_mid", "stand"), ("stand_done", "up.")], **BIG)],
    keys=[(0, 1.4, .5, .4), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "es_whoosh", .25), ("floor,", "es_thud", .3), ("up.", "es_pop2", .25)]),
 S_("No hands. No knees. Can you do it?", [act([("stand_done", 0)], **BIG)], [N("hands.", "NO HANDS", 0.5, 0.12, 130, RED), N("knees.", "NO KNEES", 0.5, 0.22, 130, RED), N("Can", "CAN YOU?", 0.5, 0.34, 150, NAVY)],
    sfx=[("hands.", "es_pop", .25), ("knees.", "es_pop", .25), ("Can", "es_ding", .2)], keys=DRIFT + [("Can", 1.05, .5, .45)]),
 M("Easy. Watch this... okay, not easy.", [act([("sit_cross", 0), ("rise_mid", "Watch"), ("rise_hand", "okay,")], x=0.42, y=0.6, h=0.55, shiver=[("Watch", "okay,")])], "mini_shy_cut",
   shake=[("okay,", .05)], sfx=[("Watch", "es_grit", .35), ("okay,", "es_fall", .3), ("not", "es_thud", .35), ("easy.", "es_boing", .25)]),
 S_("This is the sit-down stand-up test. Scientists used it on over two thousand adults.", [act([("p_count", 0)], x=0.5, y=0.62, h=0.55), IC("i_paper_c", "Scientists", 0.78, 0.3, 0.12)],
    [N("sit-down", "SIT-DOWN", 0.5, 0.1, 120, NAVY), N("stand-up", "STAND-UP TEST", 0.5, 0.18, 110, TEAL), N("two", "2,000+ ADULTS", 0.3, 0.3, 90, NAVY)],
    sfx=[("sit-down", "es_pop", .25), ("Scientists", "es_pop2", .25)]),
 S_("You start with ten points. Lose one point every time you use a hand, a knee, or your arm.", [act([("sit_cross", 0), ("rise_hand", "hand,")], x=0.5, y=0.68, h=0.46)],
    counters=[SC("ten", 0, 10, 0.6)], kinetic=[N("hand,", "-1 HAND", 0.5, 0.28, 90, RED), N("knee,", "-1 KNEE", 0.5, 0.35, 90, RED), N("arm.", "-1 ARM", 0.5, 0.42, 90, RED)],
    sfx=[("ten", "es_ding", .2), ("hand,", "es_pop", .25), ("knee,", "es_pop", .25), ("arm.", "es_pop", .25)]),
 S_("Pause the video and try it right now. I'll wait.", [act([("p_wag", 0), ("g_think", "I'll")], **BIG)], [N("Pause", "PAUSE & TRY IT", 0.5, 0.14, 120, RED)],
    sfx=[("Pause", "es_click", .4), ("wait.", "es_ticktock2", .35), ("wait.+0.5", "es_ticktock2", .35), ("wait.+1.0", "es_ticktock2", .35)], keys=DRIFT + [("wait.", 1.06, .5, .45)]),
 S_("Got your score? Ten is excellent. Eight or nine is good. Under six, your body is asking for help.", [act([("stand_done", 0), ("g_thumbs", "Eight"), ("rise_hand", "Under")], x=0.5, y=0.68, h=0.48)],
    [N("score?", "YOUR SCORE?", 0.5, 0.1, 120, NAVY, until="Ten"), N("Ten", "10 = EXCELLENT", 0.5, 0.16, 100, TEAL), N("Eight", "8-9 = GOOD", 0.5, 0.26, 100, NAVY), N("Under", "UNDER 6 = HELP", 0.5, 0.36, 100, RED)],
    sfx=[("Ten", "es_ding", .2), ("Eight", "es_pop", .25), ("Under", "es_error", .25)]),
 S_("In the study, the lowest scorers were about five times more likely to die within six years than the highest.", [act([("g_think", 0)], **BIG)],
    [N("five", "5X", 0.5, 0.14, 230, RED), N("six", "WITHIN 6 YEARS", 0.5, 0.28, 90, NAVY)], shake=[("five", .03)], sfx=[("five", "es_impact", .2)]),
 M("I'm starting squats today.", [act([("stand_done", 0)], x=0.42, y=0.6, h=0.55)], "mini_laugh_cut", sfx=[(0, "es_boing", .2)]),
 S_("Good. Squats and lunges raise your score fast. Comment your score, and like if you got a perfect ten.", [act([("g_thumbs", 0), ("g_point", "Comment")], **BIG)],
    [N("Squats", "SQUATS + LUNGES", 0.5, 0.12, 100, TEAL), N("Comment", "COMMENT YOUR SCORE", 0.5, 0.24, 90, NAVY), N("perfect", "10? LIKE!", 0.5, 0.34, 120, RED)],
    sfx=[("Squats", "es_pop", .25), ("Comment", "es_pop", .25), ("perfect", "es_ding", .25)], particles=[dict(at="perfect", x=0.5, y=0.34, spread=0.3)]),
]
PLAN = dict(dir=f"{HERE}/scenes_s11", words=f"{HERE}/voice/short11_cut.words.json", voice=f"{HERE}/voice/short11_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=24, sfx_db=18, duck=True, set=TINT, scenes=S,
            cap_mode="build", cap_swipe=True, cap_words=2, cap_size=96, cap_y=0.8, cap_color=(255, 255, 255), cap_mini=(255, 255, 255), cap_stroke=8,
            cap_stroke_fill=(20, 22, 28), cap_font=f"{HERE}/fonts/anton.woff2", cap_upper=True, cap_gap=10,
            lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/short11.mp4")
