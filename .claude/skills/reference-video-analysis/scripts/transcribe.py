#!/usr/bin/env python3
"""Transcribe a video's audio and measure delivery (words/sec, pauses, opening line).

Needs faster-whisper or openai-whisper installed. Make sure the file has the ORIGINAL language track.
Usage: transcribe.py VIDEO --out DIR [--model small] [--language en]
Writes transcript.txt, segments.json, speech.json.
"""
import argparse, json, os


def run(path, model, lang):
    try:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel(model).transcribe(path, language=lang)
        return [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs]
    except ImportError:
        import whisper
        r = whisper.load_model(model).transcribe(path, language=lang)
        return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in r["segments"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--language")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    segs = run(a.video, a.model, a.language)
    words = sum(len(s["text"].split()) for s in segs)
    speech = sum(s["end"] - s["start"] for s in segs)
    gaps = [b["start"] - e["end"] for e, b in zip(segs, segs[1:])]
    total = segs[-1]["end"] if segs else 0
    stats = {"words": words, "words_per_sec_speaking": words / speech if speech else None,
             "words_per_sec_overall": words / total if total else None,
             "dead_air_pct": (1 - speech / total) * 100 if total else None,
             "pauses_over_0_5s": sum(g > 0.5 for g in gaps),
             "opening_line": segs[0]["text"] if segs else ""}
    open(os.path.join(a.out, "transcript.txt"), "w").write("\n".join(s["text"] for s in segs))
    json.dump(segs, open(os.path.join(a.out, "segments.json"), "w"), indent=2)
    json.dump(stats, open(os.path.join(a.out, "speech.json"), "w"), indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
