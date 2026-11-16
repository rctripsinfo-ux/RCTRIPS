# audio_fx.py Lxx -> Lxx.audio.json : loudness, voice vs music-bed level, SFX onsets (in speech gaps) with a rough type
import json, subprocess, sys, re, numpy as np
v = sys.argv[1]; SR = 16000
eb = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", f"{v}.mp4", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1]); TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{v}.mp4", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
hop = 400; n = len(a) // hop; fr = a[:n * hop].reshape(n, hop); rms = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-6)  # 25 ms frames
W = [w for s in json.load(open(f"{v}.words.json")) for w in s["words"]]
speech = np.zeros(n, bool)
for w in W: speech[int(w["s"] * 40):int(w["e"] * 40) + 1] = True
sp2 = speech.copy()
for k in range(1, 10): sp2[:-k] |= speech[k:]; sp2[k:] |= speech[:-k]  # +-0.25 s around words
voice = float(np.median(rms[speech])) if speech.any() else None
gap = ~sp2; gap[:40] = False; gap[-40:] = False
bed = float(np.median(rms[gap])) if gap.sum() > 40 else None
# spectral flux onsets
win = 512; hp = 160; m = (len(a) - win) // hp; idx = np.arange(win)[None, :] + hp * np.arange(m)[:, None]
S = np.abs(np.fft.rfft(a[idx] * np.hanning(win), axis=1)); fl = np.maximum(np.diff(np.log1p(S * 50), axis=0), 0).sum(1)
fl = (fl - np.median(fl)) / (np.std(fl) + 1e-6); t_fl = np.arange(1, m) * hp / SR
peaks = [k for k in range(1, len(fl) - 1) if fl[k] > 4 and fl[k] >= fl[k - 1] and fl[k] >= fl[k + 1]]
sfx = []; last = -1
for k in peaks:
    t = t_fl[k]; j = int(t * 40)
    if j >= n or t - last < 0.25: continue
    in_gap = not sp2[min(j, n - 1)]
    lv = rms[j:j + 8].max() if j + 8 < n else rms[j]
    if not in_gap and lv < (voice or -30) + 4: continue  # over speech only if clearly louder than the voice
    seg = a[int(t * SR):int(t * SR) + int(0.6 * SR)]
    if len(seg) < 800: continue
    seg = seg[:len(seg) // 160 * 160]; env = np.abs(seg).reshape(-1, 160).max(1); dur = (env > env.max() * 0.25).sum() * 0.01
    sp = np.abs(np.fft.rfft(seg[:4096] * np.hanning(min(4096, len(seg))))) if len(seg) >= 4096 else np.abs(np.fft.rfft(seg))
    fq = np.fft.rfftfreq(len(seg[:4096]) if len(seg) >= 4096 else len(seg), 1 / SR); cen = float((sp * fq).sum() / (sp.sum() + 1e-9))
    flat = float(np.exp(np.log(sp + 1e-9).mean()) / (sp.mean() + 1e-9)); peaky = sp.max() / (sp.mean() + 1e-9)
    kind = "pop/click" if dur < 0.09 else "ding/tonal" if peaky > 40 and dur > 0.2 else "whoosh/noise" if flat > 0.2 else "impact/other"
    sfx.append(dict(t=round(float(t), 2), in_gap=bool(in_gap), dur=round(float(dur), 2), centroid=int(cen), kind=kind)); last = t
dur_s = len(a) / SR
from collections import Counter
res = dict(v=v, lufs=I, true_peak=TP, voice_db=round(voice, 1) if voice else None, bed_in_gaps_db=round(bed, 1) if bed else None,
           bed_under_voice_db=round(voice - bed, 1) if voice and bed else None, sfx_per_min=round(len(sfx) / dur_s * 60, 1), sfx_types=dict(Counter(s["kind"] for s in sfx)), sfx=sfx)
json.dump(res, open(f"{v}.audio.json", "w")); print(v, I, TP, res["voice_db"], res["bed_in_gaps_db"], res["bed_under_voice_db"], res["sfx_per_min"], res["sfx_types"])
