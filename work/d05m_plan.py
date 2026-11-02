# Day 5 MIX (owner 1 Nov: "make Day 5 like Day 6"): WHITE set, H library poses animated on the words (squat reps,
# sore knee, point, glutes look-back, good squat -> knees cave in, count 3, glute bridge down -> up reps, teacher)
# mixed with the owner's 9:16 scene images where poses can't show it. Highlights vary: pain circle, spotlight, tag,
# arrow, ring. White one-word captions in the middle. Day 4 exercise cards.
# usage: python3 d05m_plan.py [t0 t1]   -> final/day05.mp4
import sys
from director import render, HERE

def loop(a, b, at, n, step=0.4):
    return [((a, b)[k % 2], (at + k * step) if isinstance(at, (int, float)) else (at if k == 0 else f"{at}+{round(k * step, 2)}")) for k in range(n)]
STAND = dict(width=0.92, y=0.6)
RED = (225, 29, 46)

S = [
 dict(text="You start your squats feeling fine,", poses=loop("hero_squat_top", "hero_squat_mid", 0, 7, 0.4), place=dict(width=0.78, y=0.58),
      enter=("right", 0.4, 0.3), keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], sfx=[(0, "whoosh_soft", .2)]),
 dict(text="but by the tenth rep your knees begin to ache.", img="v20.jpg", tr="smash", keys=[(0, 1.0, .5, .5), ("knees", 1.12, .38, .5)],
      shake=[("ache", .03)], sfx=[(0, "whoosh_fast", .3), ("ache", "bone_crack", .45)],
      marks=[dict(at="knees", style="pain", x=.25, y=.565, r=.09)]),
 dict(text="You try going slower and lighter,", img="v11.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .5)],
      marks=[dict(at="slower", until="lighter", style="tag", text="SLOWER", x=.68, y=.27), dict(at="lighter", style="tag", text="LIGHTER", x=.25, y=.62)]),
 dict(text="and they still feel sore.", poses=[("hero_sore_knee", 0)], place=STAND, tr="push_l", keys=[(0, 1.0, .5, .5), ("sore", 1.03, .5, .55)],
      texts=[dict(text="STILL SORE", at="still", y=0.14, size=150, color=RED)]),
 dict(text="If that sounds like you,", poses=[("hero_point_viewer", 0)], place=STAND, tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .4)]),
 dict(text="the problem might not be your knees at all.", img="v04.jpg", tr="flash", keys=[(0, 1.2, .47, .42), ("knees", 1.0, .5, .5)],
      marks=[dict(at="knees", style="spot", x=.5, y=.5, r=.28)]),
 dict(text="Your glutes are the big muscles in your butt.", poses=[("hero_hands_hips_look_back", 0)], place=dict(width=0.84, x=0.4, y=0.6), tr="swing",
      keys=[(0, 1.0, .5, .5), ("butt", 1.06, .45, .5)], extras=[dict(asset="anat_muscle_glutes", at="glutes", x=0.8, y=0.68, w=0.32)]),
 dict(text="Part of their job is to keep your knees steady when you bend down.", img="v12.jpg", tr="push_l",
      keys=[(0, 1.0, .5, .5), ("steady", 1.1, .45, .5)], marks=[dict(at="steady", style="arrow", x=.37, y=.63, r=.07, arrow="left")]),
 dict(text="When they're weak, your knees often cave in toward each other as you squat,", poses=[("hero_squat_front", 0), ("hero_squat_wrong", "cave")],
      place=STAND, tr="whip_r", keys=[(0, 1.0, .5, .5), ("cave", 1.0, .5, .5), ("E", 1.03, .5, .55)],
      texts=[dict(text="WEAK GLUTES", at=0, until="cave", y=0.14, size=150), dict(text="KNEES CAVE IN", at="cave", y=0.14, size=150, color=RED)],
      sfx=[("cave", "whoosh_short", .3)]),
 dict(text="and that puts extra stress on them.", img="v03.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("stress", 1.06, .5, .55)],
      marks=[dict(at="stress", style="pain", x=.25, y=.68, r=.08), dict(at="stress", style="pain", x=.75, y=.68, r=.08)], sfx=[("stress", "hammer", .3)]),
 dict(text="Here are three easy moves to fix it.", poses=[("hero_count_3", 0)], place=dict(width=0.84, y=0.64), tr="smash",
      keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], texts=[dict(text="3 EASY MOVES", at="three", y=0.13, size=150, color=RED)],
      shake=[("three", .04)], sfx=[(0, "whoosh_fire", .35), ("three", "hammer", .3)]),
 # --- #1 glute bridge: card -> real bridge (down while lying, down/up reps from "lift") -> 15 counter
 dict(text="First, glute bridges.", img="v13.jpg", card=("01", "GLUTE BRIDGES"), tr="push_l", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Lie on your back with your knees bent, then squeeze your butt and lift your hips up.",
      poses=[("hero_glute_bridge_down", 0)] + loop("hero_glute_bridge_up", "hero_glute_bridge_down", "lift", 6, 0.55), place=dict(width=0.95, y=0.58),
      tr="push_l", keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], texts=[dict(text="SQUEEZE!", at="squeeze", until="lift", y=0.25, size=170, color=RED)],
      sfx=[("lift", "swoosh_up", .35)]),
 dict(text="Do fifteen.", img="v05.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .45)], sfx=[("fifteen", "click", .45)]),
 # --- #2 clamshell (no library pose): card -> the owner's image, arrow on the opening knee
 dict(text="Second, clamshells.", img="v08.jpg", card=("02", "CLAMSHELLS"), tr="push_r", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Lie on your side with your knees bent and open your top knee like a book. Do fifteen on each side.", img="v08.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("open", 1.1, .6, .5), ("Do", 1.0, .5, .5)], marks=[dict(at="open", until="Do", style="arrow", x=.66, y=.48, r=.07, arrow="up")],
      sfx=[("open", "swoosh_up", .35), ("fifteen", "click", .45)]),
 # --- #3 box squat: card -> sit back (tag) -> knees out (rings) -> stand up -> 10
 dict(text="Third, box squats.", img="v18.jpg", card=("03", "BOX SQUATS"), tr="push_u", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Sit back onto a chair,", img="v14.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("chair", 1.08, .45, .5)],
      marks=[dict(at="back", style="tag", text="SIT BACK", x=.42, y=.58)]),
 dict(text="push your knees out so they stay in line with your toes,", img="v07.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("toes", 1.08, .5, .55)],
      marks=[dict(at="knees", style="ring", x=.33, y=.68, r=.09, arrow="left"), dict(at="knees", style="ring", x=.67, y=.68, r=.09, arrow="right")]),
 dict(text="and stand up.", img="v17.jpg", tr="push_u", keys=[(0, 1.06, .5, .52), ("up", 1.0, .5, .5)], sfx=[("stand", "swoosh_up", .35)]),
 dict(text="Do ten.", img="v02.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .45)], sfx=[("ten", "click", .45)]),
 # --- ending
 dict(text="Do these three times a week,", poses=[("hero_teacher_pointer", 0)], place=dict(width=0.86, x=0.4, y=0.6), tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], extras=[dict(asset="prop_calendar", at="three", x=0.8, y=0.4, w=0.3)],
      texts=[dict(text="3x A WEEK", at="week", y=0.14, size=150, color=RED)], sfx=[("week", "pop", .35)]),
 dict(text="and watch your knees in the mirror when you squat.", img="v06.jpg", tr="push_l", keys=[(0, 1.0, .5, .5), ("mirror", 1.08, .45, .5)],
      marks=[dict(at="mirror", style="spot", x=.26, y=.62, r=.13)]),
 dict(text="If the pain is sharp or doesn't go away, see a doctor.", img="v22.jpg", tr="fade", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)],
      marks=[dict(at="sharp", until="doctor", style="arrow", x=.45, y=.5, r=.08, arrow="ur")]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/day05_cut.words.json", voice=f"{HERE}/voice/day05_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", scenes=S, cap_y=0.5, lead=0.06, tail=0.6, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day05{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
