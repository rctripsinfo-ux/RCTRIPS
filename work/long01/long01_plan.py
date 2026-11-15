# LONG 01 "I Did 100 Push-Ups Every Day for 30 Days" (16:9, ~4.7 min), THE METHOD in landscape:
# pose animation in every scene, Mini-H cameo on his lines, labels placed off faces automatically, chapter cards.
# usage: LANDSCAPE=1 LUFS=-16 python3 long01/long01_plan.py [t0 t1]
import os, sys; os.environ["LANDSCAPE"] = "1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from PIL import Image
from director import render, W, H
L, W1, P2, A2 = f"{HERE}/long01/img", f"{HERE}/week1/img", f"{HERE}/pilot2/img", f"{HERE}/week1/img2"
HD = os.path.expanduser("~/reel-engine-tool/public/library/hero")
SLATE, SLATE_NUM = (75, 85, 104), (104, 116, 138)

def path(n):
    for f in (f"{L}/{n}_al_c.png", f"{L}/{n}_c.png", f"{L}/{n}_al.png", f"{L}/{n}.png", f"{A2}/{n}_al.png", f"{W1}/{n}.png", f"{P2}/{n}.png", f"{HD}/{n}.png"):
        if os.path.exists(f): return f
    raise FileNotFoundError(n)
def wfor(n, h):  # layer width (fraction of W) that gives the picture a height of h (fraction of H)
    im = Image.open(path(n)); return h * H * im.width / im.height / W
def fig(n, at=0, until=None, x=0.32, y=0.5, h=0.9, **k): return dict(at=at, until=until, w=wfor(n, h), x=x, y=y, asset=path(n), **k)
def act(seq, at=0, until=None, x=0.32, y=0.5, h=0.9, **k):  # one layer, pose swaps on words (all poses share one canvas)
    return dict(at=at, until=until, w=wfor(seq[0][0], h), x=x, y=y, poses=[(path(p), a) for p, a in seq], **k)
def reps(a, b, n=6, step=0.55, t0=0.0): return [(a if i % 2 == 0 else b, round(t0 + i * step, 2)) for i in range(n)]
def pu(n=8, step=0.55, x=0.34, h=1.5, **k):  # the push-up rep loop (stock pair)
    return act(reps("hero_pushup_pair_a", "hero_pushup_pair_b", n, step), x=x, h=h, y=0.52, ghost=dict(asset=path("hero_pushup_pair_b"), at=0, alpha=0.25), **k)
def pair(a, b, n=8, step=0.6, x=0.4, h=0.85, **k): return act(reps(a, b, n, step), x=x, h=h, y=0.5, **k)
def mini(n, side="r"): return dict(at=0, w=wfor(n, 0.62), x=0.87 if side == "r" else 0.13, y=0.66, asset=path(n), enter=(f"corner_{side}", 0.4), z=3, focus=True)
def lab(at, text, x=0.74, y=0.25, until=None, size=58, **k): return dict(at=at, text=text, x=x, y=y, until=until, size=size, **k)
def stack(items, x=0.72, y0=0.2, dy=0.12): return [lab(a, t, x, y0 + i * dy) for i, (a, t) in enumerate(items)]
def punch(at, z0, z1, f=(.5, .5)): return [(at, z0, *f), (at + 0.1 if isinstance(at, (int, float)) else f"{at}+0.1", z1, *f)]
K = [(0, 1.0, .5, .5), ("E", 1.04, .5, .5)]
def card(text, num, label, tr="brush"):
    return dict(text=text, poses=[], tr=tr, d=0.3, set=SLATE, nocap=True, sfx=[(0, "whoosh_short", .3)],
                bgwords=[dict(text=num, at=-0.5, x=0.5, y=0.42, size=520, color=SLATE_NUM, cps=0.001)],
                labels=[dict(text=label, at=0.12, x=0.5, y=0.66, size=66, fixed=True)], keys=[(0, 1.0, .5, .5), ("E", 1.05, .5, .45)])
def M(text, base, m, side="r"): return dict(text=text, poses=[], tr="cut", layers=[base, mini(m, side)], keys=K, sfx=[(0, "pop_soft", .3)])

S = [
 # ---- HOOK ----
 dict(text="One hundred push-ups. Every day. For thirty days.", poses=[], layers=[pu(10, 0.45)],
      labels=[lab("hundred", "100 PUSH-UPS"), lab("thirty", "x 30 DAYS", y=0.4)], keys=[(0, 1.9, .3, .5), (0.35, 1.0, .5, .5), ("E", 1.05, .5, .5)],
      shake=[("thirty", .04)], sfx=[(0, "whoosh_big", .2), ("hundred", "pop", .3), ("thirty", "pop", .3)]),
 dict(text="No gym, no weights, no days off.", poses=[], tr="squash", d=0.37, layers=[act([("g_cross", 0), ("g_palm", "weights,"), ("g_hips", "days")])],
      labels=stack([("gym,", "NO GYM"), ("weights,", "NO WEIGHTS"), ("days", "NO DAYS OFF")]), keys=K, sfx=[("gym,", "pop", .3), ("weights,", "pop", .3), ("days", "pop", .3)]),
 M("That's three thousand push-ups! You can barely do twenty!", act([("g_hips", 0)]), "mini_scared_cut") | dict(labels=[lab("three", "3,000", x=0.6, y=0.2)]),
 dict(text="Exactly. So let's see what actually happens to the body. Day by day.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("g_point", "see"), ("g_think", "body."), ("g_one", "Day")])],
      labels=[lab("Day", "DAY BY DAY")], keys=K + punch("Day", 1.04, 1.1, (.4, .45)), sfx=[("Day", "pop", .3)]),
 M("And if it goes wrong, I get to say I told you so.", act([("g_think", 0)]), "mini_laugh_cut"),
 # ---- DAY 1 ----
 card("Day one.", "1", "DAY 1: THE TEST"),
 dict(text="First, a test. Max push-ups in one go, clean form.", poses=[], tr="brush", d=0.3, layers=[act([("g_one", 0), ("g_point", "Max"), ("g_palm", "clean")])],
      labels=[lab("Max", "MAX TEST"), lab("clean", "CLEAN FORM", y=0.38)], keys=K, sfx=[("Max", "pop", .3), ("clean", "pop", .3)]),
 dict(text="Chest close to the floor, body straight like a plank.", poses=[], tr="cut", layers=[pu(8, 0.55)],
      labels=[lab("Chest", "CHEST TO FLOOR"), lab("straight", "BODY STRAIGHT", y=0.38)], keys=K, sfx=[("Chest", "pop", .3), ("straight", "pop", .3)]),
 dict(text="Twenty-two. That's where we start.", poses=[], tr="cut", layers=[pu(5, 0.6)],
      labels=[lab(0.1, "MAX = 22", size=80)], particles=[dict(at=0.2, x=0.72, y=0.3, spread=0.3)], keys=K + punch(0.1, 1.0, 1.06), sfx=[(0.1, "chime", .4)]),
 M("So how do you get to a hundred?", act([("g_think", 0)]), "s6_mini_squint_cut"),
 dict(text="You don't do them all at once. You split them.", poses=[], tr="cut", layers=[act([("g_cross", 0), ("g_palm", "split")])],
      labels=[lab("split", "SPLIT THEM")], keys=K + punch("split", 1.0, 1.06, (.4, .45)), sfx=[("split", "pop", .3)]),
 dict(text="Five sets of twenty, or ten sets of ten, spread across the day.", poses=[], tr="brush", d=0.3, layers=[fig("L_clock", enter=("slide_r", 0.4))],
      labels=[lab("Five", "5 x 20"), lab("ten", "10 x 10", y=0.38), lab("spread", "ALL DAY", y=0.51)], keys=K, sfx=[("Five", "pop", .3), ("ten", "pop", .3), ("spread", "pop", .3)]),
 M("So, push-ups before breakfast. Push-ups before lunch. Push-ups before you cry.", fig("L_clock"), "mini_laugh_cut"),
 dict(text="Pretty much. Day one, a hundred done. It felt easy.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("g_flex", "hundred"), ("g_hips", "easy.")])],
      labels=[lab("hundred", "DAY 1: DONE")], particles=[dict(at="hundred", x=0.4, y=0.4, spread=0.4)], keys=K, sfx=[("hundred", "chime", .4)]),
 M("Famous last words.", act([("g_hips", 0)]), "mini_shy_cut"),
 # ---- DAY 2-3 ----
 card("Day two.", "2", "DAY 2-3: THE PAIN"),
 dict(text="Chest sore. Arms sore. Lifting a cup of tea feels like a workout.", poses=[], tr="brush", d=0.3, layers=[fig("L_sore", shiver=[(0, "workout.")])],
      labels=[lab("Chest", "CHEST: SORE"), lab("Arms", "ARMS: SORE", y=0.38)], keys=K, sfx=[("Chest", "pop", .3), ("Arms", "pop", .3)]),
 M("Is that the muscle growing?", fig("L_sore"), "s6_mini_squint_cut"),
 dict(text="No. That's normal muscle soreness from a new exercise.", poses=[], tr="cut", layers=[act([("g_cross", 0), ("g_palm", "normal"), ("g_point", "new")])],
      labels=[lab("normal", "NORMAL SORENESS")], keys=K, sfx=[("normal", "pop", .3)]),
 dict(text="It peaks around one or two days after, then it fades.", poses=[], tr="cut", layers=[act([("g_one", 0), ("g_two", "two"), ("g_thumbs", "fades.")])],
      labels=[lab("peaks", "PEAKS: DAY 1-2"), lab("fades.", "THEN FADES", y=0.38)], keys=K, sfx=[("peaks", "pop", .3), ("fades.", "pop", .3)]),
 dict(text="Soreness is not a sign of growth. It's a sign of something new.", poses=[], tr="cut", layers=[act([("g_one", 0), ("g_cross", "not"), ("g_point", "new.")])],
      labels=[lab("not", "SORE IS NOT GROWTH")], keys=K + punch("new.", 1.04, 1.1, (.4, .45)), sfx=[("not", "pop", .3)]),
 M("So the pain is just... a welcome message?", act([("g_point", 0)]), "mini_laugh_cut"),
 dict(text="A loud one. Day three, I did the hundred anyway, but in smaller sets. Ten at a time. Form first.", poses=[], tr="cut",
      layers=[act([("g_shrug", 0)], until="Day"), pu(14, 0.6, at="Day")],
      labels=[lab("Day", "DAY 3"), lab("Ten", "10 AT A TIME", y=0.38), lab("Form", "FORM FIRST", y=0.51)], keys=K,
      sfx=[("Day", "whoosh_short", .25), ("Ten", "pop", .3), ("Form", "pop", .3)]),
 # ---- WEEK 1 ----
 card("End of week one,", "W1", "WEEK 1: THE WRISTS"),
 dict(text="the muscles feel better. But something else starts talking. The wrists.", poses=[], tr="brush", d=0.3,
      layers=[act([("g_thumbs", 0), ("g_think", "But")], until="wrists."), fig("L_wrist", at="wrists.", enter=("fade", 0.2))],
      labels=[lab("wrists.", "THE WRISTS")], keys=K, sfx=[("wrists.", "whoosh_short", .25)]),
 M("Your wrists have opinions now?", fig("L_wrist"), "s6_mini_squint_cut"),
 dict(text="Seven hundred push-ups in a week is a lot of pressure on bent wrists.", poses=[], tr="cut", layers=[fig("L_wrist")],
      labels=[lab("Seven", "700 / WEEK"), lab("bent", "BENT WRISTS", y=0.38)], keys=K + punch("bent", 1.04, 1.1, (.4, .5)), sfx=[("Seven", "pop", .3), ("bent", "pop", .3)]),
 dict(text="Simple fix: do them on your fists, or hold two dumbbells, so the wrist stays straight. And spread your fingers wide.", poses=[], tr="brush", d=0.3,
      layers=[pair("L_fist_a", "L_fist_b", 16, 0.6)], labels=[lab("fists,", "ON YOUR FISTS", y=0.15), lab("straight.", "WRIST STRAIGHT", y=0.15, until=None)],
      keys=K, sfx=[("fists,", "pop", .3), ("straight.", "pop", .3)]),
 M("Fist push-ups. Very action movie.", pair("L_fist_a", "L_fist_b", 6, 0.6), "mini_laugh_cut", "l"),
 dict(text="Also, elbows. Don't flare them out like a T.", poses=[], tr="cut", layers=[fig("L_elbow_bad", x=0.42, h=0.62)],
      labels=[lab("flare", "NOT LIKE A T", y=0.12)], keys=K + punch("T.", 1.04, 1.1, (.42, .5)), sfx=[("flare", "pop", .3)]),
 dict(text="Keep them at about forty-five degrees from your body. Your shoulders will thank you.", poses=[], tr="squash", d=0.37, layers=[fig("L_elbow_good", x=0.42, h=0.62)],
      labels=[lab("forty-five", "45 DEGREES", y=0.12)], particles=[dict(at="thank", x=0.42, y=0.4, spread=0.4)], keys=K, sfx=[("forty-five", "pop", .3), ("thank", "chime", .4)]),
 # ---- WEEK 2 ----
 card("Week two,", "W2", "WEEK 2: STRANGE GAINS"),
 dict(text="something strange happens. The hundred gets faster. The sets get bigger. Twenty, twenty-five in a row.", poses=[], tr="brush", d=0.3,
      layers=[pu(20, 0.38)], labels=[lab("faster.", "FASTER"), lab("bigger.", "BIGGER SETS", y=0.38), lab("Twenty,", "20... 25 IN A ROW", y=0.51)], keys=K,
      sfx=[("faster.", "pop", .3), ("bigger.", "pop", .3), ("Twenty,", "pop", .3)]),
 M("Wait, did you grow muscle that fast?", pu(6, 0.38), "mini_scared_cut"),
 dict(text="Not really. Most of the early strength comes from the brain and the nerves, not new muscle.", poses=[], tr="cut",
      layers=[act([("g_cross", 0)], until="brain"), act([("L_brain", "brain"), ("L_brain_b", "nerves,")], at="brain")],
      labels=[lab("brain", "BRAIN + NERVES"), lab("not#2", "NOT NEW MUSCLE", y=0.38)], keys=K, sfx=[("brain", "whoosh_short", .25), ("not#2", "pop", .3)]),
 dict(text="Your nervous system learns the movement. It switches on more muscle fibres, at the same time, more smoothly.", poses=[], tr="cut",
      layers=[act([("L_brain", 0), ("L_brain_b", "switches"), ("L_brain", "same"), ("L_brain_b", "smoothly.")])],
      labels=[lab("learns", "IT LEARNS"), lab("more", "MORE FIBRES", y=0.38), lab("same", "AT THE SAME TIME", y=0.51)], keys=K,
      sfx=[("learns", "pop", .3), ("more", "pop", .3), ("same", "pop", .3)]),
 M("So your muscles didn't get bigger. They just got... organised.", fig("L_brain_b"), "mini_laugh_cut"),
 dict(text="Exactly. Same team, better coordination. Muscle growth you can actually see usually takes more like six to eight weeks.", poses=[], tr="cut",
      layers=[act([("g_thumbs", 0), ("g_two", "Same"), ("g_think", "Muscle"), ("g_point", "six")])],
      labels=[lab("coordination.", "BETTER TEAMWORK"), lab("six", "VISIBLE SIZE: 6-8 WEEKS", y=0.38)], keys=K, sfx=[("coordination.", "pop", .3), ("six", "pop", .3)]),
 # ---- WEEK 3 ----
 card("Week three. The mirror.", "W3", "WEEK 3: THE MIRROR"),
 M("Ooh. Abs? Huge chest? Movie star?", fig("L_mirror"), "s9_mini_point_cut"),
 dict(text="The chest and the back of the arms look a little fuller. Mostly a pump, and a little real growth.", poses=[], tr="cut", layers=[fig("L_mirror")],
      labels=[lab("chest", "CHEST"), lab("back", "TRICEPS", y=0.38), lab("Mostly", "MOSTLY A PUMP", y=0.51)], keys=K + punch("Mostly", 1.04, 1.08, (.35, .4)),
      sfx=[("chest", "pop", .3), ("back", "pop", .3), ("Mostly", "pop", .3)]),
 dict(text="Posture looks better too, because a push-up is basically a moving plank. The core works the whole time.", poses=[], tr="cut", layers=[pu(14, 0.6)],
      labels=[lab("Posture", "BETTER POSTURE"), lab("moving", "A MOVING PLANK", y=0.38), lab("core", "CORE: ON", y=0.51)], keys=K,
      sfx=[("Posture", "pop", .3), ("moving", "pop", .3), ("core", "pop", .3)]),
 M("And the belly?", pu(4, 0.6), "s6_mini_squint_cut"),
 dict(text="Same belly. A hundred push-ups burn maybe thirty to fifty calories. That's one biscuit.", poses=[], tr="cut",
      layers=[act([("g_shrug", 0)], until="hundred"), fig("L_biscuit", at="hundred", enter=("fade", 0.2))],
      labels=[lab("thirty", "= 30-50 KCAL"), lab("biscuit.", "= 1 BISCUIT", y=0.38)], keys=K + punch("biscuit.", 1.04, 1.12, (.32, .3)),
      sfx=[("thirty", "pop", .3), ("biscuit.", "pop", .3)]),
 M("One biscuit?! Three weeks of pain for a biscuit?", fig("L_biscuit"), "mini_scared_cut"),
 dict(text="Push-ups build strength. Fat loss comes from food and walking. Different jobs.", poses=[], tr="cut",
      layers=[act([("g_one", 0), ("g_two", "Fat"), ("g_palm", "Different")])],
      labels=[lab("strength.", "PUSH-UPS = STRENGTH"), lab("Fat", "FAT LOSS = FOOD + WALKING", y=0.38)], keys=K, sfx=[("strength.", "pop", .3), ("Fat", "pop", .3)]),
 # ---- WEEK 4 ----
 card("Week four.", "W4", "WEEK 4: THE PLATEAU"),
 dict(text="The hundred is now easy. Four sets of twenty-five. Done in ten minutes.", poses=[], tr="brush", d=0.3, layers=[pair("L_bored_a", "L_bored_b", 14, 0.7)],
      labels=[lab("easy.", "EASY NOW", y=0.13), lab("Four", "4 x 25", x=0.3, y=0.13), lab("ten", "10 MIN", x=0.5, y=0.87, until=None)], keys=K,
      sfx=[("easy.", "pop", .3), ("Four", "pop", .3), ("ten", "pop", .3)]),
 M("That's good, right?", pair("L_bored_a", "L_bored_b", 4, 0.7), "s9_mini_point_cut"),
 dict(text="It's good, but it's also the problem. When something gets easy, the body stops changing. It has no reason to.", poses=[], tr="cut",
      layers=[act([("g_thumbs", 0), ("g_think", "problem."), ("g_shrug", "stops"), ("g_palm", "reason")])],
      labels=[lab("problem.", "THE PROBLEM"), lab("stops", "EASY = NO CHANGE", y=0.38)], keys=K + punch("stops", 1.04, 1.1, (.35, .45)),
      sfx=[("problem.", "pop", .3), ("stops", "pop", .3)]),
 M("So the challenge... stops being a challenge.", act([("g_palm", 0)]), "s3_mini_disappointed_cut"),
 dict(text="Right. Muscles grow when you keep asking for a little more. More reps, a harder version, or slower reps.", poses=[], tr="cut",
      layers=[act([("g_point", 0), ("g_one", "More"), ("g_two", "harder"), ("g_thumbs", "slower")])],
      labels=[lab("little", "ASK FOR A LITTLE MORE", y=0.15)] + stack([("More", "+ REPS"), ("harder", "HARDER VERSION"), ("slower", "SLOWER REPS")], y0=0.3),
      keys=K, sfx=[("little", "pop", .3), ("More", "pop", .3), ("harder", "pop", .3), ("slower", "pop", .3)]),
 # ---- DAY 30 ----
 card("Day thirty.", "30", "DAY 30: THE RESULT"),
 dict(text="The final test. Max push-ups in one go.", poses=[], tr="brush", d=0.3, layers=[pu(8, 0.45)], labels=[lab("Max", "FINAL TEST")], keys=K, sfx=[("Max", "pop", .3)]),
 M("Drumroll please...", pu(6, 0.45), "mini_laugh_cut"),
 dict(text="Thirty-eight. From twenty-two to thirty-eight in one month.", poses=[], tr="squash", d=0.37, layers=[act([("g_flex", 0), ("g_thumbs", "From"), ("g_flex", "one")])],
      labels=[lab(0.05, "MAX = 38", size=80), lab("From", "22 TO 38", y=0.42)], particles=[dict(at=0.1, x=0.6, y=0.3, spread=0.5)],
      keys=K + punch(0.05, 1.0, 1.08, (.4, .45)), shake=[(0.05, .04)], sfx=[(0.05, "chime", .4), ("From", "pop", .3)]),
 M("That's almost double!", act([("g_flex", 0)]), "mini_scared_cut"),
 dict(text="Here's the honest summary. Strength: way up. Endurance: way up. Chest and arms: a little bigger. Belly fat: no change. Wrists: survived, after the fix.",
      poses=[], tr="cut", layers=[act([("g_point", 0), ("g_flex", "Strength:"), ("g_thumbs", "Endurance:"), ("g_hips", "Chest"), ("g_shrug", "Belly"), ("g_thumbs", "Wrists:")])],
      labels=stack([("Strength:", "STRENGTH: WAY UP"), ("Endurance:", "ENDURANCE: WAY UP"), ("Chest", "CHEST + ARMS: A BIT BIGGER"), ("Belly", "BELLY FAT: NO CHANGE"), ("Wrists:", "WRISTS: SURVIVED")], x=0.68, y0=0.12, dy=0.13),
      keys=K, sfx=[("Strength:", "pop", .3), ("Endurance:", "pop", .3), ("Chest", "pop", .3), ("Belly", "pop", .3), ("Wrists:", "pop", .3)]),
 # ---- THE SMARTER VERSION ----
 M("So should people do it or not?", act([("g_think", 0)]), "s6_mini_squint_cut"),
 dict(text="Do it. But do the smarter version. Three rules.", poses=[], tr="cut", layers=[act([("g_thumbs", 0), ("g_point", "smarter"), ("g_one", "Three")])],
      labels=[lab("smarter", "THE SMART VERSION")], keys=K + punch("Three", 1.04, 1.1, (.35, .45)), sfx=[("smarter", "pop", .3)]),
 card("Rule one.", "#1", "SPLIT IT"),
 dict(text="Split the reps across the day. Never grind them out in one ugly set.", poses=[], tr="brush", d=0.3,
      layers=[fig("L_clock", until="Never"), act([("g_cross", "Never")], at="Never")],
      labels=[lab("Split", "SPREAD ACROSS THE DAY"), lab("ugly", "NO UGLY SETS", y=0.38)], keys=K, sfx=[("Split", "pop", .3), ("ugly", "pop", .3)]),
 card("Rule two.", "#2", "EASY DAY"),
 dict(text="Take one easy day a week. Fifty push-ups instead of a hundred. Joints need recovery too.", poses=[], tr="brush", d=0.3, layers=[fig("d7_couch", h=1.3, x=0.36)],
      labels=[lab("easy", "1 EASY DAY / WEEK"), lab("Fifty", "50, NOT 100", y=0.38), lab("Joints", "JOINTS RECOVER", y=0.51)], keys=K,
      sfx=[("easy", "pop", .3), ("Fifty", "pop", .3), ("Joints", "pop", .3)]),
 card("Rule three.", "#3", "MAKE IT HARDER"),
 dict(text="After two weeks, make it harder. Slow the way down to three seconds, or raise your feet on a chair.", poses=[], tr="brush", d=0.3,
      layers=[pu(4, 1.5, until="raise"), pair("L_decline_a", "L_decline_b", 6, 0.7, at="raise")],
      labels=[lab("Slow", "3 SEC DOWN", until="raise"), lab("raise", "FEET ON A CHAIR", y=0.13)], keys=K, sfx=[("Slow", "pop", .3), ("raise", "whoosh_short", .25)]),
 M("And if you can't do one push-up?", act([("g_point", 0)]), "mini_shy_cut"),
 dict(text="Then start on your knees,", poses=[], tr="cut", layers=[pair("L_knee_a", "L_knee_b", 6, 0.6)], labels=[lab("knees,", "ON YOUR KNEES", y=0.13)], keys=K, sfx=[("knees,", "pop", .3)]),
 dict(text="or with your hands on a wall or a table. Same muscles, less weight. A hundred wall push-ups still counts.", poses=[], tr="squash", d=0.37,
      layers=[pair("L_wall_a", "L_wall_b", 14, 0.6, x=0.32, h=0.85)],
      labels=[lab("wall", "WALL OR TABLE"), lab("Same", "SAME MUSCLES", y=0.38), lab("counts.", "100 WALL = COUNTS", y=0.51)], keys=K,
      sfx=[("wall", "pop", .3), ("Same", "pop", .3), ("counts.", "chime", .4)]),
 # ---- CTA ----
 M("Okay. Who's actually starting tomorrow?", act([("g_point", 0)]), "s9_mini_point_cut"),
 dict(text="Do the day one test. Comment your max push-ups right now. And come back in thirty days with your new number.", poses=[], tr="cut",
      layers=[act([("g_one", 0), ("g_point", "Comment"), ("g_thumbs", "come"), ("g_flex", "new")])],
      labels=[lab("Comment", "COMMENT YOUR MAX"), lab("thirty", "DAY 30: NEW NUMBER", y=0.38)], keys=K, sfx=[("Comment", "pop", .3), ("thirty", "pop", .3)]),
 M("No lying. We will know.", act([("g_flex", 0)]), "mini_laugh_cut"),
]
for s_ in S:  # landscape: labels sit beside the figure, so keep the pose animation sharp (blur only for the 5-line summary)
    if "honest" not in s_["text"]: s_.setdefault("no_textmode", True)
PLAN = dict(dir=f"{HERE}/scenes_long01", words=f"{HERE}/voice/long01_cut.words.json", voice=f"{HERE}/voice/long01_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=13, sfx_db=16, duck=False, set=(255, 255, 255),
            scenes=S, cap_mode="build", cap_words=4, cap_size=54, cap_stroke=6, cap_y=0.9, cap_mini=(185, 168, 255),
            lead=0.06, tail=0.8, keywords=[], breathe=True)
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/long01{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
