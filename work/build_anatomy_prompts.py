# Anatomy inset images for the Captain-style zoom bubbles (owner, 26 Oct): a line from H's body part opens a circle
# showing the real muscle / bone inside. One style for all so they look like one set. Owner makes them in Flow.
STYLE = ("Realistic 3D medical anatomy illustration, high detail, clean studio render. Pure white background (#FFFFFF), "
         "no shadows on the background, nothing else in the frame. Square 1:1 image. The subject is centered and fills "
         "about 75% of the frame, fully inside an imaginary circle, so it can be cropped into a round frame without "
         "cutting anything important. Skin removed, muscles shown in natural muted pink-beige tones with fine fiber "
         "detail, bones in soft ivory. ONLY the target area is highlighted: {hl}. No text, no labels, no arrows, no "
         "watermark, no logo, no person's face. Soft even lighting, sharp focus.")
RED = "the target glows bright saturated red (#E53935) with a soft red glow around it, clearly standing out from everything else"
PAIN = ("the painful spot glows hot red-orange with a pulsing inflamed look, small jagged red pain lightning marks radiating "
        "from it, the surrounding tissue slightly swollen")
WEAK = "the target is dull grey-blue and faded, looking weak and switched off, while the surrounding muscles keep normal colour"

P = [
 ("MUSCLES — UPPER BODY (target in red)", RED, [
  ("muscle_traps", "Upper back and neck seen from behind: the trapezius muscle"),
  ("muscle_neck", "Neck seen from the side: the neck muscles (sternocleidomastoid and upper trapezius)"),
  ("muscle_front_delts", "Right shoulder seen from the front: the front deltoid"),
  ("muscle_side_delts", "Right shoulder seen from the side: the side (lateral) deltoid"),
  ("muscle_rear_delts", "Right shoulder seen from behind: the rear deltoid"),
  ("muscle_rotator_cuff", "Right shoulder seen from behind, deltoid made transparent: the rotator cuff muscles"),
  ("muscle_chest", "Chest seen from the front: both pectoralis major muscles"),
  ("muscle_upper_chest", "Chest seen from the front: only the upper (clavicular) part of the chest"),
  ("muscle_biceps", "Right upper arm seen from the front, elbow bent: the biceps"),
  ("muscle_triceps", "Right upper arm seen from behind: the triceps (all three heads)"),
  ("muscle_forearms", "Right forearm seen from the inside, hand open: the forearm flexor muscles"),
  ("muscle_forearm_grip", "Right forearm and hand gripping a bar: the forearm and grip muscles"),
  ("muscle_lats", "Back seen from behind: both latissimus dorsi (the V-shape wings)"),
  ("muscle_rhomboids", "Upper back seen from behind, traps made transparent: the rhomboids between the shoulder blades"),
  ("muscle_lower_back", "Lower back seen from behind: the erector spinae muscles along the lower spine"),
  ("muscle_serratus", "Torso seen from the side: the serratus anterior on the ribs"),
 ]),
 ("MUSCLES — CORE AND HIPS (target in red)", RED, [
  ("muscle_abs", "Torso seen from the front: the rectus abdominis (six-pack)"),
  ("muscle_lower_abs", "Torso seen from the front: only the lower part of the abs, below the belly button"),
  ("muscle_obliques", "Torso seen from the front at a slight angle: the obliques on the sides of the waist"),
  ("muscle_deep_core", "Torso seen from the front, outer abs made transparent: the deep core (transverse abdominis) wrapping the waist like a belt"),
  ("muscle_hip_flexors", "Hip and pelvis seen from the front: the hip flexors (iliopsoas) running from the lower spine to the top of the thigh"),
  ("muscle_glutes", "Hips seen from behind: both gluteus maximus muscles"),
  ("muscle_glute_medius", "Hip seen from the side: the gluteus medius on the upper side of the hip"),
 ]),
 ("MUSCLES — LEGS (target in red)", RED, [
  ("muscle_quads", "Right thigh seen from the front: the quadriceps"),
  ("muscle_hamstrings", "Right thigh seen from behind: the hamstrings"),
  ("muscle_adductors", "Inner thighs seen from the front: the adductor muscles"),
  ("muscle_calves", "Right lower leg seen from behind: the calf muscles (gastrocnemius and soleus)"),
  ("muscle_tibialis", "Right lower leg seen from the front: the tibialis anterior along the shin"),
  ("muscle_it_band", "Right thigh seen from the side: the IT band running down the outside of the thigh"),
 ]),
 ("WEAK / SWITCHED-OFF MUSCLES (target grey-blue)", WEAK, [
  ("weak_glutes", "Hips seen from behind: both gluteus maximus muscles"),
  ("weak_core", "Torso seen from the front: the abs and deep core"),
  ("weak_hamstrings", "Right thigh seen from behind: the hamstrings"),
  ("weak_upper_back", "Upper back seen from behind: the rhomboids and middle trapezius"),
 ]),
 ("PAIN AND INJURY", PAIN, [
  ("pain_lower_back", "Lower back seen from behind with the lumbar spine visible: lower back muscles and lumbar vertebrae"),
  ("pain_disc", "Close-up side view of three lumbar vertebrae: one disc bulging out and pressing on a yellow nerve"),
  ("pain_sciatica", "Lower back, buttock and back of the right leg seen from behind: the sciatic nerve (yellow) running from the lower spine down the leg"),
  ("pain_neck", "Neck seen from the side with the cervical spine visible: the neck vertebrae and neck muscles"),
  ("pain_shoulder", "Right shoulder joint seen from the front: the shoulder joint and rotator cuff tendon"),
  ("pain_elbow", "Right elbow seen from the outside: the outer elbow tendon (tennis elbow)"),
  ("pain_wrist", "Right wrist seen from the top with the small wrist bones visible: the wrist joint"),
  ("pain_hip", "Right hip joint seen from the front with the pelvis and thigh bone visible: the hip joint"),
  ("pain_knee", "Right knee seen from the front with the kneecap visible: the knee joint and kneecap tendon"),
  ("pain_ankle", "Right ankle seen from the outside: the ankle ligaments"),
  ("pain_shin", "Right lower leg seen from the front: the inner edge of the shin bone (shin splints)"),
  ("pain_hamstring_strain", "Right thigh seen from behind: a small torn spot in the middle of the hamstring"),
  ("pain_tight_hip_flexor", "Pelvis seen from the side: a tight, shortened hip flexor pulling the pelvis forward and arching the lower back"),
 ]),
 ("BONES AND POSTURE (target in red)", RED, [
  ("bone_spine_bad", "Full human spine seen from the side with a hunched rounded upper back and head pushed forward: the rounded upper back area"),
  ("bone_pelvis_tilt", "Pelvis and lower spine seen from the side, pelvis tipped forward (anterior pelvic tilt): the pelvis"),
  ("bone_rounded_shoulders", "Upper skeleton seen from the side with shoulders rolled forward: the shoulder blades and collarbones"),
  ("bone_knee_joint", "Right knee joint, bones only, seen from the front: the knee joint"),
  ("bone_shoulder_joint", "Right shoulder joint, bones only, seen from the front: the ball and socket"),
 ]),
 ("HEALTHY REFERENCE", "the whole subject has a calm, soft green glow (#43A047) showing it is healthy, no red anywhere", [
  ("bone_spine_good", "Full human spine seen from the side with a healthy natural S-curve, bones only: the whole spine"),
 ]),
 ("INSIDE THE MUSCLE (target in red)", RED, [
  ("inside_muscle_fibers", "Close-up of a single muscle opened up showing bundles of muscle fibers: the fibers"),
  ("inside_micro_tears", "Close-up of muscle fibers with tiny tears after a workout: the torn fibers"),
  ("inside_muscle_growth", "Two muscle fiber bundles side by side, left thin, right thick and grown: the thick one"),
  ("inside_fat_vs_muscle", "Cross-section of a thigh showing skin, a thick yellow fat layer and the muscle underneath: the muscle (the fat stays yellow)"),
  ("inside_blood_flow", "Close-up of a muscle with blood vessels around it: the blood vessels pumping blood into the muscle"),
  ("inside_heart", "Realistic human heart: the whole heart"),
  ("inside_lungs", "Realistic human lungs: both lungs"),
  ("inside_tendon", "Close-up of a muscle connecting to a bone through a tendon: the tendon"),
 ]),
]

out = ["EFFORTLESS EXERCISE — ANATOMY INSET IMAGES (for the zoom circles in videos)",
       "",
       "How to use: paste ONE prompt at a time into Flow. Make it 1:1 (square). Save each image with the file name",
       "written above its prompt (e.g. muscle_glutes.png) and send them all as one zip. White background, no text.",
       ""]
n = 0
for head, hl, items in P:
    out += ["=" * 70, head, "=" * 70, ""]
    for name, subject in items:
        n += 1
        out += [f"{n}. {name}.png", f"{subject}. " + STYLE.format(hl=hl), ""]
open("anatomy/anatomy-prompts.txt", "w").write("\n".join(out))
print(n)
