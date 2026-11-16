# LONG 02 DEMO: the new long-form system (research/LONGFORM-24-ANALYSIS-AND-PLAN.md, D6).
# Pale-teal set, world backdrops, dip / grey-out transitions, pose in-betweens, puppet sway, insets that grow from the body,
# kinetic italic words (no boxes), counters / stopwatch / calendar / bars, dark-red section cards, no burned captions.
# usage: LUFS=-14 python3 long02/long02_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D2, L1, W1, P2, A2 = (f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
HD = os.path.expanduser("~/reel-engine-tool/public/library/hero")
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{A2}/{n}_al.png", f"{W1}/{n}.png", f"{P2}/{n}.png", f"{HD}/{n}.png"):
        if os.path.exists(f): return f
    raise FileNotFoundError(n)
def wfor(n, h): im = Image.open(path(n)); return h * H * im.width / im.height / W
def fig(n, at=0, until=None, x=0.27, y=0.52, h=0.9, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), **k)
def act(seq, at=0, until=None, x=0.25, y=0.52, h=0.92, **k): return dict(at=at, until=until, w=wfor(seq[0][0], h), x=x, y=y, poses=[(path(p), a) for p, a in seq], **k)
def reps(a, b, n, step, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def pu(n=10, step=0.5, x=0.36, y=0.6, h=1.45, **k): return act(reps("hero_pushup_pair_a", "hero_pushup_pair_b", n, step), x=x, y=y, h=h, **k)
def pair(a, b, n=10, step=0.55, x=0.4, y=0.55, h=0.85, **k): return act(reps(a, b, n, step), x=x, y=y, h=h, **k)
def world(n, **k): return dict(at=0, w=1.0, x=0.5, y=0.5, asset=path(n), z=-1, **k)
def mini(n): return dict(at=0, w=wfor(n, 0.6), x=0.88, y=0.68, asset=path(n), enter=("corner_r", 0.3), z=3)
def kin(at, text, x=0.72, y=0.3, size=110, color=INK, until=None, frm="l", **k): return dict(at=at, text=text, x=x, y=y, size=size, color=color, until=until, **{"from": frm}, **k)
def card(text, big, small, tr="cut"):
    return dict(text=text, poses=[], set=RED, tr=tr, nocap=True, kinetic=[kin(0, big, 0.5, 0.42, 190, WHITE), kin(0.15, small, 0.5, 0.62, 70, (240, 200, 200), frm="b")],
                keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_short", .3)])
def M(text, base, m): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)])
DRIFT = [(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]

S = [
 # ---- HOOK ----
 dict(text="One hundred push-ups. Every day. For thirty days.", poses=[], layers=[world("W_living"), pu(10, 0.45)],
      counters=[dict(at="hundred", a=0, b=100, dur=0.9, x=0.74, y=0.72, size=190, color=INK, label="PUSH-UPS", stroke=8)],
      kinetic=[kin("thirty", "x 30 DAYS", 0.74, 0.93, 90, RED, stroke=8)],
      keys=[(0, 1.35, .4, .6), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_big", .2), ("hundred", "pop", .3), ("thirty", "pop", .3)]),
 dict(text="That's three thousand push-ups.", poses=[], tr="dip", d=0.5, layers=[act([("g_shock", 0)], x=0.2)],
      calendars=[dict(at=0, x=0.55, y=0.55, w=0.48, cols=10, n=30, ticks=[("three", 30)])], kinetic=[kin("thousand", "3,000", 0.55, 0.17, 120, RED)],
      keys=DRIFT, sfx=[("thousand", "pop", .3)]),
 M("You can't even do twenty.", [act([("g_shock", 0)], x=0.2)], "mini_laugh_cut") | dict(calendars=[dict(at=0, x=0.55, y=0.55, w=0.48, cols=10, n=30, ticks=[(-5, 30)])]),
 dict(text="Exactly. So on day one, I tested my max.", poses=[], tr="dip", d=0.5, layers=[act([("g_thumbs", 0), ("g_one", "day"), ("g_point", "tested")])],
      kinetic=[kin("max.", "MAX TEST", 0.68, 0.4, 130)], keys=DRIFT + [("max.", 1.05, .5, .5), ("max.+0.1", 1.1, .45, .5)], sfx=[("max.", "pop", .3)]),
 dict(text="Twenty-two. Then my arms quit.", poses=[], tr="cut", layers=[world("W_living"), pu(4, 0.3, until="quit."), fig("H_collapse", at="quit.", x=0.4, y=0.72, h=0.3, enter=("drop", 0.25))],
      counters=[dict(at=0, a=0, b=22, dur=0.7, x=0.8, y=0.8, size=200, color=RED, label="MAX", stroke=8)], shake=[("quit.", .05)],
      keys=DRIFT, sfx=[(0.7, "pop", .3), ("quit.", "whoosh_short", .3)]),
 dict(text="But the hard part wasn't day one. It was day two.", poses=[], tr="cut", layers=[act([("g_think", 0), ("g_point", "day#2")])],
      kinetic=[kin("day#2", "DAY 2", 0.68, 0.42, 180, RED)], keys=DRIFT + [("day#2", 1.05, .5, .5), ("day#2+0.1", 1.12, .45, .45)], sfx=[("day#2", "pop", .3)]),
 # ---- DAY 1 ----
 card("Day one.", "DAY 1", "THE PLAN"),
 dict(text="I split the hundred into five sets of twenty. Morning, lunch, afternoon, evening, and one angry set before bed.", poses=[], tr="cut",
      layers=[act([("g_palm", 0), ("g_two", "five"), ("g_point", "Morning"), ("g_cross", "angry")], x=0.18)],
      kinetic=[kin("five", "5 x 20", 0.6, 0.15, 110)],
      bars=[dict(at="Morning", x=0.62, y=0.8, w=0.56, h=0.45, values=[20, 20, 20, 20, 20], labels=["AM", "LUNCH", "PM", "EVE", "BED"], stagger=0.62, hi_last=True, show_values=False)],
      keys=DRIFT, sfx=[("five", "pop", .3), ("angry", "pop", .3)]),
 M("The angry set is my favourite.", [act([("g_cross", 0)], x=0.18)], "mini_laugh_cut") | dict(bars=[dict(at=-5, x=0.62, y=0.8, w=0.56, h=0.45, values=[20] * 5, labels=["AM", "LUNCH", "PM", "EVE", "BED"], stagger=0, hi_last=True, show_values=False)]),
 dict(text="Total time? Eleven minutes. It felt easy. Too easy.", poses=[], tr="dip", d=0.5, layers=[act([("g_think", 0), ("g_thumbs", "Eleven"), ("g_shrug", "Too")])],
      rings=[dict(at="Eleven", x=0.66, y=0.45, r=0.24, dur=0.9, max=11, unit="MIN")], kinetic=[kin("Too", "TOO EASY", 0.66, 0.86, 80, RED)],
      keys=DRIFT, sfx=[("Eleven", "pop", .3), ("Too", "pop", .3)]),
 # ---- DAY 2 ----
 card("Day two.", "DAY 2", "THE PAIN"),
 dict(text="I woke up, reached for my phone, and my chest said no.", poses=[], tr="cut", layers=[world("H_bed_phone")],
      kinetic=[kin("no.", "NO.", 0.8, 0.2, 170, RED)], keys=[(0, 1.12, .3, .65), ("chest", 1.12, .55, .45), ("E", 1.2, .55, .45)], shake=[("no.", .04)],
      sfx=[("no.", "pop", .3)]),
 dict(text="That's normal muscle soreness. It peaks one to two days after something new, then it fades.", poses=[], tr="dip", d=0.5,
      layers=[fig("L_sore", x=0.18, h=0.85)], kinetic=[kin("soreness.", "SORENESS", 0.62, 0.13, 90)],
      bars=[dict(at="peaks", x=0.64, y=0.82, w=0.5, h=0.5, values=[3, 9, 10, 6, 3, 1], labels=["D1", "D2", "D3", "D4", "D5", "D6"], stagger=0.18, show_values=False, color=TEAL)],
      keys=DRIFT, sfx=[("peaks", "pop", .3), ("fades.", "pop", .3)]),
 M("So pain means growth, right?", [fig("L_sore", x=0.18, h=0.85)], "s6_mini_squint_cut"),
 dict(text="No. Soreness means new. Not growth.", poses=[], tr="cut", layers=[act([("g_cross", 0), ("g_one", "Soreness"), ("g_palm", "Not")])],
      kinetic=[kin("Soreness", "SORE = NEW", 0.66, 0.35, 120, TEAL), kin("Not", "NOT GROWTH", 0.66, 0.58, 120, RED)], keys=DRIFT, sfx=[("Soreness", "pop", .3), ("Not", "pop", .3)]),
 # ---- WEEK 1 ----
 card("By day five,", "WEEK 1", "THE WRISTS"),
 dict(text="the soreness was gone. But my wrists started complaining.", poses=[], tr="cut",
      layers=[act([("g_thumbs", 0)], until="wrists"), fig("L_wrist", at="wrists", x=0.27, h=0.9, enter=("fade", 0.2))],
      kinetic=[kin("gone.", "SORENESS: GONE", 0.68, 0.3, 80, TEAL, until="wrists"), kin("wrists", "THE WRISTS", 0.68, 0.3, 130, RED)], keys=DRIFT, sfx=[("wrists", "whoosh_short", .25)]),
 dict(text="Seven hundred push-ups a week, all on bent wrists.", poses=[], tr="cut", layers=[fig("L_wrist", x=0.2, h=0.9)],
      counters=[dict(at=0, a=0, b=700, dur=1.0, x=0.68, y=0.3, size=170, color=INK, label="PUSH-UPS / WEEK")],
      insets=[dict(at="bent", asset=path("L_wrist"), crop=(0.37, 0.43, 0.32), x=0.68, y=0.72, r=0.09, bg=(255, 255, 255), grow=(0.162, 0.45), mark="x")],
      keys=DRIFT, sfx=[("bent", "pop", .3)]),
 dict(text="The fix took ten seconds. Push-ups on my fists. Wrist straight, pain gone.", poses=[], tr="dip", d=0.5,
      layers=[world("W_living"), pair("L_fist_a", "L_fist_b", 16, 0.55, x=0.42, y=0.62, h=0.75)],
      kinetic=[kin("fists.", "ON YOUR FISTS", 0.5, 0.13, 110, INK, stroke=8)],
      insets=[dict(at="Wrist", asset=path("L_fist_a"), crop=(0.2, 0.74, 0.22), x=0.8, y=0.4, r=0.09, bg=(255, 255, 255), grow=(0.23, 0.8), mark="tick")],
      keys=DRIFT, sfx=[("fists.", "pop", .3), ("Wrist", "pop", .3)]),
 M("Fist push-ups. Very action movie.", [world("W_living"), pair("L_fist_a", "L_fist_b", 6, 0.55, x=0.42, y=0.62, h=0.75)], "mini_laugh_cut"),
 dict(text="And by day seven, my max went from twenty-two to twenty-seven.", poses=[], tr="cut", layers=[act([("g_point", 0), ("g_flex", "twenty-seven.")])],
      bars=[dict(at="from", x=0.66, y=0.82, w=0.32, h=0.55, values=[22, 27], labels=["DAY 1", "DAY 7"], stagger=0.9, hi_last=True, hi_color=TEAL, color=(150, 160, 170))],
      kinetic=[kin("twenty-seven.", "+5", 0.9, 0.45, 130, TEAL)], particles=[dict(at="twenty-seven.", x=0.72, y=0.3, spread=0.3)],
      keys=DRIFT, sfx=[("from", "pop", .3), ("twenty-seven.", "chime", .4)]),
 M("Muscle already?", [act([("g_flex", 0)])], "s6_mini_squint_cut"),
 dict(text="Not yet. That's my brain learning the move. The muscle part comes later.", poses=[], tr="dip", d=0.5,
      layers=[act([("L_brain", 0), ("L_brain_b", "brain"), ("L_brain", "muscle"), ("L_brain_b", "later.")], x=0.27)],
      kinetic=[kin("brain", "BRAIN FIRST", 0.68, 0.32, 120, TEAL), kin("muscle", "MUSCLE: LATER", 0.68, 0.56, 100, RED)],
      keys=DRIFT, sfx=[("brain", "pop", .3), ("muscle", "pop", .3)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long02", words=f"{HERE}/voice/long02_cut.words.json", voice=f"{HERE}/voice/long02_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_xf=0.1)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long02_demo{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
