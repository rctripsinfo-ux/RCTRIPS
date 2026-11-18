#!/usr/bin/env python3
"""Word-level transcript with faster-whisper -> words.json (+ .srt)."""
import argparse, json, os, sys


def load_audio(path, sr=16000):
    """Decode with ffmpeg (avoids PyAV version issues) -> float32 mono numpy array."""
    import subprocess, numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def split_points(audio, sr=16000, every=25.0, search=4.0):
    """Cut points near every `every` sec, placed at the quietest 20 ms frame within +-search sec."""
    import numpy as np
    hop = int(sr * 0.02)
    n = len(audio) // hop
    rms = np.sqrt((audio[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    pts, t = [0], every
    while t < len(audio) / sr - 5:
        a, b = int((t - search) / 0.02), int((t + search) / 0.02)
        pts.append((a + int(rms[a:b].argmin())) * hop)
        t = pts[-1] / sr + every
    return pts + [len(audio)]


def transcribe(path, model="large-v3-turbo", language=None, prompt=None):
    """Chunked at pauses (~25 s) so Whisper doesn't skip or hallucinate on long clips."""
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="auto", compute_type="auto")
    sr = 16000
    audio = load_audio(path, sr)
    pts = split_points(audio, sr)
    words, lang = [], language
    for a, b in zip(pts, pts[1:]):
        segs, info = m.transcribe(audio[a:b], language=lang, word_timestamps=True, vad_filter=False,
                                  condition_on_previous_text=False, initial_prompt=prompt)
        lang = lang or info.language
        off = a / sr
        for s in segs:
            for w in s.words or []:
                words.append({"w": w.word.strip(), "s": round(w.start + off, 3), "e": round(w.end + off, 3),
                              "p": round(w.probability, 3)})
    return {"language": lang, "duration": round(len(audio) / sr, 3), "words": words}


def srt(words, per=4):
    def t(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02}:{int(m):02}:{int(s):02},{int(round((s % 1) * 1000)):03}"
    out = []
    for i in range(0, len(words), per):
        g = words[i:i + per]
        out.append(f"{len(out)+1}\n{t(g[0]['s'])} --> {t(g[-1]['e'])}\n{' '.join(x['w'] for x in g)}\n")
    return "\n".join(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--out", required=True)
    p.add_argument("--model", default="large-v3-turbo", help="large-v3-turbo (best for Hindi) | small (fast, weak on Hindi) | medium")
    p.add_argument("--language", default=None, help="e.g. en, hi (auto if omitted)")
    p.add_argument("--prompt", default=None, help="names/brands/words to spell right, e.g. \"boAt, Sony, JBL\"")
    a = p.parse_args()
    try:
        r = transcribe(a.video, a.model, a.language, a.prompt)
    except ImportError:
        sys.exit("faster-whisper not installed. Run: pip install -U faster-whisper")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(r, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.splitext(a.out)[0] + ".srt", "w", encoding="utf-8").write(srt(r["words"]))
    print(json.dumps({"ok": True, "language": r["language"], "duration": r["duration"],
                      "words": len(r["words"]), "out": a.out}))
