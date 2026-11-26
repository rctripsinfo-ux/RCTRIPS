# LONG 12 "I Did 100 Squats Every Day for 30 Days" (16:9). Owner rules: rooms slide in (cubic ease), varied poses, smooth moves, text never on H's face.
# usage: LUFS=-14 python3 long12/long12_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE); sys.path.insert(0, f"{HERE}/long11")
import long11_plan as L
from long11_plan import *
from director import render
_old = L.path
def path(n):
    for f in (f"{HERE}/long12/img/{n}_al.png", f"{HERE}/short11/img/{n}_al.png") + ((f"{HERE}/long03/img/{n}.png", f"{HERE}/long02/img/{n}.png") if n.startswith(("bk_", "W_")) else ()):
        if os.path.exists(f): return f
    return _old(n)
L.path = path
def BG(n, slide=None): return dict(at=0, w=1.0, x=0.5, y=0.5, asset=path(n), z=-1, puppet=False, breathe=False, smooth=True, enter=(slide, 0.55) if slide else ("cut", 0))
FULL = dict(x=0.3, y=0.55, h=0.9)            # whole body (squats need the legs)
def F(seq, **k): return act(seq, **{**FULL, **k})
def SQ(n, step=0.42, t0=0.0, **k): return F(reps("stand_done", "squat_b", n, step, t0), **k)   # squat reps
def R(at, text, color=NAVY, x=0.73, y=0.3, size=110, until=None): return N(at, text, x, y, size, color, until)  # words on the right, away from the face
def REP(at, a, b, dur, x=0.74, y=0.5, col=NAVY, label="SQUATS"): return dict(at=at, a=a, b=b, dur=dur, x=x, y=y, size=200, color=col, label=label, stroke=8)
def W_(seq, x0=-0.2, x1=0.3, dur=0.9, **k): return WK(seq, WALK, [(0, x0), (dur, x1)], h=0.9, y=0.55, **k)
def MM(text, base, m="mini_laugh_cut", **k):
    d = dict(text=text, poses=[], tr="cut", layers=base + [mini(m)], keys=[(0, 1.0, .5, .5), ("E", 1.04, .55, .5)], sfx=[(0, "es_pop", .3)]); d.update(k); return d
S = [
 # ===== HOOK =====
 P("One hundred squats. Every day. For thirty days.", [BG("bk_studio"), SQ(8, 0.38)], counters=[REP(0, 0, 100, 2.2)], sfx=[(0, "es_whoosh", .3), (2.2, "es_ding", .3)],
   keys=[(0, 1.2, .3, .6), (1.6, 1.0, .5, .5), ("E", 1.03, .5, .5)]),
 P("No gym, no weights, just my legs.", [BG("bk_studio"), F([("g_flex", 0)])], [R("gym,", "NO GYM", RED, y=0.25), R("weights,", "NO WEIGHTS", RED, y=0.42), R("legs.", "JUST LEGS", TEAL, y=0.62)],
   sfx=[("gym,", "es_error", .25), ("weights,", "es_error", .25), ("legs.", "es_pop", .3)]),
 MM("That's three thousand squats! Your knees are going to file a complaint.", [BG("bk_studio"), F([("g_shock", 0)], x=0.35)], kinetic=[R("thousand", "3,000", RED, x=0.6, y=0.18, size=150)],
    sfx=[(0, "es_pop", .3), ("complaint.", "es_boing", .25)]),
 P("That's what I thought too.", [BG("bk_studio"), F([("g_shrug", 0)])], sfx=[]),
 P("But on day ten, something happened that I didn't expect. Stay for that one.", [BG("bk_night", "slide_r"), H_([("p_ominous", 0)], **CLOSE)],
   [R("ten,", "DAY 10: ???", RED, x=0.82, y=0.2, size=120)], keys=[(0, 1.0, .5, .5), ("E", 1.25, .5, .35)], sfx=[(0, "es_whoosh", .3), ("ten,", "es_rise", .25)]),
 # ===== DAY 1 =====
 DAY("Day one.", 1, "THE FIRST TRY"),
 P("I did them in sets of twenty-five.", [BG("bk_garage", "slide_l"), SQ(6, 0.4)], counters=[REP(0.2, 0, 25, 1.8)], sfx=[(0, "es_whoosh", .3)]),
 P("By the last set, my legs were shaking like jelly.", [BG("bk_garage"), F([("squat_b", 0), ("sq_shake", "shaking")], shiver=[("shaking", "jelly.+0.5")])],
   [R("jelly.", "JELLY LEGS", RED, y=0.4, size=120)], sfx=[("shaking", "es_grit", .35), ("jelly.", "es_boing", .3)], keys=[(0, 1.0, .5, .5), ("shaking", 1.15, .32, .7), ("E", 1.15, .32, .7)]),
 P("The next morning, I couldn't sit down without holding the wall.", [BG("W_living", "slide_r"), W_([("stand_done", 0), ("sq_wall", "sit")], x1=0.35)],
   [R("wall.", "SORE!", RED, y=0.3, size=150)], sfx=[(0, "es_whoosh", .3), ("sit", "es_squeak", .3), ("wall.", "es_thud", .3)]),
 MM("And the stairs? How were the stairs?", [BG("W_living"), F([("sq_wall", 0)], x=0.35)], "s6_mini_squint_cut", sfx=[(0, "es_pop", .3)]),
 P("Going down the stairs was the worst part.", [BG("bk_hotel", "slide_l"), F([("sq_stairs", 0)], x=0.4)], [R("worst", "THE WORST", RED, y=0.3)],
   shake=[("worst", .03)], sfx=[(0, "es_whoosh", .3), ("stairs", "es_squeak", .3), ("worst", "es_teeth", .3)]),
 P("That's normal soreness.", [BG("bk_hotel"), F([("p_wag", 0)])], [R("normal", "NORMAL", TEAL, size=140)], sfx=[("normal", "es_pop", .3)]),
 P("Your muscles get tiny damage, then they repair and come back stronger.", [BG("bk_clinic", "slide_r"), F([("sq_glow", 0), ("g_flex", "stronger.")])],
   [R("damage,", "TINY DAMAGE", RED, y=0.25), R("repair", "REPAIR", NAVY, y=0.42), R("stronger.", "STRONGER", TEAL, y=0.6, size=130)],
   sfx=[(0, "es_whoosh", .3), ("damage,", "es_impact", .2), ("repair", "es_pop", .3), ("stronger.", "es_ding", .3)]),
 # ===== DAY 5 =====
 DAY("Day five.", 5, "FASTER"),
 P("The soreness was gone.", [BG("bk_park", "slide_l"), F([("stand_win", 0)])], [R("gone.", "NO PAIN", TEAL, size=130)], sfx=[(0, "es_whoosh", .3), ("gone.", "es_chime", .3)]),
 P("One hundred squats took me just eight minutes.", [BG("bk_park"), SQ(10, 0.3)], counters=[REP(0.2, 0, 8, 1.6, col=TEAL, label="MINUTES")],
   kinetic=[R("hundred", "100 SQUATS", NAVY, y=0.25, size=100)], sfx=[("eight", "es_ticktock", .3)]),
 P("Here's why it works. A squat uses the biggest muscles in your body.", [BG("bk_studio", "slide_r"), F([("g_point", 0), ("sq_glow", "squat")])],
   [R("biggest", "BIGGEST MUSCLES", RED, y=0.3, size=100)], sfx=[(0, "es_whoosh", .3), ("biggest", "es_impact", .2)]),
 P("Your thighs, your glutes, and your core all work together.", [BG("bk_studio"), F([("sq_glow", 0)], h=1.1, y=0.62)],
   [R("thighs,", "THIGHS", RED, y=0.22), R("glutes,", "GLUTES", RED, y=0.4), R("core", "CORE", ORANGE, y=0.58)],
   sfx=[("thighs,", "es_pop", .3), ("glutes,", "es_pop", .3), ("core", "es_pop", .3)], keys=[(0, 1.0, .5, .5), ("E", 1.1, .45, .6)]),
 MM("So it's leg day. Every day.", [BG("bk_studio"), SQ(6, 0.4, x=0.35)], "mini_laugh_cut", sfx=[(0, "es_pop", .3)]),
 P("Exactly.", [BG("bk_studio"), H_([("g_thumbs", 0)], **CLOSE)], sfx=[(0, "es_pop2", .3)]),
 # ===== DAY 10 =====
 DAY("Day ten.", 10, "THE SURPRISE"),
 P("Here's the surprise. My knees used to crack and ache on the stairs.", [BG("bk_hotel", "slide_r"), F([("sq_stairs", 0)], x=0.4)],
   [R("crack", "CRACK!", RED, y=0.3, size=140)], sfx=[(0, "es_whoosh", .3), ("crack", "es_click", .5)]),
 P("Now they felt better, not worse.", [BG("bk_hotel"), F([("sq_knee", 0)])], [R("better,", "BETTER", TEAL, y=0.3, size=150), R("worse.", "NOT WORSE", NAVY, y=0.5)],
   sfx=[("better,", "es_chime", .3)], keys=[(0, 1.0, .5, .5), ("E", 1.12, .35, .7)]),
 P("Strong thigh muscles take pressure off your knees.", [BG("bk_clinic", "slide_l"), F([("sq_glow", 0), ("sq_knee", "pressure")])],
   [R("pressure", "LESS PRESSURE", TEAL, y=0.3, size=100)], sfx=[(0, "es_whoosh", .3), ("pressure", "es_pop", .3)]),
 P("Squats done right don't wreck your knees. They protect them.", [BG("bk_clinic"), F([("p_wag", 0), ("g_thumbs", "protect")])],
   [R("wreck", "DON'T WRECK", RED, y=0.25), R("protect", "PROTECT", TEAL, y=0.45, size=140)], sfx=[("wreck", "es_error", .25), ("protect", "es_ding", .3)]),
 P("Just keep your heels down, and let your knees point the same way as your toes.", [BG("bk_studio", "slide_r"), F([("sq_bottom", 0)], h=1.0, y=0.6)],
   [R("heels", "HEELS DOWN", NAVY, y=0.25), R("toes.", "KNEES = TOES", TEAL, y=0.45)], sfx=[(0, "es_whoosh", .3), ("heels", "es_pop", .3), ("toes.", "es_pop", .3)],
   keys=[(0, 1.0, .5, .5), ("heels", 1.25, .3, .85), ("toes.", 1.0, .5, .5)]),
 # ===== DAY 20 =====
 DAY("Day twenty.", 20, "THE JEANS"),
 P("My jeans felt tight around my thighs. In a good way.", [BG("bk_mirror", "slide_l"), W_([("stand_done", 0), ("sq_jeans", "jeans")], x1=0.32)],
   [R("tight", "TIGHT JEANS", RED, y=0.25), R("good", "(GOOD TIGHT)", TEAL, y=0.42, size=80)], sfx=[(0, "es_whoosh", .3), ("tight", "es_squeak", .3), ("good", "es_ding", .3)]),
 MM("Wait. Your legs got bigger without weights?", [BG("bk_mirror"), F([("sq_jeans", 0)], x=0.35)], "s6_mini_squint_cut", sfx=[(0, "es_pop", .3)]),
 P("A little, yes. For a beginner, one hundred reps a day is enough to grow.", [BG("bk_mirror"), F([("g_shrug", 0), ("g_flex", "grow.")])],
   [R("beginner,", "BEGINNERS:", NAVY, y=0.25), R("enough", "100/DAY = GROWTH", TEAL, y=0.42, size=90)], sfx=[("beginner,", "es_pop", .3), ("grow.", "es_ding", .3)]),
 P("And my glutes finally filled out my pants.", [BG("bk_mirror"), F([("sq_jeans", 0)])], [R("glutes", "GLUTES: YES", TEAL, y=0.3, size=130)], sfx=[("glutes", "es_boing", .3)]),
 MM("Too much information.", [BG("bk_mirror"), F([("g_facepalm", 0)], x=0.35)], "mini_shy_cut", sfx=[(0, "es_pop2", .3)]),
 # ===== DAY 30 =====
 DAY("Day thirty.", 30, "THE FINAL TEST"),
 P("The final test. On day one, I could do thirty-five squats without stopping.", [BG("bk_garage", "slide_r"), SQ(8, 0.38)], counters=[REP("one,", 0, 35, 1.6, col=RED)],
   sfx=[(0, "es_whoosh", .3), ("stopping.", "es_thud", .3)]),
 P("Today, I did one hundred in a row.", [BG("bk_garage"), SQ(14, 0.22)], counters=[REP(0, 35, 100, 2.4, col=TEAL)], particles=[dict(at="row.", x=0.74, y=0.4, spread=0.25)],
   sfx=[("hundred", "es_rise", .3), ("row.", "es_cheer", .25)], keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .5)]),
 P("Almost three times more.", [BG("bk_rooftop", "slide_l"), F([("stand_win", 0)])], [R("three", "3X MORE", RED, y=0.35, size=170)], sfx=[(0, "es_whoosh", .3), ("three", "es_impact", .2)]),
 P("My legs look stronger, stairs feel easy, and I can stand up from the floor without hands.",
   [BG("bk_rooftop"), F([("g_flex", 0), ("sit_cross", "floor"), ("rise_mid", "without"), ("stand_win", "hands.")])],
   [R("stronger,", "STRONGER", TEAL, y=0.2), R("easy,", "EASY STAIRS", TEAL, y=0.36), R("hands.", "NO HANDS", NAVY, y=0.52)],
   sfx=[("stronger,", "es_pop", .3), ("easy,", "es_pop", .3), ("floor", "es_thud", .3), ("hands.", "es_ding", .3)]),
 MM("The sit-down stand-up test! Ten points!", [BG("bk_rooftop"), F([("stand_win", 0)], x=0.35)], "mini_laugh_cut", kinetic=[R("Ten", "10/10", TEAL, x=0.62, y=0.2, size=150)],
    sfx=[(0, "es_pop", .3), ("Ten", "es_ding", .3)]),
 P("Ten points. But here's the honest part.", [BG("bk_night", "slide_r"), H_([("g_think", 0)], **CLOSE)], [R("honest", "THE HONEST PART", RED, x=0.8, y=0.15, size=80)],
   sfx=[(0, "es_whoosh", .3), ("honest", "es_rise", .2)]),
 P("After two weeks, it got easy. To keep growing, you have to make it harder.", [BG("bk_night"), F([("g_shrug", 0), ("p_wag", "harder.")])],
   [R("easy.", "TOO EASY", NAVY, y=0.25), R("harder.", "MAKE IT HARDER", RED, y=0.45, size=90)], sfx=[("easy.", "es_pop", .3), ("harder.", "es_impact", .2)]),
 P("Slow down each rep, pause at the bottom, or hold a backpack full of books.", [BG("bk_garage", "slide_l"), F([("squat_b", 0), ("sq_bottom", "pause"), ("sq_pack", "backpack")])],
   [R("Slow", "1. SLOW", NAVY, y=0.22), R("pause", "2. PAUSE", NAVY, y=0.38), R("backpack", "3. BACKPACK", TEAL, y=0.54)],
   sfx=[(0, "es_whoosh", .3), ("Slow", "es_pop", .3), ("pause", "es_pop", .3), ("backpack", "es_thud", .3)]),
 # ===== HOW TO =====
 card("If you want to try it,", "HOW TO", "START TODAY"),
 P("start with fifty a day, in small sets. Add ten more every few days.", [BG("bk_studio", "slide_r"), SQ(8, 0.4)],
   [R("fifty", "50 / DAY", NAVY, y=0.25, size=140), R("ten", "+10", TEAL, y=0.48, size=170)], sfx=[(0, "es_whoosh", .3), ("fifty", "es_pop", .3), ("ten", "es_ding", .3)]),
 P("Feet shoulder width apart. Sit back like there's a chair behind you. Chest up. Then push through your heels.",
   [BG("bk_studio"), F([("stand_done", 0), ("sit_lower", "Sit"), ("sq_bottom", "chair"), ("stand_done", "push"), ("g_thumbs", "heels.")])],
   [R("shoulder", "SHOULDER WIDTH", NAVY, y=0.2, size=80), R("Sit", "SIT BACK", NAVY, y=0.34, size=90), R("Chest", "CHEST UP", NAVY, y=0.48, size=90), R("heels.", "PUSH: HEELS", TEAL, y=0.62, size=90)],
   sfx=[("shoulder", "es_pop", .3), ("Sit", "es_pop", .3), ("Chest", "es_pop", .3), ("heels.", "es_ding", .3)]),
 P("How many squats can you do in a row right now? Test it, and comment your number.", [BG("bk_rooftop", "slide_l"), SQ(10, 0.34)], counters=[REP(0.4, 0, 99, 3.0)],
   kinetic=[R("comment", "COMMENT YOUR NUMBER", RED, y=0.78, size=70)], sfx=[(0, "es_whoosh", .3), ("comment", "es_pop", .3)]),
]
PLAN = dict(L.PLAN, dir=f"{HERE}/scenes_long12", words=f"{HERE}/voice/long12_cut.words.json", voice=f"{HERE}/voice/long12_cut.wav", scenes=S,
            music_db=24, sfx_db=18, duck=True, pose_pop=0.0, pose_xf=0.1, smooth_moves=True)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long12{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
