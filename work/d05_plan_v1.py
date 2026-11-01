# Day 5 (knees hurt in squats -> weak glutes): owner's images (download_9 9:16, download_10 16:9), master workflow.
# CONCEPT "Knee detective": different from Day 4's comic punches. Red iris reveals that always open ON THE KNEE,
# fast whip-pans (motion blur) between the problem shots, a red hook banner, the cause told with zooms into the glass
# knee and a pan across the anatomy, floor exercises shown wide on white (16:9 images, no stretching), the 3 moves
# introduced by the owner's big number art (1, 2, 3) with a title banner, calm fades at the end.
# usage: python3 d05_plan.py [t0 t1]
import sys
from director import render, HERE

S = [
 dict(text="You start your squats feeling fine,", img="01.jpg",
      keys=[(0, 1.7, .5, .66), ("feeling", 1.75, .5, .66), ("E", 1.0, .5, .5)], sfx=[(0.05, "whoosh_soft", .12)]),
 dict(text="but by the tenth rep your knees begin to ache.", img="02.jpg", tr="circle:0.32,0.62", d=0.4,
      keys=[(0, 1.0, .5, .5), ("knees", 1.0, .5, .5), ("ache", 1.3, .35, .62)], shake=[("ache", .04)], sfx=[(0, "whoosh_short", .2), ("ache", "bone_crack", .45)]),
 dict(text="You try going slower and lighter,", img="03.jpg", tr="whip_l",
      keys=[(0, 1.0, .5, .5), ("lighter", 1.15, .4, .62)], sfx=[(0, "whoosh_fast", .25)]),
 dict(text="and they still feel sore.", img="04.jpg", tr="whip_r",
      keys=[(0, 1.0, .5, .5), ("E", 1.2, .45, .62)], sfx=[(0, "whoosh_fast", .25)]),
 dict(text="If that sounds like you,", img="05.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.12, .45, .45)], sfx=[(0, "whoosh_soft", .25)]),
 dict(text="the problem might not be your knees at all.", img="06.jpg", tr="circle:0.5,0.5", d=0.4,
      keys=[(0, 1.0, .5, .5), ("knees", 1.0, .5, .5), ("all", 1.35, .5, .45)], sfx=[("knees", "whoosh_short", .2)]),
 dict(text="Your glutes are the big muscles in your butt.", img="07.jpg", pad=True, tr="whip_l",
      keys=[(0, 2.4, .2, .5), ("glutes", 2.4, .2, .5), ("big", 2.4, .8, .5)], sfx=[("glutes", "swish", .3)]),  # pan: the knee (?) -> the glutes
 dict(text="Part of their job is to keep your knees steady when you bend down.", img="08.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("steady", 1.12, .5, .55), ("down", 1.12, .5, .6)]),
 dict(text="When they're weak,", img="09.jpg", pad=True, tr="whip_r",
      keys=[(0, 2.3, .22, .5), ("weak", 2.3, .6, .5)], sfx=[("weak", "electric", .2)]),  # pan: H -> the broken "glute engine"
 dict(text="your knees often cave in toward each other as you squat,", img="10.jpg", tr="circle:0.5,0.66", d=0.4,
      keys=[(0, 1.0, .5, .5), ("cave", 1.0, .5, .5), ("squat", 1.3, .5, .66)], sfx=[("cave", "whoosh_short", .2)]),
 dict(text="and that puts extra stress on them.", img="11.jpg", tr="whip_l",
      keys=[(0, 1.0, .5, .5), ("stress", 1.25, .45, .55)], shake=[("stress", .03)], sfx=[("stress", "hammer", .25)]),
 dict(text="Here are three easy moves to fix it.", img="12.jpg", tr="flash",
      keys=[(0, 1.0, .5, .48), ("E", 1.08, .5, .45)], sfx=[(0, "whoosh_fire", .3), ("three", "hammer", .3)]),
 dict(text="First, glute bridges.", img="13.jpg", tr="push_u", banner=("01 ", "GLUTE BRIDGES"),
      keys=[(0, 1.0, .5, .55), ("E", 1.1, .5, .6)], sfx=[(0, "whoosh_swipe", .3), (0.1, "pop", .35)], nocap=True),
 dict(text="Lie on your back with your knees bent,", img="14.jpg", pad=True, tr="whip_l",
      keys=[(0, 1.35, .5, .5), ("E", 1.45, .5, .5)], cap_y=0.74),
 dict(text="then squeeze your butt and lift your hips up.", img="15.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("squeeze", 1.0, .5, .5), ("lift", 1.3, .58, .45)], sfx=[("lift", "swoosh_up", .3)]),
 dict(text="Do fifteen.", img="16.jpg", tr="flash", keys=[(0, 1.0, .5, .45), ("E", 1.08, .5, .35)], sfx=[("fifteen", "click", .4)]),
 dict(text="Second, clamshells.", img="17.jpg", pad=True, tr="push_u", banner=("02 ", "CLAMSHELLS"),
      keys=[(0, 2.2, .3, .5), ("E", 2.2, .72, .5)], sfx=[(0, "whoosh_swipe", .3), (0.1, "pop", .35)], nocap=True),  # pan along the big 2 to H
 dict(text="Lie on your side with your knees bent", img="18.jpg", tr="whip_l",
      keys=[(0, 1.0, .5, .5), ("E", 1.15, .5, .5)], cap_y=0.74),
 dict(text="and open your top knee like a book.", img="19.jpg", pad=True, tr="whip_l",
      keys=[(0, 1.4, .5, .52), ("open", 1.4, .5, .52), ("book", 1.7, .62, .5)], sfx=[("open", "swoosh_up", .3)], cap_y=0.74),
 dict(text="Do fifteen on each side.", img="20.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], sfx=[("fifteen", "click", .4)], nocap=True),  # the picture itself says 15 EACH SIDE
 dict(text="Third, box squats.", img="21.jpg", tr="push_u", banner=("03 ", "BOX SQUATS"),
      keys=[(0, 1.0, .5, .55), ("E", 1.1, .5, .55)], sfx=[(0, "whoosh_swipe", .3), (0.1, "pop", .35)], nocap=True),
 dict(text="Sit back onto a chair,", img="22.jpg", tr="whip_r", keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .55)], sfx=[("Sit", "whoosh_soft", .25)]),
 dict(text="push your knees out so they stay in line with your toes,", img="23.jpg", tr="circle:0.5,0.62", d=0.4,
      keys=[(0, 1.0, .5, .5), ("knees", 1.0, .5, .5), ("toes", 1.25, .5, .7)]),
 dict(text="and stand up.", img="24.jpg", tr="whip_r", keys=[(0, 1.1, .5, .62), ("E", 1.0, .5, .45)], sfx=[("stand", "swoosh_up", .3)]),
 dict(text="Do ten.", img="25.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.08, .55, .35)], sfx=[("ten", "click", .4)]),
 dict(text="Do these three times a week,", img="26.jpg", tr="zoom", keys=[(0, 1.0, .45, .4), ("week", 1.2, .38, .33)], sfx=[("week", "pop", .3)]),
 dict(text="and watch your knees in the mirror when you squat.", img="27.jpg", tr="fade", d=0.35,
      keys=[(0, 1.0, .5, .5), ("mirror", 1.2, .62, .55)]),
 dict(text="If the pain is sharp or doesn't go away, see a doctor.", img="28.jpg", tr="fade", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .5)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05", words=f"{HERE}/voice/day05_cut.words.json", voice=f"{HERE}/voice/day05_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_vol=0.06, sfx_gain=0.6, scenes=S, cap_y=0.8, lead=0.06, tail=0.6,
            hook=dict(text=("KNEES ", "HURT?"), until="fine+0.3", y=0.085, bg=(225, 29, 46, 255), colors=((255, 255, 255), (255, 255, 255))),
            keywords=["fine", "tenth", "ache", "slower", "lighter", "sore", "knees", "glutes", "butt", "steady", "weak", "cave", "stress",
                      "three", "fix", "squeeze", "hips", "fifteen", "book", "side", "chair", "out", "toes", "ten", "week", "mirror", "sharp", "doctor"])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day05{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
