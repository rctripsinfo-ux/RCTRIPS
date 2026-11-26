# SHORT 11 "The Sit-Down Stand-Up Test" 9:16 (self-test, engagement beats: challenge, pause-and-try, score, comment/like)
# the character explains with poses (5 arm-level poses on one canvas, curl reps, triceps flex + red, doorframe pair, level-up montage, mirror),
# kinetic italic words instead of label boxes, pose pop swaps, puppet sway, Mini-H in front, small build captions kept (Shorts).
# usage: LUFS=-14 python3 short11/short11_plan.py
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
D = [f"{HERE}/short11/img", f"{HERE}/long09/img", f"{HERE}/week1/img3", f"{HERE}/week1/img", f"{HERE}/short10/img", f"{HERE}/long11/img", f"{HERE}/long03/img", f"{HERE}/long09/img", f"{HERE}/week1/img2", f"{HERE}/long03/img", f"{HERE}/pilot3/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img"]
TINT, RED, TEAL, INK, WHITE = (221, 239, 237), (122, 26, 26), (15, 139, 133), (34, 40, 48), (255, 255, 255)

def path(n):
    for d in D:
        for f in (f"{d}/{n}_al.png", f"{d}/{n}_c.png", f"{d}/{n}.png"):
            if os.path.exists(f): return f
    raise FileNotFoundError(n)
def wfor(n, h): im = Image.open(path(n)); return h * H * im.width / im.height / W
def act(seq, at=0, until=None, x=0.5, y=0.56, h=0.62, **k): return dict(at=at, until=until, w=wfor(seq[0][0], h), x=x, y=y, poses=[(path(p), a) for p, a in seq], **k)
def fig(n, at=0, until=None, x=0.5, y=0.56, h=0.62, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), **k)
def reps(a, b, n, step, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def mini(n, side="r"): return dict(at=0, w=wfor(n, 0.3), x=0.8 if side == "r" else 0.2, y=0.74, asset=path(n), enter=(f"corner_{side}", 0.25), z=3)
def kin(at, text, x=0.5, y=0.12, size=120, color=INK, until=None, frm="l", **k): return dict(at=at, text=text, x=x, y=y, size=size, color=color, until=until, maxw=0.9, **{"from": frm}, **k)
DRIFT = [(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]
def S_(text, layers, kinetic=(), tr="cut", **k): return dict(text=text, poses=[], tr=tr, layers=layers, kinetic=list(kinetic), keys=k.pop("keys", DRIFT), **k)
def M(text, base, m, **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m)], keys=[(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)], **k)
def level(text, n, name, pose, extra=()):
    return S_(text, [act([(pose, 0)] + list(extra))], [kin(0, f"LEVEL {n}", 0.5, 0.09, 90, TEAL), kin("the", name, 0.5, 0.16, 110, RED if n in (1, 5) else INK)],
              sfx=[(0, "pop", .3)])

NAVY, LTEAL = (30, 42, 72), (15, 139, 133)
def IC(n, at=0, x=0.75, y=0.4, h=0.18, until=None, **k):  # icon pop (one picture per phrase)
    return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), puppet=False, breathe=False, enter=k.pop("enter", ("pop", 0.22)), **k)
def N(at, text, x=0.5, y=0.14, size=150, color=NAVY, until=None, **k): return kin(at, text, x, y, size, color, until=until, stroke=8, stroke_fill=WHITE, **k)
POP = lambda *a: [(t, "pop", .3) for t in a]
PU = lambda n, step=0.28, t0=0.0, **k: act([("pu_top", 0)] + reps("pu_bot", "pu_top", n, step, t0), **{"h": 0.3, "y": 0.6, **k})
BIG = dict(x=0.5, y=0.58, h=0.74)
def M(text, base, m, **k): return dict(text=text, poses=[], tr="cut", layers=base + [mini(m)], **{"keys": [(0, 1.02, .5, .5), ("E", 1.05, .5, .5)], "sfx": [(0, "pop_soft", .3)], **k})
SC = lambda at, a, b, dur, y=0.16, col=NAVY: dict(at=at, a=a, b=b, dur=dur, x=0.5, y=y, size=230, color=col, label="POINTS", stroke=8)
def INS0(n, at, crop, x, y, r=0.13, until=None): return dict(at=at, until=until, asset=path(n), crop=crop, x=x, y=y, r=r, bg=(226, 234, 244))

CLOSE = dict(x=0.5, y=0.95, h=1.5)  # face / chest fill the frame
D.extend([f"{HERE}/long08/img", f"{HERE}/long07/img", f"{HERE}/long06/img", f"{HERE}/long03/img"])
def BG(n, slide=None):  # 16:9 room as a 9:16 backdrop; slides in with a cubic ease (no overshoot)
    return dict(at=0, w=3.25, x=0.5, y=0.5, asset=path(n), z=-1, puppet=False, breathe=False, smooth=True, enter=(slide, 0.5) if slide else ("cut", 0))
def WALKIN(stand, at=0, x0=-0.3, x1=0.5, dur=1.0, **k):
    return dict(at=at, w=wfor(stand[0][0], 0.74), x=x1, y=0.58, poses=[(path(p), a) for p, a in stand], track=[(at, x0, 0.58), (at + dur, x1, 0.58)],
                walk=dict(a=path("d5_walk_a"), b=path("d5_walk_b"), w=wfor("d5_walk_a", 0.74), step=0.26), **k)
def B_(at, text, y=0.26, size=170, color=WHITE, until=None):  # big word BEHIND the character (owner: never over the face)
    return kin(at, text, 0.5, y, size, color, until=until, stroke=10, stroke_fill=NAVY, behind=True)
CYC = lambda t0, n, step=0.34: [(p, round(t0 + i * step, 2)) for i, p in enumerate((["sit_lower", "sit_cross", "rise_mid", "stand_done"] * 8)[:n])]
S = [
 S_("Sit on the floor, then stand back up.", [BG("bk_mirror"), WALKIN([("stand_done", 0), ("sit_lower", "floor,"), ("sit_cross", "floor,+0.3"), ("rise_mid", "stand"), ("stand_win", "up.")], dur=0.9)],
    keys=[(0, 1.0, .5, .5), ("floor,", 1.0, .5, .5), ("floor,+0.35", 1.15, .5, .62), ("stand", 1.0, .5, .5)], sfx=[(0, "es_whoosh", .2), ("floor,+0.3", "es_thud", .3), ("up.", "es_ding", .2)]),
 S_("No hands. No knees. Can you do it?", [BG("bk_mirror"), act([("stand_done", 0)], **CLOSE)], [B_("hands.", "NO HANDS", 0.16, 150, WHITE), B_("knees.", "NO KNEES", 0.27, 150, WHITE), kin("Can", "CAN YOU?", 0.5, 0.1, 150, RED, stroke=10, stroke_fill=WHITE)],
    sfx=[("hands.", "es_pop", .25), ("knees.", "es_pop", .25), ("Can", "es_ding", .2)], keys=[(0, 1.0, .5, .5), ("Can", 1.0, .5, .5), ("E", 1.12, .5, .45)]),
 M("Easy. Watch this... okay, not easy.", [BG("bk_garage", "slide_r"), act([("stand_done", 0), ("sit_lower", "Watch"), ("rise_mid", "this..."), ("rise_hand", "okay,")], x=0.42, y=0.58, h=0.72, shiver=[("this...", "okay,")], until="not"),
    act([("laugh_floor", 0)], at="not", x=0.42, y=0.58, h=0.72, enter=("drop", 0.18))], "mini_laugh_cut",
   shake=[("not", .06)], keys=[(0, 1.0, .5, .5), ("this...", 1.15, .42, .45), ("not", 1.0, .5, .5)],
   sfx=[("this...", "es_grit", .3), ("okay,", "es_fall", .25), ("not", "es_thud", .35), ("easy.", "es_boing", .2)]),
 S_("This is the sit-down stand-up test.", [BG("bk_studio", "slide_l"), act(CYC(0.3, 8, 0.34), **BIG)], [B_("sit-down", "SIT-DOWN", 0.17, 160), B_("stand-up", "STAND-UP", 0.28, 160, (255, 214, 79))],
    sfx=[(0, "es_whoosh", .2), ("sit-down", "es_pop", .25), ("stand-up", "es_pop", .25)]),
 S_("Scientists used it on over two thousand adults.", [BG("bk_clinic", "slide_r"), act([("shocked_read", 0)], **BIG)], [B_("two", "2,000+", 0.2, 210), B_("thousand", "ADULTS", 0.31, 130)],
    sfx=[(0, "es_whoosh", .2), ("two", "es_pop", .25)], keys=[(0, 1.0, .5, .5), ("E", 1.12, .5, .42)]),
 S_("You start with ten points.", [BG("bk_studio", "slide_l"), act([("point_floor", 0)], **BIG)], counters=[SC(0.2, 0, 10, 0.6)], sfx=[(0, "es_whoosh", .2), (0.2, "es_ding", .2)]),
 S_("Lose one point every time you use a hand, a knee, or your arm.", [BG("bk_studio"), act([("sit_cross", 0), ("rise_hand", "hand,")], **BIG)],
    counters=[dict(at=0, a=10, b=10, dur=0.1, x=0.5, y=0.12, size=230, color=NAVY, label="POINTS", stroke=8, until="hand,"),
              dict(at="hand,", a=9, b=9, dur=0.1, x=0.5, y=0.12, size=230, color=RED, label="POINTS", stroke=8, until="knee,"),
              dict(at="knee,", a=8, b=8, dur=0.1, x=0.5, y=0.12, size=230, color=RED, label="POINTS", stroke=8, until="arm."),
              dict(at="arm.", a=7, b=7, dur=0.1, x=0.5, y=0.12, size=230, color=RED, label="POINTS", stroke=8)],
    shake=[("hand,", .02), ("knee,", .02), ("arm.", .02)], keys=[(0, 1.0, .5, .5), ("hand,", 1.1, .5, .6), ("E", 1.0, .5, .5)],
    sfx=[("hand,", "es_error", .25), ("knee,", "es_error", .25), ("arm.", "es_error", .25)]),
 S_("Pause the video and try it right now.", [BG("bk_hotel", "slide_r"), act([("g_point", 0)], **CLOSE)], [B_("Pause", "PAUSE", 0.18, 200, (255, 214, 79)), B_("try", "& TRY IT", 0.3, 140)],
    sfx=[(0, "es_whoosh", .2), ("Pause", "es_click", .4)], keys=[(0, 1.0, .5, .5), ("E", 1.12, .5, .45)]),
 S_("I'll wait.", [BG("bk_hotel"), act([("stand_done", 0), ("sit_lower", 0.15), ("sit_wait", 0.45)], **BIG), IC("i_watch_c", 0.6, 0.8, 0.3, 0.12)],
    sfx=[(0.45, "es_thud", .25), (0.7, "es_ticktock2", .35), (1.2, "es_ticktock2", .35), (1.7, "es_ticktock2", .35)], keys=[(0, 1.0, .5, .5), ("E", 1.15, .5, .62)]),
 S_("Got your score? Ten is excellent.", [BG("bk_rooftop", "slide_l"), act([("sit_scratch", 0), ("rise_mid", "Ten"), ("stand_win", "excellent.")], **BIG)],
    [B_("score?", "SCORE?", 0.22, 190, until="Ten"), B_("Ten", "10 = EXCELLENT", 0.22, 120, (255, 214, 79))], particles=[dict(at="excellent.", x=0.5, y=0.2, spread=0.35)],
    sfx=[(0, "es_whoosh", .2), ("Ten", "es_swish", .2), ("excellent.", "es_ding", .2)]),
 S_("Eight or nine is good.", [BG("bk_rooftop"), act([("g_thumbs", 0)], **CLOSE)], [B_(0, "8-9 = GOOD", 0.2, 140)], sfx=[(0, "es_pop", .25)], keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .45)]),
 S_("Under six, your body is asking for help.", [BG("bk_rooftop"), act([("rise_hand", 0)], **BIG)], [B_(0, "UNDER 6", 0.2, 180, (255, 120, 120)), B_("help.", "= HELP", 0.31, 130)],
    sfx=[(0, "es_error", .25), ("help.", "es_grit", .25)], keys=[(0, 1.0, .5, .5), ("E", 1.2, .5, .65)]),
 S_("In the study, the lowest scorers were about five times more likely to die within six years than the highest.", [BG("bk_clinic", "slide_r"), act([("shocked_read", 0), ("stand_done", "highest.")], **BIG)],
    [B_("five", "5X", 0.2, 300, (255, 120, 120)), kin("six", "WITHIN 6 YEARS", 0.5, 0.06, 90, NAVY, stroke=8, stroke_fill=WHITE)], shake=[("five", .03)],
    sfx=[(0, "es_whoosh", .2), ("five", "es_impact", .2), ("highest.", "es_pop2", .2)], keys=[(0, 1.0, .5, .5), ("five", 1.12, .5, .4), ("E", 1.0, .5, .5)]),
 M("I'm starting squats today.", [BG("bk_garage", "slide_l"), act([("stand_done", 0)] + [(("squat_b", "stand_done")[i % 2], round(0.35 + i * 0.36, 2)) for i in range(8)], x=0.42, y=0.58, h=0.72)], "mini_laugh_cut",
   sfx=[(0, "es_whoosh", .2), (0.4, "es_boing", .2)]),
 S_("Good. Squats and lunges raise your score fast.", [BG("bk_garage"), act([("squat_b", 0), ("stand_done", 0.36), ("squat_b", 0.72), ("lunge_fa", "lunges"), ("lunge_fb", "lunges+0.4"), ("lunge_fa", "lunges+0.8"), ("lunge_fb", "raise"), ("stand_win", "fast.")], **BIG)],
    [B_("Squats", "SQUATS", 0.17, 170, (255, 214, 79)), B_("lunges", "+ LUNGES", 0.28, 150)], sfx=[("Squats", "es_pop", .25), ("lunges", "es_pop", .25), ("fast.", "es_ding", .2)]),
 S_("Comment your score, and like if you got a perfect ten.", [BG("bk_rooftop", "slide_r"), act([("g_point", 0), ("stand_win", "like")], **CLOSE)],
    [B_("Comment", "COMMENT", 0.18, 170), B_("score,", "YOUR SCORE", 0.29, 130, (255, 214, 79)), kin("perfect", "10? LIKE!", 0.5, 0.06, 120, RED, stroke=8, stroke_fill=WHITE)],
    particles=[dict(at="perfect", x=0.5, y=0.2, spread=0.35)], sfx=[(0, "es_whoosh", .2), ("Comment", "es_pop", .25), ("perfect", "es_ding", .25)]),
]
PLAN = dict(dir=f"{HERE}/scenes_s11", words=f"{HERE}/voice/short11_cut.words.json", voice=f"{HERE}/voice/short11_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=24, sfx_db=18, duck=True, set=TINT, scenes=S,
            cap_mode="build", cap_swipe=True, cap_words=2, cap_size=96, cap_y=0.8, cap_color=(255, 255, 255), cap_mini=(255, 255, 255), cap_stroke=8,
            cap_stroke_fill=(20, 22, 28), cap_font=f"{HERE}/fonts/anton.woff2", cap_upper=True, cap_gap=10,
            lead=0.06, tail=0.8, keywords=[], breathe=True, puppet=True, pose_pop=0.0, pose_xf=0.1, smooth_moves=True)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/short11.mp4")
