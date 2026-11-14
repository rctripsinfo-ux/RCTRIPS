# DEMO 01 "Can't do a single pull-up?" (14 Nov 2026): first Short built from the competitor study
# (research/COMPETITOR-01-INITIAL.md). Original script and angle. 4 STAGES instead of 20+ slides: H stays on the
# white set, poses swap IN PLACE on the words, layers enter / leave on their own (commentator cameo from a corner,
# fall off the bar), big grey words and numbers typed BEHIND H, one close-up by camera scale, a real comedy pause
# after the hook joke. Voice ~175 wpm with pauses kept, music bed ~12 dB under the voice with ducking, -15 LUFS.
# 30 fps study (research section 9): slides 0.5 s ease-out + small overshoot, smear + streaks, 2x->1x blurred zoom-out hook.
# usage: LUFS=-15 python3 demo01_plan.py [t0 t1]
import sys
from director import render, HERE

INK, RED = (17, 17, 17), (225, 29, 46)
HANG = dict(w=0.84, x=0.5, y=0.6)        # front-view hang poses share one framing -> swaps stay in place
SIDE = dict(w=0.78, x=0.5, y=0.55)

S = [
 # STAGE A: the fail. One H, one bar; only the pose changes. Close-up on the strained face, then a held beat.
 dict(text="You grab the bar. You pull with everything you've got. And your chin... stays exactly where it was. Here's the fix.",
      poses=[], sfx=[(0.0, "whoosh_big", .2), ("grab", "click_soft", .3)],
      layers=[dict(at=0, **HANG, poses=[("hero_hang_perfect", 0), ("hero_hang_struggle", "pull")],
                   shiver=[("pull", "stays")])],
      bgwords=[dict(text="0 REPS", at="stays", y=0.9, size=210)],
      texts=[dict(text="HERE'S THE FIX", at="Here's", y=0.12, size=150, color=RED)],
      keys=[(0, 2.0, .5, .3), (0.27, 1.0, .5, .5), ("chin...", 1.0, .5, .5), ("stays", 1.35, .5, .3), ("Here's", 1.35, .5, .3), ("fix.", 1.0, .5, .5)]),
 # STAGE B: the why. Arms-only hang -> his back -> back on the bar shaking while a second H judges from the corner -> he drops.
 dict(text="Most people pull with their arms only. But a pull-up starts in your back. If your back never switches on, your arms are lifting your whole body alone. No wonder they quit.",
      poses=[], tr="push_l", sfx=[(0, "whoosh_short", .3), ("quit.", "concrete_break", .3)],
      layers=[dict(at=0, until="But", **SIDE, asset="hero_pullup_hang", shiver=[(0, "But")], exit=("fade", 0.2)),
              dict(at="But", until="If", w=0.82, x=0.5, y=0.6, asset="hero_back_view", enter=("pop", 0.3), exit=("fade", 0.2)),
              dict(at="If", until="quit.", **HANG, poses=[("hero_hang_struggle", "If")], shiver=[("If", "quit.")], exit=("fall", 0.45)),
              dict(at="arms#2", w=0.5, x=0.84, y=0.86, poses=[("hero_arms_crossed", "arms#2"), ("hero_shrug", "No")], enter=("corner_r", 0.4), z=2)],
      bgwords=[dict(text="ARMS ONLY", at="arms", until="But", y=0.13, size=170, color=(200, 205, 212)),
               dict(text="BACK FIRST", at="back", until="If", y=0.13, size=170, color=(200, 205, 212))],
      marks=[dict(at="back", until="If", style="tag", text="LATS", x=.36, y=.4)],
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .5)]),
 # STAGE C: the fix. Giant grey 1 / 2 / 3 typed behind H, the pose changes in place for each step.
 dict(text="Three steps. One: dead hangs. Just hang with straight arms for thirty seconds. That builds your grip. Two: scap pulls. Stay hanging and pull your shoulders down, without bending your arms. Do ten. Three: negatives. Jump to the top, then lower yourself as slowly as you can. Do five.",
      poses=[], tr="push_u", sfx=[(0, "whoosh_swipe", .3), ("One:", "pop", .4), ("Two:", "pop", .4), ("Three:#2", "pop", .4), ("ten.", "click", .4), ("five.", "click", .4)],
      layers=[dict(at=0, until="One:", w=0.8, x=0.5, y=0.62, asset="hero_count_3", enter=("rise", 0.3)),
              dict(at="One:", until="Three:#2", **HANG,
                   poses=[("hero_hang_perfect", "One:"), ("hero_hang_slip", "shoulders"), ("hero_hang_perfect", "shoulders+0.6"), ("hero_hang_slip", "shoulders+1.2"),
                          ("hero_hang_perfect", "shoulders+1.8"), ("hero_hang_slip", "ten."), ("hero_hang_perfect", "ten.+0.5")], enter=("pop", 0.25)),
              dict(at="Three:#2", **SIDE, poses=[("hero_pullup_hang", "Three:#2"), ("hero_pullup_top", "Jump"), ("hero_pullup_hang", "lower")],
                   ghost=dict(asset="hero_pullup_top", at="lower", alpha=0.28), enter=("pop", 0.25))],
      bgwords=[dict(text="1", at="One:", until="Two:", x=0.5, y=0.45, size=900, color=(214, 218, 224)),
               dict(text="2", at="Two:", until="Three:#2", x=0.5, y=0.45, size=900, color=(214, 218, 224)),
               dict(text="3", at="Three:#2", x=0.5, y=0.45, size=900, color=(214, 218, 224))],
      texts=[dict(text="DEAD HANG", at="dead", until="thirty", y=0.075, size=130), dict(text="30 SEC", at="thirty", until="Two:", y=0.075, size=160, color=RED),
             dict(text="SCAP PULLS", at="scap", until="ten.", y=0.075, size=130), dict(text="x10", at="ten.", until="Three:#2", y=0.075, size=180, color=RED),
             dict(text="NEGATIVES", at="negatives.", until="five.", y=0.075, size=130), dict(text="x5", at="five.", y=0.075, size=180, color=RED)],
      marks=[dict(at="lower", until="Do#2", style="arrow", x=.62, y=.45, r=.05, arrow="up")],
      keys=[(0, 1.0, .5, .5), ("E", 1.03, .5, .5)]),
 # STAGE D: the payoff + question.
 dict(text="Train this three days a week, and in a month that bar won't stand a chance. What's your max right now? Comment it below.",
      poses=[], tr="zoom", sfx=[("chance.", "sparkle", .35)],
      layers=[dict(at=0, until="What's", **SIDE, asset="hero_pullup_top", exit=("slide_l", 0.35)),
              dict(at="What's", w=0.86, x=0.5, y=0.6, asset="hero_point_viewer", enter=("slide_r", 0.5))],
      bgwords=[dict(text="3x A WEEK", at="three", until="What's", y=0.86, size=200, color=(205, 210, 216))],
      texts=[dict(text="YOUR MAX?", at="max", y=0.12, size=170, color=RED)],
      keys=[(0, 1.0, .5, .5), ("chance.", 1.1, .5, .4), ("What's", 1.0, .5, .5), ("E", 1.1, .5, .38)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/demo01_cut.words.json", voice=f"{HERE}/voice/demo01_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=12, sfx_db=14, duck=True,
            scenes=S, cap_y=0.5, lead=0.06, tail=0.8, keywords=[])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/demo01{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
