# Day 6 v2 (owner 1 Nov): WHITE set, a MIX of (a) H library poses animated by swapping real poses on the words
# (curl reps, push-up reps, dip down/up, confused -> shrug, flex) and (b) the owner's scene images where poses can't
# show it (T-shirt, glowing anatomy, cross-section, 2/3 chart, puzzle piece, overhead extension, share).
# Highlights change with the meaning (no single green circle): red pain circle, spotlight, red label tag, red arrow,
# white ring. White one-word captions in the middle (they dodge the highlight). Day 4 exercise cards.
# usage: python3 d06_plan.py [t0 t1]
import sys
from director import render, HERE

def loop(a, b, at, n, step=0.4):
    return [((a, b)[k % 2], (at + k * step) if isinstance(at, (int, float)) else (at if k == 0 else f"{at}+{round(k * step, 2)}")) for k in range(n)]
STAND = dict(width=0.92, y=0.6)

S = [
 # --- hook: curl reps from frame 1, calendar pops in on "every single day"
 dict(text="You do bicep curls every single day,", poses=loop("hero_curl_down", "hero_curl_up", 0, 7, 0.32), place=dict(width=0.86, x=0.42, y=0.6),
      enter=("right", 0.4), keys=[(0, 1.0, .5, .5), ("E", 1.08, .45, .5)], sfx=[(0, "whoosh_soft", .2)],
      extras=[dict(asset="prop_calendar", at="every", x=0.8, y=0.3, w=0.28)]),
 dict(text="but your arms still look small in your T-shirt.", img="i07.jpg", tr="smash", keys=[(0, 1.0, .5, .5), ("small", 1.12, .45, .45)],
      shake=[("small", .03)], sfx=[(0, "whoosh_fast", .3)], marks=[dict(at="small", style="tag", text="SMALL?", x=.3, y=.5)]),
 dict(text="You're working hard, so why aren't they growing?", poses=[("hero_confused_scratch", 0), ("hero_shrug", "why")], place=STAND,
      tr="zoom", keys=[(0, 1.0, .5, .5), ("growing", 1.1, .5, .4)], sfx=[("why", "pop", .3)]),
 dict(text="Here's the secret most people miss.", img="i16.jpg", tr="flash", keys=[(0, 1.18, .4, .45), ("E", 1.0, .5, .5)], sfx=[(0, "whoosh_fire", .3)]),
 # --- the why
 dict(text="Your bicep is the muscle on the front of your arm.", poses=[("hero_curl_up", 0)], place=STAND, tr="swing",
      keys=[(0, 1.0, .5, .5), ("front", 1.1, .5, .45)],
      marks=[dict(at="bicep", style="pain", x=.36, y=.38, r=.065)]),
 dict(text="Your tricep is on the back,", poses=[("hero_back_double_biceps", 0)], place=dict(width=0.84, x=0.42, y=0.6), tr="push_l",
      keys=[(0, 1.0, .5, .5), ("back", 1.06, .45, .45)], extras=[dict(asset="anat_muscle_triceps", at="back", x=0.8, y=0.72, w=0.3)],
      marks=[dict(at="tricep", style="spot", x=.28, y=.32, r=.08)]),
 dict(text="and it's actually bigger.", img="i18.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("bigger", 1.1, .45, .35)],
      shake=[("bigger", .03)], sfx=[("bigger", "hammer", .3)], marks=[dict(at="actually", style="tag", text="BIGGER", x=.27, y=.2)]),
 dict(text="It makes up about two-thirds of your upper arm.", img="i13.jpg", tr="push_l", keys=[(0, 1.0, .5, .5), ("two-thirds", 1.1, .6, .45)],
      marks=[dict(at="two-thirds", style="arrow", x=.66, y=.38, r=.12, arrow="dr")]),
 dict(text="So if you only train biceps,", img="i01.jpg", tr="whip_r", keys=[(0, 1.0, .5, .5), ("biceps", 1.1, .42, .45)],
      marks=[dict(at="only", style="tag", text="ONLY BICEPS", x=.3, y=.46)]),
 dict(text="you're skipping the biggest part of your arm.", img="i19.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("biggest", 1.12, .6, .38)],
      marks=[dict(at="biggest", style="pain", x=.73, y=.33, r=.13)]),
 dict(text="Here are three easy moves for your triceps.", poses=[("hero_count_3", 0)], place=dict(width=0.84, y=0.64), tr="smash",
      keys=[(0, 1.0, .5, .5), ("E", 1.06, .5, .5)], texts=[dict(text="3 EASY MOVES", at="three", y=0.13, size=150, color=(225, 29, 46))],
      shake=[("three", .04)], sfx=[(0, "whoosh_fire", .35), ("three", "hammer", .3)]),
 # --- #1 close-grip push-ups: card -> scene image for the hand position -> real push-up reps
 dict(text="First, close-grip push-ups.", img="i15.jpg", card=("01", "CLOSE-GRIP PUSH-UPS"), tr="push_l", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Put your hands close together under your chest", img="i03.jpg", tr="push_l", keys=[(0, 1.0, .5, .5), ("close", 1.12, .55, .62)],
      marks=[dict(at="close", style="tag", text="HANDS CLOSE", x=.35, y=.72)]),
 dict(text="and keep your elbows tucked in. Do ten.", poses=loop("hero_pushup_top", "hero_pushup_mid", 0, 10, 0.45), place=dict(width=0.92, x=0.5, y=0.58),
      tr="push_l", keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], texts=[dict(text="x10", at="ten", y=0.2, size=200, color=(225, 29, 46))],
      marks=[dict(at="elbows", until="Do", style="arrow", x=.6, y=.56, r=.05, arrow="down")], sfx=[("ten", "click", .45)]),
 # --- #2 bench dips: card -> chair grip image -> dip down on "lower", up on "push", reps
 dict(text="Second, bench dips.", img="i02.jpg", card=("02", "BENCH DIPS"), tr="push_r", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Put your hands on a chair behind you,", img="i04.jpg", tr="push_r", keys=[(0, 1.0, .5, .5), ("chair", 1.1, .45, .5)],
      marks=[dict(at="chair", style="arrow", x=.3, y=.45, r=.08, arrow="left")]),
 dict(text="bend your elbows to lower yourself, then push back up. Do twelve.",
      poses=[("hero_dip_top", 0), ("hero_dip_bottom", "lower")] + loop("hero_dip_top", "hero_dip_bottom", "push", 8, 0.5), place=STAND, tr="push_r",
      keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .5)], texts=[dict(text="x12", at="twelve", y=0.15, size=200, color=(225, 29, 46))],
      marks=[dict(at="elbows", until="push", style="ring", x=.42, y=.46, r=.06, arrow="left")],
      sfx=[("push", "swoosh_up", .35), ("twelve", "click", .45)]),
 # --- #3 overhead extensions: no library pose -> the owner's images as a 3-step sequence
 dict(text="Third, overhead extensions.", img="i12.jpg", card=("03", "OVERHEAD EXTENSIONS"), tr="push_u", sfx=[(0, "whoosh_swipe", .35), (0.1, "pop", .4)]),
 dict(text="Hold one dumbbell or a water bottle with both hands above your head,", img="i05.jpg", tr="push_u", keys=[(0, 1.0, .5, .5), ("above", 1.1, .5, .4)]),
 dict(text="lower it behind your head,", img="i10.jpg", tr="flash", keys=[(0, 1.0, .5, .5), ("behind", 1.1, .5, .4)],
      marks=[dict(at="lower", style="arrow", x=.35, y=.25, r=.1, arrow="left")]),
 dict(text="then lift it back up.", img="i11.jpg", tr="flash", keys=[(0, 1.08, .5, .5), ("up", 1.0, .5, .45)],
      marks=[dict(at="lift", style="pain", x=.25, y=.42, r=.09), dict(at="lift", style="pain", x=.75, y=.42, r=.09)], sfx=[("lift", "swoosh_up", .35)]),
 dict(text="Do twelve.", img="i21.jpg", tr="zoom", keys=[(0, 1.0, .5, .5), ("E", 1.06, .55, .4)], sfx=[("twelve", "click", .45)]),
 # --- ending
 dict(text="Do these twice a week along with your curls,", img="i14.jpg", tr="push_l", keys=[(0, 1.0, .5, .5), ("twice", 1.1, .62, .4)],
      marks=[dict(at="twice", style="arrow", x=.9, y=.5, r=.08, arrow="left")]),
 dict(text="and your arms will start to look fuller.", poses=[("hero_double_biceps", 0)], place=STAND, tr="zoom",
      keys=[(0, 1.0, .5, .5), ("fuller", 1.12, .5, .4)], sfx=[("fuller", "sparkle", .35)]),
 dict(text="Share this with a friend who only trains biceps.", img="i06.jpg", tr="fade", d=0.35, keys=[(0, 1.0, .5, .5), ("friend", 1.1, .55, .55)],
      marks=[dict(at="Share", style="spot", x=.6, y=.7, r=.14)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d06", words=f"{HERE}/voice/day06_cut.words.json", voice=f"{HERE}/voice/day06_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", scenes=S, cap_y=0.5, lead=0.06, tail=0.6, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/day06{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
