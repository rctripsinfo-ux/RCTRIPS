# Reference voice pacing: 3.5-4.1 words/s, almost no pauses (gaps > 0.25 s total < 1 s per video).
# Generates every line with am_fenrir back to back (short breath gaps, one beat held for the blast), then writes
#   voice/voice_tight.wav, voice/words_tight.json (word times) and voice/warp.json (old line start -> new line start),
#   which Whale.tsx uses to re-time the whole picture without re-authoring it.
import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("models/kokoro.onnx", "models/voices.bin"); SR = 24000; SPEED = 1.2
L = json.load(open("voice/lines.json"))
GAP = {"Three.": 0.18, "Two.": 0.18, "One.": 0.95}            # the count keeps its beats, the boom gets ~1 s
def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower()) or "a"; n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0); return max(1, n)
t = 0.12; chunks = [np.zeros(int(t * SR), np.float32)]; words = []; warp = []
for l in L:
    a, _ = k.create(l["text"], voice="am_fenrir", speed=SPEED, lang="en-us"); a = a.astype(np.float32)
    e = np.abs(a) > 0.012; i0 = int(np.argmax(e)); i1 = len(a) - int(np.argmax(e[::-1])); a = a[max(0, i0 - 60):min(len(a), i1 + 200)]
    d = len(a) / SR; ws = l["text"].split(); wt = [syl(w) + .35 for w in ws]; c = t
    for w, x in zip(ws, wt): dd = d * x / sum(wt); words.append({"w": w.strip(), "s": round(c, 3), "e": round(c + dd, 3)}); c += dd
    warp.append([l["s"], round(t, 3)])
    gap = GAP.get(l["text"], 0.16 if l["text"].endswith((".", "?", ":")) else 0.06)
    chunks += [a, np.zeros(int(gap * SR), np.float32)]; t += d + gap
v = np.concatenate(chunks + [np.zeros(int(0.5 * SR), np.float32)])
warp.append([1975 / 30, round(len(v) / SR, 3)])
sf.write("voice/voice_tight.wav", v / np.abs(v).max() * 0.89, SR)
json.dump(words, open("voice/words_tight.json", "w")); json.dump(warp, open("voice/warp.json", "w"))
n = len(words); dur = len(v) / SR
print(f"duration {dur:.2f}s  words {n}  rate {n / (words[-1]['e'] - words[0]['s']):.2f} w/s  frames {round(dur * 30)}")
