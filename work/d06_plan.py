# Day 6 (small arms -> train the triceps): owner's 23 images (download_12, all 9:16), director.py.
# Day 4 camera language (gentle push-ins / pans, head stays in), Day 4 exercise cards, white one-word captions in the
# middle, rings + arrows on what the voice names (no ring sound), voice > sfx > music.
# CONCEPT "The missing piece": the hook is the frustration (curls every day -> still small -> tape measure), the
# answer is revealed like a mystery (glowing anatomy, the back of the arm, the 2/3 chart, the missing puzzle piece),
# the fix is three clean pendulum sections, the end is a flex + share.
# usage: python3 d06_plan.py [t0 t1]
import sys
from director import render, HERE

S = [
 dict(text="You do bicep curls every single day,", img="i09.jpg", enter=("right", 0.45),
      keys=[(0, 1.0, .5, .5), ("E", 1.1, .45, .45)], sfx=[(0.0, "whoosh_soft", .2)],
      marks=[dict(at="every", x=.82, y=.25, r=.1)]),                                                  # the calendar
 dict(text="but your arms still look small in your T-shirt.", img="i07.jpg", tr="smash",
      keys=[(0, 1.0, .5, .5), ("small", 1.15, .45, .45)], shake=[("small", .03)], sfx=[(0, "whoosh_fast", .3)]),
 dict(text="You're working hard, so why aren't they growing?", img="i08.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("why", 1.12, .45, .45)], marks=[dict(at="why", x=.36, y=.56, r=.13, arrow="dl")]),  # tape on the arm
 dict(text="Here's the secret most people miss.", img="i16.jpg", tr="flash",
      keys=[(0, 1.18, .4, .45), ("E", 1.0, .5, .5)], sfx=[(0, "whoosh_fire", .3)]),                   # reveal
 dict(text="Your bicep is the muscle on the front of your arm.", img="i00.jpg", tr="swing",
      keys=[(0, 1.0, .5, .5), ("front", 1.1, .5, .55)], marks=[dict(at="bicep", x=.5, y=.56, r=.17, arrow="dr")]),
 dict(text="Your tricep is on the back,", img="i17.jpg", tr="push_l",
      keys=[(0, 1.0, .5, .5), ("back", 1.12, .62, .5)], marks=[dict(at="tricep", x=.75, y=.52, r=.13, arrow="dl")]),
 dict(text="and it's actually bigger.", img="i18.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("bigger", 1.12, .5, .35)], shake=[("bigger", .03)], sfx=[("bigger", "hammer", .3)]),
 dict(text="It makes up about two-thirds of your upper arm.", img="i13.jpg", tr="push_l",
      keys=[(0, 1.0, .5, .5), ("two-thirds", 1.12, .62, .45)], marks=[dict(at="two-thirds", x=.63, y=.4, r=.15, arrow="dr")]),
 dict(text="So if you only train biceps,", img="i01.jpg", tr="whip_r",
      keys=[(0, 1.0, .5, .5), ("biceps", 1.12, .42, .45)], marks=[dict(at="only", x=.3, y=.46, r=.13, arrow="ul")]),
 dict(text="you're skipping the biggest part of your arm.", img="i19.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("biggest", 1.15, .55, .4)], marks=[dict(at="biggest", x=.73, y=.33, r=.13, arrow="right")]),  # missing piece
 dict(text="Here are three easy moves for your triceps.", img="i20.jpg", tr="smash",
      keys=[(0, 1.0, .5, .5), ("E", 1.08, .5, .45)], shake=[("three", .04)], sfx=[(0, "whoosh_fire", .35), ("three", "hammer", .3)]),
 # --- the fix (Day 4 format: card = picture on top + 01 + name -> demonstration)
 dict(text="First, close-grip push-ups.", img="i15.jpg", card=("01", "CLOSE-GRIP PUSH-UPS"), tr="push_l", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Put your hands close together under your chest and keep your elbows tucked in. Do ten.", img="i03.jpg", tr="push_l",
      keys=[(0, 1.0, .5, .5), ("hands", 1.12, .55, .62), ("elbows", 1.12, .4, .5), ("ten", 1.0, .5, .5)],
      marks=[dict(at="elbows", until="ten", x=.16, y=.62, r=.09, arrow="up")], sfx=[("ten", "click", .45)]),
 dict(text="Second, bench dips.", img="i02.jpg", card=("02", "BENCH DIPS"), tr="push_r", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Put your hands on a chair behind you,", img="i04.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("chair", 1.12, .5, .55)], marks=[dict(at="chair", x=.3, y=.45, r=.1, arrow="left")]),
 dict(text="bend your elbows to lower yourself, then push back up. Do twelve.", img="i22.jpg", tr="push_r",
      keys=[(0, 1.0, .5, .5), ("lower", 1.1, .45, .5), ("push", 1.0, .5, .5), ("twelve", 1.08, .6, .4)],
      sfx=[("push", "swoosh_up", .35), ("twelve", "click", .45)]),
 dict(text="Third, overhead extensions.", img="i12.jpg", card=("03", "OVERHEAD EXTENSIONS"), tr="push_u", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Hold one dumbbell or a water bottle with both hands above your head,", img="i05.jpg", tr="push_u",
      keys=[(0, 1.0, .5, .5), ("above", 1.1, .5, .4)]),
 dict(text="lower it behind your head,", img="i10.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("behind", 1.1, .5, .4)],
      marks=[dict(at="lower", x=.35, y=.25, r=.12, arrow="left")]),
 dict(text="then lift it back up.", img="i11.jpg", tr="push_u", keys=[(0, 1.08, .5, .5), ("up", 1.0, .5, .45)],
      marks=[dict(at="lift", x=.25, y=.42, r=.1), dict(at="lift", x=.75, y=.42, r=.1)], sfx=[("lift", "swoosh_up", .35)]),
 dict(text="Do twelve.", img="i21.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .4)], sfx=[("twelve", "click", .45)]),
 # --- ending
 dict(text="Do these twice a week along with your curls,", img="i14.jpg", tr="zoom",
      keys=[(0, 1.0, .5, .5), ("twice", 1.1, .62, .4)], marks=[dict(at="twice", x=.93, y=.2, r=.08, glow=False)]),
 dict(text="and your arms will start to look fuller. Share this with a friend who only trains biceps.", img="i06.jpg", tr="fade", d=0.35,
      keys=[(0, 1.0, .5, .5), ("fuller", 1.12, .6, .3), ("Share", 1.0, .5, .5), ("friend", 1.12, .42, .55)],
      marks=[dict(at="Share", x=.62, y=.71, r=.12, arrow="left")], sfx=[("fuller", "sparkle", .35)]),   # flex -> the phone (share)
]
PLAN = dict(dir=f"{HERE}/scenes_d06", words=f"{HERE}/voice/day06_cut.words.json", voice=f"{HERE}/voice/day06_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", scenes=S, cap_y=0.5, lead=0.06, tail=0.6, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day06{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
