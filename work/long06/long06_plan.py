# LONG 06 "How Skinny Guys Beat Big Guys" (16:9) STORY format, THE LONG METHOD; helpers from long04/05
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long06/long06_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{HERE}/long06/img/{n}_al.png", f"{HERE}/long06/img/{n}.png", f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
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

# ---------- long 06: story staging ----------
NAVY = (30, 42, 72)
def clue(text, big, small):
    return dict(text=text, poses=[], set=NAVY, tr="cut", nocap=True, kinetic=[kin(0, big, 0.5, 0.42, 190, WHITE), kin(0.12, small, 0.5, 0.63, 84, (120, 200, 196), frm="b")],
                keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], sfx=[(0, "whoosh_short", .3)])
def BK(n, *layers): return [world(n)] + list(layers)
def H_(seq, x=0.3, y=0.56, h=0.82, **k): return act(seq, x=x, y=y, h=h, **k)
def K_(seq, x=0.7, y=0.56, h=0.82, **k): return act(seq, x=x, y=y, h=h, **k)
def AW(seq, h=0.66, **k): return act(seq, x=0.5, y=0.6, h=h, puppet=False, **k)
def T(at, text, color=WHITE, x=0.5, y=0.1, size=100, until=None): return kin(at, text, x, y, size, color, until=until, stroke=10, stroke_fill=INK)
def loopk(a, b, n=10, step=0.5, x=0.5, y=0.56, h=0.82, **k): return pair(a, b, n, step, x=x, y=y, h=h, **k)
SLOW = [(0, 1.0, .5, .55), ("E", 1.12, .5, .5)]
XR = lambda seq, **k: dict(at=0, w=1.0, x=0.5, y=0.5, poses=[(path(p), a) for p, a in seq], z=-1, puppet=False, breathe=False, **k)

S = [
 # ===== THE LOSS =====
 S_("I weigh ninety kilos. I train six days a week.", BK("bk_armgym", H_([("g_flex", 0), ("g_hips", "train")], x=0.3)),
    [T("ninety", "90 KG", WHITE, 0.72, 0.3, 150), T("six", "6 DAYS / WEEK", WHITE, 0.72, 0.5, 90)], keys=[(0, 1.3, .3, .4), (0.4, 1.0, .5, .5), ("E", 1.05, .5, .5)],
    sfx=[(0, "whoosh_big", .2), ("ninety", "pop", .3)]),
 S_("And last month, I lost an arm-wrestling match to a guy who weighs sixty.", BK("bk_armgym", AW([("aw_base", 0), ("aw_shake", "arm-wrestling"), ("aw_kwin", "sixty.")])),
    [T("lost", "I LOST", (230, 90, 90), 0.5, 0.1, 120, until="sixty."), T("sixty.", "TO A 60 KG GUY", WHITE, 0.5, 0.1, 110)], shake=[("sixty.", .05)], keys=SLOW, sfx=[("sixty.", "whoosh_short", .3)]),
 S_("His name is Kabir.", BK("bk_armgym", K_([("k_base", 0), ("k_calm", "Kabir.")], x=0.62, enter=("slide_r", 0.35))), [T("Kabir.", "KABIR", WHITE, 0.3, 0.42, 160)], sfx=[("Kabir.", "pop", .3)]),
 S_("Skinny arms. No pump. No supplements.", BK("bk_armgym", K_([("k_calm", 0)], x=0.62)),
    [T(0, "SKINNY ARMS", WHITE, 0.28, 0.3, 90), T("pump.", "NO PUMP", WHITE, 0.28, 0.48, 90), T("supplements.", "NO SUPPLEMENTS", WHITE, 0.28, 0.66, 90)],
    sfx=[(0, "pop", .3), ("pump.", "pop", .3), ("supplements.", "pop", .3)]),
 S_("He beat me in four seconds.", BK("bk_armgym", AW([("aw_base", 0), ("aw_kwin", "seconds.")])), [T("four", "0:04", (230, 90, 90), 0.86, 0.18, 150)],
    rings=[dict(at="four", x=0.86, y=0.5, r=0.11, dur=0.8, max=4, unit="SEC")], keys=SLOW, shake=[("seconds.", .04)]),
 S_("So I asked him to do it again. He beat me again.", BK("bk_armgym", AW([("aw_base", 0), ("aw_shake", "again."), ("aw_kwin", "beat")])), [T("again.#2", "AGAIN.", (230, 90, 90), 0.5, 0.1, 130)],
    tr="dip", d=0.4, shake=[("again.#2", .04)]),
 S_("Then he did twenty pull-ups like it was nothing.", BK("bk_garage", loopk("k_pull_a", "k_pull_b", 16, 0.3, x=0.62, h=0.95), H_([("g_shock", "pull-ups")], x=0.22, h=0.7, at="pull-ups")),
    counters=[dict(at="twenty", a=0, b=20, dur=1.6, x=0.86, y=0.24, size=150, color=WHITE, stroke=10)], sfx=[("nothing.", "pop", .3)]),
 S_("I couldn't sleep that night.", BK("bk_night", act([("bed_wake", 0)], x=0.5, y=0.62, h=0.6, puppet=False)), [T("sleep", "CAN'T SLEEP", WHITE, 0.5, 0.12, 100)], tr="dip", d=0.6,
    keys=[(0, 1.0, .5, .55), ("E", 1.08, .5, .55)]),
 S_("How is a guy with half my muscle stronger than me?", BK("bk_night", H_([("g_think", 0), ("p_temple", "half"), ("g_shrug", "stronger")], x=0.5, h=0.8)),
    [T("half", "HALF THE MUSCLE", WHITE, 0.5, 0.1, 90, until="stronger"), T("stronger", "STRONGER?", (230, 90, 90), 0.5, 0.1, 120)]),
 S_("The answer is not muscle. It's three things almost nobody trains.", BK("bk_night", H_([("p_wag", 0), ("p_count", "three")], x=0.28)),
    [T("not", "NOT MUSCLE", WHITE, 0.7, 0.3, 110), T("three", "3 THINGS", (120, 200, 196), 0.7, 0.5, 120)], sfx=[("three", "pop", .3)]),
 S_("And by the end of this video, I'll show you what happened in the rematch.", BK("bk_armgym", AW([("aw_base", 0), ("aw_shake", "rematch.")], h=0.6)),
    [T("rematch.", "THE REMATCH?", WHITE, 0.5, 0.1, 120)], keys=[(0, 1.0, .5, .55), ("E", 1.15, .5, .5)], shake=[("rematch.", .03)]),
 # ===== CLUE 1 =====
 clue("Here's the first thing I learned.", "CLUE #1", "THE WIRES"),
 S_("A muscle doesn't move by itself.", BK("bk_garage", H_([("g_one", 0), ("g_cross", "itself.")], x=0.72, flip=True)), [T("itself.", "NOT BY ITSELF", WHITE, 0.3, 0.42, 100)]),
 S_("Your brain sends a signal down your nerves, and that signal decides how much of the muscle actually fires.", [act([("p_temple", 0), ("p_brain", "brain"), ("p_flexglow", "fires.")], x=0.24, h=0.92)],
    [kin("brain", "BRAIN", 0.68, 0.25, 110, TEAL), kin("nerves,", "NERVES", 0.68, 0.45, 110, TEAL), kin("fires.", "HOW MUCH FIRES", 0.68, 0.65, 100, RED)]),
 S_("Every muscle is made of thousands of little units.", [XR([("xr_half", 0)])], [T("thousands", "1000s OF UNITS", WHITE, 0.5, 0.1, 100)], tr="dip", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.1, .45, .5)]),
 S_("A beginner can only switch on part of them at the same time. The rest just sit there.", [XR([("xr_half", 0)])],
    [T("part", "ONLY PART FIRES", (240, 170, 60), 0.5, 0.1, 100, until="rest"), T("rest", "THE REST: ASLEEP", WHITE, 0.5, 0.1, 100)], keys=[(0, 1.1, .45, .5), ("E", 1.2, .45, .5)]),
 S_("Years of heavy lifting teach your nervous system to switch on more of them, faster, all at once.", [XR([("xr_half", 0), ("xr_full", "more")])],
    [T("more", "MORE", WHITE, 0.5, 0.1, 120, until="faster,"), T("faster,", "FASTER", WHITE, 0.5, 0.1, 120, until="all"), T("all", "ALL AT ONCE", (240, 170, 60), 0.5, 0.1, 120)],
    particles=[dict(at="all", x=0.5, y=0.45, spread=0.4)], sfx=[("more", "pop", .3), ("faster,", "pop", .3), ("all", "chime", .4)]),
 S_("Kabir's muscles are smaller. But when he pulls, almost all of it fires.", BK("bk_garage", loopk("k_pull_a", "k_pull_b", 10, 0.5, x=0.66, h=0.95)),
    [T("smaller.", "SMALLER", WHITE, 0.28, 0.3, 110), T("all", "ALL OF IT FIRES", (240, 170, 60), 0.28, 0.5, 90)]),
 S_("Mine had more muscle and a worse connection.", BK("bk_garage", H_([("g_flex", 0), ("g_facepalm", "worse")], x=0.32)),
    [T("more", "MORE MUSCLE", WHITE, 0.72, 0.3, 100), T("worse", "WORSE CONNECTION", (230, 90, 90), 0.72, 0.5, 90)]),
 M("So you bought a sports car and never learned to drive.", BK("bk_garage", H_([("g_facepalm", 0)], x=0.32)), "mini_laugh_cut"),
 S_("Exactly.", BK("bk_garage", H_([("g_thumbs", 0)], x=0.5, y=0.86, h=1.4)), [T(0, "EXACTLY.", WHITE, 0.5, 0.1, 130)]),
 # ===== CLUE 2 =====
 clue("So I asked Kabir how he trains.", "CLUE #2", "THE TRAINING"),
 S_("His answer made me feel stupid.", BK("bk_garage", K_([("k_calm", 0)], x=0.66), H_([("g_facepalm", "stupid.")], x=0.3)), [T("stupid.", "STUPID.", WHITE, 0.5, 0.1, 120)]),
 S_("I train like a bodybuilder. Ten to fifteen reps, chase the burn, chase the pump.", BK("bk_garage", loopk("curl_a", "curl_b", 12, 0.3, x=0.32, h=0.85)),
    [T("bodybuilder.", "BODYBUILDER", WHITE, 0.72, 0.25, 100), T("Ten", "10-15 REPS", (240, 170, 60), 0.72, 0.45, 110), T("pump.", "THE PUMP", WHITE, 0.72, 0.65, 100)]),
 S_("Kabir does the opposite. Heavy weight. Three to five reps. Long rest. He never chases the burn.", BK("bk_garage", act([("k_lift_a", 0), ("k_lift_b", "Heavy"), ("k_lift_a", "Three+0.4"), ("k_lift_b", "five+0.2"), ("k_lift_a", "Long"), ("k_calm", "rest.")], x=0.66, h=0.85, puppet=False)),
    [T("Heavy", "HEAVY", WHITE, 0.28, 0.25, 110), T("Three", "3-5 REPS", (120, 200, 196), 0.28, 0.45, 110), T("Long", "LONG REST", WHITE, 0.28, 0.65, 100)],
    rings=[dict(at="Long", x=0.28, y=0.85, r=0.08, dur=1.2, max=3, unit="MIN")]),
 S_("High reps mostly build size. Heavy low reps mostly build strength.", [act([("curl_b", 0), ("k_lift_b", "Heavy")], x=0.24, h=0.85, puppet=False)],
    bars=[dict(at=0, x=0.66, y=0.82, w=0.34, h=0.5, values=[10, 4], labels=["SIZE", "STRENGTH"], stagger=1.6, show_values=False, hi_last=True, hi_color=TEAL, color=RED)],
    kinetic=[kin(0, "HIGH REPS = SIZE", 0.66, 0.12, 80, RED, until="Heavy"), kin("Heavy", "LOW REPS = STRENGTH", 0.66, 0.12, 80, TEAL)], tr="dip", d=0.4),
 S_("Both build muscle, but only one teaches your body to lift something really heavy.", BK("bk_garage", act([("k_lift_a", 0), ("k_lift_b", "lift")], x=0.5, h=0.85, puppet=False)),
    [T("one", "ONLY ONE TEACHES HEAVY", WHITE, 0.5, 0.1, 90)]),
 S_("Strength is a skill. You get good at what you practice.", BK("bk_garage", H_([("p_snap", 0), ("p_temple", "practice.")], x=0.5, y=0.86, h=1.4)),
    [T("skill.", "STRENGTH = SKILL", WHITE, 0.5, 0.1, 110)]),
 S_("I practiced getting a pump. He practiced being strong.", BK("bk_garage", loopk("curl_a", "curl_b", 6, 0.3, x=0.28, h=0.8, until="He"), act([("k_lift_b", 0)], x=0.7, h=0.85, at="He", puppet=False, enter=("slide_r", 0.3))),
    [T("pump.", "ME: PUMP", (240, 170, 60), 0.5, 0.1, 100, until="He"), T("He", "HIM: STRONG", (120, 200, 196), 0.5, 0.1, 100)]),
 # ===== CLUE 3 =====
 clue("The third clue was on his hands.", "CLUE #3", "THE CABLES"),
 S_("His fingers were thick. His forearms looked like cables.", BK("bk_climb", loopk("k_climb_a", "k_climb_b", 8, 0.6, x=0.68, h=0.95)), [T("fingers", "THICK FINGERS", WHITE, 0.27, 0.3, 80), T("cables.", "CABLE FOREARMS", WHITE, 0.27, 0.45, 80)],
    keys=[(0, 1.0, .5, .5), ("E", 1.1, .68, .4)]),
 S_("Kabir grew up climbing rocks", BK("bk_climb", loopk("k_climb_a", "k_climb_b", 6, 0.45, x=0.68, h=0.95)), [T("climbing", "CLIMBING ROCKS", WHITE, 0.28, 0.12, 80)]),
 S_("and carrying bricks on his uncle's construction site.", BK("bk_site", loopk("k_bricks_a", "k_bricks_b", 10, 0.4, x=0.5, h=0.85)), [T("bricks", "CARRYING BRICKS", WHITE, 0.5, 0.1, 100)], tr="dip", d=0.3),
 S_("Years of that made his tendons strong.", BK("bk_site", loopk("k_bricks_a", "k_bricks_b", 6, 0.4, x=0.5, h=0.85)), [T("tendons", "STRONG TENDONS", (120, 200, 196), 0.5, 0.1, 110)]),
 S_("Tendons are the cables that connect muscle to bone. Stiffer cables pass force faster, with less lost on the way.", [XR([("xr_tendon", 0)])],
    [T("cables", "TENDON = CABLE", WHITE, 0.3, 0.12, 100, until="Stiffer"), T("Stiffer", "STIFFER = FASTER FORCE", (240, 170, 60), 0.4, 0.12, 90)], tr="dip", d=0.4,
    keys=[(0, 1.0, .5, .5), ("E", 1.12, .6, .5)]),
 S_("Muscle grows in weeks. Tendons take months and years.", BK("bk_studio", H_([("g_one", 0), ("p_count", "Tendons")], x=0.3)),
    [T("weeks.", "MUSCLE: WEEKS", WHITE, 0.72, 0.3, 100), T("months", "TENDONS: YEARS", (240, 170, 60), 0.72, 0.5, 100)]),
 S_("That's why the strongest grip in the gym often belongs to the guy who looks the least impressive.", BK("bk_studio", K_([("k_base", 0), ("k_calm", "least")], x=0.5, y=0.86, h=1.4)),
    [T("strongest", "STRONGEST GRIP", WHITE, 0.5, 0.1, 100, until="least"), T("least", "LEAST IMPRESSIVE", (120, 200, 196), 0.5, 0.1, 100)]),
 # ===== GENETICS =====
 S_("And there's one thing neither of us can change.", BK("bk_studio", H_([("g_think", 0)], x=0.3), K_([("k_calm", 0)], x=0.7)), [T("neither", "CAN'T CHANGE", WHITE, 0.5, 0.1, 110)], tr="dip", d=0.4),
 S_("Leverage.", BK("bk_studio", H_([("p_ominous", 0)], x=0.5, y=0.86, h=1.4)), [T(0, "LEVERAGE", (240, 170, 60), 0.5, 0.1, 150)], keys=DRIFT + [(0.1, 1.04, .5, .5), (0.2, 1.1, .5, .45)]),
 S_("Shorter forearms and tendons that attach a little further from the joint give some people a natural advantage, like a longer handle on a wrench.",
    BK("bk_studio", K_([("k_point", 0), ("k_calm", "natural")], x=0.3)),
    [T("Shorter", "SHORT FOREARM", WHITE, 0.7, 0.25, 100), T("further", "TENDON FURTHER OUT", WHITE, 0.7, 0.45, 90), T("wrench.", "= LONGER WRENCH", (240, 170, 60), 0.7, 0.65, 100)]),
 S_("Kabir has short forearms. In arm wrestling, that's a cheat code.", BK("bk_armgym", AW([("aw_base", 0), ("aw_kwin", "cheat")])), [T("cheat", "CHEAT CODE", (240, 170, 60), 0.5, 0.1, 130)], shake=[("code.", .03)]),
 S_("You can't train that. But the first three, you can.", BK("bk_studio", H_([("p_wag", 0), ("g_thumbs", "But")], x=0.3)),
    [T("can't", "CAN'T TRAIN", (230, 90, 90), 0.72, 0.3, 100), T("first", "THE FIRST 3: YOU CAN", (120, 200, 196), 0.72, 0.5, 80)]),
 # ===== PLAN =====
 clue("So I made a plan. Eight weeks. Three changes.", "THE PLAN", "8 WEEKS"),
 S_("One. Heavy and low. Three days a week, three to five reps on the big lifts, with three minutes of rest.", BK("bk_garage", act([("pu_top", 0)] + reps("pu_top", "pu_bot", 8, 0.9, 0.5), x=0.42, y=0.7, h=0.62, puppet=False)),
    [T(0, "1. HEAVY + LOW", WHITE, 0.5, 0.1, 110, until="Three"), T("Three", "3x / WEEK  ·  3-5 REPS", WHITE, 0.5, 0.1, 90)], rings=[dict(at="minutes", x=0.86, y=0.3, r=0.1, dur=1.0, max=3, unit="MIN")]),
 S_("Two. Grip every day.", BK("bk_garage", act([("h_hang", 0), ("h_towel", "Grip")], x=0.5, y=0.53, h=0.98, puppet=False)), [T(0, "2. GRIP DAILY", WHITE, 0.5, 0.1, 110)]),
 S_("Dead hangs, towel hangs, farmer carries.", BK("bk_garage", act([("h_hang", 0), ("h_towel", "towel")], x=0.3, y=0.53, h=0.98, puppet=False, until="farmer"), loopk("h_farmer_a", "h_farmer_b", 6, 0.35, x=0.55, h=0.8, at="farmer")),
    [T(0, "DEAD HANGS", WHITE, 0.72, 0.2, 90, until="towel"), T("towel", "TOWEL HANGS", WHITE, 0.72, 0.2, 90, until="farmer"), T("farmer", "FARMER CARRIES", WHITE, 0.5, 0.1, 100)]),
 S_("Three. Practice the actual skill. Twice a week, I arm-wrestled anyone who would say yes.", BK("bk_armgym", AW([("aw_base", 0), ("aw_shake", "actual"), ("aw_kwin", "Twice"), ("aw_shake", "anyone"), ("aw_hwin", "yes.")], h=0.6)),
    [T(0, "3. PRACTICE THE SKILL", WHITE, 0.5, 0.1, 100)]),
 M("You lost to the gym's receptionist.", BK("bk_armgym", AW([("aw_kwin", 0)], h=0.55)), "mini_laugh_cut"),
 S_("Twice. We don't talk about it.", BK("bk_armgym", H_([("g_facepalm", 0)], x=0.5, y=0.86, h=1.4)), [T(0, "TWICE.", (230, 90, 90), 0.5, 0.1, 130)]),
 # ===== REMATCH =====
 clue("Eight weeks later.", "THE REMATCH", "8 WEEKS LATER"),
 S_("Same table. Same guy.", BK("bk_armgym", H_([("g_cross", 0)], x=0.28), K_([("k_calm", 0)], x=0.72)), [T(0, "SAME TABLE", WHITE, 0.5, 0.1, 100, until="Same#2"), T("Same#2", "SAME GUY", WHITE, 0.5, 0.1, 100)],
    keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .45)]),
 S_("He went first. I didn't move.", BK("bk_armgym", AW([("aw_base", 0), ("aw_shake", "went")])), [T("didn't", "I DIDN'T MOVE", WHITE, 0.5, 0.1, 110)], keys=SLOW, shake=[("went", .02)]),
 S_("Five seconds. Ten seconds.", BK("bk_armgym", AW([("aw_shake", 0)], shiver=[(0, "seconds.#2+1")])), [T(0, "0:05", WHITE, 0.5, 0.1, 140, until="Ten"), T("Ten", "0:10", (240, 170, 60), 0.5, 0.1, 140)],
    keys=[(0, 1.05, .5, .5), ("E", 1.25, .5, .45)]),
 S_("Fifteen seconds in, I felt it.", BK("bk_armgym", AW([("aw_shake", 0)], shiver=[(0, "it.+1")])), [T(0, "0:15", (230, 90, 90), 0.5, 0.1, 150)], keys=[(0, 1.25, .5, .45), ("E", 1.4, .5, .42)]),
 S_("Everything fired at once.", [XR([("xr_half", 0), ("xr_full", "fired")])], [T("fired", "EVERYTHING FIRED", (240, 170, 60), 0.5, 0.1, 110)], particles=[dict(at="fired", x=0.5, y=0.45, spread=0.5)],
    sfx=[("fired", "whoosh_big", .3)], keys=[(0, 1.0, .5, .5), ("E", 1.15, .45, .5)]),
 S_("And I won.", BK("bk_armgym", AW([("aw_shake", 0), ("aw_hwin", "won.")])), [T("won.", "I WON.", (120, 200, 196), 0.5, 0.1, 150)], shake=[("won.", .06)],
    particles=[dict(at="won.", x=0.5, y=0.3, spread=0.5)], sfx=[("won.", "chime", .5)]),
 S_("Then Kabir pointed at the pull-up bar and said: best of three.", BK("bk_garage", K_([("k_shake", 0), ("k_point", "pointed")], x=0.55, h=0.85)), [T("best", "BEST OF THREE?", WHITE, 0.5, 0.1, 110)]),
 S_("I lost that one. I'm still not a fan of pull-ups.", BK("bk_garage", loopk("k_pull_a", "k_pull_b", 10, 0.3, x=0.68, h=0.95), H_([("g_facepalm", 0)], x=0.26, h=0.75)),
    [T("lost", "LOST.", (230, 90, 90), 0.28, 0.12, 120)], counters=[dict(at=0, a=0, b=20, dur=2.0, x=0.86, y=0.24, size=130, color=WHITE, stroke=10)]),
 # ===== LESSON =====
 S_("Here's what I learned.", BK("bk_rooftop", H_([("g_think", 0)], x=0.3), K_([("k_calm", 0)], x=0.7)), [T(0, "THE LESSON", WHITE, 0.5, 0.1, 120)], tr="dip", d=0.6),
 S_("Muscle is the engine. Your nerves are the driver, your tendons are the cables, and your training decides which one you build.", BK("bk_rooftop", H_([("g_flex", 0), ("p_temple", "nerves"), ("p_wrist", "tendons"), ("g_point", "training")], x=0.3)),
    [T("engine.", "MUSCLE = ENGINE", WHITE, 0.72, 0.2, 90), T("driver,", "NERVES = DRIVER", (240, 170, 60), 0.72, 0.38, 90), T("cables,", "TENDONS = CABLES", (120, 200, 196), 0.72, 0.56, 90),
     T("training", "TRAINING DECIDES", WHITE, 0.72, 0.74, 90)], sfx=[("engine.", "pop", .3), ("driver,", "pop", .3), ("cables,", "pop", .3)]),
 S_("If you want to look strong, chase the pump. If you want to be strong, lift heavy, train your grip, and practice the skill.", BK("bk_rooftop", H_([("g_flex", 0)], x=0.3), K_([("k_calm", 0), ("k_lift_b", "lift")], x=0.72)),
    [T("look", "LOOK STRONG: PUMP", WHITE, 0.5, 0.08, 90, until="be"), T("be", "BE STRONG: HEAVY + GRIP + SKILL", (120, 200, 196), 0.5, 0.08, 80)]),
 S_("Tell me in the comments: have you ever lost to a skinny guy? Be honest.", BK("bk_rooftop", H_([("g_point", 0)], x=0.3), K_([("k_shake", 0)], x=0.72)),
    [T("comments:", "LOST TO A SKINNY GUY?", WHITE, 0.5, 0.08, 100), T("honest.", "BE HONEST", (240, 170, 60), 0.5, 0.2, 90)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long06", words=f"{HERE}/voice/long06_cut.words.json", voice=f"{HERE}/voice/long06_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=20, sfx_db=16, duck=False, set=TINT,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05, text_overlay=True)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long06{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
