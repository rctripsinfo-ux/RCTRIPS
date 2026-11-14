# DEMO 02 "push-ups every day, still look like a fridge from behind" (14 Nov 2026), built to the measured STYLE RULEBOOK
# in research/REFERENCE-c01-BREAKDOWN.md: one flat set #BAC8D0, action on frame 1 with a 2x->1x blurred zoom-out,
# layer exits / rises on the same set, 1.6 s joke pause, grey bumper on the empty set, myth flip with labels,
# giant grey 1/2/3 behind each move, commentator cameo from a corner, ghost reps, recap collage, hard cuts only between
# sections, bottom lowercase captions built word by word, ~150 wpm, music bed 11 dB under the voice, sparse SFX.
# usage: LUFS=-20 python3 demo02_plan.py [t0 t1]
import sys
from director import render, HERE

GREY_NUM, GREY_TXT = (172, 184, 192), (118, 130, 140)
def loop(a, b, at, n, step):
    return [((a, b)[k % 2], at if k == 0 else f"{at}+{round(k * step, 2)}") for k in range(n)]

S = [
 # 1 HOOK: push-up reps already happening -> he drops out, his back rises in -> push-in, 1.6 s pause -> empty set bumper
 dict(text="You're doing push-ups every single day, but from behind you still look like a fridge? Here's the fix.", poses=[],
      layers=[dict(at=0, until="but", w=1.0, x=0.45, y=0.6,  # aligned pose PAIR (owner 14 Nov): faded top frame behind, bold frame on top
                   poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.45), ("hero_pushup_pair_b", 0.9), ("hero_pushup_pair_a", 1.35), ("hero_pushup_pair_b", 1.8), ("hero_pushup_pair_a", 2.25)],
                   ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.35),
                   shiver=[(0, "but")], exit=("rise", 0.4)),
              dict(at="behind", until="Here's", w=0.78, x=0.5, y=0.6, asset="hero_back_view", enter=("rise", 0.4), exit=("fade", 0.15))],
      bgwords=[dict(text="FRIDGE?", at="fridge?", until="Here's", y=0.16, size=210, color=GREY_TXT),
               dict(text="HERE'S THE FIX", at="Here's", y=0.46, size=170, color=GREY_TXT, cps=0.02)],
      keys=[(0, 1.9, .72, .5), (0.4, 1.0, .5, .5), ("like", 1.0, .5, .5), ("fridge?", 1.4, .5, .4), ("Here's", 1.0, .5, .5)],
      sfx=[(0.0, "whoosh_soft", .2)]),
 # 2 MYTH FLIP: front flex (chest) -> swap in place to the back flex (back) -> push into the V -> 3 fingers
 dict(text="Here's the truth. Your chest doesn't make you look wide. Your back does. And if you want that V-shape, you need to train your lats and your upper back. Here are three moves that get it done.",
      poses=[], tr="cut",
      layers=[dict(at=0, w=0.86, x=0.5, y=0.6, poses=[("hero_double_biceps", 0), ("hero_back_double_biceps", "back"), ("hero_count_3", "three")], enter=("pop", 0.5))],
      marks=[dict(at="chest", until="back", style="tag", text="CHEST", x=.5, y=.36), dict(at="back", until="V-shape", style="tag", text="BACK", x=.5, y=.36),
             dict(at="lats", until="three", style="tag", text="LATS", x=.32, y=.42)],
      keys=[(0, 1.0, .5, .5), ("wide.", 1.0, .5, .5), ("does.", 1.15, .5, .42), ("V-shape,", 1.45, .5, .4), ("three", 1.0, .5, .5)]),
 # 3 FIX 1: giant grey 1, then the row slides in front of it; reps from "Keep"
 dict(text="First, inverted rows. A table, a bar, a broomstick across two chairs, it doesn't matter. Keep your body straight, and pull your chest to the bar.",
      poses=[], tr="cut", sfx=[("rows.", "whoosh_short", .25)],
      bgwords=[dict(text="1", at=0, x=0.5, y=0.42, size=1000, color=GREY_NUM, cps=0.001)],
      layers=[dict(at="rows.", w=0.86, x=0.5, y=0.6, poses=[("hero_row_start", "rows.")] + loop("hero_row_end", "hero_row_start", "pull", 6, 0.6),
                   enter=("slide_r", 0.5))],  # no ghost: row_start / row_end are different drawings (owner 14 Nov)
      keys=[(0, 1.0, .5, .5), ("Keep", 1.0, .5, .5), ("pull", 1.1, .5, .52)]),
 # 4 FIX 2: giant grey 2, pull-up reps; "Can't do one yet?" -> a thinking cameo rises from the corner; jump up, ghost while lowering
 dict(text="Second, pull-ups. Perfect for building width without any machine. Hands wide, chest up, pull your elbows down to your ribs. Can't do one yet? Jump up and lower yourself slowly. Slow and brutal, in a good way.",
      poses=[], tr="cut", sfx=[("pull-ups.", "whoosh_short", .25)],
      bgwords=[dict(text="2", at=0, x=0.5, y=0.42, size=1000, color=GREY_NUM, cps=0.001)],
      layers=[dict(at="pull-ups.", w=0.8, x=0.5, y=0.56, enter=("slide_r", 0.5),
                   poses=[("hero_pullup_hang", "pull-ups.")] + loop("hero_pullup_top", "hero_pullup_hang", "Hands", 6, 0.8) + [("hero_pullup_top", "Jump"), ("hero_pullup_hang", "lower")]),  # no ghost until an aligned pull-up pair exists
              dict(at="Can't", w=0.55, x=0.84, y=0.86, asset="hero_thinking", enter=("corner_r", 0.45), z=2)],
      keys=[(0, 1.0, .5, .5), ("Hands", 1.0, .5, .5), ("ribs.", 1.2, .5, .42), ("Can't", 1.0, .5, .5)]),
 # 5 FIX 3: giant grey 3, dead hang holds still (no shake: it is a calm hold)
 dict(text="Third, dead hangs. This one stretches your lats and builds your grip. Arms straight, shoulders down, hold for thirty seconds.",
      poses=[], tr="cut", sfx=[("hangs.", "whoosh_short", .25)],
      bgwords=[dict(text="3", at=0, x=0.5, y=0.42, size=1000, color=GREY_NUM, cps=0.001)],
      layers=[dict(at="hangs.", w=0.9, x=0.5, y=0.58, asset="hero_deadhang_front", enter=("slide_r", 0.5))],
      texts=[dict(text="30 SEC", at="thirty", y=0.1, size=150, color=(17, 17, 17))],
      keys=[(0, 1.0, .5, .5), ("Arms", 1.0, .5, .5), ("seconds.", 1.15, .5, .4)]),
 # 6 ENDING: recap collage of the three moves + a thinking cameo with the question
 dict(text="These three back moves will turn that fridge into a V. Which one are you skipping?",
      poses=[], tr="cut",
      layers=[dict(at="These", w=0.5, x=0.28, y=0.27, asset="hero_row_end", enter=("slide_l", 0.5)),
              dict(at="three", w=0.42, x=0.76, y=0.34, asset="hero_pullup_top", enter=("slide_r", 0.5)),
              dict(at="back", w=0.42, x=0.28, y=0.66, asset="hero_hang_perfect", enter=("slide_l", 0.5)),
              dict(at="Which", w=0.52, x=0.8, y=0.86, asset="hero_thinking", enter=("corner_r", 0.45), z=2)],
      keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/demo02_cut.words.json", voice=f"{HERE}/voice/demo02_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, set=(186, 200, 208),
            scenes=S, cap_mode="build", cap_words=3, cap_size=80, cap_y=0.78, lead=0.06, tail=0.8, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/demo02{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
