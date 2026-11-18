"""Speech-to-text for SubGrab using faster-whisper (free, runs locally).

Usage: python transcribe.py AUDIO_FILE [--model large-v3-turbo] [--language auto]
Prints JSON: {"language": "en", "segments": [{"start", "end", "text", "words": [{"start", "end", "word"}]}]}
"""
import argparse
import json
import os
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("audio")
    p.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "large-v3-turbo"))
    p.add_argument("--language", default="auto")
    a = p.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper is not installed. Run: python -m pip install --user -U faster-whisper", file=sys.stderr)
        sys.exit(2)

    device = os.environ.get("WHISPER_DEVICE", "auto")
    compute = os.environ.get("WHISPER_COMPUTE", "default")
    model = WhisperModel(a.model, device=device, compute_type=compute)
    segments, info = model.transcribe(
        a.audio,
        language=None if a.language in ("", "auto") else a.language,
        beam_size=5,
        word_timestamps=True,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    out = []
    for s in segments:
        words = [{"start": round(w.start, 3), "end": round(w.end, 3), "word": w.word.strip()} for w in (s.words or []) if w.word.strip()]
        out.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": words})
    json.dump({"language": info.language, "probability": round(info.language_probability, 3), "segments": out}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
