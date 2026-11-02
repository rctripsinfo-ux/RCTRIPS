# Day 4 MIX (owner 1 Nov: "make Day 4 like Day 5 / Day 6"): WHITE set, H library poses animated on the words
# (phone scrolling -> hunched over the phone, point, teacher, count 3, stopwatch, hunched -> sitting tall, thumbs up)
# mixed with the owner's Day 4 scene images (concrete head, ropes, crowd, scale, anatomy, comparisons, chin tucks,
# doorway, wall angels, doctor). Highlights vary (pain circle, spotlight, tag, arrow, ring). White middle captions.
# usage: python3 d04m_plan.py [t0 t1]   -> final/day04.mp4
import sys
from director import render, HERE

def loop(a, b, at, n, step=0.4):
    return [((a, b)[k % 2], (at + k * step) if isinstance(at, (int, float)) else (at if k == 0 else f"{at}+{round(k * step, 2)}")) for k in range(n)]
STAND = dict(width=0.86, y=0.6)
SIT = dict(width=0.8, x=0.42, y=0.6)
RED = (225, 29, 46)

S = [
 dict(text="You finish a long day on your phone or laptop,", poses=loop("hero_phone_scroll", "hero_phone_scroll_v2", 0, 4, 0.45) + [("hero_bad_posture_desk", "laptop")],
      place=STAND, enter=("right", 0.4, 0.3), keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], sfx=[(0, "whoosh_soft", .2)],
      texts=[dict(text="STIFF NECK?", at=0, y=0.13, size=170, color=RED)]),
 dict(text="and your neck feels stiff and heavy.", img="02.jpg", tr="smash", d=0.34, keys=[(0, 1.0, .5, .5), ("E", 1.1, .42, .42)],
      shake=[("heavy", .04)], sfx=[(0, "whoosh_fast", .3), ("heavy", "concrete_break", .45)],
      marks=[dict(at="stiff", style="pain", x=.66, y=.55, r=.1)]),
 dict(text="Your shoulders are tight,", img="03.jpg", tr="zoom", keys=[(0, 1.0, .5, .45), ("E", 1.1, .5, .4)],
      marks=[dict(at="shoulders", style="tag", text="TIGHT", x=.3, y=.4)]),
 dict(text="and you keep rolling your head to get some relief.", img="04.jpg", tr="swing", d=0.36, keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .4)],
      sfx=[("rolling", "bone_crack", .45)]),
 dict(text="If that sounds like you,", poses=[("hero_point_viewer", 0)], place=STAND, tr="push_l", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .42)]),
 dict(text="you're not alone,", img="06.jpg", tr="flash", keys=[(0, 1.6, .5, .43), ("E-0.15", 1.0, .5, .5)]),       # zoom-out reveal: the crowd
 dict(text="and there's a simple reason it happens.", poses=[("hero_teacher_pointer", 0)], place=dict(width=0.86, x=0.45, y=0.6), tr="zoom",
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)]),
 dict(text="Your head weighs about five kilos.", img="08.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("kilos", 1.12, .4, .45)],
      marks=[dict(at="five", style="spot", x=.33, y=.42, r=.14)], sfx=[("five", "pop", .4)]),
 dict(text="When you tilt it forward to look down at a screen,", img="09.jpg", tr="push_u", keys=[(0, 1.12, .5, .3), ("E", 1.12, .58, .42)],
      marks=[dict(at="forward", style="arrow", x=.55, y=.2, r=.07, arrow="left")]),
 dict(text="your neck muscles have to work much harder to hold it up.", img="10.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.12, .42, .4)],
      marks=[dict(at="neck", style="pain", x=.42, y=.42, r=.12)], shake=[("harder", .03)], sfx=[("harder", "hammer", .25)]),
 dict(text="Research suggests a deep forward tilt can feel like many times that weight.", img="11.jpg", tr="push_l",
      keys=[(0, 1.6, .27, .5), ("deep", 1.6, .27, .5), ("feel", 1.6, .73, .5)], shake=[("many", .03)], sfx=[("deep", "swish", .3)]),
 dict(text="Do that for hours every day", img="12.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .45)]),
 dict(text="and your neck gets tired and sore.", img="13.jpg", tr="push_r", keys=[(0, 1.0, .5, .5), ("E", 1.1, .45, .35)],
      marks=[dict(at="neck", style="pain", x=.4, y=.25, r=.1)]),
 dict(text="Here are three easy moves to fix it.", poses=[("hero_count_3", 0)], place=dict(width=0.8, y=0.64), tr="smash",
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], texts=[dict(text="3 EASY MOVES", at="three", y=0.14, size=150, color=RED)],
      shake=[("three", .04)], sfx=[(0, "whoosh_fire", .35), ("three", "hammer", .3)]),
 # --- #1 chin tucks: card -> hunched -> sits tall (pose swap) -> tuck panels -> double chin -> stopwatch
 dict(text="First, chin tucks.", img="15.jpg", card=("01", "CHIN TUCKS"), tr="push_l", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Sit tall and gently", poses=[("hero_bad_posture_desk", 0), ("hero_good_posture_desk", "tall")], place=SIT, tr="push_l",
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)], sfx=[("tall", "swoosh_up", .3)]),
 dict(text="slide your chin straight back,", img="17.jpg", tr="push_l", keys=[(0, 1.5, .28, .45), (0.25, 1.5, .28, .45), ("E-0.1", 1.5, .72, .45)],
      marks=[dict(at="back", style="arrow", x=.83, y=.5, r=.05, arrow="right")], sfx=[(0.25, "swish", .3)]),
 dict(text="like you're making a double chin.", img="18.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .55)],
      marks=[dict(at="double", style="tag", text="DOUBLE CHIN", x=.5, y=.66)]),
 dict(text="Hold for three seconds and do ten.", poses=[("hero_stopwatch", 0)], place=STAND, tr="push_l", keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)],
      texts=[dict(text="3 SEC", at="three", until="ten", y=0.14, size=170, color=RED), dict(text="x10", at="ten", y=0.14, size=200, color=RED)],
      sfx=[("three", "click", .45), ("ten", "click", .45)]),
 # --- #2 doorway stretch
 dict(text="Second, the doorway stretch.", img="20.jpg", card=("02", "DOORWAY STRETCH"), tr="push_r", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Put your forearms on a door frame", img="21.jpg", tr="push_r", keys=[(0, 1.0, .5, .5), ("E", 1.1, .5, .38)],
      marks=[dict(at="forearms", style="ring", x=.8, y=.35, r=.08, arrow="right")]),
 dict(text="and step forward slowly until you feel your chest open.", img="22.jpg", tr="push_r", keys=[(0, 1.0, .5, .5), ("E", 1.12, .5, .38)],
      marks=[dict(at="chest", style="spot", x=.5, y=.33, r=.16)], sfx=[("open", "stretch", .3)]),
 dict(text="Hold for twenty seconds.", img="23.jpg", tr="push_r", keys=[(0, 1.0, .5, .5), ("twenty", 1.15, .66, .52)],
      marks=[dict(at="twenty", style="arrow", x=.85, y=.6, r=.07, arrow="left")], sfx=[("twenty", "click", .45)]),
 # --- #3 wall angels
 dict(text="Third, wall angels.", img="24.jpg", card=("03", "WALL ANGELS"), tr="push_u", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Stand with your back against a wall", img="25.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .45)]),
 dict(text="and slowly slide your arms up and down,", img="26.jpg", tr="push_u", keys=[(0, 1.5, .3, .44), ("slide", 1.5, .3, .44), ("down", 1.5, .72, .44)],
      sfx=[("slide", "swoosh_up", .3)]),
 dict(text="ten times.", img="27.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .55)], sfx=[("ten", "click", .45)]),
 # --- ending: evening -> hunched over the phone -> phone up to the eyes (pose swap) -> thumbs up -> doctor
 dict(text="Do these every evening,", img="28b.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .42)]),
 dict(text="and lift your phone to eye level during the day.", img="29.jpg", tr="push_l",
      keys=[(0, 1.5, .27, .45), ("lift", 1.5, .27, .45), ("eye", 1.5, .74, .45)], sfx=[("lift", "swish", .3)],
      marks=[dict(at="level", style="tag", text="EYE LEVEL", x=.8, y=.25)]),
 dict(text="Your neck will thank you.", poses=[("hero_thumbs_up", 0)], place=STAND, tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .42)],
      texts=[dict(text="NECK: FREE", at="thank", y=0.14, size=170)], sfx=[("thank", "sparkle", .35)]),
 dict(text="If the pain is sharp or doesn't go away, see a doctor.", img="31.jpg", tr="fade", d=0.4, keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .45)],
      marks=[dict(at="sharp", until="doctor", style="arrow", x=.4, y=.62, r=.06, arrow="dl")]),
]
PLAN = dict(dir=f"{HERE}/scenes_d04v2", words=f"{HERE}/voice/day04_cut.words.json", voice=f"{HERE}/voice/day04_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", scenes=S, cap_y=0.5, lead=0.06, tail=0.6, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day04{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
