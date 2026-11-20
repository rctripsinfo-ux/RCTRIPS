# LONG 07 "I Took Creatine for 365 Days" (16:9) STORY format; helpers from long06
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long07/long07_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{HERE}/long07/img/{n}_al.png", f"{HERE}/long07/img/{n}_c.png", f"{HERE}/long07/img/{n}.png", f"{HERE}/long06/img/{n}_al.png", f"{HERE}/long06/img/{n}.png", f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
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
XR = lambda seq, **k: dict(at=0, w=1.0, x=0.5, y=0.5, poses=[(path(p), a) for p, a in seq], z=-1, puppet=False, breathe=False, **k)
ORANGE, LTEAL, LRED = (240, 170, 60), (120, 200, 196), (240, 120, 120)

S = [
 # ===== HOOK =====
 S_("For one year, I took five grams of creatine every single day. Three hundred sixty-five scoops.", BK("bk_kitchen", H_([("c_scoop", 0), ("c_drink", "every")], x=0.3)),
    [T("five", "5 G / DAY", WHITE, 0.72, 0.2, 110)], counters=[dict(at="Three", a=0, b=365, dur=1.0, x=0.72, y=0.45, size=170, color=WHITE, label="SCOOPS", stroke=10)],
    keys=[(0, 1.3, .3, .4), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_big", .2), ("Three", "pop", .3)]),
 S_("Everyone warned me. You'll get fat. You'll bloat. You'll wreck your kidneys. And you'll lose your hair.", BK("bk_kitchen", P_("prop_tub", 0, "fat.", x=0.5, y=0.58, h=0.62, enter=("pop", 0.2)), P_("prop_tub_warn", "fat.", None, x=0.5, y=0.58, h=0.62, enter=("cut", 0))),
    [T("fat.", "FAT?", LRED, 0.18, 0.25, 110), T("bloat.", "BLOAT?", LRED, 0.82, 0.25, 110), T("kidneys.", "KIDNEYS?", LRED, 0.18, 0.62, 110), T("hair.", "HAIR?", LRED, 0.82, 0.62, 110)],
    shake=[("fat.", .03), ("bloat.", .03), ("kidneys.", .03), ("hair.", .03)], sfx=[("fat.", "pop", .3), ("bloat.", "pop", .3), ("kidneys.", "pop", .3), ("hair.", "pop", .3)]),
 S_("So I tracked everything. My weight, my strength, my blood tests.", BK("bk_garage", H_([("g_point", 0), ("p_count", "weight,")], x=0.3)),
    [T("weight,", "WEIGHT", WHITE, 0.72, 0.25, 100), T("strength,", "STRENGTH", WHITE, 0.72, 0.45, 100), T("blood", "BLOOD TESTS", WHITE, 0.72, 0.65, 100)], tr="dip", d=0.4),
 S_("And yes, my hair.", BK("bk_garage", H_([("c_rubhead", 0)], x=0.5, y=0.93, h=1.4)), [T("hair.", "MY HAIR.", WHITE, 0.5, 0.1, 140)], keys=DRIFT + [("hair.", 1.04, .5, .5), ("hair.+0.1", 1.1, .5, .45)]),
 M("You don't have any hair.", BK("bk_garage", H_([("c_rubhead", 0)], x=0.32)), "mini_laugh_cut"),
 S_("That's why I was the perfect test subject. Stay till the end for that one.", BK("bk_garage", H_([("g_thumbs", 0), ("p_ominous", "Stay")], x=0.3)),
    [T("perfect", "PERFECT TEST SUBJECT", WHITE, 0.68, 0.3, 80), T("end", "THE HAIR: AT THE END", ORANGE, 0.68, 0.5, 80)]),
 # ===== WHAT IT IS =====
 chap("First, what is creatine?", "WHAT IS IT?", "CREATINE 101", NAVY),
 S_("It's not a steroid.", BK("bk_studio", H_([("p_wag", 0)], x=0.3)), [T(0, "NOT A STEROID", LRED, 0.7, 0.42, 110)]),
 S_("It's a compound your body already makes, and it's in red meat and fish.", BK("bk_studio", H_([("g_palm", 0), ("g_point", "red")], x=0.3)),
    [T("body", "YOUR BODY MAKES IT", WHITE, 0.7, 0.3, 80), T("red", "RED MEAT + FISH", ORANGE, 0.7, 0.5, 90)]),
 S_("Your muscles use it to recharge their energy for short, hard efforts. Think of it as a tiny battery for every heavy rep.", [XR([("xr_bat", 0)])],
    [T("recharge", "RECHARGES ENERGY", WHITE, 0.5, 0.1, 100, until="battery"), T("battery", "A TINY BATTERY", ORANGE, 0.5, 0.1, 110)], tr="dip", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .5)]),
 S_("Most people only have their batteries about two-thirds full. Five grams a day tops them up. That's it.", [XR([("xr_bat", 0), ("xr_bat_full", "tops")])],
    [T("two-thirds", "2/3 FULL", ORANGE, 0.5, 0.1, 120, until="tops"), T("tops", "5 G = FULL", LTEAL, 0.5, 0.1, 130)], particles=[dict(at="tops", x=0.5, y=0.5, spread=0.3)], sfx=[("tops", "chime", .4)]),
 # ===== MONTH 1 =====
 chap("Month one.", "MONTH 1", "THE SCALE"),
 S_("I stepped on the scale and I was one and a half kilos heavier.", BK("bk_bathroom", H_([("g_base", 0), ("c_scale", "heavier.")], x=0.38, h=0.78), P_("prop_scale", 0, None, x=0.38, y=0.91, h=0.14, enter=("cut", 0))),
    [T("one", "+1.5 KG", LRED, 0.78, 0.35, 150)], shake=[("heavier.", .04)], sfx=[("heavier.", "pop", .3)]),
 S_("My first thought: it's making me fat. It wasn't.", BK("bk_bathroom", H_([("c_worried", 0), ("p_wag", "wasn't.")], x=0.32)),
    [T("fat.", "FAT?", LRED, 0.72, 0.35, 140, until="wasn't."), T("wasn't.", "NOPE.", LTEAL, 0.72, 0.35, 140)]),
 S_("Creatine pulls water into your muscle cells, not under your skin.", [XR([("xr_cell", 0), ("xr_cell_full", "muscle")])],
    [T("water", "WATER INTO THE MUSCLE", LTEAL, 0.5, 0.1, 90, until="not"), T("not", "NOT UNDER THE SKIN", WHITE, 0.5, 0.1, 90)], tr="dip", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .55)]),
 S_("So the muscle looks fuller, not puffy.", BK("bk_bathroom", H_([("g_flex", 0)], x=0.5, y=0.93, h=1.4)), [T("fuller,", "FULLER", LTEAL, 0.5, 0.1, 120, until="not"), T("not", "NOT PUFFY", WHITE, 0.5, 0.1, 120)]),
 S_("And no bloated belly. That only happens with huge loading doses. I just took five grams with breakfast.", BK("bk_kitchen", H_([("p_wag", 0), ("c_drink", "just")], x=0.3)),
    [T("bloated", "NO BLOAT", LTEAL, 0.72, 0.25, 100), T("loading", "ONLY WITH HUGE DOSES", WHITE, 0.72, 0.45, 80), T("five", "5 G + BREAKFAST", ORANGE, 0.72, 0.65, 90)]),
 # ===== MONTH 3 =====
 chap("Month three, the gym changed.", "MONTH 3", "THE REPS"),
 S_("Not a lot. But every set, I got one or two extra reps.", BK("bk_garage", pair("c_bench_a", "c_bench_b", 12, 0.45, x=0.42, y=0.7, h=0.5)),
    [T("extra", "+1-2 REPS", LTEAL, 0.5, 0.1, 130)], counters=[dict(at="every", a=8, b=10, dur=1.2, x=0.85, y=0.3, size=150, color=WHITE, stroke=10)]),
 S_("Those extra reps add up. More reps every week means more work, and more work means more muscle over time.", BK("bk_garage", pair("c_bench_a", "c_bench_b", 16, 0.5, x=0.3, y=0.7, h=0.5)),
    bars=[dict(at="More", x=0.72, y=0.8, w=0.4, h=0.5, values=[8, 9, 10, 11, 12], labels=["W1", "W2", "W3", "W4", "W5"], label_color=WHITE, label_stroke=6, stagger=0.3, show_values=False, hi_last=True, hi_color=TEAL, color=(150, 160, 170))],
    kinetic=[T("add", "IT ADDS UP", WHITE, 0.72, 0.12, 100)]),
 M("So creatine doesn't build muscle by itself?", BK("bk_garage", H_([("g_think", 0)], x=0.32)), "s6_mini_squint_cut"),
 S_("No. It lets you train a little harder. You still have to show up and do the work.", BK("bk_garage", H_([("p_wag", 0), ("g_point", "train"), ("g_flex", "work.")], x=0.3)),
    [T("harder.", "TRAIN A BIT HARDER", WHITE, 0.7, 0.3, 90), T("work.", "YOU DO THE WORK", ORANGE, 0.7, 0.5, 90)]),
 # ===== MONTH 6 =====
 chap("Month six.", "MONTH 6", "THE BLOOD TEST", NAVY),
 S_("Time to check the scary one. My kidneys.", BK("bk_clinic", H_([("c_worried", 0)], x=0.4)), [T("kidneys.", "THE KIDNEYS", LRED, 0.75, 0.3, 120)]),
 S_("My creatinine came back a bit high, and for one second I panicked.", BK("bk_clinic", fig("c_blood", x=0.3, y=0.58, h=0.78, puppet=False), P_("lab_red", 0, None, x=0.75, y=0.55, h=0.7)),
    [T("high,", "A BIT HIGH", LRED, 0.75, 0.1, 110)], shake=[("panicked.", .04)], sfx=[("high,", "pop", .3)]),
 S_("Then my doctor explained it. Creatinine is just the waste product of creatine. Take more creatine, you make more of it.", BK("bk_clinic", H_([("g_think", 0), ("p_temple", "waste")], x=0.3), P_("lab_red", 0, None, x=0.75, y=0.55, h=0.7)),
    [T("waste", "= WASTE PRODUCT", WHITE, 0.75, 0.1, 90, until="Take"), T("Take", "MORE IN = MORE OUT", ORANGE, 0.75, 0.1, 90)]),
 S_("It doesn't mean your kidneys are damaged.", BK("bk_clinic", H_([("g_thumbs", 0)], x=0.3), P_("lab_green", 0, None, x=0.75, y=0.55, h=0.7)), [T("damaged.", "NOT DAMAGE", LTEAL, 0.75, 0.1, 110)],
    particles=[dict(at="damaged.", x=0.75, y=0.4, spread=0.25)], sfx=[(0, "chime", .4)]),
 S_("In healthy people, studies over years show no kidney damage at normal doses. If you already have kidney problems, talk to your doctor first.", BK("bk_clinic", H_([("g_one", 0), ("p_phone", "If")], x=0.3)),
    [T("healthy", "HEALTHY: SAFE", LTEAL, 0.7, 0.3, 100), T("If", "KIDNEY ISSUES? ASK A DOCTOR", ORANGE, 0.66, 0.5, 70)]),
 # ===== MONTH 12 =====
 chap("One full year.", "MONTH 12", "THE RESULTS"),
 S_("Here's everything that changed.", BK("bk_rooftop", H_([("g_point", 0)], x=0.5, y=0.93, h=1.4)), [T(0, "WHAT CHANGED?", WHITE, 0.5, 0.1, 120)]),
 S_("My weight went up two kilos and most of it stayed as muscle and water in the muscle.", BK("bk_rooftop", H_([("g_flex", 0)], x=0.3)),
    [T("two", "+2 KG", WHITE, 0.72, 0.3, 140), T("muscle", "MUSCLE + MUSCLE WATER", LTEAL, 0.72, 0.5, 80)]),
 S_("My bench press went up more than my friend's, and we trained together, same plan.", BK("bk_garage", pair("c_bench_a", "c_bench_b", 10, 0.5, x=0.3, y=0.7, h=0.48), act([("k_calm", 0), ("k_thumbs", "same")], x=0.78, h=0.8)),
    [T("bench", "BENCH: UP MORE", WHITE, 0.5, 0.1, 110, until="same"), T("same", "SAME PLAN", ORANGE, 0.5, 0.1, 110)]),
 S_("My energy in long sets was better. And on low-sleep days, my head felt a bit sharper. There's early research on that, too.", BK("bk_rooftop", H_([("g_thumbs", 0), ("p_yawn", "low-sleep"), ("p_brain", "head")], x=0.3)),
    [T("energy", "MORE ENERGY", WHITE, 0.7, 0.25, 100), T("sharper.", "SHARPER ON LOW SLEEP", ORANGE, 0.7, 0.45, 80)]),
 S_("What didn't change? No fat gain. No bloat. No stomach problems. And I never needed a loading phase.", BK("bk_rooftop", H_([("g_cross", 0), ("g_thumbs", "never")], x=0.3)),
    [T("fat", "NO FAT GAIN", LTEAL, 0.7, 0.2, 90), T("bloat.", "NO BLOAT", LTEAL, 0.7, 0.36, 90), T("stomach", "NO STOMACH ISSUES", LTEAL, 0.7, 0.52, 80), T("loading", "NO LOADING", LTEAL, 0.7, 0.68, 90)]),
 # ===== HAIR =====
 chap("Now, the hair.", "THE HAIR", "QUESTION", NAVY),
 S_("This myth comes from one small study in rugby players, where one hormone went up.", BK("bk_studio", H_([("p_count", 0), ("p_temple", "hormone")], x=0.3)),
    [T("one", "1 SMALL STUDY", WHITE, 0.7, 0.3, 100), T("hormone", "1 HORMONE UP", ORANGE, 0.7, 0.5, 100)]),
 S_("Nobody actually measured hair loss in that study, and newer studies haven't found the same effect.", BK("bk_studio", H_([("p_wag", 0), ("g_thumbs", "newer")], x=0.3)),
    [T("measured", "HAIR NOT MEASURED", LRED, 0.7, 0.3, 90), T("newer", "NEWER STUDIES: NO", LTEAL, 0.7, 0.5, 90)]),
 S_("So creatine is very unlikely to make you lose your hair.", BK("bk_studio", H_([("g_point", 0)], x=0.3)), [T("unlikely", "VERY UNLIKELY", LTEAL, 0.7, 0.42, 130)]),
 S_("As for me, I'll let you be the judge.", BK("bk_studio", H_([("c_rubhead", 0)], x=0.5, y=0.93, h=1.4)), [T("judge.", "YOU BE THE JUDGE", WHITE, 0.5, 0.1, 110)],
    particles=[dict(at="judge.", x=0.5, y=0.3, spread=0.15)], keys=DRIFT + [("judge.", 1.05, .5, .5), ("judge.+0.1", 1.15, .5, .4)], sfx=[("judge.", "chime", .4)]),
 # ===== HOW TO =====
 chap("If you want to try it, it's simple.", "HOW TO", "TAKE IT"),
 S_("Plain creatine monohydrate. Three to five grams a day, every day, any time.", BK("bk_kitchen", H_([("c_scoop", 0)], x=0.3), P_("prop_tub", 0, None, x=0.72, y=0.58, h=0.55)),
    [T("monohydrate.", "MONOHYDRATE", WHITE, 0.5, 0.1, 110, until="Three"), T("Three", "3-5 G / DAY", ORANGE, 0.5, 0.1, 120, until="any"), T("any", "ANY TIME", LTEAL, 0.5, 0.1, 120)]),
 S_("Mix it in water, juice or your coffee. No fancy versions, no loading, no cycling.", BK("bk_kitchen", H_([("c_drink", 0), ("p_wag", "No")], x=0.3)),
    [T("water,", "WATER / JUICE / COFFEE", WHITE, 0.68, 0.3, 80), T("fancy", "NO FANCY VERSIONS", LRED, 0.68, 0.5, 80)]),
 S_("And drink enough water.", BK("bk_kitchen", H_([("c_drink", 0)], x=0.5, y=0.93, h=1.4)), [T("water.", "DRINK WATER", LTEAL, 0.5, 0.1, 120)]),
 S_("Have you tried creatine? Tell me what happened in the comments.", BK("bk_rooftop", H_([("g_point", 0)], x=0.3), act([("k_thumbs", 0)], x=0.75, h=0.8)),
    [T("tried", "TRIED CREATINE?", WHITE, 0.5, 0.08, 100), T("comments.", "TELL ME BELOW", ORANGE, 0.5, 0.2, 90)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long07", words=f"{HERE}/voice/long07_cut.words.json", voice=f"{HERE}/voice/long07_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=20, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05, text_overlay=True, dip_color=(10, 12, 18))
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long07{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
