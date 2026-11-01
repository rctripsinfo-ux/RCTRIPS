# Voiceover with the owner's Google AI Studio voice (same logic as superhero-voiceover-ai/server.ts):
# Gemini TTS, prebuilt voice + the same style instructions. Needs GEMINI_API_KEY in the environment (never in the repo).
# usage: python3 gemini_voice.py day14.txt out.wav [--voice Fenrir] [--emotion heroic] [--pitch deep] [--texture clean] [--speed 1.0]
#        voice "TheThinker" = Zephyr + the Thinker persona (the app's default)
import argparse, base64, json, os, sys, urllib.request, wave

p = argparse.ArgumentParser()
p.add_argument("script"); p.add_argument("out")
p.add_argument("--voice", default=os.environ.get("H_VOICE", "TheThinker"))
p.add_argument("--emotion", default=os.environ.get("H_EMOTION", "heroic"))
p.add_argument("--pitch", default=os.environ.get("H_PITCH", "default"), choices=["default", "deep", "high"])
p.add_argument("--texture", default=os.environ.get("H_TEXTURE", "default"), choices=["default", "clean", "gravelly", "robotic"])
p.add_argument("--speed", type=float, default=float(os.environ.get("H_SPEED", "1.0")))
p.add_argument("--model", default="gemini-2.5-flash-preview-tts")
a = p.parse_args()
key = os.environ.get("GEMINI_API_KEY")
if not key: sys.exit("GEMINI_API_KEY is not set (add it in the environment settings, then open a new session).")
text = open(a.script).read().strip()
ins = []
if a.voice == "TheThinker":
    ins += ["Perform as a calm, natural, young male voice in his early 20s",
            "Style: Very human, not robotic, conversational, diary-like, late-night thoughts",
            "Emotion: Honest, reflective, and slightly vulnerable",
            "Delivery: Speak like you are thinking out loud to yourself or one person, not an audience",
            "Add slight pauses between sentences for natural reflection",
            "Avoid any dramatic acting, announcer tone, or exaggeration",
            "Natural mix of English and Hinglish where applicable", "Soft confidence, not motivational"]
    if a.speed == 1.0: ins.append("Speed: slow to medium")
else:
    ins.append(f"perform with the emotion: {a.emotion}")
ins += {"deep": ["use a deep, bassy tone"], "high": ["use a high-pitched sharp tone"]}.get(a.pitch, [])
ins += {"gravelly": ["add grit and gravel to the voice"], "clean": ["make the voice crystal clean and clear"],
        "robotic": ["speak like a machine"]}.get(a.texture, [])
if a.speed != 1.0: ins.append(f"speak at {a.speed:.1f}x speed")
prompt = f"[Instructions: {', '.join(ins)}.] {text}"
voice = "Zephyr" if a.voice == "TheThinker" else a.voice
body = {"contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
try:
    r = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e:
    sys.exit(f"Gemini error {e.code}: {e.read().decode()[:400]}")
part = next(p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p)
pcm = base64.b64decode(part["inlineData"]["data"])
if pcm[:4] == b"RIFF": pcm = pcm[44:]
with wave.open(a.out, "wb") as w:  # Gemini TTS returns 24 kHz, 16-bit, mono PCM
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
print(f"{a.out}: {len(pcm) / 48000:.1f} s, voice {voice} ({a.voice})")
