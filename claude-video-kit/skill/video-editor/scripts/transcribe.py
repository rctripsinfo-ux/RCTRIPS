#!/usr/bin/env python3
"""Word-level transcript with faster-whisper -> words.json (+ .srt)."""
import argparse, json, os, sys


def transcribe(path, model="small", language=None):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="auto", compute_type="auto")
    segs, info = m.transcribe(path, language=language, word_timestamps=True, vad_filter=False)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3),
                          "p": round(w.probability, 3)})
    return {"language": info.language, "duration": round(info.duration, 3), "words": words}


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
    p.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3 (bigger = slower, better)")
    p.add_argument("--language", default=None, help="e.g. en, hi (auto if omitted)")
    a = p.parse_args()
    try:
        r = transcribe(a.video, a.model, a.language)
    except ImportError:
        sys.exit("faster-whisper not installed. Run: pip install -U faster-whisper")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(r, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.splitext(a.out)[0] + ".srt", "w", encoding="utf-8").write(srt(r["words"]))
    print(json.dumps({"ok": True, "language": r["language"], "duration": r["duration"],
                      "words": len(r["words"]), "out": a.out}))
