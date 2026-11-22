# SHORT 10 "Can You Do 40 Push-Ups?" 9:16 (self-test format = best retention in analytics; push-ups = best topic)
# the character explains with poses (5 arm-level poses on one canvas, curl reps, triceps flex + red, doorframe pair, level-up montage, mirror),
# kinetic italic words instead of label boxes, pose pop swaps, puppet sway, Mini-H in front, small build captions kept (Shorts).
# usage: LUFS=-14 python3 short10/short10_plan.py
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D = [f"{HERE}/short10/img", f"{HERE}/long03/img", f"{HERE}/long09/img", f"{HERE}/week1/img2", f"{HERE}/long03/img", f"{HERE}/pilot3/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img"]
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
S = [
 S_("Drop and do as many push-ups as you can.", [PU(16, 0.16, 0.2, h=0.34, y=0.55)],
    counters=[dict(at=0.3, a=0, b=12, dur=2.2, x=0.5, y=0.18, size=230, color=NAVY, stroke=8)], keys=[(0, 1.5, .5, .55), (0.35, 1.0, .5, .5), ("E", 1.06, .5, .5)],
    sfx=[(0, "whoosh_big", .2)]),
 S_("That number says more about your heart than your arms.", [act([("h_heart", 0)], x=0.5, y=0.6, h=0.62), IC("i_heart_c", "heart", 0.8, 0.3, 0.12, z=3)],
    [N("heart", "YOUR HEART", 0.5, 0.14, 140, RED)], keys=DRIFT + [("heart", 1.05, .5, .45), ("heart+0.15", 1.18, .5, .42)], shake=[("heart", .02)], sfx=POP("heart")),
 S_("Harvard researchers followed over a thousand men for ten years.", [IC("i_paper_c", 0, 0.3, 0.3, 0.2), IC("i_helmet_c", "thousand", 0.72, 0.3, 0.14)],
    [N("thousand", "1,100 MEN", 0.5, 0.5, 140), N("ten", "10 YEARS", 0.5, 0.62, 140, LTEAL)], sfx=POP(0, "thousand", "ten")),
 S_("Men who could do forty push-ups had ninety-six percent fewer heart problems than men who couldn't do ten.",
    [act([("pu_top", 0)] + reps("pu_bot", "pu_top", 10, 0.3, 0.3), x=0.5, y=0.45, h=0.3, until="than"), act([("pu_bot_tired", 0)], x=0.5, y=0.45, h=0.3, at="than", shiver=[("than", "ten.")])],
    [N("forty", "40+", 0.5, 0.3, 150, LTEAL, until="than"), N("ninety-six", "-96%", 0.5, 0.16, 190, LTEAL), N("than", "<10", 0.5, 0.3, 150, RED)],
    bars=[dict(at="fewer", x=0.5, y=0.72, w=0.5, h=0.1, values=[4, 100], labels=["40+", "<10"], stagger=0.5, show_values=False, color=(150, 160, 170), hi_last=False)],
    sfx=POP("forty", "ninety-six", "than")),
 M("I stopped at twelve.", [act([("pu_bot_tired", 0)], x=0.45, y=0.45, h=0.26)], "mini_shy_cut", kinetic=[N("twelve.", "12", 0.5, 0.18, 230, RED)]),
 S_("Here's your level.", [act([("g_point", 0)], x=0.5, y=0.6, h=0.62)], [N(0, "YOUR LEVEL?", 0.5, 0.14, 150)], sfx=POP(0)),
 S_("Under ten: start here. Ten to twenty: average. Twenty to forty: strong. Forty plus: elite.",
    [act([("pu_bot_tired", 0), ("pu_top", "Ten"), ("pu_top", "Twenty")] + reps("pu_bot", "pu_top", 8, 0.18, 6.3), x=0.5, y=0.67, h=0.2), IC("i_medal_c", "elite.", 0.8, 0.12, 0.1)],
    [N("Under", "UNDER 10: START", 0.5, 0.52, 92, RED), N("Ten", "10-20: AVERAGE", 0.5, 0.42, 92, INK), N("Twenty", "20-40: STRONG", 0.5, 0.32, 92, LTEAL), N("Forty", "40+: ELITE", 0.5, 0.2, 110, NAVY)],
    sfx=POP("Under", "Ten", "Twenty") + [("elite.", "chime", .5)], particles=[dict(at="elite.", x=0.75, y=0.2, spread=0.2)]),
 S_("It's a test, not a diagnosis.", [act([("p_wag", 0)], x=0.32, y=0.6, h=0.62), IC("i_steth_c", "diagnosis.", 0.74, 0.45, 0.2)], [N("test,", "A TEST", 0.5, 0.14, 150)], sfx=POP("diagnosis.")),
 S_("Add two push-ups a week, and comment your number.", [PU(14, 0.26, 0.2, h=0.34, y=0.55)],
    [N("two", "+2 / WEEK", 0.5, 0.18, 150, LTEAL), N("comment", "COMMENT YOUR NUMBER", 0.5, 0.3, 90)], sfx=POP("two", "comment")),
]
PLAN = dict(dir=f"{HERE}/scenes_s10", words=f"{HERE}/voice/short10_cut.words.json", voice=f"{HERE}/voice/short10_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=16, sfx_db=14, duck=False, set=TINT, scenes=S,
            cap_mode="build", cap_swipe=True, cap_words=2, cap_size=96, cap_y=0.8, cap_color=(255, 255, 255), cap_mini=(255, 255, 255), cap_stroke=8,
            cap_stroke_fill=(20, 22, 28), cap_font=f"{HERE}/fonts/anton.woff2", cap_upper=True, cap_gap=10,
            lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/short10.mp4")
