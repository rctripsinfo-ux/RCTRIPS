# LONG 11 "I Did Dead Hangs Every Day for 30 Days" (16:9) story + Yellow Dude style
# the character explains with poses (no moving still images), empty room backdrops + cut-out pose sets, kinetic words, no captions.
# usage: LUFS=-14 python3 long11/long11_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D3, D2, L1, W1, P2, A2 = (f"{HERE}/long03/img", f"{HERE}/long02/img", f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2")
I3 = f"{HERE}/week1/img3"
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for f in (f"{HERE}/long11/img/{n}_al.png", f"{HERE}/long11/img/{n}_c.png", f"{HERE}/long11/img/{n}.png", f"{HERE}/long10/img/{n}_al.png", f"{HERE}/long10/img/{n}_c.png", f"{HERE}/long10/img/{n}.png", f"{HERE}/long09/img/{n}_al.png", f"{HERE}/long09/img/{n}_c.png", f"{HERE}/long09/img/{n}.png", f"{HERE}/long08/img/{n}_al.png", f"{HERE}/long08/img/{n}_c.png", f"{HERE}/long08/img/{n}.png", f"{HERE}/long07/img/{n}_al.png", f"{HERE}/long07/img/{n}_c.png", f"{HERE}/long07/img/{n}.png", f"{HERE}/long06/img/{n}_al.png", f"{HERE}/long06/img/{n}.png", f"{D3}/{n}_al.png", f"{D3}/{n}_c.png", f"{D3}/{n}.png", f"{D2}/{n}_c.png", f"{D2}/{n}.png", f"{L1}/{n}_al_c.png", f"{L1}/{n}_c.png", f"{L1}/{n}_al.png", f"{A2}/{n}_al.png",
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
SOFT = (222, 236, 240)
def DAY(text, n, sub): return dict(text=text, poses=[], set=NAVY, tr="cut", nocap=True, kinetic=[kin(0, f"DAY {n}", 0.5, 0.42, 170, WHITE), kin(0.1, sub, 0.5, 0.6, 80, (200, 225, 222), frm="b")],
                                  keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .5)], sfx=[(0, "es_whoosh", .3), (0.1, "es_tick", .3)])
TIMER = lambda at, a, b, dur, x=0.78, y=0.4, col=NAVY: dict(at=at, a=a, b=b, dur=dur, x=x, y=y, size=210, color=col, label="SEC", stroke=8)
S = [
 # ===== HOOK =====
 P("For thirty days, I did one thing every morning. I hung from a bar. That's it.", [PU([("h_hang", 0)], x=0.32, enter=("rise", 0.25)), IC("i_cal30", 0.4, 0.75, 0.42, 0.4)],
   [N("bar.", "JUST HANG", 0.75, 0.68, 110, NAVY)], sfx=[(0, "es_whoosh", .3), (0.4, "es_pop", .3), ("bar.", "es_pop", .3)], keys=[(0, 1.25, .35, .3), (1.2, 1.0, .5, .5), ("E", 1.05, .5, .5)]),
 P("No pull-ups. No weights. Just hanging.", [PU([("h_relax", 0)], x=0.5)], [N("pull-ups.", "NO PULL-UPS", 0.18, 0.4, 80, RED), N("weights.", "NO WEIGHTS", 0.82, 0.4, 80, RED)],
   sfx=[("pull-ups.", "es_error", .25), ("weights.", "es_error", .25)]),
 M("You trained for a month by doing nothing?", [PU([("h_relax", 0)], x=0.38)], "s6_mini_squint_cut"),
 P("Basically. And on day fourteen, something happened that I didn't expect. Stay for that one.", [H_([("p_ominous", 0)], **CLOSE)],
   [N("fourteen,", "DAY 14: ???", 0.5, 0.12, 140, RED)], keys=[(0, 1.0, .5, .5), ("E", 1.3, .5, .35)], sfx=[("fourteen,", "es_rise", .25)]),
 # ===== DAY 1 =====
 DAY("Day one.", 1, "THE FIRST TRY"),
 P("I lasted twenty-two seconds. My hands burned, my fingers opened by themselves, and I dropped.",
   [PU([("h_hang", 0), ("h_burn", "burned,")], x=0.32, until="dropped."), dict(at="dropped.", w=wfor("p_fall_c", 0.42), x=0.36, y=0.8, asset=path("p_fall_c"), puppet=False, enter=("drop", 0.2))],
   counters=[TIMER(0.2, 0, 22, 1.4)],
   shake=[("dropped.", .05)], sfx=[("burned,", "es_impact", .2), ("dropped.", "es_thud", .5)]),
 P("Here's why. A dead hang is a grip test. Your forearm muscles hold your whole body weight, and most people never train them.",
   [PU([("h_burn", 0)], x=0.32, h=2.4, bar=0.1)], [N("grip", "GRIP TEST", 0.74, 0.3, 130, NAVY), N("whole", "100% BODY WEIGHT", 0.74, 0.5, 80, RED)], sfx=[("grip", "es_pop", .3), ("whole", "es_impact", .2)]),
 # ===== DAY 7 =====
 DAY("Day seven.", 7, "THE SORENESS"),
 P("Forty seconds. My forearms were sore every morning, like after a heavy workout.", [PU([("h_burn", 0)], x=0.32)], counters=[TIMER(0, 0, 40, 1.2)],
   kinetic=[N("sore", "SORE", 0.78, 0.72, 140, RED)], sfx=[("sore", "es_pop", .3)]),
 P("That's the muscles that close your fingers, working harder than they ever have.", [PU([("h_hang", 0), ("h_burn", "close")], x=0.4, h=2.6, bar=0.1)], kinetic=[N("close", "FINGER MUSCLES", 0.8, 0.55, 100, RED)], sfx=[("close", "es_pop", .3)]),
 M("So you're getting stronger by hanging out.", [PU([("h_relax", 0)], x=0.38)], "mini_laugh_cut"),
 P("Literally.", [H_([("g_thumbs", 0)], **CLOSE)], sfx=[(0, "es_pop2", .3)]),
 # ===== DAY 14 =====
 DAY("Day fourteen.", 14, "THE SURPRISE"),
 P("Here's the surprise. My lower back, which hurt every evening from sitting, stopped hurting.",
   [H_([("h_backpain", 0)], x=0.32, until="stopped"), IC("i_desk_c", "sitting,", 0.75, 0.45, 0.35, until="stopped"), PU([("h_relax", 0)], x=0.5, at="stopped", enter=("rise", 0.25))],
   [N("surprise.", "THE SURPRISE", 0.72, 0.15, 120, RED, until="stopped"), N("stopped", "NO MORE PAIN", 0.8, 0.45, 100, TEAL)], sfx=[("sitting,", "es_pop", .3), ("stopped", "es_chime", .3)]),
 P("When you hang, gravity gently pulls your spine longer, and the muscles around it relax. It feels like a stretch from the inside.",
   [PU([("h_relax", 0)], x=0.32), IC("i_spine_c", "spine", 0.74, 0.48, 0.6)], [N("longer,", "SPINE: LONGER", 0.74, 0.12, 100, TEAL)],
   sfx=[("spine", "es_whoosh2", .3), ("relax.", "es_pop2", .3)], keys=[(0, 1.0, .5, .5), ("E", 1.08, .6, .5)]),
 P("It's not a cure for back pain. But after a day at a desk, it felt amazing.", [H_([("p_wag", 0), ("g_thumbs", "amazing.")], x=0.3, y=0.7, h=1.15), IC("i_desk_c", "desk,", 0.75, 0.45, 0.3)],
   [N("cure", "NOT A CURE", 0.74, 0.15, 110, RED)], sfx=[("cure", "es_pop", .3), ("amazing.", "es_ding", .25)]),
 # ===== DAY 21 =====
 DAY("Day twenty-one.", 21, "THE SHOULDERS"),
 P("One full minute. And my shoulders stopped clicking when I lifted my arms.", [PU([("h_hang", 0)], x=0.32)], counters=[TIMER(0, 40, 60, 1.0)],
   kinetic=[N("clicking", "NO CLICKING", 0.78, 0.72, 100, TEAL)], sfx=[("clicking", "es_click", .4)]),
 P("Hanging opens up your shoulders and stretches the muscles that get tight from hunching over a phone.",
   [PU([("h_relax", 0)], x=0.32), IC("i_shoulder_c", "opens", 0.75, 0.35, 0.36), IC("i_phone2_c", "phone.", 0.75, 0.75, 0.2)], sfx=[("opens", "es_pop", .3), ("phone.", "es_pop2", .3)]),
 # ===== DAY 30 =====
 DAY("Day thirty.", 30, "THE RESULT"),
 P("One minute and thirty seconds. Four times longer than day one.", [PU([("h_hang", 0)], x=0.32)], counters=[TIMER(0, 60, 90, 1.4, col=TEAL)],
   kinetic=[N("Four", "4X LONGER", 0.78, 0.72, 120, RED)], particles=[dict(at="Four", x=0.78, y=0.4, spread=0.25)], sfx=[("Four", "es_ding", .3)]),
 P("My grip got much stronger. Jars open easily. Carrying groceries is nothing. And my forearms look thicker.",
   [H_([("g_flex", 0), ("h_jar", "Jars"), ("h_bags", "Carrying"), ("g_flex", "forearms")], x=0.35, y=0.7, h=1.15)],
   [N("grip", "STRONGER GRIP", 0.75, 0.15, 100, NAVY), N("thicker.", "THICKER FOREARMS", 0.75, 0.32, 90, TEAL)],
   sfx=[("Jars", "es_pop", .3), ("Carrying", "es_pop", .3), ("thicker.", "es_chime", .3)]),
 P("Pull-ups felt easier too, because my hands didn't quit first anymore.", [PU([("h_hang", 0), ("p_mid", "easier"), ("p_top", "hands")], x=0.4, bar=0.24)], sfx=[("easier", "es_whoosh2", .3)]),
 # ===== HOW TO =====
 card("If you want to try it,", "HOW TO", "START TODAY"),
 P("grab a bar with your hands shoulder width apart. Arms straight, shoulders relaxed, and just hang.", [PU([("h_hang", 0)], x=0.32, h=1.7, bar=0.08)],
   kinetic=[N("shoulder", "SHOULDER WIDTH", 0.76, 0.35, 90, NAVY), N("hang.", "JUST HANG", 0.76, 0.55, 100, TEAL)]),
 P("Do three hangs, as long as you can. Add five seconds every few days.", [PU([("h_hang", 0)], x=0.32)],
   [N("three", "3 HANGS", 0.76, 0.3, 140, NAVY), N("five", "+5 SEC", 0.76, 0.55, 140, TEAL)], sfx=[("three", "es_pop", .3), ("five", "es_ding", .3)]),
 P("If your hands slip, use a towel or chalk.", [PU([("h_burn", 0)], x=0.32), IC("i_chalk_c", "chalk.", 0.75, 0.45, 0.35), IC("i_towel_c", "towel", 0.75, 0.15, 0.2)], sfx=[("towel", "es_pop", .3), ("chalk.", "es_pop", .3)]),
 P("If your shoulders hurt, keep your feet on a chair and take some weight off.", [PU([("h_chair", 0)], x=0.35, h=1.05, bar=0.1)], [N("chair", "FEET ON A CHAIR", 0.78, 0.35, 90, TEAL)], sfx=[("chair", "es_pop", .3)]),
 P("How long can you hang right now? Test it today, and comment your time.", [PU([("h_hang", 0)], x=0.32)], counters=[TIMER(0.5, 0, 99, 3.0)],
   kinetic=[N("comment", "COMMENT YOUR TIME", 0.75, 0.75, 80, RED)], sfx=[("comment", "es_pop", .3)]),
]
PLAN = dict(dir=f"{HERE}/scenes_long11", words=f"{HERE}/voice/long11_cut.words.json", voice=f"{HERE}/voice/long11_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=20, sfx_db=14, duck=False, set=SOFT,
            scenes=S, cap_mode="build", cap_swipe=True, cap_words=3, cap_size=110, cap_y=0.88, cap_color=(255, 255, 255), cap_mini=(255, 255, 255), cap_stroke=8,
            cap_stroke_fill=(20, 22, 28), cap_font=f"{HERE}/fonts/anton.woff2", cap_upper=True, cap_gap=10,
            lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.05, text_overlay=True, dip_color=(10, 12, 18))
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long11{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
