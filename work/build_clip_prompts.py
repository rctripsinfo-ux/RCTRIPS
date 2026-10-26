# Exercise video clips for the Reel Engine clip library (owner, 26 Oct): H doing every common move, made in Flow
# with H's reference image so he looks the same in all of them. Same look as the existing clips: portrait, pure white
# background (the tool's multiply blend makes white disappear into any video background), static camera, one smooth loop.
# The 17 clips we already have are left out.
STYLE = ("Use the attached reference image: the SAME character H, exactly as in the reference: bald, very muscular, tan "
         "skin, white letter H on his forehead, black shorts with a dark olive military belt, black wristbands, black "
         "shoes. Same semi-realistic 3D cartoon style. Vertical 9:16 video. Pure plain white background (#FFFFFF), "
         "white floor, no room, no gym, no props except the ones named. Static camera, no zoom, no pan, no cuts. "
         "{view}. His whole body (and any equipment) stays fully inside the frame with space around it the whole time. "
         "He does the movement with perfect, slow, controlled form at a steady pace, {reps}, and ends in exactly the same "
         "position he started in so the clip loops seamlessly. Calm focused face. No text, no captions, no logo, "
         "no music, no other people. 8 seconds.")
SIDE = "Camera sees him from the side (profile), at his body's height"
FRONT = "Camera sees him straight from the front, at chest height"
ANGLE = "Camera sees him from a three-quarter front angle, at his body's height"
BACK = "Camera sees him from behind, at his body's height"
R2, R3, HOLD = "2 full repetitions", "3 full repetitions", "holding the position still and breathing calmly (only small breathing movement)"

G = [
 ("PUSH (chest, shoulders, triceps)", [
  ("clip_wide_pushup", "Wide push-ups on the floor, hands wider than the shoulders", SIDE, R3),
  ("clip_knee_pushup", "Knee push-ups (beginner push-ups) on the floor, knees down, body straight from knees to head", SIDE, R3),
  ("clip_incline_pushup", "Incline push-ups with hands on a plain white box", SIDE, R3),
  ("clip_archer_pushup", "Archer push-ups, shifting to one arm while the other arm stays straight out to the side", FRONT, R2),
  ("clip_pseudo_planche_pushup", "Pseudo planche push-ups, hands by the hips, leaning forward", SIDE, R2),
  ("clip_bench_dip", "Bench dips with hands on a plain white box behind him, legs straight", SIDE, R3),
  ("clip_parallel_bar_dip", "Dips on simple black parallel bars", SIDE, R2),
  ("clip_overhead_press", "Standing dumbbell overhead press with two black dumbbells", FRONT, R3),
  ("clip_dumbbell_bench_press", "Dumbbell chest press lying on a plain white flat bench", SIDE, R3),
  ("clip_front_raise", "Dumbbell front raises with two black dumbbells", SIDE, R3),
  ("clip_tricep_extension", "Overhead triceps extension holding one black dumbbell with both hands", SIDE, R3),
  ("clip_handstand_hold", "Wall handstand hold, chest facing a plain white wall", SIDE, HOLD),
 ]),
 ("PULL (back, biceps, grip)", [
  ("clip_pullup", "Pull-ups on a simple black pull-up bar, chin over the bar", FRONT, R2),
  ("clip_chinup", "Chin-ups on a simple black pull-up bar, palms facing him", FRONT, R2),
  ("clip_scapula_pullup", "Scapular pull-ups: hanging from a black bar and only squeezing the shoulder blades down, arms straight", BACK, R3),
  ("clip_negative_pullup", "Slow negative pull-ups: starting with chin over the bar and lowering very slowly", FRONT, "2 slow repetitions"),
  ("clip_dumbbell_row", "One-arm dumbbell row with one knee and hand on a plain white bench", SIDE, R3),
  ("clip_bent_over_row", "Bent-over row with a black barbell", SIDE, R3),
  ("clip_superman", "Superman back raises lying face down on the floor", SIDE, R3),
  ("clip_biceps_curl", "Standing dumbbell biceps curls with two black dumbbells", FRONT, R3),
  ("clip_farmer_walk", "Farmer's hold: standing tall holding two heavy black dumbbells at his sides, walking in place", FRONT, "walking in place for 6 steps"),
  ("clip_band_pull_apart", "Band pull-aparts with a red resistance band at chest height", FRONT, R3),
 ]),
 ("LEGS AND GLUTES", [
  ("clip_lunge", "Forward lunges, alternating legs", SIDE, "2 repetitions on each leg"),
  ("clip_reverse_lunge", "Reverse lunges, alternating legs", SIDE, "2 repetitions on each leg"),
  ("clip_jump_squat", "Jump squats, landing softly", SIDE, R3),
  ("clip_sumo_squat", "Sumo squats with a wide stance and toes out", FRONT, R3),
  ("clip_wall_sit", "Wall sit with the back against a plain white wall, thighs parallel to the floor", SIDE, HOLD),
  ("clip_step_up", "Step-ups onto a plain white box, alternating legs", SIDE, "2 repetitions on each leg"),
  ("clip_romanian_deadlift", "Romanian deadlift with two black dumbbells, hinging at the hips with a flat back", SIDE, R3),
  ("clip_deadlift", "Conventional deadlift with a black barbell from the floor", SIDE, R2),
  ("clip_hip_thrust", "Hip thrusts with the upper back on a plain white bench, knees bent", SIDE, R3),
  ("clip_single_leg_glute_bridge", "Single-leg glute bridge lying on the floor, one leg straight up", SIDE, R3),
  ("clip_donkey_kick", "Donkey kicks on hands and knees, one leg kicking up behind", SIDE, "3 repetitions with one leg"),
  ("clip_fire_hydrant", "Fire hydrants on hands and knees, lifting one bent knee out to the side", BACK, "3 repetitions with one leg"),
  ("clip_side_lying_leg_raise", "Side-lying leg raises lying on his side on the floor", FRONT, R3),
  ("clip_calf_raise", "Standing calf raises on the floor", SIDE, R3),
  ("clip_pistol_squat", "Pistol squat on one leg, the other leg straight out in front", SIDE, R2),
 ]),
 ("CORE", [
  ("clip_crunch", "Crunches lying on the floor, knees bent", SIDE, R3),
  ("clip_bicycle_crunch", "Bicycle crunches lying on the floor", ANGLE, "4 repetitions (2 each side)"),
  ("clip_russian_twist", "Russian twists sitting on the floor, feet off the ground", FRONT, "4 repetitions (2 each side)"),
  ("clip_dead_bug", "Dead bug lying on his back, opposite arm and leg lowering", SIDE, "4 repetitions (2 each side)"),
  ("clip_bird_dog", "Bird dog on hands and knees, opposite arm and leg reaching out", SIDE, "4 repetitions (2 each side)"),
  ("clip_hollow_hold", "Hollow body hold lying on his back, arms and legs lifted", SIDE, HOLD),
  ("clip_flutter_kicks", "Flutter kicks lying on his back, legs straight and low", SIDE, "6 small kicks"),
  ("clip_reverse_crunch", "Reverse crunches lying on his back, knees pulled to the chest", SIDE, R3),
  ("clip_hanging_knee_raise", "Hanging knee raises from a simple black pull-up bar", SIDE, R3),
  ("clip_plank_shoulder_tap", "Plank shoulder taps, hips staying still", FRONT, "4 taps"),
  ("clip_v_up", "V-ups lying on his back, hands and feet meeting in the middle", SIDE, R2),
  ("clip_heel_touch", "Heel touches lying on his back, knees bent, reaching side to side", FRONT, "4 repetitions (2 each side)"),
 ]),
 ("CARDIO / FULL BODY", [
  ("clip_burpee", "Burpees: squat, jump the feet back, push-up, jump the feet in, jump up", SIDE, R2),
  ("clip_jumping_jacks", "Jumping jacks", FRONT, "4 repetitions"),
  ("clip_high_knees", "High knees running in place", SIDE, "8 steps"),
  ("clip_butt_kicks", "Butt kicks running in place", SIDE, "8 steps"),
  ("clip_skater_jump", "Skater jumps side to side", FRONT, "4 jumps"),
  ("clip_bear_crawl", "Bear crawl in place, knees just above the floor, moving forward 2 steps and back 2 steps", SIDE, "2 rounds"),
  ("clip_jump_rope", "Jumping rope with a black jump rope", FRONT, "8 jumps"),
  ("clip_shadow_boxing", "Shadow boxing: jab, cross, hook in a boxing stance", ANGLE, "2 combinations"),
  ("clip_kettlebell_swing", "Kettlebell swings with one black kettlebell, hinging at the hips", SIDE, R3),
 ]),
 ("STRETCHES AND MOBILITY", [
  ("clip_hip_flexor_stretch", "Kneeling hip flexor stretch, one knee down, pushing the hips forward gently", SIDE, HOLD),
  ("clip_hamstring_stretch", "Standing hamstring stretch, one heel forward, hinging over the straight leg", SIDE, HOLD),
  ("clip_quad_stretch", "Standing quad stretch, holding one foot behind him", SIDE, HOLD),
  ("clip_pigeon_stretch", "Pigeon stretch on the floor, front leg bent across", ANGLE, HOLD),
  ("clip_childs_pose", "Child's pose on the floor, arms stretched forward", SIDE, HOLD),
  ("clip_cobra_stretch", "Cobra stretch lying face down, pushing the chest up", SIDE, HOLD),
  ("clip_cat_cow", "Cat-cow on hands and knees, rounding and arching the back", SIDE, "2 slow repetitions"),
  ("clip_worlds_greatest_stretch", "World's greatest stretch: deep lunge, elbow to the instep, then rotating the arm up", ANGLE, "1 slow repetition"),
  ("clip_doorway_chest_stretch", "Chest stretch with forearm on a plain white door frame, leaning forward", SIDE, HOLD),
  ("clip_neck_stretch", "Seated neck stretch, ear toward the shoulder, hand gently helping", FRONT, HOLD),
  ("clip_shoulder_cross_stretch", "Cross-body shoulder stretch, one arm pulled across the chest", FRONT, HOLD),
  ("clip_arm_circles", "Arm circles, arms straight out to the sides", FRONT, "6 circles"),
  ("clip_deep_squat_hold", "Deep squat hold, heels down, elbows pushing the knees out", FRONT, HOLD),
  ("clip_butterfly_stretch", "Seated butterfly stretch, soles of the feet together", FRONT, HOLD),
  ("clip_spinal_twist", "Lying spinal twist, knees dropping to one side, arms out", ANGLE, HOLD),
  ("clip_wrist_stretch", "Kneeling wrist stretch, palms on the floor with fingers pointing back toward the knees", SIDE, HOLD),
 ]),
 ("WRONG FORM (for 'mistakes' videos: same move done badly, clearly visible)", [
  ("clip_wrong_pushup_sagging", "Push-ups with BAD form: hips sagging toward the floor and elbows flared out wide", SIDE, R2),
  ("clip_wrong_squat_knees_in", "Squats with BAD form: knees caving inward and heels lifting off the floor", FRONT, R2),
  ("clip_wrong_squat_rounded_back", "Squats with BAD form: back rounding and chest falling forward", SIDE, R2),
  ("clip_wrong_deadlift_rounded", "Deadlift with a black barbell with BAD form: lower back rounded like a cat", SIDE, R2),
  ("clip_wrong_plank_hips_high", "Plank with BAD form: hips pushed far too high", SIDE, HOLD),
  ("clip_wrong_curl_swinging", "Dumbbell curls with BAD form: swinging the whole body and elbows moving forward", SIDE, R2),
  ("clip_wrong_pullup_kipping", "Pull-ups with BAD form: half reps, kicking the legs and swinging", FRONT, R2),
  ("clip_wrong_lunge_knee", "Lunges with BAD form: front knee shooting far past the toes and torso leaning forward", SIDE, R2),
  ("clip_wrong_crunch_neck", "Crunches with BAD form: hands pulling hard on the neck, chin to chest", SIDE, R2),
  ("clip_wrong_posture_desk", "Sitting on a plain white stool with BAD posture: hunched over a phone, head forward, rounded back", SIDE, "scrolling the phone, small movements"),
 ]),
]

out = ["EFFORTLESS EXERCISE — EXERCISE CLIPS FOR THE LIBRARY (H doing every move)",
       "",
       "How to use (Flow / Veo):",
       "1. Attach H's reference image every time: work/character/H-standing-front-white.png",
       "2. Paste ONE prompt, 9:16 portrait, 8 seconds. Check that H looks like the reference and the background is pure white.",
       "3. Save each video with the file name above its prompt (e.g. clip_pullup.mp4) and send them in one zip.",
       "4. If H's face or body changes, or the background is not white, generate it again (don't send that one).",
       "We already have 17 clips (push-up, squat, plank, glute bridge, dead hang, etc.), so they are not in this list.",
       ""]
n = 0
for head, items in G:
    out += ["=" * 70, head, "=" * 70, ""]
    for name, move, view, reps in items:
        n += 1
        out += [f"{n}. {name}.mp4", f"H does: {move}. " + STYLE.format(view=view, reps=reps), ""]
open("clips/clip-prompts.txt", "w").write("\n".join(out))
print(n)
