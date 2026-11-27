# SHORT 12 "Doing Calf Raises Wrong? Why Your Calves Won't Grow" 9:16. Workouts Made Simple: problem (bouncing) + fix (deep stretch, 2 s pause, slow up, squeeze).
# Owner rules: rooms slide in (cubic ease), varied poses, smooth moves, big words behind H, never on the face. usage: LUFS=-14 python3 short12/short12_plan.py
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE); sys.path.insert(0, f"{HERE}/short11")
import short11_plan as P11
from short11_plan import *
from director import render
P11.D.insert(0, f"{HERE}/short12/img")
LEGS = [(0, 1.0, .5, .5), (0.6, 1.35, .5, .8), ("E", 1.4, .5, .8)]          # push in on the calves
def C(seq, **k): return act(seq, **{**BIG, "h": 0.8, **k})
def RAISE(n, step=0.3, t0=0.0, a="cr_low2", b="cr_high3"): return C(reps(a, b, n, step, t0))
def T(at, a, b, dur, label, y=0.13, col=NAVY): return dict(at=at, a=a, b=b, dur=dur, x=0.5, y=y, size=210, color=col, label=label, stroke=8)
YEL = (255, 214, 79)
S = [
 S_("You've done a thousand calf raises.", [BG("bk_armgym"), RAISE(10, 0.2)], counters=[T(0.1, 0, 1000, 1.6, "CALF RAISES")], sfx=[(0, "es_whoosh", .2), (1.7, "es_ding", .2)]),
 S_("And your calves still look like sticks.", [BG("bk_armgym"), C([("cr_sad", 0)])], [B_("sticks.", "STICKS?", 0.52, 190, (255, 120, 120))], keys=LEGS,
    sfx=[("sticks.", "es_boing", .25)]),
 M("Genetics, bro. Just accept it.", [BG("bk_armgym"), C([("cr_sad", 0)], x=0.42)], "mini_laugh_cut", sfx=[(0, "es_pop", .25)]),
 S_("Nope.", [BG("bk_armgym"), act([("p_wag", 0)], **CLOSE)], sfx=[(0, "es_error", .2)]),
 S_("You're bouncing. Watch this.", [BG("bk_garage", "slide_r"), RAISE(10, 0.13, a="cr_bounce", b="cr_base")], [B_("bouncing.", "BOUNCING", 0.18, 170, (255, 120, 120))],
    sfx=[(0, "es_whoosh", .2), ("bouncing.", "es_boing", .3)]),
 S_("Fast and bouncy.", [BG("bk_garage"), RAISE(10, 0.12, a="cr_bounce", b="cr_base")], [B_("Fast", "FAST = WRONG", 0.18, 130, (255, 120, 120))], sfx=[("Fast", "es_error", .25)]),
 S_("Your Achilles tendon acts like a spring and does the work.", [BG("bk_garage"), RAISE(14, 0.14, a="cr_bounce", b="cr_base")],
    [B_("spring", "SPRING", 0.55, 190, YEL)], keys=[(0, 1.0, .5, .5), ("spring", 1.5, .5, .85), ("E", 1.5, .5, .85)], sfx=[("spring", "es_boing", .3)]),
 S_("Your calf barely moves.", [BG("bk_garage"), C([("cr_point2", 0)])], [B_("barely", "BARELY WORKS", 0.18, 120, (255, 120, 120))], sfx=[("barely", "es_error", .25)]),
 S_("Now the fix.", [BG("bk_studio", "slide_l"), C([("cr_base", 0)])], [B_("fix.", "THE FIX", 0.18, 190, (120, 230, 200))], sfx=[(0, "es_whoosh", .2), ("fix.", "es_ding", .25)]),
 S_("Go all the way down, heels below the step. Pause for two seconds.", [BG("bk_studio"), C([("cr_base", 0), ("cr_low2", "down,")])],
    [B_("heels", "HEELS DOWN", 0.5, 140)], counters=[T("Pause", 0, 2, 2.0, "SEC", y=0.62, col=TEAL)], keys=[(0, 1.0, .5, .5), ("heels", 1.4, .5, .82), ("E", 1.4, .5, .82)],
    sfx=[("down,", "es_swish", .25), ("Pause", "es_ticktock", .3)]),
 S_("Then rise slowly, all the way up on your toes.", [BG("bk_studio"), C([("cr_low2", 0), ("cr_high3", "slowly,")], pose_xf=0.8)], [B_("slowly,", "SLOW UP", 0.18, 180)],
    sfx=[("slowly,", "es_rise", .25)]),
 S_("Squeeze for one second at the top.", [BG("bk_studio"), C([("cr_glow", 0)], shiver=[(0.1, "top.")])], [B_("Squeeze", "SQUEEZE", 0.5, 180, (255, 120, 120))],
    counters=[T("one", 0, 1, 1.0, "SEC", y=0.62, col=TEAL)], keys=LEGS, sfx=[("Squeeze", "es_grit", .3)]),
 M("That burns way more!", [BG("bk_studio"), C([("cr_glow", 0)], x=0.42)], "mini_scared_cut", sfx=[(0, "es_pop", .25), ("burns", "es_teeth", .25)]),
 S_("Exactly. That burn means the muscle is finally working.", [BG("bk_rooftop", "slide_r"), act([("g_thumbs", 0)], **CLOSE)], [B_("burn", "BURN = GROWTH", 0.13, 130, YEL)],
    sfx=[(0, "es_whoosh", .2), ("working.", "es_ding", .25)]),
 S_("Do three sets of twelve slow reps, every other day.", [BG("bk_rooftop"), RAISE(6, 0.7)], [B_("three", "3 x 12", 0.16, 200), B_("every", "EVERY OTHER DAY", 0.27, 100, YEL)],
    sfx=[("three", "es_pop", .25), ("every", "es_pop", .25)]),
 S_("One leg at a time if two legs feel easy.", [BG("bk_rooftop"), C([("cr_one", 0)])], [B_("One", "1 LEG", 0.18, 200, YEL)], sfx=[("One", "es_pop", .25)]),
 S_("Calves love slow reps and the deep stretch at the bottom.", [BG("bk_armgym", "slide_l"), C([("cr_high3", 0), ("cr_low2", "deep")], pose_xf=0.6)],
    [B_("slow", "SLOW", 0.16, 170), B_("deep", "+ DEEP STRETCH", 0.27, 110, YEL)], sfx=[(0, "es_whoosh", .2), ("slow", "es_pop", .25), ("deep", "es_swish", .25)]),
 S_("Be honest. Have you been bouncing?", [BG("bk_armgym"), C([("cr_point2", 0)])], [B_("bouncing?", "BOUNCER?", 0.18, 190, (255, 120, 120))], sfx=[("bouncing?", "es_boing", .3)]),
 S_("Comment \"bouncer\" or \"slow\".", [BG("bk_armgym"), act([("g_point", 0)], **CLOSE)], [B_(0, "COMMENT:", 0.1, 110), kin(0.2, "BOUNCER or SLOW", 0.5, 0.2, 110, NAVY, stroke=8, stroke_fill=WHITE)],
    sfx=[(0, "es_pop", .25)]),
]
PLAN = dict(P11.PLAN, dir=f"{HERE}/scenes_s12", words=f"{HERE}/voice/short12_cut.words.json", voice=f"{HERE}/voice/short12_cut.wav", scenes=S, cap_y=0.9)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/short12.mp4")
