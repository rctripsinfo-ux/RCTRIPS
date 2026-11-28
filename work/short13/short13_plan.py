# SHORT 13 "Glute Bridges Not Working Your Glutes? Move Your Feet Here" in the Day-1 "Build Muscle the Lazy Way" format (owner, 28 Nov 2026):
# white set, act() pose swaps, auto-placed labels, #N slate cards, inset badges with tick/X, brush/squash/iris transitions, Mini-H cameo with focus blur.
# usage: LUFS=-14 python3 short13/short13_plan.py
import sys; sys.path.insert(0, __file__.rsplit("/", 2)[0] + "/week1")
from w1 import *
from director import render
I = f"{HERE}/short13/img"
def B(n): return f"{I}/{n}_al.png"
def BR(seq, **k): return act([(B(p), a) for p, a in seq], **{"w": 1.0, "y": 0.56, **k})          # bridge poses (side view, one canvas)
def REPS(a, b, n, step, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def INS(at, n, crop, mark, until=None): return dict(at=at, until=until, asset=B(n), crop=crop, x=0.8, y=0.16, r=0.12, bg=(236, 230, 214), mark=mark, mark_delay=0.15)
HAM, QUAD, GLU, BACK = (0.6, 0.68, 0.25), (0.72, 0.29, 0.25), (0.63, 0.49, 0.25), (0.48, 0.5, 0.25)
S = [
 dict(text="Doing glute bridges and only feeling your thighs?", poses=[], layers=[BR([("gb_down", 0), ("gb_close", "bridges")])], labels=[lab("thighs?", "THIGHS?", y=0.3)],
      insets=[INS("thighs?", "gb_close", QUAD, "x")], keys=hook_keys((.6, .55)), sfx=[(0, "whoosh_big", .2), ("thighs?", "pop", .3)]),
 dict(text="Your feet are in the wrong spot.", poses=[], tr="squash", d=0.37, layers=[BR([("gb_far", 0), ("gb_close", "wrong")])], labels=[lab("wrong", "WRONG SPOT", y=0.3)],
      shake=[("wrong", .03)], keys=[(0, 1.0, .5, .5)] + punch("spot.", 1.0, 1.1, (.6, .6)), sfx=[("wrong", "es_error", .25)]),
 dict(text="Wait. My feet control my butt?", poses=[], tr="cut", layers=[act([("g_shock", 0)]), mini("s6_mini_squint_cut")], keys=[(0, 1.06, .5, .45)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Completely.", poses=[], tr="cut", layers=[act([("g_thumbs", 0)])], keys=[(0, 1.0, .5, .45)] + punch("Completely.", 1.0, 1.08, (.5, .4)), sfx=[(0, "pop", .3)]),
 card("Fix one.", "#1", "FEET POSITION", "brush"),
 dict(text="Feet too far away? Your hamstrings take over.", poses=[], tr="brush", d=0.3, layers=[BR([("gb_down", 0), ("gb_far", "far"), ("gb_down", "Your"), ("gb_far", "hamstrings")], enter=("slide_r", 0.5))],
      labels=[lab("far", "TOO FAR", y=0.3)], insets=[INS("hamstrings", "gb_far", HAM, "x")], sfx=[("far", "pop", .3), ("hamstrings", "es_error", .25)]),
 dict(text="Feet too close? Your thighs take over.", poses=[], tr="squash", d=0.37, layers=[BR([("gb_down", 0), ("gb_close", "close?"), ("gb_down", "Your"), ("gb_close", "thighs")])],
      labels=[lab("close?", "TOO CLOSE", y=0.3)], insets=[INS("thighs", "gb_close", QUAD, "x")], sfx=[("close?", "pop", .3), ("thighs", "es_error", .25)]),
 dict(text="Put your heels about one foot from your hips.", poses=[], tr="fade", d=0.3, layers=[BR([("gb_down", 0)])], labels=[lab("foot", "1 FOOT FROM YOUR HIPS", y=0.3)],
      arcs=[dict(at="foot", x=0.62, y=0.7, r=0.1, a0=180, a1=360)], keys=[(0, 1.0, .5, .5), ("E", 1.12, .62, .65)], sfx=[("foot", "pop", .3)]),
 dict(text="At the top, your shins point straight up.", poses=[], tr="cut", layers=[BR([("gb_down", 0), ("gb_up", "top,")], ghost=dict(asset=B("gb_down"), at="top,", alpha=0.3))],
      labels=[lab("shins", "SHINS STRAIGHT UP", y=0.28)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .55, .55)], sfx=[("top,", "whoosh_short", .25), ("shins", "pop", .3)]),
 dict(text="Like a table!", poses=[], tr="cut", layers=[BR([("gb_up", 0)]), mini("mini_laugh_cut", "l")], keys=[(0, 1.05, .5, .5)], sfx=[(0, "pop_soft", .3)]),
 dict(text="Exactly.", poses=[], tr="cut", layers=[BR([("gb_up", 0)])], labels=[lab(0, "TABLE TOP", y=0.3)], keys=[(0, 1.0, .55, .55), (0.1, 1.08, .55, .55)], sfx=[(0, "pop", .3)]),
 card("Fix two.", "#2", "HEELS", "brush"),
 dict(text="Push through your heels, not your toes.", poses=[], tr="brush", d=0.3, layers=[BR([("gb_up", 0), ("gb_toes", "toes.")], enter=("slide_r", 0.5))],
      labels=[lab("heels,", "HEELS DOWN", y=0.28, until="toes."), lab("toes.", "NOT TOES", y=0.28)], shake=[("toes.", .02)],
      keys=[(0, 1.0, .5, .5), ("E", 1.12, .7, .7)], sfx=[("heels,", "pop", .3), ("toes.", "es_error", .25)]),
 card("Fix three.", "#3", "SQUEEZE", "iris:1.0,0.4"),
 dict(text="Squeeze at the top for two seconds.", poses=[], tr="brush", d=0.3, layers=[BR([("gb_down", 0), ("gb_up", 0.3), ("gb_up_red", "Squeeze")], shiver=[("Squeeze", "seconds.")])],
      labels=[lab("two", "2 SEC SQUEEZE", y=0.28)], insets=[INS("Squeeze", "gb_up_red", GLU, "tick")], particles=[dict(at="seconds.", x=0.55, y=0.5, spread=0.35)],
      sfx=[("Squeeze", "pop", .3), ("two", "es_tick", .3), ("seconds.", "chime", .4)]),
 dict(text="Don't arch your lower back.", poses=[], tr="squash", d=0.37, layers=[BR([("gb_arch", 0)])], labels=[lab("arch", "NO ARCH", y=0.28)],
      insets=[INS("lower", "gb_arch", BACK, "x")], shake=[("back.", .03)], sfx=[("arch", "es_error", .25)]),
 dict(text="Lift with your hips.", poses=[], tr="cut", layers=[BR(REPS("gb_down", "gb_up", 4, 0.3))], labels=[lab("hips.", "HIPS LIFT", y=0.28)], sfx=[("hips.", "pop", .3)]),
 dict(text="Three sets of fifteen. By rep ten, your glutes will be on fire.", poses=[], tr="fade", d=0.3, layers=[BR(REPS("gb_down", "gb_up_red", 14, 0.32))],
      labels=stack([("Three", "3 x 15"), ("ten,", "REP 10 = FIRE")], y0=0.22, dy=0.07), particles=[dict(at="fire.", x=0.55, y=0.5, spread=0.4)],
      keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .55)], sfx=[("Three", "pop", .3), ("ten,", "pop", .3), ("fire.", "chime", .4)]),
 dict(text="Where did you feel it before? Thighs, back, or glutes? Comment below.", poses=[], tr="cut", layers=[act([("g_think", 0), ("g_point", "Comment")]), mini("s9_mini_point_cut")],
      labels=stack([("Thighs,", "THIGHS?"), ("back,", "BACK?"), ("glutes?", "GLUTES?")], y0=0.12, dy=0.065), keys=[(0, 1.04, .5, .5)],
      sfx=[(0, "pop_soft", .3), ("Thighs,", "pop", .3), ("back,", "pop", .3), ("glutes?", "pop", .3)]),
]
PLAN = dict(plan(13, S), words=f"{HERE}/voice/short13_cut.words.json", voice=f"{HERE}/voice/short13_cut.wav", dir=f"{HERE}/scenes_s13", music_db=22, sfx_db=16, duck=True)
if __name__ == "__main__": render(PLAN, f"{HERE}/final/short13.mp4")
