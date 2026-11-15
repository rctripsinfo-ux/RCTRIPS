# DEMO 03 (15 Nov 2026): same script + voice as Demo 02, rebuilt with the effects library measured on 36 competitor Shorts
# (research/EFFECTS-LIBRARY-36-VIDEOS.md): circle inset badges (pop-from-big, red X / green tick), muscle colour that BLINKS 2x
# then stays, translucent discs with rolling dashed rims + whole-frame DIM, typewriter bumper with a blinking cursor,
# white label boxes that drop in, dashed motion arcs, green plus particles, focus blur behind a cameo, aspiration ghost,
# squash / brush-stroke / iris transitions into dark-slate section cards. Set #BAC8D0, bottom captions, -20 LUFS.
# usage: LUFS=-20 python3 demo03_plan.py [t0 t1]
import sys
from director import render, HERE

GREY_TXT, SLATE, SLATE_NUM = (118, 130, 140), (75, 85, 104), (104, 116, 138)
STAND = dict(w=0.62, x=0.5, y=0.6)
RED, GREEN = (225, 29, 46), (46, 170, 80)
def punch(at, z0, z1, f=(.5, .5)): return [(at, z0, *f), (f"{at}+0.1", z1, *f)]
def card(text, num, label, tr):  # dark slate section card: giant number + white label box dropping in
    return dict(text=text, poses=[], tr=tr, d=0.3, set=SLATE,
                bgwords=[dict(text=num, at=-0.5, x=0.5, y=0.4, size=640, color=SLATE_NUM, cps=0.001)],
                labels=[dict(text=label, at=0.15, x=0.5, y=0.6, size=62)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .45)])

S = [
 # 1 HOOK: push-ups to "but" (aligned pair + ghost) -> back view rises -> fridge slides in, wobbles in the pause
 dict(text="You're doing push-ups every single day, but from behind you still look like a fridge?", poses=[],
      layers=[dict(at=0, until="but", w=0.9, x=0.47, y=0.6,
                   poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.5), ("hero_pushup_pair_b", 1.0), ("hero_pushup_pair_a", 1.5), ("hero_pushup_pair_b", 2.0), ("hero_pushup_pair_a", 2.5)],
                   ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.35), exit=("rise", 0.4)),
              dict(at="behind", w=0.6, x=0.33, y=0.6, asset="hero_back_view", enter=("rise", 0.4)),
              dict(at="fridge?", w=0.34, x=0.72, y=0.6, asset="prop_fridge", enter=("slide_r", 0.45), shiver=[("fridge?+0.5", "fridge?+0.8")])],
      insets=[dict(at="push-ups", until="but", asset="hero_pushup_pair_a", crop=(0.62, 0.45, 0.42), x=0.8, y=0.17, r=0.12, paint=(0.5, 0.55, 0.22, 0.12, RED), mark="x")],
      keys=[(0, 1.9, .72, .5), (0.4, 1.0, .5, .5), ("fridge?+0.4", 1.0, .5, .5), ("fridge?+0.5", 1.15, .5, .53)],
      sfx=[(0.0, "whoosh_soft", .2), ("fridge?+0.1", "whoosh_short", .25)]),
 # 2 BUMPER: typed on the empty set with a blinking cursor (caption hidden: the line shows once)
 dict(text="Here's the fix.", poses=[], tr="cut", nocap=True,
      bgwords=[dict(text="HERE'S THE FIX", at=0, y=0.4, size=150, color=GREY_TXT, cps=0.03, cursor=True)], keys=[(0, 1.0, .5, .5)]),
 # 3 MYTH: chest -> red badge with X, chest colour blinks 2x then stays
 dict(text="Your chest doesn't make you look wide.", poses=[], tr="cut",
      layers=[dict(at=0, **STAND, asset="hero_double_biceps", enter=("pop", 0.45))],
      insets=[dict(at="chest", asset="hero_double_biceps", crop=(0.5, 0.36, 0.4), x=0.8, y=0.16, r=0.12, paint=(0.5, 0.55, 0.32, 0.14, RED), mark="x", mark_delay=0.6)],
      marks=[dict(at="chest", style="paint", text="CHEST", x=.5, y=.455, rx=.12, ry=.04, blink=2)],
      keys=[(0, 1.0, .5, .5)] + punch("wide.", 1.0, 1.1, (.5, .45))),
 # 4 FLIP: squash transition to his back; back colour blinks green + green tick badge; lats = two discs + whole frame dims
 dict(text="Your back does. And if you want that V-shape, you need to train your lats and your upper back.", poses=[], tr="squash", d=0.37,
      layers=[dict(at=0, **STAND, asset="hero_back_double_biceps")],
      insets=[dict(at="does.", until="lats", asset="hero_back_double_biceps", crop=(0.5, 0.36, 0.4), x=0.78, y=0.25, r=0.12, paint=(0.5, 0.55, 0.3, 0.2, GREEN), mark="tick")],
      marks=[dict(at="back", until="lats", style="paint", text="BACK", x=.5, y=.47, rx=.1, ry=.07, color=GREEN, blink=2),
             dict(at="lats", style="disc", x=.41, y=.468, r=.055), dict(at="lats", style="disc", x=.59, y=.468, r=.055)],
      dim=[dict(at="lats", amount=0.44, ramp=0.8)],
      keys=[(0, 1.0, .5, .5)] + punch("does.", 1.0, 1.15, (.5, .53)) + [("V-shape,", 1.15, .5, .53), ("lats", 1.15, .5, .53)]),
 # 5 THREE MOVES: three badges pop in an arc around his head, one per word beat
 dict(text="Here are three moves that get it done.", poses=[], tr="cut",
      layers=[dict(at=0, **STAND, asset="hero_count_3", enter=("pop", 0.4))],
      insets=[dict(at="three", asset="hero_row_end", crop=(0.5, 0.5, 0.75), x=0.2, y=0.17, r=0.11, bg=(236, 230, 214)),
              dict(at="moves", asset="hero_pullup_top", crop=(0.5, 0.35, 0.7), x=0.5, y=0.1, r=0.11, bg=(225, 220, 245)),
              dict(at="get", asset="hero_deadhang_front", crop=(0.5, 0.35, 0.7), x=0.8, y=0.17, r=0.11, bg=(236, 230, 214))],
      sfx=[("three", "pop", .3), ("moves", "pop", .3), ("get", "pop", .3)], keys=[(0, 1.0, .5, .5)]),
 # 6 #1 card (brush-stroke wipe in)
 card("First, inverted rows.", "#1", "INVERTED ROWS", "brush"),
 # 7 ROWS: props per noun, then the row with a dashed pull arc + lats badge
 dict(text="A table, a bar, a broomstick across two chairs, it doesn't matter. Keep your body straight, and pull your chest to the bar.",
      poses=[], tr="brush", d=0.3, sfx=[("table,", "pop", .3), ("bar,", "pop", .3), ("broomstick", "pop", .3)],
      layers=[dict(at=0, until="bar,", w=0.62, x=0.5, y=0.5, asset="prop_table", enter=("pop", 0.3), exit=("fade", 0.15)),
              dict(at="bar,", until="broomstick", w=0.7, x=0.5, y=0.5, asset="prop_pullup_bar_v2", enter=("pop", 0.3), exit=("fade", 0.15)),
              dict(at="broomstick", until="Keep", w=0.72, x=0.5, y=0.5, asset="prop_broom_chairs", enter=("pop", 0.3), exit=("fade", 0.2)),
              dict(at="Keep", w=0.66, x=0.5, y=0.6, poses=[("hero_row_start", "Keep"), ("hero_row_end", "pull")], enter=("slide_r", 0.5))],
      labels=[dict(at="matter.", until="Keep", text="ANY BAR WORKS", x=0.5, y=0.2), dict(at="straight,", text="BODY STRAIGHT", x=0.36, y=0.13),
              dict(at="chest", text="CHEST TO BAR", x=0.36, y=0.2)],
      arcs=[dict(at="pull", x=0.5, y=0.52, r=0.13, a0=110, a1=20, color=(255, 255, 255))],
      insets=[dict(at="pull", asset="hero_back_double_biceps", crop=(0.5, 0.36, 0.4), x=0.82, y=0.12, r=0.1, paint=(0.3, 0.6, 0.1, 0.16, GREEN))],
      keys=[(0, 1.0, .5, .5)] + punch("pull", 1.0, 1.12)),
 # 8 #2 card (iris from the right)
 card("Second, pull-ups.", "#2", "PULL-UPS", "iris:1.0,0.4"),
 # 9 PULL-UPS: labels drop per cue, elbow arcs, cameo with focus blur, jump + slow lower arc
 dict(text="Perfect for building width without any machine. Hands wide, chest up, pull your elbows down to your ribs. Can't do one yet? Jump up and lower yourself slowly. Slow and brutal, in a good way.",
      poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, w=0.58, x=0.5, y=0.56, enter=("slide_r", 0.5),
                   poses=[("hero_pullup_hang", 0), ("hero_pullup_top", "pull"), ("hero_pullup_hang", "Can't"), ("hero_pullup_top", "Jump"), ("hero_pullup_hang", "lower")]),
              dict(at="Can't", until="Jump", w=0.42, x=0.77, y=0.74, asset="hero_thinking", enter=("corner_r", 0.45), exit=("fade", 0.2), z=2, focus=True)],
      labels=[dict(at="Hands", until="Can't", text="HANDS WIDE", x=0.24, y=0.22), dict(at="chest", until="Can't", text="CHEST UP", x=0.76, y=0.22),
              dict(at="Jump", text="JUMP UP", x=0.24, y=0.22), dict(at="lower", text="LOWER SLOWLY", x=0.69, y=0.22)],
      arcs=[dict(at="elbows", until="Can't", x=0.36, y=0.3, r=0.09, a0=200, a1=110, color=(255, 255, 255)),
            dict(at="elbows", until="Can't", x=0.64, y=0.3, r=0.09, a0=340, a1=70, color=(255, 255, 255)),
            dict(at="lower", x=0.64, y=0.42, r=0.09, a0=300, a1=420, color=(255, 255, 255))],
      keys=[(0, 1.0, .5, .5)] + punch("brutal,", 1.0, 1.12, (.5, .53))),
 # 10 #3 card (brush)
 card("Third, dead hangs.", "#3", "DEAD HANGS", "brush"),
 # 11 DEAD HANG: long still hold, green plus particles on "stretches", lats badge, 30 SEC label
 dict(text="This one stretches your lats and builds your grip. Arms straight, shoulders down, hold for thirty seconds.", poses=[], tr="brush", d=0.3,
      layers=[dict(at=0, w=0.62, x=0.5, y=0.56, asset="hero_deadhang_front", enter=("slide_r", 0.5))],
      particles=[dict(at="stretches", until="Arms", x=0.5, y=0.5, spread=0.5)],
      marks=[dict(at="lats", until="Arms", style="paint", x=.39, y=.5, rx=.035, ry=.07, color=GREEN, blink=2),
             dict(at="lats", until="Arms", style="paint", x=.61, y=.5, rx=.035, ry=.07, color=GREEN, blink=2)],
      labels=[dict(at="grip.", text="GRIP", x=0.2, y=0.2, leader=(0.33, 0.3)), dict(at="thirty", text="30 SEC", x=0.75, y=0.12, size=64)],
      keys=[(0, 1.0, .5, .5)] + punch("thirty", 1.0, 1.1, (.5, .4))),
 # 12 PAYOFF: fridge squashes into the V: back view with his future self as a big faded ghost behind
 dict(text="These three back moves will turn that fridge into a V.", poses=[], tr="squash", d=0.37,
      layers=[dict(at="turn", w=0.84, x=0.5, y=0.55, asset="hero_back_double_biceps", alpha=0.28, enter=("fade", 0.6)),
              dict(at=0, w=0.5, x=0.5, y=0.62, asset="hero_back_view", enter=("pop", 0.4))],
      marks=[dict(at="V.", style="paint", x=.5, y=.52, rx=.1, ry=.08, color=GREEN, blink=2)],
      keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)]),
 # 13 QUESTION: thinking pose, focus on him
 dict(text="Which one are you skipping?", poses=[], tr="cut",
      layers=[dict(at=0, w=0.6, x=0.5, y=0.6, asset="hero_thinking", enter=("pop", 0.4))],
      bgwords=[dict(text="?", at="skipping?", x=0.78, y=0.3, size=300, color=GREY_TXT, cps=0.001)],
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .55)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/demo02_cut.words.json", voice=f"{HERE}/voice/demo02_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=(186, 200, 208),
            scenes=S, cap_mode="build", cap_words=3, cap_size=80, cap_y=0.78, lead=0.06, tail=0.8, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/demo03{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
