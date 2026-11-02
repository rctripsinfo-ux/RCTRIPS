# Day 4 (stiff neck) v2: owner's 31 Flow images (download_8), master workflow 1 Nov.
# CONCEPT "Tech-neck rescue, comic-book punch": hook = 4 fast hits (desk -> concrete head SMASH -> rope shoulders ->
# neck-roll swing); the science part travels in depth (zoom-through, push-ins, a zoom-out reveal of the crowd,
# motion-matched pans across the comparison images); the fix part is a clean pendulum of horizontal pushes with a white
# intro card per move (01 left, 02 right, 03 up); the ending slows down (zoom, fade).
# usage: python3 d04_plan.py [t0 t1]   -> final/day04.mp4 (or a preview clip)
import sys
from director import render, HERE

S = [  # text (exact script words), img, transition in, camera keys (t, zoom, fx, fy), caption y, shake, sfx
 dict(text="You finish a long day on your phone or laptop,", img="01.jpg",
      keys=[(0, 1.75, .32, .42), ("long", 1.8, .32, .41), ("day+0.08", 1.65, .76, .22), ("phone+0.1", 1.65, .76, .22), ("laptop+0.15", 1.0, .5, .5)],
      sfx=[(0.05, "whoosh_soft", .12), ("long", "whoosh_short", .15)]),  # stressed face -> the clock (long day) -> pull out to the desk
 dict(text="and your neck feels stiff and heavy.", img="02.jpg", tr="smash", d=0.34,
      keys=[(0, 1.0, .5, .5), ("E", 1.1, .42, .42)], shake=[("heavy", .05)], sfx=[(0, "whoosh_fast", .4), ("heavy", "concrete_break", .5)]),
 dict(text="Your shoulders are tight,", img="03.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .45), ("E", 1.14, .5, .38)], sfx=[("tight", "stretch", .45)]),
 dict(text="and you keep rolling your head to get some relief.", img="04.jpg", tr="swing", d=0.36,
      keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .35)], sfx=[(0, "whoosh_soft", .4), ("rolling", "bone_crack", .5)]),
 dict(text="If that sounds like you,", img="05.jpg", tr="push_l",
      keys=[(0, 1.0, .5, .5), ("E", 1.16, .38, .45)], sfx=[(0, "whoosh_short", .3)]),
 dict(text="you're not alone,", img="06.jpg", tr="flash",
      keys=[(0, 1.9, .5, .43), ("E-0.15", 1.0, .5, .5)]),  # zoom-OUT reveal: one man -> a whole crowd on phones
 dict(text="and there's a simple reason it happens.", img="07.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.12, .55, .38)], sfx=[(0, "whoosh_soft", .3)]),
 dict(text="Your head weighs about five kilos.", img="08.jpg", tr="push_u",
      keys=[(0, 1.0, .5, .5), ("five", 1.0, .5, .5), ("kilos+0.2", 1.45, .32, .43)], sfx=[(0, "whoosh_short", .3), ("five", "pop", .5)]),
 dict(text="When you tilt it forward to look down at a screen,", img="09.jpg", tr="push_u",
      keys=[(0, 1.35, .5, .2), ("E", 1.35, .62, .42)]),  # camera follows his eyes down to the phone
 dict(text="your neck muscles have to work much harder to hold it up.", img="10.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.25, .4, .38)], shake=[("harder", .03)], sfx=[("harder", "hammer", .3)]),
 dict(text="Research suggests a deep forward tilt can feel like many times that weight.", img="11.jpg", tr="push_l",
      keys=[(0, 1.85, .27, .5), ("deep", 1.85, .27, .5), ("feel", 1.85, .73, .5)], shake=[("many", .04)],
      sfx=[("deep", "swish", .35), ("many", "hammer", .35)]),  # pan: neutral -> forward tilt
 dict(text="Do that for hours every day", img="12.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .45)]),
 dict(text="and your neck gets tired and sore.", img="13.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("E", 1.2, .42, .3)], sfx=[(0, "whoosh_short", .3)]),
 dict(text="Here are three easy moves to fix it.", img="14.jpg", tr="smash",
      keys=[(0, 1.0, .5, .5), ("E", 1.07, .5, .4)], shake=[("three", .05)], sfx=[(0, "whoosh_fire", .45), ("three", "hammer", .45)]),
 dict(text="First, chin tucks.", card=("01", "CHIN TUCKS"), tr="push_l", sfx=[(0, "whoosh_swipe", .4), (0.1, "pop", .45)]),
 dict(text="Sit tall and gently", img="16.jpg", tr="push_l", keys=[(0, 1.15, .55, .4), ("E", 1.22, .58, .3)], cap_y=0.84),
 dict(text="slide your chin straight back,", img="17.jpg", tr="push_l",
      keys=[(0, 1.75, .28, .45), (0.25, 1.75, .28, .45), ("E-0.1", 1.75, .72, .45)], sfx=[(0.25, "swish", .35)]),  # pan: neutral -> tucked
 dict(text="like you're making a double chin.", img="18.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.15, .5, .6)], cap_y=0.87),
 dict(text="Hold for three seconds and do ten.", img="19.jpg", tr="push_l",
      keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .45)], sfx=[("three", "click", .45), ("ten", "click", .45)]),
 dict(text="Second, the doorway stretch.", card=("02", "DOORWAY STRETCH"), tr="push_r", sfx=[(0, "whoosh_swipe", .4), (0.1, "pop", .45)]),
 dict(text="Put your forearms on a door frame", img="21.jpg", tr="push_r", keys=[(0, 1.0, .5, .5), ("E", 1.12, .5, .38)]),
 dict(text="and step forward slowly until you feel your chest open.", img="22.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("E", 1.18, .5, .38)], sfx=[("open", "stretch", .35)]),
 dict(text="Hold for twenty seconds.", img="23.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("twenty", 1.35, .68, .52)], sfx=[("twenty", "click", .45)]),
 dict(text="Third, wall angels.", card=("03", "WALL ANGELS"), tr="push_u", sfx=[(0, "whoosh_swipe", .4), (0.1, "pop", .45)]),
 dict(text="Stand with your back against a wall", img="25.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .45)]),
 dict(text="and slowly slide your arms up and down,", img="26.jpg", tr="push_u",
      keys=[(0, 1.7, .3, .44), ("slide", 1.7, .3, .44), ("down", 1.7, .72, .44)], sfx=[("slide", "swoosh_up", .35)], cap_y=0.84),  # pan: position A -> B
 dict(text="ten times.", img="27.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.08, .55, .55)], sfx=[("ten", "click", .45)]),
 dict(text="Do these every evening,", img="28b.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .4)]),  # owner: the grey 3-panel image looked bad -> H relaxing on the sofa in the evening
 dict(text="and lift your phone to eye level during the day.", img="29.jpg", tr="push_l",
      keys=[(0, 1.75, .27, .45), ("lift", 1.75, .27, .45), ("eye", 1.75, .74, .45)], sfx=[("lift", "swish", .35)]),  # pan: bad -> good posture
 dict(text="Your neck will thank you.", img="30.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .4)], sfx=[("thank", "sparkle", .4)]),
 dict(text="If the pain is sharp or doesn't go away, see a doctor.", img="31.jpg", tr="fade", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .45)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d04v2", words=f"{HERE}/voice/day04_cut.words.json", voice=f"{HERE}/voice/day04_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_vol=0.06, sfx_gain=0.6, scenes=S, cap_y=0.8, lead=0.06, tail=0.6,
            hook=dict(text=("STIFF ", "NECK?"), until="and", y=0.085),
            keywords=["stiff", "heavy", "tight", "relief", "alone", "five", "kilos", "harder", "many", "hours", "sore", "three", "fix",
                      "chin", "tucks", "double", "ten", "doorway", "stretch", "forearms", "chest", "twenty", "wall", "angels",
                      "evening", "eye", "level", "thank", "sharp", "doctor"])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day04{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
