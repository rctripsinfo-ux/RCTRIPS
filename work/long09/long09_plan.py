# LONG 09 "Why You Can't Do a Single Pull-Up" (16:9) YELLOW DUDE STYLE (long09/STYLE.md): plain background, an icon / gag per line, fast changes
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long09/long09_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{HERE}/long09/img/{n}_al.png", f"{HERE}/long09/img/{n}_c.png", f"{HERE}/long09/img/{n}.png", f"{HERE}/long08/img/{n}_al.png", f"{HERE}/long08/img/{n}_c.png", f"{HERE}/long08/img/{n}.png", f"{HERE}/long07/img/{n}_al.png", f"{HERE}/long07/img/{n}_c.png", f"{HERE}/long07/img/{n}.png", f"{HERE}/long06/img/{n}_al.png", f"{HERE}/long06/img/{n}.png", f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
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

def WK(stand, walk, track, h=0.82, y=0.56, step=0.28, **k):  # character that walks / runs along a track, then stands in the given poses
    return dict(at=k.pop("at", 0), until=k.pop("until", None), w=wfor(stand[0][0], h), x=track[-1][1], y=y, poses=[(path(p), a) for p, a in stand],
                track=[(a, x, y) for a, x in track], walk=dict(a=path(walk + "_a"), b=path(walk + "_b"), w=wfor(walk + "_a", h * (0.8 if walk == "w_run" else 1)), dy=0.06 if walk == "w_run" else 0, step=step), **k)
WALK = "d5_walk"
CREAM = (245, 240, 230)
def PU(seq, x=0.5, h=1.0, bar=0.12, **k):  # pull-up bar poses share one canvas (bar at 25 % of its height): bar_y fixed on screen
    return act(seq, x=x, y=bar + 0.25 * h, h=h, puppet=False, **k)
def IC(n, at=0, x=0.75, y=0.45, h=0.3, until=None, **k):  # icon pop (Yellow Dude: one picture per phrase)
    return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), puppet=False, breathe=False, enter=k.pop("enter", ("pop", 0.22)), **k)
def N(at, text, x=0.75, y=0.45, size=170, color=INK, until=None): return kin(at, text, x, y, size, color, until=until, stroke=10, stroke_fill=WHITE)
CLOSE = dict(x=0.5, y=0.93, h=1.45)
def P(text, layers, kinetic=(), **k):  # plain-set scene
    k.setdefault("sfx", []); return S_(text, layers, kinetic, **k)
def card(text, num, name): return dict(text=text, poses=[], set=NAVY, tr="cut", nocap=True, kinetic=[kin(0, num, 0.5, 0.4, 120, (200, 210, 230)), kin(0.1, name, 0.5, 0.58, 120, WHITE, frm="b")],
                                    keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], sfx=[(0, "whoosh_short", .3)])
POP = lambda *ats: [(a, "pop", .3) for a in ats]
S = [
 # ===== HOOK =====
 P("You walk up to the pull-up bar.", [WK([("g_base", 0)], WALK, [(0, -0.2), (1.6, 0.5)], h=0.7, y=0.6)], keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .45)]),
 P("Everyone's watching.", [H_([("c_worried", 0)], **CLOSE), IC("i_eyes", 0.05, 0.15, 0.3, 0.22), IC("i_eyes", 0.25, 0.85, 0.25, 0.2), IC("i_phone", 0.45, 0.82, 0.62, 0.3)], sfx=POP(0.05, 0.25, 0.45)),
 P("You jump, you grab it, and nothing.", [PU([("h_hang", 0), ("p_kick_a", "nothing."), ("p_kick_b", "nothing.+0.25"), ("p_kick_a", "nothing.+0.5")], enter=("rise", 0.25))],
   keys=[(0, 1.0, .5, .5), ("nothing.", 1.0, .5, .5), ("nothing.+0.3", 1.6, .5, .25)], sfx=[(0, "whoosh_short", .3)]),
 P("You just hang there, like a wet towel.", [PU([("p_towel", 0)], x=0.35), IC("i_towel", "towel.", 0.75, 0.5, 0.5)], sfx=POP("towel.")),
 M("Twenty seconds of kicking. Zero pull-ups.", [PU([("p_kick_a", 0)] + reps("p_kick_b", "p_kick_a", 14, 0.22, 0.2), x=0.38)], "mini_laugh_cut",
   kinetic=[N("Zero", "0", 0.6, 0.35, 260, LRED)]),
 P("Here's the thing. It's not your arms.", [H_([("p_wag", 0)], **CLOSE), IC("i_noarm", "arms.", 0.8, 0.45, 0.42)], sfx=POP("arms."), keys=[(0, 1.15, .5, .4), ("E", 1.0, .5, .5)]),
 P("Most people fail the pull-up for three reasons,", [H_([("p_count", 0)], x=0.32)], [N("three", "3", 0.72, 0.42, 300, NAVY)], sfx=POP("three")),
 P("and none of them is weak biceps.", [IC("i_noarm", 0, 0.5, 0.5, 0.75)], shake=[("biceps.", .03)], sfx=POP(0)),
 P("Fix those three, and in about thirty days you can do your first one.", [H_([("g_point", 0), ("g_thumbs", "first")], x=0.28), IC("i_cal30", "thirty", 0.72, 0.4, 0.42), IC("i_trophy", "first", 0.88, 0.68, 0.3)], sfx=POP("thirty", "first")),
 P("Stay to the end for the exact plan.", [H_([("p_ominous", 0)], **CLOSE)], keys=[(0, 1.0, .5, .5), ("E", 1.3, .5, .35)]),
 # ===== REASON 1 =====
 card("Reason one.", "#1", "THE GRIP"),
 P("Your grip gives up before your back does.", [IC("i_slip", 0, 0.5, 0.5, 0.8)], shake=[("gives", .03)], sfx=POP(0), keys=[(0, 1.0, .5, .5), ("E", 1.12, .5, .5)]),
 P("If you can't hold your own body weight for thirty seconds, your hands quit first.", [PU([("p_kick_a", 0)] + reps("p_kick_b", "p_kick_a", 10, 0.3, 0.3), x=0.3, until="quit"),
   IC("i_watch", "thirty", 0.75, 0.4, 0.38), dict(at="quit", w=wfor("p_fall_c", 0.4), x=0.4, y=0.78, asset=path("p_fall_c"), puppet=False, enter=("drop", 0.2))],
   shake=[("quit", .05)], sfx=POP("thirty") + [("quit", "whoosh_big", .3)]),
 P("So start with the dead hang. Grab the bar, arms straight, and just hang.", [PU([("h_hang", 0)], x=0.5, enter=("rise", 0.25), until="Grab"),
   PU([("h_hang", 0)], x=0.5, h=1.6, bar=0.08, at="Grab")], keys=[(0, 1.0, .5, .5), ("Grab", 1.0, .5, .5), ("E", 1.05, .5, .4)], sfx=[(0, "whoosh_short", .3), ("Grab", "pop", .3)]),
 P("Thirty seconds. Three times. Every day.", [PU([("h_hang", 0)], x=0.28)],
   counters=[dict(at=0, a=0, b=30, dur=1.0, x=0.72, y=0.3, size=200, color=NAVY, label="SEC", stroke=10)], kinetic=[N("Three", "x3", 0.72, 0.58, 160, TEAL), N("Every", "EVERY DAY", 0.72, 0.78, 100, NAVY)], sfx=POP("Three", "Every")),
 M("That's it? Just hanging?", [PU([("h_hang", 0)], x=0.38)], "s6_mini_squint_cut"),
 P("Just hanging. It's harder than it looks.", [PU([("h_hang", 0), ("p_kick_a", "harder"), ("p_kick_b", "harder+0.3"), ("p_kick_a", "harder+0.6"), ("p_towel", "looks.")], x=0.5)],
   keys=[(0, 1.0, .5, .5), ("harder", 1.4, .5, .3), ("E", 1.5, .5, .3)]),
 # ===== REASON 2 =====
 card("Reason two.", "#2", "THE WRONG MUSCLES"),
 P("You pull with your arms.", [PU([("p_kick_a", 0)] + reps("p_kick_b", "p_kick_a", 6, 0.25, 0.25), x=0.5)]),
 P("But a pull-up is a back exercise.", [H_([("g_point", 0)], x=0.3)], [N("back", "BACK", 0.7, 0.42, 200, TEAL)], sfx=POP("back")),
 P("Your lats, the big wings on your back, are supposed to start the move.", [IC("i_wings", "wings", 0.5, 0.42, 0.75, z=-1), H_([("g_flex", 0)], x=0.5, y=0.6, h=0.75)],
   sfx=POP("wings") + [("wings", "chime", .3)], keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .45)]),
 P("Here's how you wake them up.", [H_([("g_think", 0)], **CLOSE)]),
 P("Hang, then pull your shoulders down, away from your ears, without bending your arms.", [PU([("h_hang", 0)] + reps("p_scap", "h_hang", 8, 0.8, 0.6), x=0.5, h=1.3, bar=0.1)],
   keys=[(0, 1.0, .5, .5), ("shoulders", 1.5, .5, .3), ("without", 1.0, .5, .5)]),
 P("It's a tiny move. Ten of those, three sets.", [PU([("h_hang", 0)] + reps("p_scap", "h_hang", 8, 0.45, 0.2), x=0.3)],
   counters=[dict(at="Ten", a=1, b=10, dur=1.0, x=0.72, y=0.35, size=200, color=NAVY, stroke=10)], kinetic=[N("three", "x3", 0.72, 0.62, 160, TEAL)], sfx=POP("three")),
 # ===== REASON 3 =====
 card("Reason three.", "#3", "THE WAY DOWN"),
 P("You only practise the way up, which you can't do yet.", [PU([("p_kick_a", 0)] + reps("p_kick_b", "p_kick_a", 10, 0.25, 0.25), x=0.35)], [N("up,", "UP", 0.75, 0.4, 200, LRED)], sfx=POP("up,")),
 P("But your muscles are stronger on the way down than on the way up.", [H_([("g_flex", 0)], x=0.3)], [N("down", "DOWN", 0.72, 0.32, 180, TEAL), N("than", "> UP", 0.72, 0.56, 160, NAVY)], sfx=POP("down", "than")),
 P("So jump to the top, chin over the bar,", [PU([("p_top", 0)], x=0.5, enter=("rise", 0.25))], sfx=[(0, "whoosh_short", .3)], keys=[(0, 1.0, .5, .5), ("chin", 1.4, .5, .25)]),
 P("and lower yourself as slowly as you can. Five seconds down.", [PU([("p_top", 0), ("p_mid", "slowly"), ("h_hang", "Five")], x=0.32)],
   counters=[dict(at="Five", a=5, b=0, dur=1.6, x=0.74, y=0.4, size=240, color=NAVY, stroke=10)]),
 P("These are called negatives, and they are the fastest way to your first pull-up.", [H_([("g_point", 0)], x=0.28), IC("i_rocket", "fastest", 0.72, 0.45, 0.55, enter=("slide_l", 0.3))],
   [N("negatives,", "NEGATIVES", 0.7, 0.15, 110, NAVY)], sfx=POP("negatives,") + [("fastest", "whoosh_big", .3)]),
 M("So I cheat on the way up?", [PU([("p_top", 0)], x=0.38)], "mini_laugh_cut"),
 P("You skip the part you can't do, and train the part you can.", [H_([("p_wag", 0), ("g_thumbs", "train")], **CLOSE)]),
 # ===== PLAN =====
 card("So here's the plan.", "THE PLAN", "30 DAYS"),
 P("Three days a week.", [IC("i_cal30", 0, 0.5, 0.45, 0.6)], [N(0.3, "3 DAYS / WEEK", 0.5, 0.88, 110, NAVY)], sfx=POP(0)),
 P("Dead hangs, three times thirty seconds.", [PU([("h_hang", 0)], x=0.3)], [N("three", "3 x 30 SEC", 0.72, 0.45, 130, NAVY)], sfx=POP("three")),
 P("Shoulder pulls, three sets of ten.", [PU([("h_hang", 0)] + reps("p_scap", "h_hang", 6, 0.4, 0.1), x=0.3)], [N("three", "3 x 10", 0.72, 0.45, 160, NAVY)], sfx=POP("three")),
 P("Negatives, three sets of three, five seconds each.", [PU([("p_top", 0), ("p_mid", 0.8), ("h_hang", 1.6), ("p_top", 2.2), ("p_mid", 3.0), ("h_hang", 3.8)], x=0.3)],
   [N("three", "3 x 3", 0.72, 0.4, 160, NAVY), N("five", "5 SEC DOWN", 0.72, 0.62, 100, TEAL)], sfx=POP("three", "five")),
 P("And a bonus. Rows under a sturdy table, three sets of eight.", [act([("r_row_a_c", 0)] + reps("r_row_b_c", "r_row_a_c", 10, 0.5, 0.8), x=0.38, y=0.6, h=0.5, puppet=False)],
   [N("bonus.", "BONUS", 0.5, 0.15, 120, LRED), N("three", "3 x 8", 0.82, 0.45, 150, NAVY)], sfx=POP("bonus.", "three")),
 P("Every week, hang a little longer, and lower a little slower.", [PU([("h_hang", 0), ("p_mid", "lower"), ("h_hang", "slower.")], x=0.3), IC("i_watch", "longer,", 0.74, 0.45, 0.4)], sfx=POP("longer,")),
 # ===== RESULT =====
 P("Week one, the hang gets easy.", [PU([("h_hang", 0)], x=0.32)], [N(0, "WEEK 1", 0.72, 0.4, 140, NAVY)], sfx=POP(0)),
 P("Week two, the negatives get slower.", [PU([("p_mid", 0), ("h_hang", 1.2)], x=0.32)], [N(0, "WEEK 2", 0.72, 0.4, 140, NAVY)], sfx=POP(0)),
 P("Week three, you can stop halfway.", [PU([("p_mid", 0)], x=0.32, shiver=[(0.8, 9.0)])], [N(0, "WEEK 3", 0.72, 0.4, 140, NAVY)], sfx=POP(0)),
 P("And around week four,", [PU([("h_hang", 0)], x=0.5), IC("i_drum", 0, 0.85, 0.7, 0.28)], keys=[(0, 1.0, .5, .5), ("E", 1.25, .5, .3)], sfx=POP(0)),
 P("you pull, and your chin goes over the bar.", [PU([("h_hang", 0), ("p_mid", "pull,"), ("p_top", "chin")], x=0.5)],
   particles=[dict(at="chin", x=0.5, y=0.2, spread=0.4)], shake=[("chin", .03)], sfx=[("chin", "chime", .5), ("chin", "pop", .4)], keys=[(0, 1.2, .5, .3), ("chin", 1.0, .5, .5)]),
 M("Everyone's watching again.", [PU([("p_top", 0)], x=0.4), IC("i_clap", 0.1, 0.12, 0.35, 0.25), IC("i_eyes", 0.3, 0.15, 0.7, 0.2)], "mini_laugh_cut"),
 P("This time, that's a good thing.", [PU([("p_top", 0)], x=0.32), IC("i_trophy", "good", 0.74, 0.45, 0.45)], sfx=POP("good")),
 P("How many pull-ups can you do right now? Zero counts. Tell me in the comments.", [H_([("g_point", 0)], **CLOSE)],
   [N("Zero", "0 COUNTS", 0.5, 0.15, 120, NAVY)], sfx=POP("Zero"), keys=[(0, 1.1, .5, .45), ("E", 1.0, .5, .5)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long09", words=f"{HERE}/voice/long09_cut.words.json", voice=f"{HERE}/voice/long09_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=20, sfx_db=14, duck=False, set=CREAM,
            scenes=S, cap_mode="none", lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05, text_overlay=True, dip_color=(10, 12, 18))
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long09{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
