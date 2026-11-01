# Builds MASTER-30-DAYS.xlsx + IMAGE-PROMPTS-DAY4-30.md from the approved topic plan (TOPICS-30-DAYS.md),
# the finished Day 1-3 files and the real hero library. Nothing is invented: missing scripts are marked MISSING,
# image needs for Days 4-30 come from each topic's listed moves / anatomy / gag, and every "EXISTS" is checked
# against ~/reel-engine-tool/public/library/hero.
import datetime as dt, os, re
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

W = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, W)
from scripts_d4_30 import S as SCR, P2, COMMON_SCENE
HAVE = {f.rsplit(".", 1)[0] for f in os.listdir(os.path.expanduser("~/reel-engine-tool/public/library/hero"))}
HAVE |= {f.rsplit(".", 1)[0] for f in os.listdir(f"{W}/character/new")}

# ---- topic plan (TOPICS-30-DAYS.md table, unchanged) ----
rows = [l for l in open(f"{W}/TOPICS-30-DAYS.md") if re.match(r"^\| \d+ \|", l)]
T = {}
for l in rows:
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    T[int(c[0])] = dict(title=c[1], hook=c[2], moves=[m.strip() for m in c[3].split(",") if m.strip() and m.strip() != "—"],
                        anat=c[4], gag=c[5])
KIND = {3: "Test / level", 10: "Test / level", 16: "Test / level", 20: "Test / level", 28: "Test / level",
        7: "30-day story", 14: "30-day story", 21: "30-day story", 30: "30-day story",
        2: "Problem fix (medical: soft wording)", 13: "Problem fix (medical: soft wording)", 17: "Problem fix (medical: soft wording)",
        29: "Problem fix (medical: soft wording)"}

# ---- Days 1-3: real finished files ----
DONE = {
    1: dict(script=open(f"{W}/forearms3.txt").read().strip(), video="final/forearms3.mp4", status="Rendered (upload not recorded in repo)"),
    2: dict(script=open(f"{W}/day2b.txt").read().strip(), video="final/day2b.mp4", status="Rendered (upload not recorded in repo)"),
    3: dict(script=open(f"{W}/day3d.txt").read().strip(), video="final/day3d.mp4", status="Uploaded (owner confirmed 1 Nov 2026)"),
}
SEO3 = dict(title="Can You Hold a Dead Hang for 60 Seconds? 😳 #shorts",
            desc=("Most people drop off the bar before 30 seconds. Under 20 sec = weak grip, 30 = average, 60 = strong, 90+ = beast mode. "
                  "It's not your arms, it's your grip. The fix: dead hangs, as long as you can, 3 times, and add 5 seconds every day. "
                  "Comment your time, and be honest 👇"),
            tags="#deadhang #gripstrength #forearms #homeworkout #fitness #shorts",
            keys="dead hang, dead hang 60 seconds, dead hang challenge, dead hang test, grip strength, grip strength test, forearm workout, "
                 "how to dead hang, pull up bar workout, stronger grip, fitness test, home workout, effortless exercise, shorts")
CANDIDATE = {6: "armsmall.txt / noodlearms2.txt (older video scripts on the same idea: triceps make the arm big)",
             11: "pushup3.txt (older video: 'You are making these three mistakes')",
             7: "deadhang30.txt shows the '30 days' story format (different exercise)"}

# ---- move -> existing frames (same camera view) or NEW ids ----
MOVE = {
    "dead_hang": ["hero_hang_perfect"], "farmer_walk": ["hero_dumbbell_hold", "hero_pick_dumbbell"],
    "dead_bug": ["NEW:hero_dead_bug_a", "NEW:hero_dead_bug_b"], "glute_bridge": ["hero_glute_bridge_down", "hero_glute_bridge_up"],
    "hip_flexor_stretch": ["hero_hip_flexor_stretch"], "neck_stretch": ["hero_neck_stretch"],
    "doorway_chest_stretch": ["NEW:hero_doorway_chest_stretch"],
    "band_pull_apart": ["NEW:hero_band_pull_apart_start", "NEW:hero_band_pull_apart_end"],
    "wrong_squat_knees_in": ["hero_squat_wrong"], "fire_hydrant": ["NEW:hero_fire_hydrant_down", "NEW:hero_fire_hydrant_up"],
    "side_lying_leg_raise": ["NEW:hero_side_leg_raise_down", "NEW:hero_side_leg_raise_up"],
    "bench_dip": ["hero_dip_top", "hero_dip_bottom"], "diamond_pushup": ["NEW:hero_diamond_pushup_top", "NEW:hero_diamond_pushup_bottom"],
    "tricep_extension": ["NEW:hero_tricep_ext_start", "NEW:hero_tricep_ext_end"],
    "pushup": ["hero_pushup_top_v3", "hero_pushup_mid", "NEW:hero_pushup_bottom"],
    "wide_pushup": ["NEW:hero_wide_pushup_top", "NEW:hero_wide_pushup_bottom"],
    "scapula_pullup": ["hero_pullup_hang", "NEW:hero_scap_pullup_top"], "negative_pullup": ["hero_pullup_top", "hero_pullup_hang"],
    "russian_twist": ["NEW:hero_russian_twist_left", "NEW:hero_russian_twist_right"], "side_plank": ["NEW:hero_side_plank"],
    "bicycle_crunch": ["NEW:hero_bicycle_crunch_left", "NEW:hero_bicycle_crunch_right"],
    "wrong_pushup_sagging": ["NEW:hero_pushup_hips_sag"], "knee_pushup": ["NEW:hero_knee_pushup_top", "NEW:hero_knee_pushup_bottom"],
    "hamstring_stretch": ["hero_stretch_hamstring", "hero_stretch_hamstring_v2"], "worlds_greatest_stretch": ["NEW:hero_worlds_greatest_stretch"],
    "deep_squat_hold": ["hero_deep_squat_hold"], "pigeon_stretch": ["NEW:hero_pigeon_stretch"], "spinal_twist": ["NEW:hero_spinal_twist"],
    "plank": ["hero_plank"], "plank_shoulder_tap": ["NEW:hero_plank_shoulder_tap"],
    "pike_pushup": ["hero_pike_top", "hero_pike_bottom"], "overhead_press": ["NEW:hero_overhead_press_start", "NEW:hero_overhead_press_end"],
    "lateral_raise": ["NEW:hero_lateral_raise_down", "NEW:hero_lateral_raise_up"], "archer_pushup": ["NEW:hero_archer_pushup"],
    "bird_dog": ["NEW:hero_bird_dog_a", "NEW:hero_bird_dog_b"], "hollow_hold": ["NEW:hero_hollow_hold"],
    "incline_pushup": ["NEW:hero_incline_pushup"], "decline_pushup": ["NEW:hero_decline_pushup"],
    "squat": ["hero_squat_top", "hero_squat_mid"], "lunge": ["hero_lunge", "hero_lunge_v2"],
    "calf_raise": ["NEW:hero_calf_raise_down", "NEW:hero_calf_raise_up"], "wall_sit": ["NEW:hero_wall_sit"],
    "jump_squat": ["hero_squat_mid", "NEW:hero_jump_squat_air"], "sumo_squat": ["hero_sumo_squat"],
    "leg_raise": ["hero_leg_raise_down", "hero_leg_raise_up"], "reverse_crunch": ["hero_reverse_crunch", "hero_reverse_crunch_v2"],
    "flutter_kicks": ["NEW:hero_flutter_kicks_a", "NEW:hero_flutter_kicks_b"],
    "cat_cow": ["NEW:hero_cat_pose", "NEW:hero_cow_pose"], "childs_pose": ["hero_childs_pose"], "cobra_stretch": ["hero_cobra_stretch"],
    "wrist_stretch": ["NEW:hero_wrist_stretch"], "knuckle-style pushup": ["NEW:hero_knuckle_pushup"],
    "jump_rope": ["NEW:hero_jump_rope"], "skater_jump": ["NEW:hero_skater_left", "NEW:hero_skater_right"],
    "burpee": ["hero_burpee_jump", "hero_burpee_jump_v2"], "mountain_climbers": ["hero_mountain_a", "hero_mountain_b"],
    "high_knees": ["hero_high_knees"], "jumping_jacks": ["NEW:hero_jack_closed", "NEW:hero_jack_open"],
    "wrong_posture_desk": ["hero_bad_posture_desk"], "pistol_squat": ["NEW:hero_pistol_squat"],
}
# story images per day (hook / problem / test), only where the topic needs something the library lacks
STORY = {
    4: [("Hook", "NEW:hero_text_neck_phone", "H looks down at his phone, head far forward (the 27 kg head)")],
    12: [("Hook", "NEW:hero_toe_touch_fail", "H bends forward and cannot reach his toes")],
    23: [("Hook", "NEW:hero_stiff_morning_bed", "H wakes up stiff on the edge of his bed")],
    28: [("Test", "NEW:hero_sit_cross_legged", "start of the sit-to-stand test"), ("Test", "NEW:hero_stand_no_hands", "standing up without hands")],
    29: [("Hook", "NEW:hero_butt_pain_sit", "H sits on a chair and winces, pain in his buttock")],
    11: [("Mistake", "NEW:hero_pushup_hips_pike", "2nd mistake option: hips piked up")],
}
BG = {4: "bg_office_desk", 13: "bg_office_desk", 27: "bg_office_desk", 23: "bg_bedroom_morning", 26: "bg_gym_interior",
      7: "bg_gym_interior", 14: "bg_home_living_room", 21: "bg_gym_interior", 30: "bg_gym_interior", 19: "bg_gym_interior",
      25: "bg_park_morning", 10: "bg_home_living_room", 16: "bg_home_living_room"}
CTA = ["hero_teacher_pointer", "hero_point_viewer", "hero_clipboard", "hero_writing_notes", "hero_phone_scroll", "hero_lean_in_talk",
       "hero_crouch_talk", "hero_explain", "hero_present_right", "hero_whisper"]
RESULT = ["hero_double_biceps", "hero_victory", "hero_trophy", "hero_side_chest", "hero_medal", "hero_celebrate_jump", "hero_superhero"]

# ---- NEW image prompts ----
COMMON = ("Use the attached reference image: the SAME character H, exactly as in the reference: bald, very muscular, warm tan skin, "
          "white letter \"H\" on his forehead, black shorts, olive harness straps, olive utility belt with pouches and a silver buckle, "
          "black wrist wraps, olive combat sneakers. Same semi-realistic comic style, same face, same proportions. Vertical 9:16 image "
          "(768x1376). Pure plain white background (#FFFFFF), no floor texture, no text, no logos. Whole body (and any equipment) fully "
          "inside the frame with space around it. Correct anatomy: two arms, two legs, five fingers per hand. Correct, safe exercise form "
          "unless the prompt says WRONG form.")
COMMON_BG = ("Vertical 9:16 background image (1080x1920), NO people, NO text, NO logos. Semi-realistic comic illustration style with bold "
             "outlines that matches a muscular cartoon fitness character. Soft depth of field, calm colours, the lower middle third kept "
             "clear and uncluttered so a character can be placed there. Natural perspective at standing eye level.")
P = {**P2, **{
 "hero_pushup_bottom": "Push-up BOTTOM position, SIDE view, head to the right: chest about 3 cm above the floor, elbows about 45 degrees from the body, body straight from head to heels.",
 "hero_pushup_hips_sag": "Push-up top position, SIDE view, head to the right, WRONG form: arms straight but hips sag toward the floor, lower back arched, strained face.",
 "hero_pushup_hips_pike": "Push-up top position, SIDE view, head to the right, WRONG form: arms straight but hips pushed high (pike), body like an upside-down V.",
 "hero_knee_pushup_top": "Knee push-up TOP position, SIDE view, head to the right: knees on the floor, arms straight, hands under the shoulders, straight line from knees to head.",
 "hero_knee_pushup_bottom": "Knee push-up BOTTOM position, SIDE view, head to the right: knees on the floor, chest close to the floor, elbows about 45 degrees.",
 "hero_wide_pushup_top": "Wide push-up TOP position, FRONT view (head toward the camera, camera at floor level): hands about 1.5x shoulder width, arms straight, body straight.",
 "hero_wide_pushup_bottom": "Wide push-up BOTTOM position, FRONT view (head toward the camera, camera at floor level): hands 1.5x shoulder width, chest close to the floor, elbows bent out to the sides.",
 "hero_diamond_pushup_top": "Diamond push-up TOP position, FRONT view (head toward the camera, camera at floor level): hands together under the chest, thumbs and index fingers forming a diamond, arms straight.",
 "hero_diamond_pushup_bottom": "Diamond push-up BOTTOM position, same front view: hands in a diamond under the chest, chest close to the hands, elbows bent back along the body.",
 "hero_archer_pushup": "Archer push-up, FRONT view (camera at floor level): hands very wide, body lowered toward the right hand with the right elbow bent, left arm straight out to the side.",
 "hero_incline_pushup": "Incline push-up, SIDE view, head to the right: hands on a flat gym bench, feet on the floor, body straight, chest lowered toward the bench edge.",
 "hero_decline_pushup": "Decline push-up, SIDE view, head to the right: feet up on a flat gym bench, hands on the floor, body straight, chest lowered toward the floor.",
 "hero_knuckle_pushup": "Knuckle push-up TOP position, SIDE view, head to the right: weight on closed fists (knuckles) instead of flat hands, wrists straight, arms straight.",
 "hero_tricep_ext_start": "Overhead triceps extension START, SIDE view facing right, standing: both hands hold one dumbbell behind the head, elbows bent and pointing up.",
 "hero_tricep_ext_end": "Overhead triceps extension END, same side view: dumbbell pressed straight up overhead, arms straight, elbows close to the head.",
 "hero_overhead_press_start": "Dumbbell overhead press START, FRONT view, standing: dumbbells at shoulder height, palms forward, elbows under the wrists.",
 "hero_overhead_press_end": "Dumbbell overhead press END, FRONT view: dumbbells pressed straight overhead, arms straight, core tight.",
 "hero_lateral_raise_down": "Dumbbell lateral raise START, FRONT view, standing: light dumbbells at the sides, slight bend in the elbows.",
 "hero_lateral_raise_up": "Dumbbell lateral raise TOP, FRONT view: arms raised out to the sides to shoulder height, slight bend in the elbows, like a T.",
 "hero_band_pull_apart_start": "Resistance band pull-apart START, FRONT view, standing: both hands hold a red resistance band straight in front at chest height, arms straight.",
 "hero_band_pull_apart_end": "Resistance band pull-apart END, FRONT view: band stretched across the chest, arms pulled wide out to the sides, shoulder blades squeezed.",
 "hero_doorway_chest_stretch": "Doorway chest stretch, SIDE view facing right: H stands in a plain wooden door frame, forearms on both sides of the frame at shoulder height, one foot stepped forward, chest opening. Draw the door frame.",
 "hero_scap_pullup_top": "Scapula pull-up, SIDE view: hanging from a pull-up bar with straight arms, shoulders pulled DOWN away from the ears so the body rises a few cm. Bar near the top of the image.",
 "hero_russian_twist_left": "Russian twist, FRONT view: sitting on the floor leaning back, feet lifted, hands together holding a small dumbbell, torso twisted to his LEFT, dumbbell beside the left hip.",
 "hero_russian_twist_right": "Same Russian twist, torso twisted to his RIGHT, dumbbell beside the right hip.",
 "hero_side_plank": "Side plank, FRONT view: on the right forearm and the side of the right foot, body in one straight line from head to feet, left hand on the hip.",
 "hero_bicycle_crunch_left": "Bicycle crunch, 3/4 front view: lying on the back, hands behind the head, right elbow touching the left knee, right leg extended.",
 "hero_bicycle_crunch_right": "Bicycle crunch, same view: left elbow touching the right knee, left leg extended.",
 "hero_worlds_greatest_stretch": "World's greatest stretch, SIDE view: deep lunge, back knee down, one hand on the floor inside the front foot, other arm reaching straight up to the ceiling, chest rotated open.",
 "hero_pigeon_stretch": "Pigeon stretch, 3/4 front view on the floor: front leg bent across the body, back leg straight behind, hands on the floor, chest tall.",
 "hero_spinal_twist": "Lying spinal twist, top-down 3/4 view: lying on the back, arms out like a T, both knees bent and dropped to the right side, head turned left.",
 "hero_plank_shoulder_tap": "Plank shoulder tap, FRONT view (head toward camera, camera low): straight-arm plank on the left hand, right hand touching the left shoulder, hips level.",
 "hero_dead_bug_a": "Dead bug, SIDE view: lying on the back, LEFT arm straight overhead and RIGHT leg straight out low above the floor, other arm up and other knee bent at 90 degrees, lower back flat.",
 "hero_dead_bug_b": "Dead bug, same view: RIGHT arm straight overhead and LEFT leg straight out low, other arm up and other knee bent at 90 degrees.",
 "hero_bird_dog_a": "Bird dog, SIDE view: on hands and knees, RIGHT arm reaching straight forward and LEFT leg straight back, both level with the back, back flat.",
 "hero_bird_dog_b": "Bird dog, same view: LEFT arm forward and RIGHT leg back.",
 "hero_hollow_hold": "Hollow body hold, SIDE view: lying on the back, arms straight overhead, legs straight and lifted a few cm, shoulders off the floor, body in a shallow banana shape.",
 "hero_calf_raise_down": "Calf raise START, SIDE view facing right: standing tall, heels on the floor.",
 "hero_calf_raise_up": "Calf raise TOP, SIDE view facing right: standing high on the balls of the feet, heels lifted high, calves flexed.",
 "hero_wall_sit": "Wall sit, SIDE view facing right: back flat against a plain wall (draw the wall edge), thighs parallel to the floor, knees at 90 degrees, arms crossed, sweating.",
 "hero_jump_squat_air": "Jump squat in the AIR, FRONT view: body fully off the ground, legs straight, arms swung down, small shadow on the floor below.",
 "hero_flutter_kicks_a": "Flutter kicks, SIDE view: lying on the back, hands under the hips, legs straight, right leg higher than the left, both off the floor.",
 "hero_flutter_kicks_b": "Flutter kicks, same view: left leg higher than the right.",
 "hero_cat_pose": "Cat pose, SIDE view: on hands and knees, back rounded up toward the ceiling, head down.",
 "hero_cow_pose": "Cow pose, SIDE view: on hands and knees, belly dropped, chest forward, looking slightly up.",
 "hero_wrist_stretch": "Wrist stretch, FRONT view, kneeling: palms flat on the floor with fingers pointing back toward the knees, arms straight, leaning back gently.",
 "hero_jump_rope": "Jumping rope, FRONT view: mid-jump on the balls of the feet, rope passing under the feet, elbows close to the body.",
 "hero_skater_left": "Skater jump, FRONT view: landing on the LEFT leg, right leg swept behind, body leaning left, arms swinging.",
 "hero_skater_right": "Skater jump, same view: landing on the RIGHT leg, left leg swept behind.",
 "hero_jack_closed": "Jumping jack START, FRONT view: feet together, arms at the sides.",
 "hero_jack_open": "Jumping jack OPEN, FRONT view: feet wide, arms straight overhead.",
 "hero_pistol_squat": "Pistol squat BOTTOM, SIDE view facing right: squatting on the left leg, right leg straight out in front off the floor, arms forward for balance.",
 "hero_fire_hydrant_down": "Fire hydrant START, 3/4 back view: on hands and knees, back flat.",
 "hero_fire_hydrant_up": "Fire hydrant TOP, same view: right knee lifted out to the side to hip height, knee bent 90 degrees, back flat.",
 "hero_side_leg_raise_down": "Side-lying leg raise START, FRONT view: lying on the left side, head on the left arm, legs straight and stacked.",
 "hero_side_leg_raise_up": "Side-lying leg raise TOP, same view: top (right) leg raised straight up to about 45 degrees, toes forward.",
 "hero_text_neck_phone": "Standing, SIDE view facing right: looking down at a phone held at belly height, head pushed far forward, neck bent, shoulders rounded, unhappy face.",
 "hero_toe_touch_fail": "Standing forward bend, SIDE view facing right: legs straight, reaching down, fingertips stuck at mid-shin far from the toes, strained face.",
 "hero_stiff_morning_bed": "Sitting on the edge of a simple bed, FRONT view, just woke up: one hand on the lower back, wincing, stiff, messy blanket. Draw the bed.",
 "hero_sit_cross_legged": "Sitting cross-legged on the floor, FRONT view, hands on the knees, ready to stand up, determined face.",
 "hero_stand_no_hands": "Halfway standing up from cross-legged on the floor WITHOUT using the hands, FRONT view: arms stretched forward for balance, knees bending up.",
 "hero_butt_pain_sit": "Sitting on a plain office chair, SIDE view facing right: one hand on his buttock/hip, wincing, leaning to one side.",
 "bg_office_desk": "Simple home office: desk with laptop and lamp on the left, chair, window light, plain wall.",
 "bg_bedroom_morning": "Bedroom at sunrise: bed with blanket on the left, window with warm morning light, plain wall.",
 "bg_gym_interior": "Clean modern gym: dumbbell rack and a pull-up station in the background, rubber floor, warm lights.",
 "bg_home_living_room": "Bright living room: sofa on one side, yoga mat on the floor, plant, plain wall.",
 "bg_park_morning": "Park at morning: grass, trees in the distance, a path, soft sunlight.",
}}

# ---- build per-day scene plan ----
req = []  # (day, scene, beat, image id, type, status, usage)
def add(day, scene, beat, img, typ, usage):
    new = img.startswith("NEW:"); iid = img[4:] if new else img
    st = "NEW (generate)" if new and iid not in HAVE else ("EXISTS" if iid in HAVE else "MISSING (check)")
    if new and iid in HAVE: st = "EXISTS"
    if typ == "video": st = "DONE" if os.path.exists(f"{W}/{iid}") else "VIDEO FILE MISSING"
    req.append((day, scene, beat, iid, typ, st, usage))

SCENE_IDS = set()
for d in range(1, 31):
    if d <= 3:
        add(d, 0, "Finished video", DONE[d]["video"], "video", "Done: " + DONE[d]["status"]); continue
    for n, (narr, head, img) in enumerate(SCR[d], 1):
        kind = "full scene (H + background)" if img.startswith("scene:") else ("anatomy bubble" if img.startswith("anat_") else
               "gag" if img.startswith("gag_") else "character")
        if img.startswith("scene:"): SCENE_IDS.add(img[6:]); img = "NEW:" + img[6:]
        elif img.startswith("new:"): img = "NEW:" + img[4:]
        add(d, n, head or "(2nd frame of the move above)", img, kind, (f'Says: "{narr}"' if narr else "Loop with the frame above (same view)")
            + (" | clean_cutout.py first" if img.startswith("gag_") else ""))

new_ids = sorted({r[3] for r in req if r[5].startswith("NEW")})
uses = {i: sorted({r[0] for r in req if r[3] == i}) for i in new_ids}
essential = list(new_ids)
optional = []
order = sorted(essential, key=lambda i: (min(uses[i]), i)) + optional

# ---- workbook ----
wb = Workbook(); H = Font(bold=True, color="FFFFFF"); FILL = PatternFill("solid", fgColor="16191D")
def sheet(name, head, data, widths):
    ws = wb.create_sheet(name); ws.append(head)
    for c in ws[1]: c.font = H; c.fill = FILL
    for r in data: ws.append(list(r))
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
wb.remove(wb.active)
start = dt.date(2026, 11, 2)
sheet("1 Content Calendar", ["Day", "Topic", "Format", "Status", "Publish order", "Planned upload date"],
      [(d, T[d]["title"], KIND.get(d, "Problem fix"), DONE[d]["status"] if d in DONE else "Script drafted, awaiting approval", d,
        "not recorded" if d in DONE else str(start + dt.timedelta(days=d - 4))) for d in range(1, 31)], [6, 45, 26, 34, 12, 18])
sheet("2 Titles & Topics", ["Day", "Topic (approved plan)", "Main YouTube title", "Alternative titles", "Hook line (plan)"],
      [(d, T[d]["title"], SEO3["title"] if d == 3 else (T[d]["title"] + " #shorts" if d > 3 else T[d]["title"] + " (final title not stored in repo)"),
        "TO WRITE (needs approval)", T[d]["hook"]) for d in range(1, 31)], [6, 40, 46, 30, 50])
sheet("3 Scripts", ["Day", "Status", "Hook", "Full script (narration + CTA)", "Scene breakdown", "Related older script (not approved)"],
      [(d, "FINAL" if d in DONE else "DRAFT: needs owner approval", SCR[d][0][0] if d > 3 else T[d]["hook"],
        DONE[d]["script"] if d in DONE else " ".join(x[0] for x in SCR[d] if x[0]),
        "See build_day3d.py" if d == 3 else ("See " + ("build_forearms3.py" if d == 1 else "build_day2b.py") if d in DONE else
         "\n".join(f"S{n}: {h} | {x}" for n, (x, h, _) in enumerate(SCR[d], 1) if x)),
        CANDIDATE.get(d, "")) for d in range(1, 31)], [6, 22, 40, 70, 30, 40])
sheet("4 SEO & Publishing", ["Day", "Description", "Hashtags", "SEO tags / keywords", "Pinned comment"],
      [(d, SEO3["desc"] if d == 3 else ("Given in chat, not stored in repo" if d < 3 else "TO WRITE after the script"),
        SEO3["tags"] if d == 3 else "", SEO3["keys"] if d == 3 else "",
        "What's your time? Be honest 👇" if d == 3 else "") for d in range(1, 31)], [6, 70, 34, 60, 30])
sheet("5 Image Requirements", ["Day", "Scene", "Heading on screen (from the draft script)", "Image id", "Type", "Status", "Usage"],
      req, [6, 7, 30, 30, 18, 16, 50])
sheet("6 Generation Prompts", ["#", "Image id (file name .png)", "Type", "Used on days", "Copy-paste prompt (attach H-standing-front-white.png)"],
      [(n, i, "full scene" if i in SCENE_IDS else "white-bg cutout", ", ".join(map(str, uses[i])),
        (COMMON_SCENE if i in SCENE_IDS else COMMON) + " " + P.get(i, "PROMPT MISSING")) for n, i in enumerate(order, 1)], [5, 30, 12, 14, 110])
sheet("7 Production Tracker", ["Day", "Script", "Images", "Voiceover", "Video edit", "Thumbnail", "Published"],
      [(d, "Done", "Done", "Done", "Done", "Done" if os.path.exists(f"{W}/thumbnails/day2-lower-belly.jpg") and d == 2 or d == 1 else "Not recorded",
        "Yes" if d == 3 else "Not recorded") if d in DONE else
       (d, "Draft", ("Ready" if all(r[5] == "EXISTS" for r in req if r[0] == d and not r[4].startswith("background")) else
                       f"{sum(1 for r in req if r[0] == d and r[5].startswith('NEW') and not r[3].startswith('bg_'))} new needed"),
        "Not started", "Not started", "Not started", "Not started") for d in range(1, 31)], [6, 10, 18, 12, 12, 12, 12])
wb.save(f"{W}/MASTER-30-DAYS.xlsx")

with open(f"{W}/IMAGE-PROMPTS-DAY4-30.md", "w") as f:
    f.write("# New images for Days 4-30 (production order)\n\nAttach `work/character/H-standing-front-white.png` to every character prompt. "
            "Save each image with the file name shown (PNG). Background prompts (bg_*) need no reference image.\n\n")
    for n, i in enumerate(order, 1):
        f.write(f"## {n}. {i}.png ({'full scene' if i in SCENE_IDS else 'white-bg cutout'}; days {', '.join(map(str, uses[i]))})\n```\n"
                f"{(COMMON_SCENE if i in SCENE_IDS else COMMON)} {P.get(i, 'PROMPT MISSING')}\n```\n\n")
print("topics remaining:", 27, "| new images:", len(new_ids), "essential:", len(essential), "optional:", len(optional))
print("days ready now (no new essential image):", [d for d in range(4, 31) if not any(r[0] == d and r[5].startswith("NEW") and not r[3].startswith("bg_") for r in req)])
print("missing prompts:", [i for i in new_ids if i not in P])
print("reused by >1 day:", {i: uses[i] for i in new_ids if len(uses[i]) > 1})
