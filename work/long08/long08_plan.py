# LONG 08 "I Stopped Lifting for 3 Months" (16:9) STORY format (muscle memory); helpers from long07
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long08/long08_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{HERE}/long08/img/{n}_al.png", f"{HERE}/long08/img/{n}_c.png", f"{HERE}/long08/img/{n}.png", f"{HERE}/long07/img/{n}_al.png", f"{HERE}/long07/img/{n}_c.png", f"{HERE}/long07/img/{n}.png", f"{HERE}/long06/img/{n}_al.png", f"{HERE}/long06/img/{n}.png", f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
              f"{W1}/{n}.png", f"{P2}/{n}.png", f"{I3}/{n}_al.png", f"{HERE}/pilot3/img/{n}_al.png"):
        if os.path.exists(f): return f
    raise FileNotFoundError(n)
def wfor(n, h): im = Image.open(path(n)); return h * H * im.width / im.height / W
def fig(n, at=0, until=None, x=0.27, y=0.52, h=0.9, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), **k)
def act(seq, at=0, until=None, x=0.24, y=0.52, h=0.92, **k): return dict(at=at, until=until, w=wfor(seq[0][0], h), x=x, y=y, poses=[(path(p), a) for p, a in seq], **k)
def reps(a, b, n, step, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def pair(a, b, n=10, step=0.5, x=0.42, y=0.68, h=0.7, t0=0.0, **k):
    seq = ([(a, 0)] if t0 > 0 else []) + reps(a, b, n, step, t0)
    return act(seq, x=x, y=y, h=h, pop=0.02, puppet=False, **k)
def pu(n=10, step=0.4, sfx_="", **k): return pair(f"pu_top{sfx_}", f"pu_bot{sfx_}", n, step, **k)
def world(n, **k): return dict(at=0, w=1.0, x=0.5, y=0.5, asset=path(n), z=-1, puppet=False, breathe=False, **k)
def mini(n, side="r"): return dict(at=0, w=wfor(n, 0.6), x=0.88 if side == "r" else 0.12, y=0.68, asset=path(n), enter=(f"corner_{side}", 0.25), z=3)
def kin(at, text, x=0.68, y=0.3, size=110, color=INK, until=None, frm="l", **k): return dict(at=at, text=text, x=x, y=y, size=size, color=color, until=until, **{"from": frm}, **k)
def card(text, big, small):
    return dict(text=text, poses=[], set=RED, tr="cut", nocap=True, kinetic=[kin(0, big, 0.5, 0.42, 190, WHITE), kin(0.12, small, 0.5, 0.63, 84, WHITE, frm="b")],
                keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_short", .3)])
DRIFT = [(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]
def S_(text, layers, kinetic=(), tr="cut", **k): return dict(text=text, poses=[], tr=tr, layers=layers, kinetic=list(kinetic), keys=k.pop("keys", DRIFT), **k)
def M(text, base, m="mini_laugh_cut", side="r", **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m, side)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)], **k)
def room(bk, layer): return [world(bk), layer]
def ctx(text, bk, sfx_, word, step=0.22):
    return S_(text, room(bk, pu(8, step, sfx_, x=0.5, y=0.7, h=0.62)), [kin(0.05, word, 0.5, 0.2, 120, WHITE, stroke=10, stroke_fill=INK)], sfx=[(0, "whoosh_short", .25)])
def crowd(n_, cols, y0, dy, h, step=0.45, sync=None, x0=0.14, x1=0.86, sfx_=""):  # small H's doing reps; out of phase, or in phase from `sync`
    out = []
    for i in range(n_):
        x = x0 + (x1 - x0) * (i % cols) / max(1, cols - 1); y = y0 + dy * (i // cols); off = round((i * 0.37) % step, 2)
        if sync: out += [pair(f"pu_top{sfx_}", f"pu_bot{sfx_}", 8, step, x=x, y=y, h=h, t0=off, until=sync), pair(f"pu_top{sfx_}", f"pu_bot{sfx_}", 12, step * 0.8, x=x, y=y, h=h, at=sync)]
        else: out.append(pair(f"pu_top{sfx_}", f"pu_bot{sfx_}", 30, step, x=x, y=y, h=h, t0=off))
    return out
CAL = dict(x=0.52, y=0.55, w=0.44, cols=10, n=30)
SORE = dict(x=0.58, y=0.82, w=0.4, h=0.42, values=[2, 10, 8, 4, 2, 1], labels=["DAY 0", "+1", "+2", "+3", "+4", "+5"], show_values=False, color=TEAL)
def prog(vals, **k):
    lab = ["DAY 1", "DAY 7", "DAY 14", "DAY 21", "DAY 30"][:len(vals)]
    return dict(x=0.64, y=0.82, w=0.13 * len(vals) + 0.04, h=0.55, values=vals, labels=lab, hi_last=True, hi_color=TEAL, color=(150, 160, 170), **k)
SCORE = lambda vals, at: [dict(at=at, stagger=0.25, **prog(vals))]
MIR = [fig("prop_mirror", x=0.56, y=0.52, h=0.9, puppet=False, breathe=False)]
def refl(pose, at=0): return fig(pose, at=at, x=0.56, y=0.52, h=0.62, flip=True, alpha=0.45, puppet=False)

# ---------- long 07: story staging ----------
NAVY = (30, 42, 72)
def chap(text, big, small, color=TEAL):
    return dict(text=text, poses=[], set=color, tr="cut", nocap=True, kinetic=[kin(0, big, 0.5, 0.42, 190, WHITE), kin(0.12, small, 0.5, 0.63, 84, (230, 240, 238), frm="b")],
                keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], sfx=[(0, "whoosh_short", .3)])
def BK(n, *layers): return [world(n)] + list(layers)
def H_(seq, x=0.3, y=0.56, h=0.82, **k): return act(seq, x=x, y=y, h=h, **k)
def T(at, text, color=WHITE, x=0.5, y=0.1, size=100, until=None): return kin(at, text, x, y, size, color, until=until, stroke=10, stroke_fill=INK)
def P_(n, at=0, until=None, x=0.7, y=0.55, h=0.5, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), puppet=False, enter=k.pop("enter", ("pop", 0.25)), **k)
XR = lambda seq, w=1.0, **k: dict(at=0, w=w, x=0.5, y=0.5, poses=[(path(p), a) for p, a in seq], z=-1, puppet=False, breathe=False, **k)
ORANGE, LTEAL, LRED = (240, 170, 60), (120, 200, 196), (240, 120, 120)

S = [
 # ===== HOOK =====
 S_("For three months, I didn't lift a single weight. Not one push-up.", BK("bk_hotel", H_([("h_suitcase", 0)], x=0.3)),
    [T("three", "3 MONTHS", WHITE, 0.72, 0.3, 130), T("Not", "0 PUSH-UPS", LRED, 0.72, 0.5, 110)], keys=[(0, 1.3, .3, .4), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_big", .2), ("Not", "pop", .3)]),
 S_("I lost four kilos. My t-shirts got loose. My bench press dropped by twenty kilos.", BK("bk_mirror", H_([("h_thin", 0), ("h_thin_look", "bench")], x=0.3)),
    [T("four", "-4 KG", LRED, 0.72, 0.22, 130), T("t-shirts", "LOOSE T-SHIRTS", WHITE, 0.72, 0.42, 90), T("twenty", "BENCH -20 KG", LRED, 0.72, 0.6, 110)],
    shake=[("four", .03), ("twenty", .03)], sfx=[("four", "pop", .3), ("twenty", "pop", .3)], tr="dip", d=0.4),
 S_("Everyone told me, you're starting from zero.", BK("bk_mirror", H_([("h_thin", 0)], x=0.5, y=0.93, h=1.4)), [T("zero.", "FROM ZERO?", WHITE, 0.5, 0.1, 140)],
    keys=DRIFT + [("zero.", 1.04, .5, .5), ("zero.+0.1", 1.1, .5, .45)]),
 M("Zero? Like, zero zero?", BK("bk_mirror", H_([("h_thin", 0)], x=0.32)), "s6_mini_squint_cut"),
 S_("But then something strange happened. When I came back, everything came back faster than anyone expected.", BK("bk_garage", H_([("g_think", 0), ("g_flex", "everything")], x=0.3)),
    [T("strange", "SOMETHING STRANGE", WHITE, 0.7, 0.3, 90), T("faster", "FASTER THAN EXPECTED", LTEAL, 0.68, 0.5, 80)], sfx=[("faster", "chime", .4)]),
 S_("Stay till the end, because the reason is the coolest thing your body does.", BK("bk_garage", H_([("p_ominous", 0)], x=0.3)), [T("reason", "THE REASON: AT THE END", ORANGE, 0.68, 0.4, 80)]),
 # ===== WEEK 2 =====
 chap("Week two.", "WEEK 2", "NOTHING HAPPENED?", NAVY),
 S_("Here's the first surprise. For the first two weeks, I lost almost nothing.", BK("bk_hotel", H_([("g_one", 0), ("g_thumbs", "nothing.")], x=0.3)), [T("nothing.", "LOST: ALMOST NOTHING", LTEAL, 0.7, 0.4, 90)]),
 S_("Strength holds on for about two to three weeks. Muscle size too.", BK("bk_hotel", H_([("g_flex", 0)], x=0.3)),
    [T("Strength", "STRENGTH: 2-3 WEEKS", WHITE, 0.7, 0.3, 90), T("size", "SIZE: SAME", WHITE, 0.7, 0.5, 90)]),
 S_("What I lost first was the pump. My muscles looked flat, because they were holding less water and less stored energy. The muscle itself was still there.",
    BK("bk_mirror", H_([("g_think", 0)], x=0.3), P_("prop_balloon_full_c", 0, "flat,", x=0.72, y=0.55, h=0.55), P_("prop_balloon_flat_c", "flat,", None, x=0.72, y=0.62, h=0.3, enter=("cut", 0))),
    [T("pump.", "THE PUMP", ORANGE, 0.5, 0.1, 120, until="water"), T("water", "LESS WATER + ENERGY", LTEAL, 0.5, 0.1, 100, until="still"), T("still", "MUSCLE STILL THERE", WHITE, 0.5, 0.1, 100)],
    sfx=[("flat,", "whoosh_short", .3)]),
 M("So your muscles were just deflated?", BK("bk_mirror", H_([("g_think", 0)], x=0.32)), "mini_laugh_cut"),
 S_("Exactly. Like a balloon with less air, not a smaller balloon.", BK("bk_mirror", H_([("g_point", 0)], x=0.3), P_("prop_balloon_flat_c", 0, None, x=0.72, y=0.62, h=0.3)),
    [T("less", "LESS AIR", ORANGE, 0.72, 0.25, 110), T("smaller", "NOT SMALLER", LTEAL, 0.72, 0.85, 100)]),
 # ===== MONTH 1 =====
 chap("Month one.", "MONTH 1", "THE DROP"),
 S_("After about a month, the real drop started. My bench went down. Push-ups felt heavy.", BK("bk_garage", pair("c_bench_a", "c_bench_b", 8, 0.6, x=0.42, y=0.7, h=0.5)),
    [T("drop", "THE REAL DROP", LRED, 0.5, 0.1, 120, until="Push-ups"), T("Push-ups", "PUSH-UPS FEEL HEAVY", WHITE, 0.5, 0.1, 110)], shake=[("drop", .03)]),
 S_("Then, slowly, the muscle itself started to shrink.", BK("bk_garage", H_([("g_base", 0), ("h_thin", "shrink.")], x=0.5)), [T("shrink.", "SHRINKING", LRED, 0.5, 0.1, 130)], sfx=[("shrink.", "whoosh_short", .3)]),
 # ===== MONTH 3 =====
 chap("Month three.", "MONTH 3", "THE MIRROR", NAVY),
 S_("I looked in the mirror and barely recognised myself. Four kilos down. Smaller arms. Flatter chest.", BK("bk_mirror", H_([("h_thin", 0), ("h_thin_look", "Smaller")], x=0.3)),
    [T("Four", "-4 KG", LRED, 0.72, 0.22, 130), T("Smaller", "SMALLER ARMS", WHITE, 0.72, 0.42, 90), T("Flatter", "FLATTER CHEST", WHITE, 0.72, 0.58, 90)], sfx=[("Four", "pop", .3)]),
 S_("I thought it was gone for good.", BK("bk_mirror", H_([("h_thin", 0)], x=0.5, y=0.93, h=1.4)), [T("gone", "GONE FOR GOOD?", WHITE, 0.5, 0.1, 130)], keys=DRIFT + [("gone", 1.04, .5, .5), ("gone+0.1", 1.1, .5, .45)]),
 # ===== THE SECRET =====
 chap("The secret.", "THE SECRET", "MUSCLE MEMORY", NAVY),
 S_("Your muscle has a memory, and it's stored inside the cells.", BK("bk_studio", H_([("p_temple", 0), ("g_point", "inside")], x=0.3)), [T("memory,", "MUSCLE HAS A MEMORY", ORANGE, 0.7, 0.4, 90)]),
 S_("When you train, your muscle fibres grow, and they collect extra control centres called nuclei. Think of them as tiny builders.", [XR([("xr_fiber_big", 0)])],
    [T("grow,", "FIBRES GROW", WHITE, 0.5, 0.1, 110, until="nuclei."), T("nuclei.", "+ NUCLEI", ORANGE, 0.5, 0.1, 120, until="tiny"), T("tiny", "TINY BUILDERS", ORANGE, 0.5, 0.1, 120)],
    tr="dip", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .5)], sfx=[("tiny", "pop", .3)]),
 S_("When you stop, the fibres shrink. But research suggests many of those builders stay behind, maybe for years.", [XR([("xr_fiber_big", 0)], until="shrink."), XR([("xr_fiber_small", "shrink.")], w=1.8)],
    [T("shrink.", "FIBRES SHRINK", LRED, 0.5, 0.1, 110, until="builders"), T("builders", "BUILDERS STAY", LTEAL, 0.5, 0.1, 120, until="maybe"), T("maybe", "MAYBE FOR YEARS", LTEAL, 0.5, 0.1, 110)],
    keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .5)], sfx=[("shrink.", "whoosh_short", .3), ("builders", "chime", .4)]),
 M("So the builders just sit there, waiting?", [XR([("xr_fiber_small", 0)], w=1.8)], "s9_mini_point_cut"),
 S_("Waiting for the next order. That's why a comeback is much faster than the first time.", BK("bk_studio", H_([("g_point", 0), ("g_thumbs", "comeback")], x=0.3)), [T("comeback", "COMEBACK = FASTER", LTEAL, 0.7, 0.4, 100)]),
 # ===== THE COMEBACK =====
 chap("The comeback.", "THE COMEBACK", "WEEK BY WEEK"),
 S_("So I went back. Half the weight. Three days a week.", BK("bk_garage", H_([("h_thin", 0)], x=0.3)), [T("Half", "HALF THE WEIGHT", WHITE, 0.7, 0.3, 100), T("Three", "3 DAYS / WEEK", ORANGE, 0.7, 0.5, 100)]),
 S_("Week one, everything hurt. Week two, the pump was back.", BK("bk_garage", H_([("h_sore", 0), ("g_flex", "two,")], x=0.3)),
    [T("hurt.", "WEEK 1: OUCH", LRED, 0.7, 0.3, 100), T("pump", "WEEK 2: PUMP BACK", LTEAL, 0.7, 0.5, 100)], sfx=[("pump", "pop", .3)]),
 S_("Week four, my bench was almost where I left it. Muscle that took me a year to build came back in about a month.", BK("bk_garage", pair("c_bench_a", "c_bench_b", 12, 0.45, x=0.3, y=0.7, h=0.5)),
    [T("four,", "WEEK 4: BENCH BACK", LTEAL, 0.5, 0.1, 110, until="Muscle"), T("year", "1 YEAR TO BUILD", WHITE, 0.72, 0.3, 90), T("month.", "~1 MONTH BACK", LTEAL, 0.72, 0.48, 100)],
    particles=[dict(at="month.", x=0.72, y=0.45, spread=0.25)], sfx=[("month.", "chime", .4)]),
 S_("And here's the crazy part. In one study, one group trained for six months straight. The other group took three weeks off, every six weeks.", BK("bk_studio", H_([("g_one", 0), ("p_count", "other")], x=0.25)),
    [T("crazy", "THE CRAZY PART", ORANGE, 0.66, 0.15, 100, until="six"), T("six", "GROUP A: 6 MONTHS NONSTOP", WHITE, 0.66, 0.35, 70), T("other", "GROUP B: 3 WEEKS OFF EVERY 6", ORANGE, 0.66, 0.52, 66)], tr="dip", d=0.4),
 S_("At the end, both groups had about the same muscle and strength.", BK("bk_studio", H_([("g_thumbs", 0)], x=0.25)),
    bars=[dict(at=0.2, x=0.68, y=0.82, w=0.36, h=0.55, values=[100, 98], labels=["NONSTOP", "BREAKS"], label_color=WHITE, label_stroke=6, stagger=0.4, show_values=False, hi_last=True, hi_color=TEAL, color=(150, 160, 170))],
    kinetic=[T("same", "SAME RESULTS", LTEAL, 0.68, 0.12, 120)], sfx=[("same", "chime", .4)]),
 M("So breaks are free?", BK("bk_studio", H_([("g_thumbs", 0)], x=0.32)), "mini_laugh_cut"),
 S_("Short breaks almost are. Long breaks cost you, but you get it back much faster than you think.", BK("bk_rooftop", H_([("g_palm", 0), ("p_wag", "Long"), ("g_point", "faster")], x=0.3)),
    [T("Short", "SHORT BREAK: ALMOST FREE", LTEAL, 0.66, 0.3, 76), T("Long", "LONG BREAK: COMES BACK FAST", ORANGE, 0.66, 0.5, 70)]),
 S_("If you have to stop, keep your protein high, do a few push-ups or squats once a week, and when you come back, start at half the weight.", BK("bk_kitchen", H_([("g_one", 0), ("p_count", "push-ups"), ("g_point", "half")], x=0.3)),
    [T("protein", "PROTEIN HIGH", WHITE, 0.7, 0.25, 100), T("once", "1 SESSION / WEEK", WHITE, 0.7, 0.42, 100), T("half", "COME BACK AT 50%", ORANGE, 0.7, 0.59, 100)]),
 S_("Have you ever had to stop training? Tell me how long in the comments.", BK("bk_rooftop", H_([("g_point", 0)], x=0.3)),
    [T("stop", "HOW LONG DID YOU STOP?", WHITE, 0.62, 0.3, 90), T("comments.", "TELL ME BELOW", ORANGE, 0.62, 0.48, 100)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long08", words=f"{HERE}/voice/long08_cut.words.json", voice=f"{HERE}/voice/long08_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=20, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05, text_overlay=True, dip_color=(10, 12, 18))
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long08{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
