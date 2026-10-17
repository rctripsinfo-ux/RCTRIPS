import sys
sys.path.insert(0, "/root/.claude/skills/synced/370a525f-40ff-4b1d-a196-a1258fe281e4_33be9e93-4a60-43f2-9228-8bfef809efb4/reel-video-maker/scripts")
from thumb_prompts import build, stand, KNEES
V = [("skinnyfat", "Skinny arms but a soft belly? That's skinny fat",
      "Dieting makes you skinnier, bulking makes you fatter. Eat at maintenance with protein in every meal and train full body.",
      ["Push-ups, squats and rows: 3 sets of 8-12", "Protein every meal: eggs, dal or chicken", "Full body 3 days a week, add 1 rep every week"],
      "who is skinny with a belly", "#skinnyfat #bellyfat #fullbody",
      ("SKINNY ARMS?", "SOFT BELLY FIX"),
      "it names the exact body type (thin arms + belly) and promises the fix",
      "the character with an IMPORTANT BODY CHANGE to a skinny-fat body: thin skinny arms but a soft round belly, pinching his belly fat with one hand and looking down at it, worried",
      KNEES,
      stand("IMPORTANT BODY CHANGE: skinny-fat body (thin skinny arms, narrow shoulders, soft round belly hanging slightly over the belt), same face and H, left hand pinching the belly fat, right arm hanging thin by his side, worried face looking down at his belly",
            "A soft red glow on the belly only."),
      "muscular arms, big biceps, six-pack abs")]
build(V, "work/UPLOAD-TEXT.md", "# Upload text and thumbnail prompts", thumbs_path="work/THUMBNAIL-PROMPTS.md")
