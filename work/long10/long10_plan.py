# LONG 10 "Which Body Level Are You? (The Home V-Taper Test)" (16:9) Yellow Dude style: plain set, icon per line, lineup of 5 levels, motion
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long10/long10_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{HERE}/long10/img/{n}_al.png", f"{HERE}/long10/img/{n}_c.png", f"{HERE}/long10/img/{n}.png", f"{HERE}/long09/img/{n}_al.png", f"{HERE}/long09/img/{n}_c.png", f"{HERE}/long09/img/{n}.png", f"{HERE}/long08/img/{n}_al.png", f"{HERE}/long08/img/{n}_c.png", f"{HERE}/long08/img/{n}.png", f"{HERE}/long07/img/{n}_al.png", f"{HERE}/long07/img/{n}_c.png", f"{HERE}/long07/img/{n}.png", f"{HERE}/long06/img/{n}_al.png", f"{HERE}/long06/img/{n}.png", f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
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
def H_(seq, x=0.3, y=0.7, h=1.15, **k): return act(seq, x=x, y=y, h=h, **k)  # bigger, cropped at the knees (Yellow Dude framing)
def INS(n, at, crop, x=0.8, y=0.32, r=0.11, mark=None, until=None): return dict(at=at, until=until, asset=path(n), crop=crop, x=x, y=y, r=r, mark=mark, bg=(226, 234, 244))
def PU(seq, x=0.5, h=1.5, bar=0.08, **k):  # pull-up bar poses share one canvas (bar at 25 % of its height): bar_y fixed on screen
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
SOFT = (222, 236, 240)  # plain light-teal set (fuller look than cream, per the Yellow Dude comparison)
LX = [0.11, 0.305, 0.5, 0.695, 0.89]
def LINE(hi=None, at=0, h=0.55, y=0.66, stagger=0.0, dim=0.3):  # the 5 body levels side by side; hi = highlighted level (1-5)
    return [dict(at=(at + i * stagger) if stagger else at, w=wfor(f"v{i+1}", h * (1.12 if hi == i + 1 else 1)), x=LX[i], y=y, asset=path(f"v{i+1}"),
                 alpha=1.0 if hi in (None, i + 1) else dim, puppet=hi == i + 1, enter=("rise", 0.25) if stagger else ("cut", 0)) for i in range(5)]
def LV(text, n, ratio, name, icon=None, ic_at=0):
    L = LINE(hi=n) + ([IC(icon, ic_at, LX[n - 1] + (0.12 if n < 5 else -0.12), 0.3, 0.14)] if icon else [])
    return P(text, L, [N(0, f"LEVEL {n}", 0.5, 0.1, 130, NAVY), N(0.5, ratio, 0.5, 0.21, 100, TEAL), N(1.2, name, 0.5, 0.3, 90, RED)],
             sfx=[(0, "es_pop", .3), (1.2, "es_ding", .25)], keys=[(0, 1.0, .5, .5), ("E", 1.12, LX[n - 1], .5)])
PSH = lambda n=10, step=0.3, **k: act([("pu_top", 0)] + reps("pu_bot", "pu_top", n, step, 0.3), **{"h": 0.5, "y": 0.62, "x": 0.5, "puppet": False, **k})
S = [
 # ===== HOOK =====
 P("Grab a tape measure.", [WK([("m_shoulder", 0)], WALK, [(0, -0.2), (1.0, 0.32)], h=1.0, y=0.6), IC("i_tape_c", 0.3, 0.74, 0.45, 0.32)], sfx=[(0, "es_whoosh", .3), (0.3, "es_pop", .3)]),
 P("In the next three minutes, you'll know exactly what your body level is.", LINE(stagger=0.35), [N("level", "YOUR LEVEL?", 0.5, 0.12, 150, NAVY)],
   sfx=[(0, "es_pop2", .3), (0.35, "es_pop2", .3), (0.7, "es_pop2", .3), (1.05, "es_pop2", .3), (1.4, "es_pop2", .3), ("level", "es_ding", .3)]),
 P("Most guys train chest and abs all year, and still look like a rectangle in a t-shirt.", [H_([("v1", 0)], x=0.3, y=0.66, h=1.1), IC("i_shirt_c", "t-shirt.", 0.72, 0.45, 0.4)],
   [N("rectangle", "RECTANGLE?", 0.72, 0.15, 120, RED)], sfx=[("rectangle", "es_boing", .3), ("t-shirt.", "es_pop", .3)]),
 M("Hey. Rectangles are a valid shape.", [H_([("v1", 0)], x=0.35, y=0.66, h=1.1)], "mini_laugh_cut"),
 P("It's not your chest. It's two muscles almost nobody trains at home.", [H_([("p_wag", 0)], **CLOSE)], [N("two", "2 MUSCLES", 0.5, 0.12, 140, RED)],
   sfx=[("two", "es_impact", .25)], keys=[(0, 1.15, .5, .4), ("E", 1.0, .5, .5)]),
 P("Stay to the end, and you'll get the exact plan to move up a level.", [H_([("p_ominous", 0)], **CLOSE)], keys=[(0, 1.0, .5, .5), ("E", 1.3, .5, .35)], sfx=[(0, "es_rise", .2)]),
 # ===== THE TEST =====
 card("Here's the test.", "THE TEST", "2 MEASUREMENTS"),
 P("Measure around your shoulders at the widest point.", [H_([("m_shoulder", 0)], x=0.35, y=0.72, h=1.25), IC("i_tape_c", 0, 0.78, 0.6, 0.2)], [N("shoulders", "SHOULDERS", 0.74, 0.18, 120, NAVY)],
   insets=[INS("m_shoulder", "widest", (0.5, 0.28, 0.4), 0.76, 0.42, r=0.12, mark="tick")], sfx=[("shoulders", "es_pop", .3)]),
 P("Then measure your waist at your belly button.", [H_([("m_waist", 0)], x=0.35, y=0.72, h=1.25)], [N("waist", "WAIST", 0.74, 0.18, 140, NAVY)],
   insets=[INS("m_waist", "belly", (0.5, 0.52, 0.35), 0.76, 0.45, r=0.12, mark="tick")], sfx=[("waist", "es_pop", .3)]),
 P("Divide shoulders by waist.", [IC("i_calc_c", 0, 0.5, 0.5, 0.45)], [N(0.2, "SHOULDERS / WAIST", 0.5, 0.13, 120, NAVY)], sfx=[(0, "es_click", .4), (0.4, "es_click", .4)]),
 P("That number is your level.", LINE(stagger=0.18), [N("level.", "= YOUR LEVEL", 0.5, 0.12, 130, TEAL)], sfx=[(0, "es_whoosh", .3)]),
 # ===== THE LEVELS =====
 LV("Level one. Under one point two. Shoulders and waist almost the same. From the front, you look like a box.", 1, "UNDER 1.2", "THE RECTANGLE"),
 LV("Level two. One point two to one point three. There's a hint of a V, but only when you stand up straight.", 2, "1.2 - 1.3", "THE HINT"),
 LV("Level three. One point three to one point four. A clear V in a t-shirt. This is where most people who train for a year end up.", 3, "1.3 - 1.4", "THE ATHLETE", "i_shirt_c", "clear"),
 LV("Level four. One point four to one point five. Wide shoulders, narrow waist. People ask if you swim.", 4, "1.4 - 1.5", "THE SWIMMER", "i_goggles_c", "swim."),
 LV("Level five. Around one point six. The comic book shape. Rare, but you can get close at home.", 5, "ABOUT 1.6", "THE SUPERHERO", "i_cape_c", "comic"),
 M("I measured. I'm a level one point one.", LINE(hi=1), "mini_shy_cut", kinetic=[N("point", "1.1", 0.5, 0.12, 200, RED)]),
 P("Then you have the most room to grow.", [H_([("v1", 0), ("v3", "room")], x=0.5, y=0.66, h=1.1)], [N("grow.", "ROOM TO GROW", 0.5, 0.12, 130, TEAL)],
   particles=[dict(at="grow.", x=0.5, y=0.3, spread=0.3)], sfx=[("room", "es_whoosh2", .3), ("grow.", "es_chime", .3)]),
 # ===== WHY STUCK =====
 card("Here's why most people get stuck.", "WHY YOU'RE STUCK", "3 PARTS"),
 P("A V-taper is made of three things: wide shoulders, a wide back, and a narrow waist.", [H_([("v5", 0)], x=0.5, y=0.66, h=1.15)],
   [N("shoulders,", "WIDE SHOULDERS", 0.2, 0.3, 80, NAVY), N("back,", "WIDE BACK", 0.8, 0.3, 80, NAVY), N("narrow", "NARROW WAIST", 0.2, 0.6, 80, TEAL)],
   sfx=[("shoulders,", "es_pop", .3), ("back,", "es_pop", .3), ("narrow", "es_pop", .3)]),
 P("Push-ups build the front of your shoulders and your chest.", [PSH(10, 0.3)], [N("front", "FRONT + CHEST", 0.5, 0.15, 120, NAVY)], sfx=[("front", "es_pop", .3)]),
 P("But the width comes from the side of your shoulders, and from your lats, the wings on your back.", [IC("i_wings", "wings", 0.5, 0.45, 0.7, z=-1), H_([("v4", 0)], x=0.5, y=0.68, h=1.05)],
   [N("side", "SIDE DELTS", 0.18, 0.28, 90, TEAL), N("lats,", "LATS", 0.82, 0.28, 110, TEAL)], sfx=[("side", "es_pop", .3), ("wings", "es_whoosh2", .3)]),
 P("And belly fat widens your waist, so it pulls your number down from the other side.", [H_([("v1", 0)], x=0.32, y=0.66, h=1.1)],
   [N("widens", "WAIST UP", 0.72, 0.3, 120, RED), N("down", "NUMBER DOWN", 0.72, 0.5, 110, RED)], sfx=[("widens", "es_error", .3)]),
 # ===== THE PLAN =====
 card("So here's the plan.", "THE PLAN", "3 DAYS A WEEK"),
 P("Three days a week, at home.", [WK([("g_point", 0)], WALK, [(0, -0.2), (1.0, 0.35)], h=1.0, y=0.6)], [N(0.4, "3 DAYS / WEEK", 0.72, 0.4, 120, NAVY)], sfx=[(0.4, "es_pop", .3)]),
 P("One. Pike push-ups. Hips high, head down between your hands. They hit your shoulders from above. Three sets of eight.",
   [act([("pike_a", 0)] + reps("pike_b", "pike_a", 24, 0.55, 0.8), x=0.5, y=0.6, h=0.55, puppet=False)],
   [N(0, "#1 PIKE PUSH-UPS", 0.5, 0.12, 110, NAVY), N("Three", "3 x 8", 0.82, 0.3, 150, TEAL)], sfx=[(0, "es_pop", .3), ("Three", "es_ding", .3)]),
 P("Two. Side raises with two water bottles or a backpack. Slow, up to shoulder height. Three sets of fifteen. This is the move that makes you wider.",
   [act([("raise_a", 0)] + reps("raise_b", "raise_a", 20, 0.6, 0.8), x=0.35, y=0.7, h=1.15)],
   [N(0, "#2 SIDE RAISES", 0.72, 0.14, 110, NAVY), N("Three", "3 x 15", 0.74, 0.35, 150, TEAL), N("wider.", "= WIDER", 0.74, 0.55, 120, RED)],
   sfx=[(0, "es_pop", .3), ("Three", "es_ding", .3), ("wider.", "es_impact", .2)]),
 P("Three. Rows under a sturdy table, or a towel around a door handle. Pull your elbows back. Three sets of ten. This builds your wings.",
   [act([("r_row_a_c", 0)] + reps("r_row_b_c", "r_row_a_c", 20, 0.55, 0.8), x=0.42, y=0.62, h=0.55, puppet=False)],
   [N(0, "#3 TABLE ROWS", 0.5, 0.12, 110, NAVY), N("Three", "3 x 10", 0.84, 0.3, 150, TEAL)], sfx=[(0, "es_pop", .3), ("Three", "es_ding", .3)]),
 P("And for the waist, walk every day and keep your protein high. A smaller waist raises your number just as much as bigger shoulders.",
   [WK([("g_thumbs", 0)], WALK, [(0, -0.2), (3.0, 0.3)], h=1.0, y=0.6), IC("i_shake_c", "protein", 0.75, 0.42, 0.32)],
   [N("walk", "WALK DAILY", 0.72, 0.14, 110, NAVY), N("protein", "PROTEIN HIGH", 0.72, 0.72, 100, TEAL)], sfx=[("walk", "es_pop", .3), ("protein", "es_pop", .3)]),
 P("Measure again in eight weeks. Moving up even one level changes how every shirt fits.", [H_([("m_waist", 0), ("v2", "Moving"), ("v3", "level")], x=0.35, y=0.68, h=1.1), IC("i_shirt_c", "shirt", 0.74, 0.45, 0.35)],
   [N("eight", "8 WEEKS", 0.72, 0.15, 140, NAVY)], particles=[dict(at="level", x=0.35, y=0.3, spread=0.25)], sfx=[("eight", "es_pop", .3), ("level", "es_chime", .3)]),
 P("What's your number right now? Comment your level, and be honest.", LINE(stagger=0.12), [N(0, "YOUR NUMBER?", 0.5, 0.12, 150, NAVY)],
   sfx=[(0, "es_whoosh", .3), ("Comment", "es_pop", .3)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long10", words=f"{HERE}/voice/long10_cut.words.json", voice=f"{HERE}/voice/long10_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=20, sfx_db=14, duck=False, set=SOFT,
            scenes=S, cap_mode="build", cap_swipe=True, cap_words=3, cap_size=110, cap_y=0.8, cap_color=(255, 255, 255), cap_mini=(255, 255, 255), cap_stroke=8,
            cap_stroke_fill=(20, 22, 28), cap_font=f"{HERE}/fonts/anton.woff2", cap_upper=True, cap_gap=10,
            lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05, text_overlay=True, dip_color=(10, 12, 18))
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long10{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
