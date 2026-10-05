"""One wav per narration line via Gemini 3.8 TTS (Interactions API), for timings.py audio mode.

    GEMINI_API_KEY=... python tts_gemini.py lines.txt voice/
    VOICE=Kore STYLE="..." TTS_MODEL=gemini-3.8-flash-tts python tts_gemini.py lines.txt voice/

Needs `google-genai`. Files are named NN_<id>.wav; existing files are kept, so a
re-run only synthesises missing lines (delete a file to redo that line).
Never print or log the API key.
"""
import base64
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

MODEL = os.environ.get("TTS_MODEL", "gemini-3.8-flash-lite-tts")
VOICE = os.environ.get("VOICE", "Charon")
STYLE = os.environ.get("STYLE", "Read in a calm, warm, unhurried documentary-narrator voice, like a patient maths teacher.")


def read_lines(path):
    rows = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            seg_id, _, text = line.partition("|")
            rows.append((seg_id.strip(), text.strip()))
    return rows


def synth(client, text):
    interaction = client.interactions.create(
        model=MODEL,
        input=[{"type": "user_input", "content": [{
            "type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": STYLE}],
        }]}],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": VOICE}]},
    )
    data = interaction.output_audio.data
    return base64.b64decode(data) if isinstance(data, str) else bytes(data)


def main():
    lines, out = read_lines(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set")
    client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=90_000))
    for i, (seg_id, text) in enumerate(lines, 1):
        wav = out / f"{i:02d}_{seg_id}.wav"
        if wav.exists():
            continue
        for attempt in range(4):
            try:
                wav.write_bytes(synth(client, text))
                print(f"{wav.name}: ok", flush=True)
                break
            except Exception as exc:  # rate limits and transient API errors: back off and retry
                print(f"{wav.name}: {type(exc).__name__} (attempt {attempt + 1})", flush=True)
                time.sleep(5 * 2 ** attempt)
        else:
            sys.exit(f"giving up on {seg_id}")


if __name__ == "__main__":
    main()
