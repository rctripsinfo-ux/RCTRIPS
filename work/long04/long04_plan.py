# LONG 04 (full, ~6.5 min, 16:9) "I Did 100 Push-Ups Every Day for 30 Days" by THE LONG METHOD (skill shorts-director):
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long04/long04_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{A2}/{n}_al.png",
              f"{W1}/{n}.png", f"{P2}/{n}.png"):
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
MIR = [fig("prop_mirror", x=0.66, y=0.52, h=0.9, puppet=False, breathe=False)]
def refl(pose, at=0): return fig(pose, at=at, x=0.66, y=0.52, h=0.62, flip=True, alpha=0.45, puppet=False)

S = [
 # ===== HOOK =====
 S_("One hundred push-ups. Every day. For thirty days.", room("W_living", pu(10, 0.36, x=0.38, y=0.68, h=0.7)),
    [kin("thirty", "x 30 DAYS", 0.83, 0.86, 80, RED, stroke=8)], keys=[(0, 1.25, .4, .62), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)],
    counters=[dict(at="hundred", a=0, b=100, dur=0.9, x=0.83, y=0.62, size=170, color=INK, label="PUSH-UPS", stroke=8)], sfx=[(0, "whoosh_big", .2), ("hundred", "pop", .3)]),
 S_("That's three thousand push-ups.", [act([("p_count", 0), ("g_shock", "thousand")], x=0.18)], [kin("thousand", "3,000", 0.52, 0.17, 120, RED)], tr="dip", d=0.5,
    calendars=[dict(at=0, ticks=[("three", 30)], **CAL)], sfx=[("thousand", "pop", .3)]),
 M("You can't even do twenty.", [act([("p_offended", 0)], x=0.18)], calendars=[dict(at=-5, ticks=[(-5, 30)], **CAL)]),
 S_("Exactly. So I tested it.", [act([("g_thumbs", 0), ("p_knuckles", "So")])], [kin(0.05, "EXACTLY.", until="tested"), kin("tested", "I TESTED IT.", color=TEAL)]),
 S_("Twenty-two on day one. Thirty-eight on day thirty.", [act([("g_one", 0), ("g_flex", "Thirty-eight")])],
    [kin(0, "22", 0.55, 0.38, 200), kin("day", "DAY 1", 0.55, 0.6, 60), kin("Thirty-eight", "38", 0.82, 0.38, 200, TEAL), kin("day#2", "DAY 30", 0.82, 0.6, 60, TEAL)],
    sfx=[(0, "pop", .3), ("Thirty-eight", "pop", .3)]),
 S_("But the push-ups weren't the surprising part. What happened to my wrists, my brain and my belly was.",
    [act([("p_wag", 0), ("p_ominous", "What"), ("p_wrist", "wrists,"), ("p_temple", "brain"), ("g_shrug", "belly")])],
    [kin("surprising", "THE SURPRISE?", 0.68, 0.45, until="What"), kin("wrists,", "WRISTS", 0.68, 0.25, 110, RED), kin("brain", "BRAIN", 0.68, 0.45, 110, TEAL), kin("belly", "BELLY", 0.68, 0.65, 110, INK)],
    sfx=[("wrists,", "pop", .3), ("brain", "pop", .3), ("belly", "pop", .3)]),
 M("Your belly? Now I'm listening.", [act([("g_shrug", 0)])], "s6_mini_squint_cut"),
 # ===== DAY 1 =====
 card("Day one. First, a test.", "DAY 1", "THE TEST"),
 S_("One set, as many clean push-ups as I can.", [act([("p_knuckles", 0), ("p_kneel", "clean")])], [kin("set,", "1 SET", until="clean"), kin("clean", "MAX CLEAN REPS")]),
 S_("Clean means chest close to the floor, body straight like a plank, no sagging hips.",
    room("W_living", pu(12, 0.5, x=0.42, y=0.68, h=0.7, until="sagging")) + [fig("pu_sag", at="sagging", x=0.42, y=0.68, h=0.7, puppet=False, shiver=[("sagging", "hips.+2")])],
    [kin("chest", "CHEST TO FLOOR", 0.5, 0.13, 90, INK, until="body", stroke=8), kin("body", "BODY STRAIGHT", 0.5, 0.13, 90, TEAL, until="no", stroke=8),
     kin("no", "NO SAGGING HIPS", 0.5, 0.13, 90, RED, stroke=8)], tr="dip", d=0.4, sfx=[("sagging", "pop", .3)]),
 S_("Twenty-two. Then my arms quit.", room("W_living", pu(3, 0.3, x=0.38, y=0.68, h=0.7, until="Then")) +
    [fig("pu_bot", at="Then", until="quit.", x=0.38, y=0.68, h=0.7, shiver=[("Then", "quit.")], puppet=False), fig("H_collapse", at="quit.", x=0.42, y=0.7, h=0.66, enter=("drop", 0.2), puppet=False)],
    counters=[dict(at=0, a=0, b=22, dur=0.6, x=0.17, y=0.24, size=190, color=RED, label="MAX", stroke=8)], shake=[("quit.", .05)], sfx=[("quit.", "whoosh_short", .3)]),
 M("Twenty-two out of a hundred. So... only seventy-eight to go.", room("W_living", act([("H_collapse", 0), ("collapse_finger", "only")], x=0.42, y=0.7, h=0.66, puppet=False)),
   kinetic=[kin("seventy-eight", "78 TO GO", 0.5, 0.2, 120, RED, stroke=8)]),
 S_("You don't do a hundred in one go. You split it.", [act([("g_cross", 0), ("g_palm", "split")])], [kin(0.05, "100 AT ONCE?", until="split"), kin("split", "SPLIT IT", color=TEAL)], tr="dip", d=0.4),
 S_("Five sets of twenty, spread across the day.", [act([("p_count", 0), ("g_two", "twenty,")])], [kin("Five", "5 x 20", 0.68, 0.35, 170, TEAL), kin("spread", "ALL DAY", 0.68, 0.6, 90)]),
 ctx("Morning,", "bk_kitchen", "_sleepy", "MORNING"), ctx("lunch,", "bk_office", "_sandwich", "LUNCH"), ctx("afternoon,", "W_living", "", "AFTERNOON"),
 ctx("evening,", "bk_evening", "_tired", "EVENING"), ctx("and one angry set before bed.", "bk_night", "_angry", "ANGRY SET", 0.3) | dict(shake=[("angry", .03)]),
 M("The angry set is my favourite.", room("bk_night", pu(8, 0.35, "_angry", x=0.5, y=0.7, h=0.62))),
 S_("Total time? Eleven minutes.", [act([("g_think", 0), ("p_watch", "Eleven")])], [kin("Total", "TOTAL TIME?", 0.66, 0.12, 80)], tr="dip", d=0.5,
    rings=[dict(at="Eleven", x=0.66, y=0.5, r=0.24, dur=0.7, max=11, unit="MIN")]),
 S_("It felt easy. Too easy.", [act([("g_thumbs", 0), ("p_yawn", "Too")])], [kin("easy.", "EASY", 0.66, 0.35, 140, TEAL), kin("Too", "TOO EASY", 0.66, 0.6, 140, RED)]),
 # ===== DAY 2-3 =====
 card("Day two.", "DAY 2", "THE PAIN"),
 S_("I woke up, reached for my phone, and my chest said no.", [act([("bed_base", 0), ("bed_wake", "woke"), ("bed_reach", "reached"), ("bed_clutch", "chest"), ("bed_no", "no.")], x=0.45, y=0.55, h=0.9, puppet=False)],
    [kin("no.", "NO.", 0.86, 0.22, 170, RED, stroke=8)], shake=[("no.", .04)], sfx=[("no.", "pop", .3)]),
 S_("That's delayed muscle soreness.", [act([("p_rubchest", 0)])], [kin("delayed", "DELAYED", 0.66, 0.35, 100), kin("muscle", "MUSCLE SORENESS", 0.66, 0.55, 100, RED)], tr="dip", d=0.5),
 S_("It peaks one to two days after something new, then it fades.", [act([("g_palm", 0), ("g_one", "one"), ("g_two", "two"), ("g_thumbs", "fades.")], x=0.18)],
    [kin("peaks", "PEAK", 0.48, 0.3, 70, RED)], bars=[dict(at=0, stagger=0.25, **SORE)]),
 M("So pain means growth, right?", [act([("p_rubchest", 0)], x=0.18)], "s6_mini_squint_cut", bars=[dict(at=-5, stagger=0, **SORE)]),
 S_("No. Soreness means new. Not growth.", [act([("g_cross", 0), ("g_one", "Soreness"), ("p_wag", "Not")])],
    [kin(0.05, "NO.", 0.66, 0.35, 150, RED, until="Soreness"), kin("Soreness", "SORE = NEW", 0.66, 0.35, 120, TEAL), kin("Not", "NOT GROWTH", 0.66, 0.58, 120, RED)]),
 S_("You can grow without it, and you can be sore and grow nothing.", [act([("g_palm", 0), ("g_shrug", "sore")])],
    [kin("grow", "GROW WITHOUT PAIN", 0.66, 0.35, 90, TEAL), kin("sore", "SORE, NO GROWTH", 0.66, 0.58, 90, RED)]),
 S_("Day three, I still did the hundred.", [act([("g_one", 0), ("g_thumbs", "still")])], [kin(0, "DAY 3", 0.66, 0.4, 150, TEAL)]),
 S_("But ten sets of ten. Slow. Form first.", crowd(10, 5, 0.42, 0.33, 0.2, 0.6), [kin("ten", "10 x 10", 0.5, 0.12, 110, INK, stroke=8)], tr="dip", d=0.4),
 M("Ten sets of ten. That's just push-ups with extra steps.", crowd(10, 5, 0.42, 0.33, 0.2, 0.6, x1=0.7), "mini_laugh_cut"),
 S_("That's the point. Small sets, perfect reps, no grinding.", [act([("g_point", 0), ("g_one", "Small"), ("g_thumbs", "perfect"), ("g_cross", "grinding.")])],
    [kin("Small", "SMALL SETS", 0.68, 0.25, 100), kin("perfect", "PERFECT REPS", 0.68, 0.45, 100, TEAL), kin("grinding.", "NO GRINDING", 0.68, 0.65, 100, RED)]),
 # ===== WEEK 1 =====
 card("By day five, the soreness was gone.", "WEEK 1", "THE WRISTS"),
 S_("But my wrists started complaining.", [act([("g_thumbs", 0), ("p_wrist", "wrists")])], [kin("wrists", "THE WRISTS", 0.68, 0.45, 130, RED)]),
 S_("Seven hundred push-ups a week, every rep with the wrist bent back almost ninety degrees.", [act([("p_wrist", 0)])],
    [kin("ninety", "90 DEGREES", 0.66, 0.9, 80, RED)], counters=[dict(at=0, a=0, b=700, dur=0.9, x=0.66, y=0.24, size=160, color=INK, label="PUSH-UPS / WEEK")], insets="BENT"),
 S_("The fix took ten seconds.", [act([("g_think", 0), ("p_snap", "fix")])], [kin(0.05, "THE FIX?", 0.66, 0.42, 120, INK, until="ten"), kin("ten", "10 SECONDS", 0.66, 0.42, 120, TEAL)]),
 S_("Push-ups on my fists, or on two dumbbells. Wrist straight, pain gone.", room("W_living", pair("L_fist_a", "L_fist_b", 12, 0.5, x=0.42, y=0.62, h=0.75)),
    [kin("fists,", "ON YOUR FISTS", 0.42, 0.92, 100, INK, stroke=8)], tr="dip", d=0.4, insets="FIST"),
 M("Fist push-ups. Very action movie.", [act([("p_action", 0)], x=0.3)]),
 S_("Second fix: elbows.", [act([("g_two", 0)])], [kin(0.05, "FIX 2: ELBOWS", 0.66, 0.42, 120, TEAL)]),
 S_("If they flare out like a T, your shoulders take the hit.", [fig("L_elbow_bad", x=0.4, y=0.55, h=0.6, puppet=False)], [kin("T,", "NOT LIKE A T", 0.4, 0.13, 100, RED)], tr="dip", d=0.4),
 S_("Keep them about forty-five degrees from your body.", [fig("L_elbow_good", x=0.4, y=0.55, h=0.6, puppet=False)], [kin("forty-five", "45 DEGREES", 0.4, 0.13, 100, TEAL)],
    particles=[dict(at="body.", x=0.4, y=0.4, spread=0.4)]),
 S_("Day seven, I tested again. Twenty-seven. Five more in one week.", [act([("g_point", 0), ("g_flex", "Twenty-seven.")], x=0.2)],
    [kin(0, "DAY 7", 0.62, 0.3, 120, TEAL, until="Twenty-seven."), kin("Five", "+5", 0.9, 0.45, 130, TEAL)], bars=SCORE([22, 27], "Twenty-seven."), tr="dip", d=0.4),
 M("Muscle already?", [act([("g_flex", 0)], x=0.2)], "s6_mini_squint_cut", bars=[dict(at=-5, stagger=0, **(prog([22, 27]) | dict(x=0.56)))]),
 S_("Not yet. That's my brain learning the move. The muscle part comes later.", [act([("g_cross", 0), ("p_temple", "That's"), ("p_brain", "brain"), ("g_one", "muscle"), ("g_point", "later.")])],
    [kin(0.05, "NOT YET.", 0.68, 0.32, 120, INK, until="brain"), kin("brain", "BRAIN FIRST", 0.68, 0.32, 120, TEAL), kin("muscle", "MUSCLE: LATER", 0.68, 0.56, 100, RED)], tr="dip", d=0.4),
 # ===== WEEK 2 =====
 card("Week two felt like cheating.", "WEEK 2", "THE BRAIN"),
 S_("Same body, but the sets got easier every day.", room("W_living", act([("pu_top", 0)] + reps("pu_top", "pu_bot", 6, 0.55, 0.3) + reps("pu_top", "pu_bot", 10, 0.25, 3.6), x=0.42, y=0.68, h=0.7, pop=0.02, puppet=False)),
    [kin("easier", "EASIER EVERY DAY", 0.5, 0.13, 100, TEAL, stroke=8)]),
 S_("In the first weeks, most strength gains come from your nervous system, not new muscle.", [act([("p_temple", 0), ("p_brain", "nervous")])],
    [kin("strength", "STRENGTH GAINS", 0.68, 0.25, 90), kin("nervous", "NERVOUS SYSTEM", 0.68, 0.45, 100, TEAL), kin("not", "NOT NEW MUSCLE", 0.68, 0.65, 90, RED)], tr="dip", d=0.4),
 S_("Your brain learns to switch on more muscle fibres, at the same time, and stops the muscles fighting each other.",
    [act([("p_brain", 0), ("g_flex", "fibres,"), ("p_brain", "same"), ("g_cross", "fighting")])],
    [kin("more", "MORE FIBRES", 0.68, 0.25, 100, TEAL), kin("same", "AT THE SAME TIME", 0.68, 0.45, 90), kin("fighting", "NO FIGHTING", 0.68, 0.65, 100, RED)]),
 M("So your muscles didn't grow. They just got... organised.", [act([("p_brain", 0)])]),
 S_("Exactly. Same team, better teamwork.", crowd(5, 5, 0.6, 0, 0.26, 0.5, sync="better"), [kin("Same", "SAME TEAM", 0.5, 0.18, 110, until="better"), kin("better", "BETTER TEAMWORK", 0.5, 0.18, 110, TEAL)],
    tr="dip", d=0.4),
 S_("Day fourteen: thirty-one.", [act([("g_flex", 0)], x=0.2)], bars=SCORE([22, 27, 31], 0)),
 S_("And then the real enemy showed up. Boredom.", [act([("p_ominous", 0), ("p_yawn", "Boredom.")])], [kin("enemy", "THE REAL ENEMY", 0.68, 0.35, 100, until="Boredom."), kin("Boredom.", "BOREDOM", 0.68, 0.35, 150, RED)]),
 M("The push-ups were winning.", [fig("p_sofa", x=0.4, y=0.6, h=0.7, puppet=False)], "mini_laugh_cut"),
 S_("So I stopped making it a workout.", [act([("g_cross", 0)])], [kin("workout.", "NOT A WORKOUT", 0.68, 0.42, 110, RED)]),
 S_("I made it a habit.", [act([("p_snap", 0)])], [kin("habit.", "A HABIT", 0.68, 0.42, 150, TEAL)]),
 S_("Ten push-ups every time I made coffee.", room("bk_kitchen", act([("p_coffee", 0)], x=0.3, y=0.55, h=0.85, until="every")) + [pu(8, 0.3, "_sleepy", x=0.5, y=0.7, h=0.62, at="every")],
    [kin(0, "+10", 0.82, 0.2, 140, WHITE, stroke=10, stroke_fill=INK)]),
 S_("Ten every time I came back from the bathroom.", room("bk_bathroom", act([("g_thumbs", 0)], x=0.3, y=0.55, h=0.85, until="came")) + [pu(8, 0.3, x=0.5, y=0.7, h=0.62, at="came")],
    [kin(0, "+10", 0.82, 0.2, 140, WHITE, stroke=10, stroke_fill=INK)]),
 S_("By evening, the hundred was done and I never \"worked out\".", [act([("g_thumbs", 0), ("g_hips", "never")])],
    [kin("hundred", "100: DONE", 0.68, 0.35, 120, TEAL), kin("never", "ZERO WORKOUTS", 0.68, 0.58, 100)], tr="dip", d=0.4),
 # ===== WEEK 3 =====
 card("Okay, week three.", "WEEK 3", "THE MIRROR"),
 M("Abs? Huge chest? Movie star?", MIR + [refl("g_flex")], "s9_mini_point_cut",
   kinetic=[kin(0, "ABS?", 0.26, 0.28, 110, INK), kin("Huge", "HUGE CHEST?", 0.26, 0.45, 100, INK), kin("Movie", "MOVIE STAR?", 0.26, 0.62, 100, RED)]),
 S_("Chest and the back of my arms looked a little fuller. Mostly a pump, and a little real growth.", MIR + [refl("p_flexglow"), act([("g_base", 0), ("p_flexglow", "Chest")], x=0.3)],
    [kin("fuller.", "A LITTLE FULLER", 0.5, 0.1, 90, TEAL), kin("Mostly", "MOSTLY PUMP", 0.5, 0.92, 90, RED)]),
 S_("And my posture changed.", [act([("p_slouch", 0), ("g_base", "changed.")])], [kin("posture", "POSTURE", 0.66, 0.42, 150, TEAL)], tr="dip", d=0.4),
 S_("A push-up is basically a moving plank. Your core works the whole time.", room("W_living", pu(12, 0.45, x=0.42, y=0.68, h=0.7)),
    [kin("moving", "A MOVING PLANK", 0.5, 0.13, 100, INK, stroke=8, until="core"), kin("core", "CORE: ON", 0.5, 0.13, 110, TEAL, stroke=8)]),
 M("And the belly?", room("W_living", fig("pu_top", x=0.42, y=0.68, h=0.7, puppet=False)), "s6_mini_squint_cut"),
 S_("Same belly. One hundred push-ups burn maybe thirty to fifty calories.", [act([("g_shrug", 0), ("p_biscuit", "thirty")])],
    [kin(0.05, "SAME BELLY", 0.68, 0.3, 110, RED, until="One"), kin("One", "100 PUSH-UPS", 0.68, 0.3, 110), kin("thirty", "= 30-50 KCAL", 0.68, 0.52, 110, RED)], tr="dip", d=0.4),
 S_("That's one biscuit.", [act([("p_biscuit", 0)])], [kin(0.1, "= 1 BISCUIT", 0.68, 0.42, 150, RED)], keys=DRIFT + [(0.3, 1.05, .5, .5), (0.4, 1.12, .3, .3)]),
 M("One biscuit? Three weeks of pain for one biscuit?", [act([("p_biscuit", 0)])], "mini_scared_cut"),
 S_("Push-ups build strength. Fat loss comes from what you eat and how much you walk. Different jobs.", [act([("g_one", 0), ("g_two", "Fat"), ("g_palm", "Different")])],
    [kin("strength.", "PUSH-UPS = STRENGTH", 0.66, 0.25, 80, TEAL), kin("Fat", "FOOD + WALKING = FAT LOSS", 0.66, 0.45, 70, RED), kin("Different", "DIFFERENT JOBS", 0.66, 0.67, 100)]),
 S_("Day twenty-one: thirty-five.", [act([("g_flex", 0)], x=0.2)], bars=SCORE([22, 27, 31, 35], 0)),
 # ===== WEEK 4 =====
 card("Week four, the hundred was easy.", "WEEK 4", "THE PLATEAU"),
 S_("Four sets of twenty-five, done in ten minutes.", room("W_living", pu(12, 0.35, "_sleepy", x=0.42, y=0.68, h=0.7)),
    [kin("Four", "4 x 25", 0.5, 0.13, 110, INK, stroke=8, until="ten"), kin("ten", "10 MINUTES", 0.5, 0.13, 110, TEAL, stroke=8)]),
 S_("And that's the problem. When something gets easy, the body stops changing. It has no reason to.", [act([("g_think", 0), ("g_shrug", "stops"), ("g_palm", "reason")])],
    [kin("problem.", "THE PROBLEM", 0.68, 0.32, 110, until="easy,"), kin("easy,", "EASY = NO CHANGE", 0.68, 0.32, 110, RED)], tr="dip", d=0.4),
 M("So the challenge stops being a challenge.", [act([("g_palm", 0)])], "s3_mini_disappointed_cut"),
 S_("Right. Muscles grow when you keep asking for a little more.", [act([("g_point", 0), ("g_one", "more.")])], [kin("asking", "ASK FOR A LITTLE MORE", 0.66, 0.42, 90, TEAL)]),
 S_("So I made them harder. Three seconds down, one second up.", room("W_living", act([("pu_top", 0), ("pu_bot", "Three+1.2"), ("pu_top", "one+0.3")], x=0.42, y=0.68, h=0.7, pop=0.02, puppet=False)),
    [kin("harder.", "HARDER", 0.5, 0.13, 110, RED, stroke=8, until="Three"), kin("Three", "3 SEC DOWN", 0.5, 0.13, 110, INK, stroke=8)],
    rings=[dict(at="Three", x=0.85, y=0.25, r=0.13, dur=3.0, max=3, unit="SEC")], tr="dip", d=0.4),
 S_("Then feet on a chair.", room("W_living", pair("pu_decline_top", "pu_decline_bot", 6, 0.45, x=0.42, y=0.66, h=0.72)), [kin("feet", "FEET ON A CHAIR", 0.5, 0.13, 100, TEAL, stroke=8)]),
 S_("A study in 2017 found push-ups built chest muscle about as well as the bench press, as long as they kept getting harder.",
    [act([("g_point", 0), ("g_flex", "chest"), ("g_one", "long")])],
    [kin("2017", "STUDY, 2017", 0.68, 0.18, 70, INK), kin("bench", "PUSH-UPS = BENCH PRESS", 0.68, 0.38, 80, TEAL), kin("long", "IF THEY GET HARDER", 0.68, 0.58, 80, RED),
     kin("study", "Kikuchi & Nakazato, J Exerc Sci Fit 2017", 0.7, 0.93, 34, (90, 98, 108))], tr="dip", d=0.4),
 M("So the floor is a gym. Who knew?", room("W_living", pu(8, 0.4, x=0.42, y=0.68, h=0.7)), "mini_laugh_cut"),
 # ===== DAY 30 =====
 card("Day thirty. Same test as day one.", "DAY 30", "THE RESULT"),
 S_("One set, clean form.", [act([("p_knuckles", 0), ("p_kneel", "clean")])], [kin(0.05, "FINAL TEST", 0.66, 0.42, 130)]),
 M("Drumroll please.", room("W_living", pu(8, 0.3, x=0.38, y=0.68, h=0.7)), "mini_laugh_cut"),
 S_("Thirty-eight.", room("W_living", pu(4, 0.3, x=0.38, y=0.68, h=0.7)), counters=[dict(at=0, a=0, b=38, dur=0.5, x=0.83, y=0.3, size=220, color=TEAL, stroke=8)],
    sfx=[(0.5, "chime", .4)]),
 S_("From twenty-two to thirty-eight in thirty days.", [act([("g_flex", 0)], x=0.18)], bars=SCORE([22, 27, 31, 35, 38], 0), particles=[dict(at="thirty-eight", x=0.75, y=0.3, spread=0.3)]),
 S_("Here's the honest summary. Strength: way up. Endurance: way up. Chest and arms: a little bigger. Posture: better.",
    [act([("g_point", 0), ("g_flex", "Strength:"), ("g_thumbs", "Endurance:"), ("p_flexglow", "Chest"), ("g_base", "Posture:")])],
    [kin("Strength:", "STRENGTH: WAY UP", 0.68, 0.2, 70, TEAL), kin("Endurance:", "ENDURANCE: WAY UP", 0.68, 0.36, 70, TEAL),
     kin("Chest", "CHEST + ARMS: A BIT BIGGER", 0.68, 0.52, 60, INK), kin("Posture:", "POSTURE: BETTER", 0.68, 0.68, 70, TEAL)], tr="dip", d=0.4),
 S_("Belly fat: no change. And my wrists only survived because of the fix.", [act([("g_shrug", 0), ("p_wrist", "wrists")])],
    [kin(0, "BELLY FAT: NO CHANGE", 0.66, 0.35, 80, RED), kin("wrists", "WRISTS: SAVED BY THE FIX", 0.66, 0.55, 70, INK)]),
 M("So, would you do it again?", [act([("g_think", 0)])], "s6_mini_squint_cut"),
 S_("Yes. But the smarter version.", [act([("g_thumbs", 0), ("g_point", "smarter")])], [kin(0.05, "YES.", 0.66, 0.35, 150, TEAL), kin("smarter", "THE SMART VERSION", 0.66, 0.58, 100)]),
 # ===== RULES =====
 card("Rule one. Split the reps across the day.", "RULE 1", "SPLIT IT"),
 S_("Never grind one ugly set.", [act([("g_cross", 0)])], [kin(0.05, "NO UGLY SETS", 0.66, 0.42, 120, RED)]),
 S_("Rule two. Take one easy day a week. Fifty instead of a hundred.", [fig("p_sofa", x=0.35, y=0.6, h=0.7, puppet=False)],
    [kin(0, "RULE 2", 0.78, 0.2, 100, RED), kin("easy", "1 EASY DAY", 0.78, 0.4, 90, TEAL), kin("Fifty", "50, NOT 100", 0.78, 0.6, 90)], tr="dip", d=0.4),
 S_("Joints recover slower than muscles.", [act([("p_wrist", 0)])], [kin("Joints", "JOINTS: SLOWER", 0.66, 0.42, 120, RED)]),
 S_("Rule three. After two weeks, make it harder. Slower reps, or feet up.", room("W_living", pu(6, 0.8, x=0.42, y=0.68, h=0.7, until="feet")) +
    [pair("pu_decline_top", "pu_decline_bot", 6, 0.45, x=0.42, y=0.66, h=0.72, at="feet")],
    [kin(0, "RULE 3", 0.5, 0.13, 110, RED, stroke=8, until="make"), kin("make", "MAKE IT HARDER", 0.5, 0.13, 110, TEAL, stroke=8)], tr="dip", d=0.4),
 M("And if you can't do one push-up?", [act([("g_think", 0)])], "mini_shy_cut"),
 S_("Start on your knees, or with your hands on a wall or a table.", room("W_living", pair("pu_knee_top", "pu_knee_bot", 8, 0.5, x=0.42, y=0.68, h=0.7, until="wall")) +
    [pair("L_wall_a", "L_wall_b", 6, 0.55, x=0.38, y=0.6, h=0.85, at="wall")],
    [kin("knees,", "KNEES", 0.5, 0.13, 110, INK, stroke=8, until="wall"), kin("wall", "WALL OR TABLE", 0.5, 0.13, 110, TEAL, stroke=8)]),
 S_("Same muscles, less weight. A hundred wall push-ups still counts.", room("W_living", pair("L_wall_a", "L_wall_b", 12, 0.55, x=0.38, y=0.6, h=0.85)),
    [kin("Same", "SAME MUSCLES", 0.72, 0.13, 100, TEAL, stroke=8, until="hundred"), kin("hundred", "100 WALL = COUNTS", 0.72, 0.13, 100, INK, stroke=8)]),
 # ===== CTA =====
 S_("Do the day one test right now. One set, clean form. Write your number in the comments.", [act([("g_point", 0), ("g_one", "One"), ("g_point", "Write")])],
    [kin("test", "DAY 1 TEST: NOW", 0.66, 0.35, 100, TEAL, until="Write"), kin("Write", "COMMENT YOUR NUMBER", 0.66, 0.35, 90, RED)], tr="dip", d=0.4),
 S_("Then come back in thirty days and write the new one.", [act([("g_thumbs", 0), ("g_flex", "new")])], [kin("thirty", "DAY 30: NEW NUMBER", 0.66, 0.42, 90, TEAL)]),
 M("No lying. We will know.", [act([("g_flex", 0)])], "s6_mini_squint_cut"),
]

def inset_specs():
    import numpy as np
    def red_xy(n):
        a = np.array(Image.open(path(n)).convert("RGBA")).astype(int); m = (a[..., 0] > 200) & (a[..., 1] < 90) & (a[..., 2] < 90) & (a[..., 3] > 0)
        ys, xs = np.where(m); return xs.mean() / a.shape[1], ys.mean() / a.shape[0]
    rx, ry = red_xy("p_wrist"); h = 0.92; wpx = h * H * 941 / 1672; top = 0.52 * H - h * H / 2
    bent = [dict(at="bent", asset=path("p_wrist"), crop=(rx, ry, 0.22), x=0.66, y=0.62, r=0.085, bg=WHITE, grow=((0.24 * W - wpx / 2 + rx * wpx) / W, (top + ry * h * H) / H), mark="x")]
    fist = [dict(at="Wrist", asset=path("L_fist_a"), crop=(0.2, 0.74, 0.22), x=0.88, y=0.7, r=0.08, bg=WHITE, grow=(0.25, 0.8), mark="tick")]
    for s in S:
        if s.get("insets") == "BENT": s["insets"] = bent
        if s.get("insets") == "FIST": s["insets"] = fist
inset_specs()
PLAN = dict(dir=f"{HERE}/scenes_long04", words=f"{HERE}/voice/long04_cut.words.json", voice=f"{HERE}/voice/long04_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long04{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
