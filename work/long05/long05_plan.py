# LONG 05 "You're Doing Push-Ups Wrong" (16:9) by THE LONG METHOD; helpers copied from long04_plan.py
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long05/long05_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
              f"{W1}/{n}.png", f"{P2}/{n}.png", f"{I3}/{n}_al.png"):
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

# ---------- long 05 helpers ----------
def LIV(*layers): return [world("W_living")] + list(layers)
def loopf(a, b, n=10, step=0.45, x=0.42, y=0.68, h=0.7, **k): return pair(a, b, n, step, x=x, y=y, h=h, **k)
def card5(text, n, small): return card(text, f"MISTAKE {n}", small)
def X(at, x, y, size=150, until=None): return kin(at, "X", x, y, size, RED, until=until, frm="b")
def OK(at, x, y, size=150): return kin(at, "✓" if False else "OK", x, y, size, TEAL, frm="b")
ELB = dict(x=0.42, y=0.55, h=0.62)
TOPTXT = dict(stroke=8)
def top(at, text, color=INK, until=None, size=100, x=0.5): return kin(at, text, x, 0.12, size, color, until=until, stroke=8)

S = [
 # ===== HOOK =====
 S_("You've done push-ups for months.", LIV(pu(10, 0.32)), [top("months.", "MONTHS", INK, size=110)], keys=[(0, 1.25, .4, .62), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)],
    sfx=[(0, "whoosh_big", .2)]),
 S_("Same twenty reps. Same chest. Same arms.", LIV(pu(10, 0.45)),
    [top(0, "SAME 20 REPS", INK, until="chest."), top("chest.", "SAME CHEST", INK, until="arms."), top("arms.", "SAME ARMS", RED)],
    counters=[dict(at=0, a=0, b=20, dur=0.6, x=0.86, y=0.3, size=170, color=RED, stroke=8)], sfx=[("chest.", "pop", .3), ("arms.", "pop", .3)]),
 M("Hey. That's personal.", [act([("p_offended", 0)])], "mini_shy_cut"),
 S_("It's not your genetics. It's your push-up.", [act([("p_wag", 0), ("g_point", "push-up.")])],
    [kin(0.05, "NOT GENETICS", 0.66, 0.35, 110, INK), kin("push-up.", "YOUR PUSH-UP", 0.66, 0.58, 120, RED)], sfx=[("push-up.", "pop", .3)]),
 S_("Most people make the same six mistakes, and each one quietly steals your strength.", [act([("p_count", 0), ("p_ominous", "steals")])],
    [kin("six", "6 MISTAKES", 0.66, 0.2, 120, RED)] + [X(f"six+{0.25 + 0.18 * i:.2f}", 0.5 + 0.08 * (i % 3), 0.42 + 0.18 * (i // 3), 110) for i in range(6)],
    sfx=[("six", "pop", .3)]),
 S_("Fix them, and the same push-up starts building real muscle again.", [act([("p_snap", 0), ("p_flexglow", "building")])],
    [kin("Fix", "FIX THEM", 0.66, 0.35, 120, TEAL), kin("real", "= REAL MUSCLE", 0.66, 0.58, 110, TEAL)], particles=[dict(at="muscle", x=0.24, y=0.3, spread=0.3)]),
 M("Six? I was hoping for one.", [act([("p_flexglow", 0)])], "s6_mini_squint_cut"),
 S_("Stay till the end, because mistake six is the one almost everyone makes, and it's the reason most people never get past twenty.",
    [act([("g_point", 0), ("p_ominous", "six"), ("g_cross", "never")])],
    [kin("six", "MISTAKE #6", 0.66, 0.35, 120, RED), kin("never", "STUCK AT 20", 0.66, 0.58, 110, INK)], sfx=[("six", "pop", .3)]),
 # ===== 1 =====
 card5("Mistake one.", 1, "THE T"),
 S_("Elbows flared out like a T.", [loopf("L_elbow_bad", "L_elbow_bad_b", 6, 0.5, **ELB)], [top(0, "LIKE A T", RED)], sfx=[(0, "pop", .3)]),
 S_("It feels easier, because your chest gets a shorter range.", [loopf("L_elbow_bad", "L_elbow_bad_b", 8, 0.5, **ELB)], [top("easier,", "FEELS EASIER", INK, until="shorter"), top("shorter", "SHORTER RANGE", RED)]),
 S_("But your shoulders take the load, and that's where push-up pain starts.", [loopf("L_elbow_bad", "L_elbow_bad_b", 8, 0.55, shiver=[("pain", "E+5")], **ELB)],
    [top("shoulders", "SHOULDERS TAKE IT", RED, until="pain"), top("pain", "PAIN STARTS HERE", RED)], shake=[("pain", .03)], sfx=[("pain", "pop", .3)]),
 M("So that clicking in my shoulder is... a feature?", [act([("p_wrist", 0)])], "s6_mini_squint_cut", kinetic=[kin("feature?", "A FEATURE?", 0.6, 0.2, 110, RED)]),
 S_("It's a warning. Tuck your elbows to about forty-five degrees.", [loopf("L_elbow_good", "L_elbow_good_b", 8, 0.5, **ELB)],
    [top(0, "A WARNING", RED, until="Tuck"), top("Tuck", "45 DEGREES", TEAL)], particles=[dict(at="degrees.", x=0.42, y=0.4, spread=0.3)], tr="dip", d=0.4),
 S_("Think arrow, not T.", [loopf("L_elbow_good", "L_elbow_good_b", 4, 0.5, **ELB)], [top(0, "ARROW, NOT T", TEAL, size=120)], sfx=[(0, "pop", .3)]),
 S_("Seen from above, your arms and your head make an arrow. Your elbows brush past your ribs on the way down, not out to the side.",
    [act([("g_base", 0), ("g_point", "arrow."), ("g_cross", "ribs")])],
    [kin("arrow.", "ARROW SHAPE", 0.66, 0.3, 110, TEAL), kin("ribs", "ELBOWS PAST RIBS", 0.66, 0.52, 100, INK), kin("not", "NOT OUT", 0.66, 0.72, 100, RED)]),
 M("Arrow. Got it. I'm a weapon now.", [act([("p_action", 0)], x=0.3)], "mini_laugh_cut"),
 # ===== 2 =====
 card5("Mistake two.", 2, "THE BANANA"),
 S_("Sagging hips.", LIV(fig("pu_sag", x=0.42, y=0.68, h=0.7, puppet=False, shiver=[(0, "E+5")])), [top(0, "SAGGING HIPS", RED)], sfx=[(0, "pop", .3)]),
 S_("When your hips drop, your lower back takes the bend and your core switches off.", LIV(loopf("pu_top", "pu_sag", 8, 0.55)),
    [top("lower", "LOWER BACK", RED, until="core"), top("core", "CORE: OFF", RED)]),
 S_("You're doing half a push-up and half a back bend.", LIV(loopf("pu_bot", "pu_sag", 6, 0.5)), [top("half", "HALF PUSH-UP", INK, until="back"), top("back", "HALF BACK BEND", RED)]),
 M("Banana push-ups.", LIV(fig("pu_sag", x=0.42, y=0.68, h=0.7, puppet=False)), "mini_laugh_cut", kinetic=[top(0, "BANANA", RED, size=130)]),
 S_("Exactly. Squeeze your glutes and brace your stomach like someone's about to poke it.", [act([("g_thumbs", 0), ("g_flex", "Squeeze"), ("p_flexglow", "brace")])],
    [kin("Squeeze", "SQUEEZE GLUTES", 0.66, 0.32, 100, TEAL), kin("brace", "BRACE STOMACH", 0.66, 0.55, 100, TEAL)], tr="dip", d=0.4),
 S_("Head to heels, one straight line.", LIV(loopf("pu_top", "pu_bot", 6, 0.45)), [top(0, "ONE STRAIGHT LINE", TEAL)], sfx=[(0, "pop", .3)]),
 S_("Here's a quick check. Put a broomstick along your back.", LIV(fig("pu_broom", x=0.42, y=0.68, h=0.7, puppet=False)), [top("check.", "QUICK CHECK", INK, until="broomstick"), top("broomstick", "BROOMSTICK TEST", TEAL)]),
 S_("It should touch your head, your upper back and your hips at the same time.", LIV(fig("pu_broom", x=0.42, y=0.68, h=0.7, puppet=False)),
    [top("head,", "HEAD", TEAL, until="upper"), top("upper", "UPPER BACK", TEAL, until="hips"), top("hips", "HIPS", TEAL)], sfx=[("head,", "pop", .3), ("upper", "pop", .3), ("hips", "pop", .3)]),
 M("I don't own a broomstick.", LIV(fig("pu_broom", x=0.42, y=0.68, h=0.7, puppet=False)), "mini_shy_cut"),
 S_("Then film yourself from the side. The camera doesn't lie.", [act([("g_point", 0), ("p_phone", "film"), ("g_thumbs", "camera")])], [kin("film", "FILM IT", 0.66, 0.42, 130, TEAL)]),
 # ===== 3 =====
 card5("Mistake three.", 3, "HALF REPS"),
 S_("Half reps.", LIV(loopf("pu_top", "pu_half", 8, 0.18)), [top(0, "HALF REPS", RED)], counters=[dict(at=0, a=0, b=30, dur=1.2, x=0.86, y=0.3, size=150, color=RED, stroke=8)]),
 S_("Most people stop halfway down, because the bottom is the hardest part.", LIV(loopf("pu_top", "pu_half", 14, 0.25)), [top("halfway", "STOP HALFWAY", RED, until="bottom"), top("bottom", "BOTTOM = HARDEST", INK)]),
 S_("But the bottom is exactly where the chest is stretched, and stretched muscle under load is what grows.", LIV(loopf("pu_top", "pu_bot", 10, 0.7)),
    [top("chest", "CHEST STRETCHED", TEAL, until="stretched#2"), top("stretched#2", "STRETCH + LOAD = GROWTH", TEAL, size=90)], tr="dip", d=0.4),
 M("So the hard part is the good part. Rude.", LIV(fig("pu_bot", x=0.42, y=0.68, h=0.7, puppet=False)), "mini_laugh_cut", kinetic=[top("Rude.", "RUDE.", RED, size=130)]),
 S_("Chest to a fist's height from the floor. Every rep.", LIV(loopf("pu_top", "pu_bot", 8, 0.6)), [top(0, "CHEST: 1 FIST FROM FLOOR", TEAL, size=90)]),
 S_("Ten full reps beat thirty half ones.", [act([("g_one", 0), ("g_thumbs", "beat")], x=0.2)],
    bars=[dict(at=0, x=0.6, y=0.82, w=0.34, h=0.55, values=[30, 10], labels=["30 HALF", "10 FULL"], stagger=0.5, hi_last=True, hi_color=TEAL, color=RED)],
    kinetic=[kin("beat", "10 FULL > 30 HALF", 0.6, 0.14, 90, TEAL)]),
 S_("And don't bounce off the bottom. Pause for one second down there.", LIV(act([("pu_top", 0), ("pu_bot", "Pause"), ("pu_top", "there.+0.3")], x=0.42, y=0.68, h=0.7, pop=0.02, puppet=False)),
    [top("bounce", "NO BOUNCE", RED, until="Pause"), top("Pause", "PAUSE 1 SEC", TEAL)], rings=[dict(at="Pause", x=0.86, y=0.28, r=0.12, dur=1.0, max=1, unit="SEC")]),
 S_("It feels brutal, and that's exactly why it works.", [act([("p_rubchest", 0), ("g_thumbs", "works.")])], [kin("brutal,", "BRUTAL", 0.66, 0.35, 130, RED), kin("works.", "IT WORKS", 0.66, 0.58, 120, TEAL)]),
 # ===== 4 =====
 card5("Mistake four.", 4, "THE HANDS"),
 S_("Hands too far forward, or too wide.", LIV(fig("pu_fwd", x=0.42, y=0.68, h=0.7, puppet=False, shiver=[(0, "E+5")])), [top(0, "TOO FAR FORWARD", RED)]),
 S_("Hands up by your face put your wrists and shoulders in a bad spot.", LIV(loopf("pu_fwd", "pu_fwd", 2, 1)), [top("wrists", "WRISTS + SHOULDERS", RED)], shake=[("bad", .03)]),
 S_("Too wide, and the range gets tiny.", [loopf("L_elbow_bad", "L_elbow_bad_b", 6, 0.3, **ELB)], [top(0, "TOO WIDE", RED, until="tiny."), top("tiny.", "TINY RANGE", RED)]),
 S_("Hands just outside your shoulders, under your chest.", LIV(loopf("pu_top", "pu_bot", 6, 0.55)), [top(0, "UNDER YOUR SHOULDERS", TEAL)], tr="dip", d=0.4),
 S_("Fingers spread wide, gripping the floor.", [act([("g_palm", 0), ("p_flexglow", "gripping")])], [kin("spread", "FINGERS SPREAD", 0.66, 0.35, 110, TEAL), kin("gripping", "GRIP THE FLOOR", 0.66, 0.58, 110, INK)]),
 S_("If your wrists still hurt, turn your hands out a little, or do them on your fists.", [act([("p_wrist", 0), ("p_snap", "turn")])],
    [kin("hurt,", "WRISTS HURT?", 0.66, 0.35, 110, RED), kin("fists.", "USE YOUR FISTS", 0.66, 0.58, 110, TEAL)]),
 S_("Wrist straight, pain gone.", LIV(loopf("L_fist_a", "L_fist_b", 6, 0.4, y=0.62, h=0.75)), [top(0, "WRIST STRAIGHT", TEAL)]),
 M("Fist push-ups again? Very action movie.", [act([("p_action", 0)], x=0.3)], "mini_laugh_cut"),
 # ===== 5 =====
 card5("Mistake five.", 5, "THE NOD"),
 S_("The head drop.", LIV(loopf("pu_top", "pu_head", 6, 0.3)), [top(0, "HEAD DROP", RED)]),
 M("I call that the chicken.", LIV(loopf("pu_top", "pu_head", 8, 0.25)), "mini_laugh_cut", kinetic=[top("chicken.", "THE CHICKEN", RED, size=120)]),
 S_("Your nose touches the floor, so it feels like a full rep.", LIV(loopf("pu_top", "pu_head", 8, 0.4)), [top("nose", "NOSE: FLOOR", INK, until="full"), top("full", "FEELS FULL", RED)]),
 S_("Your chest never got there.", LIV(fig("pu_head", x=0.42, y=0.68, h=0.7, puppet=False)), [top(0, "CHEST: NEVER THERE", RED)], shake=[("there.", .03)]),
 S_("Look at the floor a little ahead of your hands, and keep your head in line with your body.", LIV(loopf("pu_top", "pu_bot", 10, 0.5)),
    [top("ahead", "LOOK AHEAD", TEAL, until="line"), top("line", "HEAD IN LINE", TEAL)], tr="dip", d=0.4),
 S_("Pretend you're holding an egg between your chin and your chest. Don't crush it, don't drop it.", [act([("g_think", 0), ("p_temple", "egg"), ("g_thumbs", "drop")])],
    [kin("egg", "EGG UNDER CHIN", 0.66, 0.35, 110, TEAL), kin("crush", "DON'T CRUSH IT", 0.66, 0.58, 100, RED)]),
 # ===== 6 =====
 card("And the big one. Mistake six.", "MISTAKE 6", "THE SAME 20"),
 S_("Doing the same twenty push-ups forever.", LIV(pu(10, 0.4, "_sleepy")), [top(0, "SAME 20 FOREVER", RED)], counters=[dict(at=0, a=0, b=20, dur=0.5, x=0.86, y=0.3, size=160, color=RED, stroke=8)]),
 S_("Your body adapts to what you ask. If the ask never changes, the body never changes.", [act([("g_one", 0), ("p_yawn", "never")])],
    [kin("adapts", "BODY ADAPTS", 0.66, 0.35, 110, TEAL), kin("never", "NO NEW ASK = NO CHANGE", 0.66, 0.58, 90, RED)], tr="dip", d=0.4),
 M("So my push-ups got bored of me.", [fig("p_sofa", x=0.4, y=0.6, h=0.7, puppet=False)], "mini_laugh_cut"),
 S_("Add one rep a week.", [act([("g_one", 0)])], [kin(0, "+1 REP / WEEK", 0.66, 0.42, 120, TEAL)]),
 S_("Or slow down: three seconds down.", LIV(act([("pu_top", 0), ("pu_bot", "three+1.2")], x=0.42, y=0.68, h=0.7, puppet=False)), [top(0, "3 SEC DOWN", TEAL)],
    rings=[dict(at="three", x=0.86, y=0.28, r=0.12, dur=1.5, max=3, unit="SEC")]),
 S_("Or raise your feet.", LIV(loopf("pu_decline_top", "pu_decline_bot", 4, 0.4, y=0.66, h=0.72)), [top(0, "FEET UP", TEAL)]),
 S_("Small upgrades, every week.", [act([("g_thumbs", 0)])], [kin(0, "SMALL UPGRADES", 0.66, 0.42, 110, TEAL)]),
 S_("Here's the ladder.", [act([("g_point", 0)])], [kin(0, "THE LADDER", 0.66, 0.42, 140, INK)], tr="dip", d=0.4),
 S_("Wall push-ups.", [world("W_living"), dict(at=0, w=130 / 1920, x=0.604, y=0.44, asset=path("prop_wall"), puppet=False, breathe=False), loopf("L_wall_a", "L_wall_b", 4, 0.3, x=0.38, y=0.6, h=0.85)],
    [kin(0, "LEVEL 1: WALL", 0.32, 0.12, 90, INK, stroke=8)]),
 S_("Knee push-ups.", LIV(loopf("pu_knee_top", "pu_knee_bot", 4, 0.3)), [top(0, "LEVEL 2: KNEES", INK)]),
 S_("Normal push-ups.", LIV(loopf("pu_top", "pu_bot", 4, 0.3)), [top(0, "LEVEL 3: NORMAL", INK)]),
 S_("Slow push-ups.", LIV(act([("pu_top", 0), ("pu_bot", 0.8)], x=0.42, y=0.68, h=0.7, puppet=False)), [top(0, "LEVEL 4: SLOW", INK)]),
 S_("Feet up on a chair.", LIV(loopf("pu_decline_top", "pu_decline_bot", 4, 0.3, y=0.66, h=0.72)), [top(0, "LEVEL 5: FEET UP", RED)]),
 S_("Each step is harder, and each step builds more.", [act([("g_flex", 0)], x=0.2)],
    bars=[dict(at=0, x=0.62, y=0.82, w=0.55, h=0.55, values=[1, 2, 3, 4, 5], labels=["WALL", "KNEE", "NORMAL", "SLOW", "FEET UP"], stagger=0.2, show_values=False, hi_last=True, color=TEAL)]),
 M("So when twenty gets easy, I climb.", [act([("g_flex", 0)], x=0.2)], "s9_mini_point_cut",
   bars=[dict(at=-5, x=0.6, y=0.82, w=0.5, h=0.55, values=[1, 2, 3, 4, 5], labels=["WALL", "KNEE", "NORMAL", "SLOW", "FEET UP"], stagger=0, show_values=False, hi_last=True, color=TEAL)]),
 S_("Exactly. Easy means it's time to climb.", [act([("g_thumbs", 0), ("g_point", "climb.")])], [kin("Easy", "EASY = CLIMB", 0.66, 0.42, 130, TEAL)]),
 # ===== PERFECT =====
 card("So here's the perfect push-up, start to finish.", "THE PERFECT", "PUSH-UP"),
 S_("Hands under your shoulders. Elbows at forty-five. Body in one straight line. Head neutral.", LIV(loopf("pu_top", "pu_bot", 14, 0.55)),
    [top(0, "HANDS UNDER SHOULDERS", TEAL, until="Elbows", size=90), top("Elbows", "ELBOWS 45", TEAL, until="Body", size=90), top("Body", "STRAIGHT LINE", TEAL, until="Head", size=90),
     top("Head", "HEAD NEUTRAL", TEAL, size=90)], sfx=[("Elbows", "pop", .3), ("Body", "pop", .3), ("Head", "pop", .3)]),
 S_("Lower slowly until your chest is a fist from the floor. Then push the floor away.", LIV(act([("pu_top", 0), ("pu_bot", "chest"), ("pu_top", "push")], x=0.42, y=0.68, h=0.7, pop=0.02, puppet=False)),
    [top("slowly", "LOWER SLOWLY", TEAL, until="push"), top("push", "PUSH THE FLOOR AWAY", TEAL, size=90)]),
 M("And breathe?", LIV(fig("pu_top", x=0.42, y=0.68, h=0.7, puppet=False)), "s6_mini_squint_cut"),
 S_("Breathe in on the way down, out on the way up.", LIV(act([("pu_top", 0), ("pu_bot", "in"), ("pu_top", "out")], x=0.42, y=0.68, h=0.7, pop=0.02, puppet=False)),
    [top("in", "IN ON THE WAY DOWN", TEAL, until="out", size=90), top("out", "OUT ON THE WAY UP", INK, size=90)]),
 # ===== TEST + CTA =====
 S_("Here's a test. Do one set of perfect push-ups right now.", [act([("g_point", 0), ("p_kneel", "perfect")])], [kin("test.", "THE TEST", 0.66, 0.35, 130, INK), kin("perfect", "1 PERFECT SET", 0.66, 0.58, 110, TEAL)], tr="dip", d=0.4),
 S_("Most people lose a third of their reps.", LIV(loopf("pu_top", "pu_bot", 6, 0.4)), [top("third", "-1/3 REPS", RED, size=120)],
    counters=[dict(at=0, a=30, b=20, dur=1.0, x=0.86, y=0.3, size=160, color=RED, stroke=8)]),
 M("So my thirty is really twenty?", [act([("g_shrug", 0)])], "mini_scared_cut", kinetic=[kin("twenty?", "30 = 20?", 0.6, 0.2, 130, RED)]),
 S_("Probably. But that twenty builds real strength. Comment your perfect-rep number.", [act([("g_shrug", 0), ("g_flex", "builds"), ("g_point", "Comment")])],
    [kin("builds", "REAL STRENGTH", 0.66, 0.35, 110, TEAL), kin("Comment", "COMMENT YOUR NUMBER", 0.7, 0.58, 80, RED)]),
 M("And no banana push-ups. We will know.", LIV(fig("pu_sag", x=0.42, y=0.68, h=0.7, puppet=False)), "s6_mini_squint_cut", kinetic=[top("banana", "NO BANANAS", RED, size=120)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long05", words=f"{HERE}/voice/long05_cut.words.json", voice=f"{HERE}/voice/long05_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long05{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
