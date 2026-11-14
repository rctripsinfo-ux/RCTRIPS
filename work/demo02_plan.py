# DEMO 02 v4 "push-ups every day, still look like a fridge from behind" (14 Nov 2026), rulebook + gap fixes
# (research/GAPS-DEMO02-vs-REFERENCE.md): H smaller on the set (~55 % of the height), long still holds, 1-4 frame
# punch zooms on key words, a fridge beside his back for the joke, props one per spoken noun, colour painted on the
# muscle, aligned push-up pair as ghost, 1-2 reps then hold, deep calm voice (~110 Hz) at ~139 wpm.
# Set #BAC8D0, bottom build-up captions, -20 LUFS.   usage: LUFS=-20 python3 demo02_plan.py [t0 t1]
import sys
from director import render, HERE

GREY_NUM, GREY_TXT = (172, 184, 192), (118, 130, 140)
STAND = dict(w=0.62, x=0.5, y=0.6)      # ~55 % of the screen height (reference median 54 %)
def punch(at, z0, z1, f=(.5, .5)):      # 3-frame punch zoom on a word
    return [(at, z0, *f), (f"{at}+0.1", z1, *f)]

S = [
 # 1 HOOK: aligned push-up pair (2 reps, ghost = top frame) -> back view rises -> the FRIDGE slides in beside him
 dict(text="You're doing push-ups every single day, but from behind you still look like a fridge? Here's the fix.", poses=[],
      layers=[dict(at=0, until="but", w=0.9, x=0.47, y=0.6,
                   poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.5), ("hero_pushup_pair_b", 1.0), ("hero_pushup_pair_a", 1.5)],
                   ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.35), exit=("rise", 0.4)),
              dict(at="behind", until="Here's", w=0.6, x=0.33, y=0.6, asset="hero_back_view", enter=("rise", 0.4), exit=("fade", 0.15)),
              dict(at="fridge?", until="Here's", w=0.36, x=0.75, y=0.6, asset="prop_fridge", enter=("slide_r", 0.45), exit=("fade", 0.15))],
      bgwords=[dict(text="HERE'S THE FIX", at="Here's", y=0.46, size=170, color=GREY_TXT, cps=0.02)],
      keys=[(0, 1.9, .72, .5), (0.4, 1.0, .5, .5), ("fridge?+0.6", 1.0, .5, .5), ("fridge?+0.7", 1.22, .5, .55), ("Here's", 1.22, .5, .55), ("Here's+0.1", 1.0, .5, .5)],
      sfx=[(0.0, "whoosh_soft", .2), ("fridge?+0.1", "whoosh_short", .25)]),
 # 2 MYTH FLIP: front flex -> CHEST painted; back flex -> BACK painted; LATS; then 3 fingers. Long still holds.
 dict(text="Here's the truth. Your chest doesn't make you look wide. Your back does. And if you want that V-shape, you need to train your lats and your upper back. Here are three moves that get it done.",
      poses=[], tr="cut",
      layers=[dict(at=0, **STAND, poses=[("hero_double_biceps", 0), ("hero_back_double_biceps", "back"), ("hero_count_3", "three")], enter=("pop", 0.5))],
      marks=[dict(at="chest", until="back", style="paint", text="CHEST", x=.5, y=.455, rx=.12, ry=.04),
             dict(at="back", until="V-shape,", style="paint", text="BACK", x=.5, y=.47, rx=.1, ry=.07),
             dict(at="lats", until="three", style="paint", text="LATS", x=.41, y=.468, rx=.04, ry=.065, color=(46, 170, 80))],
      keys=[(0, 1.0, .5, .5)] + punch("does.", 1.0, 1.18, (.5, .45)) + [("V-shape,", 1.18, .5, .45)] + punch("lats", 1.18, 1.4, (.5, .45)) + [("three", 1.4, .5, .45)] + punch("three", 1.4, 1.0)),
 # 3 FIX 1: giant 1; props pop one per noun (table, bar, broomstick on chairs), then the row: one rep and hold
 dict(text="First, inverted rows. A table, a bar, a broomstick across two chairs, it doesn't matter. Keep your body straight, and pull your chest to the bar.",
      poses=[], tr="cut", sfx=[("table,", "pop", .3), ("bar,", "pop", .3), ("broomstick", "pop", .3)],
      bgwords=[dict(text="1", at=0, x=0.5, y=0.42, size=1000, color=GREY_NUM, cps=0.001)],
      layers=[dict(at="table,", until="bar,", w=0.62, x=0.5, y=0.5, asset="prop_table", enter=("pop", 0.3), exit=("fade", 0.2)),
              dict(at="bar,", until="broomstick", w=0.7, x=0.5, y=0.5, asset="prop_pullup_bar_v2", enter=("pop", 0.3), exit=("fade", 0.2)),
              dict(at="broomstick", until="Keep", w=0.72, x=0.5, y=0.5, asset="prop_broom_chairs", enter=("pop", 0.3), exit=("fade", 0.2)),
              dict(at="Keep", w=0.66, x=0.5, y=0.6, poses=[("hero_row_start", "Keep"), ("hero_row_end", "pull")], enter=("slide_r", 0.5))],
      keys=[(0, 1.0, .5, .5)] + punch("First,", 1.0, 1.12) + [("table,", 1.0, .5, .5)] + punch("pull", 1.0, 1.15, (.5, .5))),
 # 4 FIX 2: giant 2, one rep then hold; "Can't do one yet?" cameo; jump to the top, lower slowly
 dict(text="Second, pull-ups. Perfect for building width without any machine. Hands wide, chest up, pull your elbows down to your ribs. Can't do one yet? Jump up and lower yourself slowly. Slow and brutal, in a good way.",
      poses=[], tr="cut", sfx=[("pull-ups.", "whoosh_short", .25)],
      bgwords=[dict(text="2", at=0, x=0.5, y=0.42, size=1000, color=GREY_NUM, cps=0.001)],
      layers=[dict(at="pull-ups.", w=0.58, x=0.5, y=0.56, enter=("slide_r", 0.5),
                   poses=[("hero_pullup_hang", "pull-ups."), ("hero_pullup_top", "pull"), ("hero_pullup_hang", "Can't"), ("hero_pullup_top", "Jump"), ("hero_pullup_hang", "lower")]),
              dict(at="Can't", w=0.42, x=0.84, y=0.86, asset="hero_thinking", enter=("corner_r", 0.45), z=2)],
      keys=[(0, 1.0, .5, .5)] + punch("Second,", 1.0, 1.12) + [("pull-ups.", 1.0, .5, .5)] + punch("brutal,", 1.0, 1.2, (.45, .4))),
 # 5 FIX 3: giant 3, dead hang = one long still hold
 dict(text="Third, dead hangs. This one stretches your lats and builds your grip. Arms straight, shoulders down, hold for thirty seconds.",
      poses=[], tr="cut", sfx=[("hangs.", "whoosh_short", .25)],
      bgwords=[dict(text="3", at=0, x=0.5, y=0.42, size=1000, color=GREY_NUM, cps=0.001)],
      layers=[dict(at="hangs.", w=0.62, x=0.5, y=0.56, asset="hero_deadhang_front", enter=("slide_r", 0.5))],
      texts=[dict(text="30 SEC", at="thirty", y=0.1, size=150, color=(17, 17, 17))],
      keys=[(0, 1.0, .5, .5)] + punch("Third,", 1.0, 1.12) + [("hangs.", 1.0, .5, .5)] + punch("thirty", 1.0, 1.12, (.5, .4))),
 # 6 ENDING: recap collage + thinking cameo with the question
 dict(text="These three back moves will turn that fridge into a V. Which one are you skipping?",
      poses=[], tr="cut",
      layers=[dict(at="These", w=0.5, x=0.28, y=0.27, asset="hero_row_end", enter=("slide_l", 0.5)),
              dict(at="three", w=0.42, x=0.76, y=0.34, asset="hero_pullup_top", enter=("slide_r", 0.5)),
              dict(at="back", w=0.42, x=0.28, y=0.66, asset="hero_deadhang_front", enter=("slide_l", 0.5)),
              dict(at="Which", w=0.48, x=0.8, y=0.86, asset="hero_thinking", enter=("corner_r", 0.45), z=2)],
      keys=[(0, 1.0, .5, .5)] + punch("fridge", 1.0, 1.1)),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/demo02_cut.words.json", voice=f"{HERE}/voice/demo02_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=(186, 200, 208),
            scenes=S, cap_mode="build", cap_words=3, cap_size=80, cap_y=0.78, lead=0.06, tail=0.8, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/demo02{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
