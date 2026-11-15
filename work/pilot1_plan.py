# PILOT 1 "Mirror Check: the fridge back" (15 Nov 2026), first video in OUR OWN style (research/CREATIVE-SYSTEM-PLAN.md):
# H's Playbook paper page, oval Mirror Check bookends, Mini-H as the excuse voice (second TTS voice, yellow captions),
# live orange marker scribbles, sticky notes, Effort-o-meter, X-Ray lens, page-turn transitions, marker-swipe captions.
# usage: LUFS=-20 python3 pilot1_plan.py [t0 t1]
import sys
from director import render, HERE, F_MARK

HDR = dict(font=F_MARK, color="text", cps=0.03)   # handwritten page header
def mini(at, pose="hero_shrug", x=0.82, y=0.8, w=0.3, until=None):  # Mini-H pops up from the bottom-right corner
    return dict(at=at, until=until, w=w, x=x, y=y, asset=pose, enter=("corner_r", 0.4), exit=("fade", 0.15), z=3)
def punch(at, z0, z1, f=(.5, .53)): return [(at, z0, *f), (f"{at}+0.1", z1, *f)]

S = [
 # A: hook in motion (push-up reps), then proud chest flex; marker circles the chest, sticky "CHEST 10/10"
 dict(text="Push-ups every single day. Chest looks great.", poses=[],
      layers=[dict(at=0, until="Chest", w=0.86, x=0.5, y=0.6, poses=[("hero_pushup_pair_b", 0), ("hero_pushup_pair_a", 0.45), ("hero_pushup_pair_b", 0.9), ("hero_pushup_pair_a", 1.35), ("hero_pushup_pair_b", 1.8), ("hero_pushup_pair_a", 2.25)],
                   ghost=dict(asset="hero_pushup_pair_a", at=0, alpha=0.3), exit=("rise", 0.35)),
              dict(at="Chest", w=0.62, x=0.5, y=0.6, asset="hero_double_biceps", enter=("pop", 0.4))],
      scribbles=[dict(at="great.", x=0.5, y=0.45, rx=0.17, ry=0.07)],
      labels=[dict(at="great.+0.2", text="CHEST 10/10", style="sticky", x=0.78, y=0.2, rot=6)],
      keys=[(0, 1.5, .5, .55), (0.45, 1.0, .5, .5)], sfx=[(0, "whoosh_soft", .2), ("great.", "marker", .5), ("great.+0.2", "slap", .5)]),
 # B: the Mirror Check: he steps aside, the mirror drops in, reflection = his back... becomes a FRIDGE; Mini-H on his shoulder
 dict(text="Now check the mirror. Wait... is that a fridge? That's your back.", poses=[], tr="cut",
      layers=[dict(at=0, w=0.46, x=0.27, y=0.62, asset="hero_double_biceps"),
              dict(at="Wait...", until="That's", w=0.15, x=0.37, y=0.36, asset="hero_shrug", enter=("pop", 0.3), exit=("fade", 0.15), z=3)],
      mirrors=[dict(at=0, x=0.72, y=0.47, w=0.5, h=0.5, show=[("hero_back_view", "mirror.", 0.92), ("prop_fridge", "fridge?", 0.8), ("hero_back_view", "back.", 0.92)])],
      scribbles=[dict(at="fridge?+0.3", until="back.", x=0.72, y=0.47, rx=0.25, ry=0.46, wd=12), dict(at="back.+0.3", kind="arrow", x=0.32, y=0.2, x1=0.55, y1=0.32, bend=-0.2)],
      labels=[dict(at="back.+0.3", text="YOUR BACK", style="sticky", x=0.25, y=0.14, rot=-5)],
      keys=[(0, 1.0, .5, .5), ("fridge?", 1.0, .5, .5), ("fridge?+0.1", 1.04, .55, .53), ("That's", 1.04, .55, .53), ("That's+0.1", 1.0, .5, .5)],
      sfx=[("mirror.", "swish", .4), ("Wait...", "pop", .4), ("fridge?+0.3", "marker", .5), ("back.+0.3", "marker", .5)]),
 # C: page turn -> THE LAZY FIX; three sticky notes slap on, number 3 gets circled
 dict(text="And the fix is lazy. Three moves. Number three takes thirty seconds.", poses=[], tr="page", d=0.45,
      bgwords=[dict(text="THE LAZY FIX", at=0, y=0.12, size=120, **HDR)],
      scribbles=[dict(at="lazy.", kind="underline", x=0.22, y=0.165, x1=0.78, y1=0.16), dict(at="thirty", x=0.73, y=0.62, rx=0.17, ry=0.07, wd=10)],
      layers=[dict(at=0, w=0.55, x=0.36, y=0.64, asset="hero_count_3", enter=("pop", 0.4))],
      labels=[dict(at="Three", text="1  ROWS", style="sticky", x=0.73, y=0.32, rot=4), dict(at="moves.", text="2  PULL-UPS", style="sticky", x=0.73, y=0.47, rot=-3),
              dict(at="Number", text="3  HANG", style="sticky", x=0.73, y=0.62, rot=5)],
      sfx=[(0, "pageflip", .5), ("lazy.", "marker", .5), ("Three", "slap", .5), ("moves.", "slap", .5), ("Number", "slap", .5), ("thirty", "marker", .5)],
      keys=[(0, 1.0, .5, .5), ("E", 1.03, .5, .55)]),
 # D: page 1 inverted rows; X-Ray lens shows the lats working
 dict(text="One. Inverted rows. Grab a table edge, keep your body straight, and pull your chest up.", poses=[], tr="page", d=0.45,
      bgwords=[dict(text="1. INVERTED ROWS", at=0, y=0.1, size=86, **HDR)],
      layers=[dict(at=0, w=0.66, x=0.5, y=0.62, poses=[("hero_row_start", 0), ("hero_row_end", "pull")], enter=("slide_r", 0.5))],
      labels=[dict(at="straight,", text="BODY STRAIGHT", style="sticky", x=0.31, y=0.24, rot=-4)],
      scribbles=[dict(at="pull", kind="curve", x=0.66, y=0.62, x1=0.6, y1=0.42, bend=0.3)],
      insets=[dict(at="chest", asset="hero_back_double_biceps", crop=(0.5, 0.4, 0.42), x=0.74, y=0.25, r=0.13, lens=True, **{"from": (1.1, 0.5)},
                   paint=(0.3, 0.6, 0.12, 0.2, "accent"), bg=(226, 236, 240))],
      sfx=[(0, "pageflip", .5), ("straight,", "slap", .5), ("pull", "marker", .5), ("chest", "swish", .4)],
      keys=[(0, 1.0, .5, .5), ("E", 1.04, .5, .55)]),
 # E: Mini-H doubts it; Effort-o-meter: effort LOW, result HIGH
 dict(text="That's it? That's it. Effort, low. Result, high.", poses=[], tr="cut",
      layers=[dict(at=0, w=0.5, x=0.5, y=0.72, asset="hero_row_end"), mini("That's", "hero_shrug", until="Effort,")],
      meters=[dict(at="Effort,", x=0.28, y=0.3, title="EFFORT", verdict="LOW", value=0.12, vcolor="good"),
              dict(at="Result,", x=0.72, y=0.3, title="RESULT", verdict="HIGH", value=0.92, vcolor="accent")],
      sfx=[("That's", "pop", .4), ("Effort,", "chime", .5), ("Result,", "level_start", .5)], keys=[(0, 1.0, .5, .5)]),
 # F: page 2 pull-ups; marker arrows pull the elbows down
 dict(text="Two. Pull-ups. Hands wide, and pull your elbows down to your ribs.", poses=[], tr="page", d=0.45,
      bgwords=[dict(text="2. PULL-UPS", at=0, y=0.1, size=110, **HDR)],
      layers=[dict(at=0, w=0.56, x=0.5, y=0.58, poses=[("hero_pullup_hang", 0), ("hero_pullup_top", "pull")], enter=("slide_r", 0.5))],
      labels=[dict(at="Hands", text="HANDS WIDE", style="sticky", x=0.29, y=0.24, rot=-5)],
      scribbles=[dict(at="elbows", kind="arrow", x=0.2, y=0.3, x1=0.24, y1=0.46), dict(at="elbows", kind="arrow", x=0.8, y=0.3, x1=0.76, y1=0.46)],
      sfx=[(0, "pageflip", .5), ("Hands", "slap", .5), ("elbows", "marker", .5)], keys=[(0, 1.0, .5, .5)]),
 # G: Mini-H "I can't do one" (everything behind blurs) -> jump up, lower slowly with a long marker arrow
 dict(text="I can't do one. Then jump to the top, and lower yourself slowly.", poses=[], tr="cut",
      layers=[dict(at=0, w=0.56, x=0.5, y=0.58, poses=[("hero_pullup_hang", 0), ("hero_pullup_top", "jump"), ("hero_pullup_hang", "lower")]),
              dict(at=0, until="Then", w=0.4, x=0.76, y=0.72, asset="hero_shrug", enter=("corner_r", 0.4), exit=("fade", 0.15), z=3, focus=True)],
      labels=[dict(at="lower", text="SLOWLY", style="sticky", x=0.76, y=0.24, rot=5)],
      scribbles=[dict(at="lower", kind="arrow", x=0.82, y=0.32, x1=0.82, y1=0.6, dur=1.2)],
      sfx=[(0, "pop", .4), ("jump", "swish", .4), ("lower", "marker", .5)], keys=[(0, 1.0, .5, .5)]),
 # H: page 3 dead hang; lats circled on both sides
 dict(text="Three. Dead hang. Just hang there for thirty seconds. It stretches your lats.", poses=[], tr="page", d=0.45,
      bgwords=[dict(text="3. DEAD HANG", at=0, y=0.1, size=110, **HDR)],
      layers=[dict(at=0, w=0.62, x=0.5, y=0.58, asset="hero_deadhang_front", enter=("slide_r", 0.5))],
      labels=[dict(at="thirty", text="30 SEC", style="sticky", x=0.76, y=0.27, rot=6)],
      scribbles=[dict(at="lats.", x=0.39, y=0.5, rx=0.05, ry=0.1, wd=10), dict(at="lats.", x=0.61, y=0.5, rx=0.05, ry=0.1, wd=10)],
      sfx=[(0, "pageflip", .5), ("thirty", "slap", .5), ("lats.", "marker", .5)], keys=[(0, 1.0, .5, .5)]),
 # I: Mini-H "hanging counts?" -> H thumbs up "Effortlessly." + meter flash
 dict(text="Hanging counts as exercise? Effortlessly.", poses=[], tr="cut",
      layers=[dict(at=0, w=0.58, x=0.36, y=0.62, asset="hero_thumbs_up", enter=("pop", 0.35)), mini(0, "hero_thinking", x=0.8, y=0.8, w=0.3, until="Effortlessly.")],
      meters=[dict(at="Effortlessly.", x=0.74, y=0.32, title="EFFORT", verdict="ZERO", value=0.02, vcolor="good")],
      sfx=[(0, "pop", .4), ("Effortlessly.", "chime", .5)], keys=[(0, 1.0, .5, .5)]),
 # J: payoff Mirror Check: fridge -> V-shaped back, marker draws the V
 dict(text="Do these three times a week, and the fridge turns into a V.", poses=[], tr="page", d=0.45,
      layers=[dict(at=0, w=0.44, x=0.27, y=0.64, asset="hero_thumbs_up")],
      mirrors=[dict(at=0, x=0.72, y=0.47, w=0.5, h=0.5, show=[("prop_fridge", 0, 0.8), ("hero_back_double_biceps", "V.", 0.9)])],
      labels=[dict(at="three", text="3x / WEEK", style="sticky", x=0.3, y=0.17, rot=-4)],
      scribbles=[dict(at="V.+0.3", kind="v", x=0.72, y=0.4, size=0.13)],
      sfx=[(0, "pageflip", .5), ("three", "slap", .5), ("V.", "level_start", .5), ("V.+0.3", "marker", .5)],
      keys=[(0, 1.0, .5, .5), ("V.", 1.0, .5, .5), ("V.+0.1", 1.1, .62, .53)]),
 # K: Mini-H asks the comment question, H points down at the comments
 dict(text="Which one are you skipping? Tell me below.", poses=[], tr="cut",
      layers=[dict(at=0, w=0.6, x=0.42, y=0.6, asset="hero_point_down", enter=("pop", 0.35)), mini(0, "hero_thinking", x=0.82, y=0.79, w=0.3)],
      scribbles=[dict(at="below.", kind="arrow", x=0.5, y=0.86, x1=0.5, y1=0.97)],
      sfx=[(0, "pop", .4), ("below.", "marker", .5)], keys=[(0, 1.0, .5, .5)]),
]
PLAN = dict(dir=f"{HERE}/scenes_d05v", words=f"{HERE}/voice/pilot1_cut.words.json", voice=f"{HERE}/voice/pilot1_cut.wav",
            music=f"{HERE}/music/hyper_lillian_thorn.mp3", music_db=11, sfx_db=16, duck=False, paper=True, theme="ice",
            scenes=S, cap_mode="build", cap_swipe=True, cap_words=3, cap_size=78, cap_y=0.85, lead=0.06, tail=0.8,
            keywords=["chest", "mirror", "fridge", "back", "lazy", "thirty", "rows", "straight", "low", "high", "wide", "elbows", "slowly", "lats", "effortlessly", "v", "skipping"])
if __name__ == "__main__":
    a = sys.argv[1:]
    render(PLAN, f"{HERE}/final/pilot1{'-preview' if a else ''}.mp4", **({"t0": float(a[0]), "t1": float(a[1])} if a else {}))
