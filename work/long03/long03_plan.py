# LONG 03 = DEMO v2 (16:9). Same voice as long02. Fixes every mistake from the frame-by-frame QA of long02 and makes
# the CHARACTER explain: a new acting pose every ~0.6-1 s (all poses on one canvas -> swap in place with a 4-frame pop),
# 5 quick context scenes instead of a bar chart, charts only as small support, Mini-H always in front, cards >= 1.5 s.
# usage: LUFS=-14 python3 long03/long03_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
HD = os.path.expanduser("~/reel-engine-tool/public/library/hero")
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{D3}/{n}_al.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{A2}/{n}_al.png",
              f"{W1}/{n}.png", f"{P2}/{n}.png", f"{HD}/{n}.png"):
        if os.path.exists(f): return f
    raise FileNotFoundError(n)
def wfor(n, h): im = Image.open(path(n)); return h * H * im.width / im.height / W
def fig(n, at=0, until=None, x=0.27, y=0.52, h=0.9, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), **k)
def act(seq, at=0, until=None, x=0.24, y=0.52, h=0.92, **k): return dict(at=at, until=until, w=wfor(seq[0][0], h), x=x, y=y, poses=[(path(p), a) for p, a in seq], **k)
def reps(a, b, n, step, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def pu(n=10, step=0.4, x=0.36, y=0.6, h=1.45, **k): return act(reps("hero_pushup_pair_a", "hero_pushup_pair_b", n, step), x=x, y=y, h=h, pop=0.02, **k)
def pair(a, b, n=10, step=0.5, x=0.42, y=0.62, h=0.75, **k): return act(reps(a, b, n, step), x=x, y=y, h=h, pop=0.02, **k)
def world(n, **k): return dict(at=0, w=1.0, x=0.5, y=0.5, asset=path(n), z=-1, puppet=False, breathe=False, **k)
def mini(n, side="r"): return dict(at=0, w=wfor(n, 0.6), x=0.88 if side == "r" else 0.12, y=0.68, asset=path(n), enter=(f"corner_{side}", 0.25), z=3)
def kin(at, text, x=0.7, y=0.3, size=110, color=INK, until=None, frm="l", **k): return dict(at=at, text=text, x=x, y=y, size=size, color=color, until=until, **{"from": frm}, **k)
def card(text, big, small, tr="cut"):
    return dict(text=text, poses=[], set=RED, tr=tr, nocap=True, kinetic=[kin(0, big, 0.5, 0.42, 190, WHITE), kin(0.12, small, 0.5, 0.63, 84, WHITE, frm="b")],
                keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_short", .3)])
def M(text, base, m, side="r", **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m, side)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)], **k)
def ctx(text, img, word, tr="cut", x=None):  # one quick context scene (full-frame world, camera push, one big word)
    return dict(text=text, poses=[], tr=tr, layers=[world(img)], kinetic=[kin(0.05, word, x or max(0.2, 0.04 + 0.024 * len(word)), 0.2, 120, WHITE, stroke=10, stroke_fill=INK)],
                keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_short", .25)])
DRIFT = [(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]
CAL = dict(x=0.52, y=0.55, w=0.44, cols=10, n=30)
SORE = dict(x=0.58, y=0.82, w=0.4, h=0.42, values=[2, 10, 8, 4, 2, 1], labels=["DAY 0", "+1", "+2", "+3", "+4", "+5"], show_values=False, color=TEAL)
BARS7 = dict(x=0.62, y=0.82, w=0.3, h=0.55, values=[22, 27], labels=["DAY 1", "DAY 7"], hi_last=True, hi_color=TEAL, color=(150, 160, 170))

S = [
 # ---- HOOK ----
 dict(text="One hundred push-ups. Every day. For thirty days.", poses=[], layers=[world("W_living"), pu(10, 0.36)],
      counters=[dict(at="hundred", a=0, b=100, dur=0.9, x=0.74, y=0.72, size=190, color=INK, label="PUSH-UPS", stroke=8)],
      kinetic=[kin("thirty", "x 30 DAYS", 0.74, 0.93, 90, RED, stroke=8)],
      keys=[(0, 1.25, .4, .62), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_big", .2), ("hundred", "pop", .3), ("thirty", "pop", .3)]),
 dict(text="That's three thousand push-ups.", poses=[], tr="dip", d=0.5, layers=[act([("p_count", 0), ("g_shock", "thousand")], x=0.18)],
      calendars=[dict(at=0, ticks=[("three", 30)], **CAL)], kinetic=[kin("thousand", "3,000", 0.52, 0.17, 120, RED)], keys=DRIFT, sfx=[("thousand", "pop", .3)]),
 M("You can't even do twenty.", [act([("p_offended", 0)], x=0.18)], "mini_laugh_cut", calendars=[dict(at=-5, ticks=[(-5, 30)], **CAL)]),
 dict(text="Exactly. So on day one, I tested my max.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("p_knuckles", "So"), ("g_one", "day"), ("g_point", "tested")])],
      kinetic=[kin(0.05, "EXACTLY.", 0.68, 0.3, 110, INK, until="day"), kin("day", "DAY 1", 0.68, 0.3, 120, TEAL), kin("tested", "MAX TEST", 0.68, 0.55, 130)], keys=DRIFT, sfx=[("day", "pop", .3), ("tested", "pop", .3)]),
 dict(text="Twenty-two. Then my arms quit.", poses=[], tr="cut",
      layers=[world("W_living"), pu(3, 0.3, until="Then"), fig("hero_pushup_pair_b", at="Then", until="quit.", x=0.36, y=0.6, h=1.45, shiver=[("Then", "quit.")], puppet=False),
              fig("H_collapse", at="quit.", x=0.4, y=0.72, h=0.3, enter=("drop", 0.2), puppet=False)],
      counters=[dict(at=0, a=0, b=22, dur=0.6, x=0.17, y=0.24, size=190, color=RED, label="MAX", stroke=8)], shake=[("quit.", .05)],
      keys=DRIFT, sfx=[(0.6, "pop", .3), ("quit.", "whoosh_short", .3)]),
 dict(text="But the hard part wasn't day one. It was day two.", poses=[], tr="cut", layers=[act([("p_wag", 0), ("g_think", "wasn't"), ("p_ominous", "It")])],
      kinetic=[kin("hard", "THE HARD PART?", 0.68, 0.3, 100), kin("day#2", "DAY 2", 0.68, 0.55, 180, RED)], keys=DRIFT + [("day#2", 1.05, .5, .5), ("day#2+0.1", 1.1, .45, .48)],
      sfx=[("hard", "pop", .3), ("day#2", "pop", .3)]),
 # ---- DAY 1 ----
 card("Day one. I split the hundred", "DAY 1", "THE PLAN"),
 dict(text="into five sets of twenty.", poses=[], tr="cut", layers=[act([("p_count", 0), ("g_two", "sets")])], kinetic=[kin("five", "5 x 20", 0.68, 0.42, 180, TEAL)],
      keys=DRIFT, sfx=[("five", "pop", .3)]),
 ctx("Morning,", "s_morning", "MORNING", x=0.72), ctx("lunch,", "s_lunch", "LUNCH", x=0.72), ctx("afternoon,", "s_afternoon", "AFTERNOON", x=0.5), ctx("evening,", "s_evening", "EVENING", x=0.72),
 ctx("and one angry set before bed.", "s_angry", "ANGRY SET") | dict(shake=[("angry", .03)]),
 M("The angry set is my favourite.", [world("s_angry")], "mini_laugh_cut", "l"),
 dict(text="Total time? Eleven minutes.", poses=[], tr="dip", d=0.5, layers=[act([("g_think", 0), ("p_watch", "Eleven")])],
      rings=[dict(at="Eleven", x=0.66, y=0.45, r=0.24, dur=0.7, max=11, unit="MIN")], kinetic=[kin("Total", "TOTAL TIME?", 0.66, 0.12, 80)], keys=DRIFT, sfx=[("Eleven", "pop", .3)]),
 dict(text="It felt easy. Too easy.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("p_yawn", "Too")])],
      kinetic=[kin("easy.", "EASY", 0.66, 0.35, 140, TEAL), kin("Too", "TOO EASY", 0.66, 0.6, 140, RED)], keys=DRIFT, sfx=[("Too", "pop", .3)]),
 # ---- DAY 2 ----
 card("Day two. I woke up,", "DAY 2", "THE PAIN"),
 dict(text="reached for my phone, and my chest said no.", poses=[], tr="cut", layers=[world("H_bed_phone")],
      kinetic=[kin("no.", "NO.", 0.86, 0.22, 170, RED, stroke=8)], keys=[(0, 1.0, .5, .5), ("chest", 1.03, .5, .5), ("E", 1.06, .5, .52)], shake=[("no.", .04)],
      sfx=[("no.", "pop", .3)]),
 dict(text="That's normal muscle soreness.", poses=[], tr="dip", d=0.5, layers=[act([("p_rubchest", 0)])], kinetic=[kin("muscle", "MUSCLE SORENESS", 0.66, 0.42, 100, RED)],
      keys=DRIFT, sfx=[("muscle", "pop", .3)]),
 dict(text="It peaks one to two days after something new, then it fades.", poses=[], tr="cut", layers=[act([("g_palm", 0), ("g_one", "one"), ("g_two", "two"), ("g_thumbs", "fades.")], x=0.18)],
      bars=[dict(at=0, stagger=0.25, **SORE)], kinetic=[kin("peaks", "PEAK", 0.48, 0.3, 70, RED)], keys=DRIFT, sfx=[("peaks", "pop", .3)]),
 M("So pain means growth, right?", [act([("p_rubchest", 0)], x=0.18)], "s6_mini_squint_cut", bars=[dict(at=-5, stagger=0, **SORE)]),
 dict(text="No. Soreness means new. Not growth.", poses=[], tr="cut", layers=[act([("g_cross", 0), ("g_one", "Soreness"), ("p_wag", "Not")])],
      kinetic=[kin(0.05, "NO.", 0.66, 0.35, 150, RED, until="Soreness"), kin("Soreness", "SORE = NEW", 0.66, 0.35, 120, TEAL), kin("Not", "NOT GROWTH", 0.66, 0.58, 120, RED)], keys=DRIFT, sfx=[("Soreness", "pop", .3), ("Not", "pop", .3)]),
 # ---- WEEK 1 ----
 card("By day five, the soreness was gone.", "WEEK 1", "THE WRISTS"),
 dict(text="But my wrists started complaining.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("p_wrist", "wrists")])],
      kinetic=[kin(0.05, "SORENESS: GONE", 0.68, 0.25, 80, TEAL), kin("wrists", "THE WRISTS", 0.68, 0.5, 130, RED)], keys=DRIFT, sfx=[("wrists", "pop", .3)]),
 dict(text="Seven hundred push-ups a week, all on bent wrists.", poses=[], tr="cut", layers=[act([("p_wrist", 0)])],
      counters=[dict(at=0, a=0, b=700, dur=0.9, x=0.66, y=0.28, size=170, color=INK, label="PUSH-UPS / WEEK")],
      insets="WRIST", keys=DRIFT, sfx=[("bent", "pop", .3)]),
 dict(text="The fix took ten seconds.", poses=[], tr="cut", layers=[act([("g_think", 0), ("p_snap", "fix")])], kinetic=[kin("ten", "10 SECONDS", 0.66, 0.42, 120, TEAL)],
      keys=DRIFT, sfx=[("fix", "pop", .3)]),
 dict(text="Push-ups on my fists. Wrist straight, pain gone.", poses=[], tr="dip", d=0.4, layers=[world("W_living"), pair("L_fist_a", "L_fist_b", 10, 0.5)],
      kinetic=[kin("fists.", "ON YOUR FISTS", 0.42, 0.92, 100, INK, stroke=8)], insets="FIST", keys=DRIFT, sfx=[("fists.", "pop", .3), ("Wrist", "pop", .3)]),
 M("Fist push-ups. Very action movie.", [act([("p_action", 0)], x=0.3)], "mini_laugh_cut"),
 dict(text="And by day seven, my max went from twenty-two to twenty-seven.", poses=[], tr="cut", layers=[act([("g_point", 0), ("g_one", "max"), ("g_flex", "twenty-seven.")], x=0.2)],
      kinetic=[kin("day", "DAY 7", 0.86, 0.25, 90, TEAL), kin("twenty-seven.", "+5", 0.86, 0.45, 130, TEAL)],
      bars=[dict(at="from", stagger=0.9, **BARS7)], particles=[dict(at="twenty-seven.", x=0.68, y=0.3, spread=0.25)],
      keys=DRIFT, sfx=[("day", "pop", .3), ("twenty-seven.", "chime", .4)]),
 M("Muscle already?", [act([("g_flex", 0)], x=0.2)], "s6_mini_squint_cut", bars=[dict(at=-5, stagger=0, **(BARS7 | dict(x=0.58)))]),
 dict(text="Not yet. That's my brain learning the move. The muscle part comes later.", poses=[], tr="dip", d=0.4,
      layers=[act([("g_cross", 0), ("p_temple", "That's"), ("p_brain", "brain"), ("g_one", "muscle"), ("g_point", "later.")])],
      kinetic=[kin(0.05, "NOT YET.", 0.68, 0.32, 120, INK, until="brain"), kin("brain", "BRAIN FIRST", 0.68, 0.32, 120, TEAL), kin("muscle", "MUSCLE: LATER", 0.68, 0.56, 100, RED)], keys=DRIFT, sfx=[("brain", "pop", .3), ("muscle", "pop", .3)]),
]

def inset_specs():  # zoom badges grow from the exact body point (measured from the red / fist pixels of the assets)
    import numpy as np
    def red_xy(n):
        a = np.array(Image.open(path(n)).convert("RGBA")).astype(int); m = (a[..., 0] > 200) & (a[..., 1] < 90) & (a[..., 2] < 90) & (a[..., 3] > 0)
        ys, xs = np.where(m); return xs.mean() / a.shape[1], ys.mean() / a.shape[0]
    rx, ry = red_xy("p_wrist"); h = 0.92; wpx = h * H * 941 / 1672; top = 0.52 * H - h * H / 2
    wrist = [dict(at="bent", asset=path("p_wrist"), crop=(rx, ry, 0.22), x=0.66, y=0.68, r=0.085, bg=WHITE, grow=((0.24 * W - wpx / 2 + rx * wpx) / W, (top + ry * h * H) / H), mark="x")]
    fist = [dict(at="Wrist", asset=path("L_fist_a"), crop=(0.2, 0.74, 0.22), x=0.88, y=0.7, r=0.08, bg=WHITE, grow=(0.25, 0.8), mark="tick")]
    for s in S:
        if s.get("insets") == "WRIST": s["insets"] = wrist
        if s.get("insets") == "FIST": s["insets"] = fist
inset_specs()
PLAN = dict(dir=f"{HERE}/scenes_long03", words=f"{HERE}/voice/long02_cut.words.json", voice=f"{HERE}/voice/long02_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long03_demo{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
