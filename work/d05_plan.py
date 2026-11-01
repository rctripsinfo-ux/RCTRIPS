# Day 5 v2 (knees hurt in squats -> weak glutes). Owner rules 1 Nov: ONLY 9:16 images (download_9), no 16:9 at all,
# Day 4's exercise intro format (picture in the upper part, big red number, name under it, then the demonstration),
# no awkward close-ups (whole H in frame, zoom <= 1.25 so no image looks soft or compressed), voice > sfx > music.
# CONCEPT "Knee detective": red iris reveals that open on the knee, whip-pans through the problem, calm pushes in the
# fix (as Day 4), camera moves that show the movement (hips up, knee open, sit back, stand up).
# Missing 9:16 assets (merged into neighbour scenes): glute anatomy, "weak glutes" visual, a "2" number art,
# clamshell knee-open frame. v09 ("15 each side", 4 tilted mini poses) left out: looks odd.
# usage: python3 d05_plan.py [t0 t1]
import sys
from director import render, HERE

S = [
 dict(text="You start your squats feeling fine,", img="v21.jpg", enter=("right", 0.45),
      keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .55)], sfx=[(0.0, "whoosh_soft", .2)]),
 dict(text="but by the tenth rep your knees begin to ache.", img="v20.jpg", tr="circle:0.36,0.66", d=0.4,
      keys=[(0, 1.0, .5, .5), ("ache", 1.12, .45, .55)], shake=[("ache", .03)], sfx=[(0, "whoosh_short", .3), ("ache", "bone_crack", .5)]),
 dict(text="You try going slower and lighter,", img="v11.jpg", tr="whip_l",
      keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .55)], sfx=[(0, "whoosh_fast", .3)]),
 dict(text="and they still feel sore.", img="v15.jpg", tr="whip_r",
      keys=[(0, 1.0, .5, .5), ("E", 1.1, .48, .6)], sfx=[(0, "whoosh_fast", .3)]),
 dict(text="If that sounds like you, the problem might not be your knees at all.", img="v04.jpg", tr="circle:0.5,0.5", d=0.4,
      keys=[(0, 1.0, .5, .5), ("E", 1.15, .5, .48)], sfx=[(0, "whoosh_short", .3)]),
 dict(text="Your glutes are the big muscles in your butt.", img="v06.jpg", tr="whip_l",
      keys=[(0, 1.25, .66, .62), ("E", 1.25, .66, .58)], sfx=[(0, "whoosh_fast", .3)]),  # H from behind: his glutes
 dict(text="Part of their job is to keep your knees steady when you bend down.", img="v12.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .58)]),
 dict(text="When they're weak, your knees often cave in toward each other as you squat, and that puts extra stress on them.", img="v03.jpg", tr="circle:0.5,0.66", d=0.4,
      keys=[(0, 1.0, .5, .5), ("cave", 1.0, .5, .5), ("squat", 1.15, .5, .62)], sfx=[("cave", "whoosh_short", .3), ("stress", "hammer", .3)]),
 dict(text="Here are three easy moves to fix it.", img="v01.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .48), ("E", 1.06, .5, .45)], sfx=[(0, "whoosh_fire", .35)]),
 # --- the fix: Day 4 format (card = picture on top, 01 + name under it -> demonstration), pushes like Day 4
 dict(text="First, glute bridges.", img="v13.jpg", card=("01", "GLUTE BRIDGES"), tr="push_l", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Lie on your back with your knees bent, then squeeze your butt and lift your hips up.", img="v10.jpg", tr="push_l",
      keys=[(0, 1.25, .5, .66), ("squeeze", 1.25, .5, .66), ("lift", 1.25, .5, .42)], sfx=[("lift", "swoosh_up", .35)]),  # camera rises with the hips
 dict(text="Do fifteen.", img="v05.jpg", tr="push_l", keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .45)], sfx=[("fifteen", "click", .45)]),
 dict(text="Second, clamshells.", img="v08.jpg", card=("02", "CLAMSHELLS"), tr="push_r", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Lie on your side with your knees bent and open your top knee like a book. Do fifteen on each side.", img="v08.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("open", 1.0, .5, .5), ("book", 1.22, .62, .56), ("Do", 1.22, .62, .56), ("side", 1.0, .5, .5)],
      sfx=[("open", "swoosh_up", .35), ("fifteen", "click", .45)]),
 dict(text="Third, box squats.", img="v18.jpg", card=("03", "BOX SQUATS"), tr="push_u", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Sit back onto a chair,", img="v14.jpg", tr="push_u", keys=[(0, 1.0, .5, .45), ("E", 1.08, .5, .55)], sfx=[("Sit", "whoosh_soft", .3)]),
 dict(text="push your knees out so they stay in line with your toes,", img="v07.jpg", tr="circle:0.5,0.75", d=0.4,
      keys=[(0, 1.0, .5, .5), ("toes", 1.15, .5, .62)]),
 dict(text="and stand up.", img="v17.jpg", tr="push_u", keys=[(0, 1.08, .5, .58), ("E", 1.0, .5, .45)], sfx=[("stand", "swoosh_up", .35)]),
 dict(text="Do ten.", img="v02.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .45)], sfx=[("ten", "click", .45)]),
 # --- ending: calm
 dict(text="Do these three times a week,", img="v19.jpg", tr="zoom", keys=[(0, 1.0, .5, .45), ("E", 1.1, .45, .4)], sfx=[("week", "pop", .35)]),
 dict(text="and watch your knees in the mirror when you squat.", img="v06.jpg", tr="fade", d=0.35,
      keys=[(0, 1.0, .5, .5), ("E", 1.1, .52, .55)]),
 dict(text="If the pain is sharp or doesn't go away, see a doctor.", img="v22.jpg", tr="fade", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .5)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/day05_cut.words.json", voice=f"{HERE}/voice/day05_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", scenes=S, cap_y=0.5, lead=0.06, tail=0.6,
            keywords=[])  # owner 1 Nov: captions all white, in the middle
# owner 1 Nov: never cut H's face or feet -> only a gentle zoom on the whole picture (1.0 <-> 1.04, centred),
# alternating in / out; no close-ups, no pans
for i, sc in enumerate(S):
    sc.pop("shake", None)
    if sc.get("img") in ("v05.jpg", "v10.jpg", "v08.jpg") and not sc.get("card"): sc["keys"] = [(0, 1.0, .5, .5)]; continue  # floor poses touch the edges: no zoom
    if not sc.get("card"): sc["keys"] = [(0, 1.0, .5, .5), ("E", 1.04, .5, .5)] if i % 2 == 0 else [(0, 1.04, .5, .5), ("E", 1.0, .5, .5)]
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day05{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
