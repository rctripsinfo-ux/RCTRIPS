# Detailed, Flow-ready prompts (one image each) from make_scene_prompts.rows.
# Output: flow/dayNN.txt (prompts only, in file-name order, one per paragraph) + flow/ALL-PROMPTS.csv (file name, prompt).
import csv, io, os, re, sys, contextlib
W = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, W)
with contextlib.redirect_stdout(io.StringIO()):
    import make_scene_prompts as S
M = S.M
CHAR = ("CHARACTER (must match the attached reference exactly): H, a bald, very muscular adult man with warm tan skin and a clean white "
        "capital letter \"H\" printed on the middle of his forehead; strong jaw, serious friendly eyes; huge defined chest, shoulders and arms, "
        "visible six-pack; black athletic shorts; olive-green harness straps over the shoulders; olive utility belt with small pouches and a "
        "silver buckle; black wrist wraps on both wrists; olive combat-style sneakers. Same face, same body proportions and same outfit as the "
        "reference in every image.")
STYLE = ("STYLE: semi-realistic comic illustration, bold clean black outlines, smooth cel shading, detailed anatomically correct muscles, "
         "crisp and sharp, high contrast so it reads on a small phone screen.")
WHITE = ("BACKGROUND: pure plain white (#FFFFFF) only, no floor texture, no props except the ones named, a soft light-grey contact shadow "
         "under him. LIGHT: soft even studio light from the top left.")
SCENE = ("BACKGROUND: a full, detailed environment as described, with natural depth of field (background slightly soft, H sharp). "
         "LIGHT: natural light that matches the place, gentle rim light on H so he stands out.")
FRAME_W = ("FRAMING: vertical 9:16 (768x1376). Whole body and any equipment fully inside the frame with about 8% empty margin on all sides; "
           "nothing cut off at the edges.")
FRAME_S = ("FRAMING: vertical 9:16 (1080x1920). Keep the top 20% of the image calm and simple (a title goes there); H in the middle and lower "
           "part, whole body visible unless the description says close-up.")
PAIR = ("LOOP PAIR: this is one of two frames of the same exercise. Use exactly the same camera angle, distance, body size and position in "
        "both frames; only the moving body parts change.")
DYN = ("POSE: dynamic and unique, like a key frame from an animated film: body turned and in motion, weight shifted, clear action and emotion, "
       "interesting camera angle. NOT a stiff straight standing pose; it must look clearly different from the plain standing reference image.")
EXR = ("POSE: correct exercise form, clearly readable start/end position, natural muscle tension and effort on the face.")
NEG = ("AVOID: any text, letters or numbers (except the H on his forehead), logos, watermarks, extra people, a different face, hair, "
       "a shirt (unless described), extra or missing fingers or limbs, twisted joints, wrong or unsafe exercise form (unless the description "
       "says WRONG form), cut-off hands or feet, blurry or low-detail output.")
def camera(a):
    a = a.lower()
    if "top view" in a or "top-down" in a: return "CAMERA: from directly above, looking down."
    if "side view" in a or "profile" in a: return "CAMERA: side profile at hip height, lens 50mm, no distortion."
    if "3/4" in a: return "CAMERA: three-quarter angle at chest height, lens 50mm."
    if "floor level" in a or "camera low" in a: return "CAMERA: low, at floor level, facing him."
    if "close-up" in a: return "CAMERA: close-up, lens 85mm."
    return "CAMERA: straight front at chest height, lens 50mm, no distortion."
os.makedirs(f"{W}/flow", exist_ok=True)
for f in os.listdir(f"{W}/flow"): os.remove(f"{W}/flow/{f}")
by_day, allrows = {}, []
for d, n, line, fid, kind, st, base in S.rows:
    full = kind.startswith("SCENE")
    action = base.split(" ", 0)[0]
    pre = M.COMMON_SCENE if full else M.COMMON
    action = base[len(pre):].strip()
    pair = fid[-1] in "ab" and fid[-2].isdigit()
    action = action if action.endswith((".", "!", "?")) else action + "."
    p = " ".join(["Use the attached reference image of H.", "SCENE ACTION: " + action, CHAR, STYLE,
                  SCENE if full else WHITE, EXR if pair or re.search(r"\b(START|TOP|BOTTOM|END)\b|^(Push-up|Knee push-up|Wide push-up|Diamond|Archer|Incline|Decline|Knuckle|Overhead|Dumbbell|Resistance band|Doorway|Scapula|Russian|Side plank|Bicycle|World's|Pigeon|Lying|Plank|Dead bug|Bird dog|Hollow|Calf|Wall sit|Jump squat|Flutter|Cat pose|Cow pose|Wrist stretch|Jumping|Skater|Pistol|Fire hydrant|Side-lying|Bodyweight squat|Sumo|Child's|Cobra|Deep squat|Kneeling hip|Pike|Lunge|Glute bridge|Burpee|Mountain|High knees|Classic crunch|Reverse crunch|Dead hang|Standing hamstring|Neck stretch|Sitting cross|Halfway standing)", action) else DYN, camera(action), FRAME_S if full else FRAME_W, PAIR if pair else "", NEG])
    p = re.sub(r"\s+", " ", p).strip()
    by_day.setdefault(d, []).append((fid, p)); allrows.append((d, n, fid, "SCENE" if full else "WHITE", line, p))
for d, items in by_day.items():
    with open(f"{W}/flow/day{d:02d}.txt", "w") as f:
        f.write("\n\n".join(p for _, p in items) + "\n")
    with open(f"{W}/flow/day{d:02d}-filenames.txt", "w") as f:
        f.write("\n".join(f"{i}. {fid}.png" for i, (fid, _) in enumerate(items, 1)) + "\n")
with open(f"{W}/flow/ALL-PROMPTS.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["day", "scene", "file_name", "type", "narration", "prompt"])
    for r in allrows: w.writerow([r[0], r[1], r[2] + ".png", r[3], r[4], r[5]])
open(f"{W}/flow/README.txt", "w").write(
    "FLOW BULK PROMPTS, Days 4-30 (290 images)\n\n"
    "1. Attach work/character/H-standing-front-white.png as the reference image.\n"
    "2. Open dayNN.txt and paste the prompts in order (one prompt = one paragraph).\n"
    "3. dayNN-filenames.txt lists the file name for each prompt in the SAME order: prompt 1 = file 1, and so on.\n"
    "4. Rename each result to its file name and send all files of a day in one zip (or all days together).\n"
    "5. Regenerate any image where H's face, body or outfit changed, the form looks wrong, or text appears.\n"
    "ALL-PROMPTS.csv has every prompt with its day, scene, file name, type and the line it illustrates.\n")
print("days:", len(by_day), "| prompts:", len(allrows), "| avg words:", sum(len(r[5].split()) for r in allrows) // len(allrows))
