# Re-voice with another Kokoro voice, fitting every line into the slot it had in voice/lines.json (so the picture stays
# in sync): natural speed when it fits, otherwise the line is generated just fast enough to fit.
import json, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
VOICE = sys.argv[1] if len(sys.argv) > 1 else "am_fenrir"; BASE = 1.1
k = Kokoro("models/kokoro.onnx", "models/voices.bin"); SR = 24000
L = json.load(open("voice/lines.json")); END = 1975 / 30
def gen(text, sp):
    a, _ = k.create(text, voice=VOICE, speed=sp, lang="en-us")
    e = np.abs(a) > 0.01; i0 = int(np.argmax(e)); i1 = len(a) - int(np.argmax(e[::-1]))
    return a[max(0, i0 - 120):min(len(a), i1 + 360)].astype(np.float32)
out = np.zeros(int(END * SR), np.float32)
for i, l in enumerate(L):
    slot = (L[i + 1]["s"] if i + 1 < len(L) else END - 0.6) - l["s"] - 0.05
    sp = BASE; a = gen(l["text"], sp)
    for _ in range(4):
        if len(a) / SR <= slot: break
        sp = min(1.6, sp * (len(a) / SR) / slot * 1.02); a = gen(l["text"], sp)
    i0 = int(l["s"] * SR); out[i0:i0 + len(a)] += a[: len(out) - i0]
    print(f'{l["s"]:6.2f} slot {slot:5.2f} got {len(a)/SR:5.2f} speed {sp:.2f}  {l["text"][:40]}')
sf.write("voice/voice.wav", out / np.abs(out).max() * 0.89, SR)
