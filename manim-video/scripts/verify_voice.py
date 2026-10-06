"""Listen back to narration made by tts_gemini.py with a Gemini text model, in two checks.

1. Words: every clip is transcribed and judged against its script line by the model, which ignores notation
   (digits vs numerals, symbols vs spoken names, punctuation, traditional vs simplified characters). Listed:
   words added, dropped or changed, above all at a clip's start or end, where a cut one pause off shows up as a
   phrase at the end of the wrong line. Read the list; the model can still be wrong.
2. Voice: each line flagged in voice_check.tsv is played between its neighbours, and the model says whether it
   stands out (pitch jump, other emotion, glitch). A flagged line that fits in is better kept than remade alone.

  python verify_voice.py lines.txt OUT_DIR            # both checks; results in OUT_DIR/verify.tsv
  python verify_voice.py lines.txt OUT_DIR --words    # only the transcription check

GEMINI_API_KEY must be set. VERIFY_MODEL (default gemini-3.8-flash) is a text model, so its quota is separate
from the TTS model's.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tts_gemini as T  # noqa: E402

MODEL = os.environ.get("VERIFY_MODEL", "gemini-3.8-flash")
GROUP = 7                                   # clips per request; a refused group is retried clip by clip
JUDGE = ("Each clip is one line of a narrated lecture, given with the script line it should say. For each clip, "
         "transcribe what is spoken, then compare it with the script. Ignore notation: digits vs spoken numbers, "
         "maths symbols vs words, punctuation, traditional vs simplified characters, Latin vs spoken letter names. "
         "ok=false only when words are added, dropped or changed in what is spoken; look hardest at the first and "
         "last words, where a phrase of the next or previous line may have been cut in or out. "
         "issue: empty when ok, else a short description.")
SCHEMA = {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {
    "heard": {"type": "STRING"}, "ok": {"type": "BOOLEAN"}, "issue": {"type": "STRING"}},
    "required": ["heard", "ok", "issue"]}}


def ask(key: str, parts: list[dict], schema: dict | None = None) -> str | None:
    cfg = {"responseMimeType": "application/json", "responseSchema": schema} if schema else {}
    for _ in range(3):                                   # an empty or refused answer is retried, then given up
        r = T._call(key, f"{T.API}models/{MODEL}:generateContent", {"contents": [{"parts": parts}], "generationConfig": cfg})
        try:
            return r["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            continue
    return None


def clip(path: Path) -> dict:
    return {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(path.read_bytes()).decode()}}


def judge(key, part, path) -> list[dict] | None:
    parts = [{"text": JUDGE}]
    for i, seg_id, text in part:
        parts += [{"text": f"Clip {seg_id}. Script: {text}"}, clip(path(i, seg_id))]
    answer = ask(key, parts, SCHEMA)
    try:
        got = json.loads(answer) if answer else None
    except ValueError:
        return None
    return got if got and len(got) == len(part) else None


def words(key, rows, path) -> list[tuple[str, bool, str, str, str]]:
    out = []
    for lo in range(0, len(rows), GROUP):
        part = rows[lo:lo + GROUP]
        got = judge(key, part, path) or [(judge(key, [r], path) or [None])[0] for r in part]
        for (_, seg_id, text), g in zip(part, got):
            if g is None:
                out.append((seg_id, False, text, "", "no usable answer: listen to it"))
            else:
                out.append((seg_id, bool(g["ok"]), text, g["heard"], g["issue"]))
    return out


def stands_out(key, rows, path, seg_id) -> str:
    k = next(j for j, r in enumerate(rows) if r[1] == seg_id)
    parts = [{"text": "Consecutive lines of one narrated lecture. Does the clip marked TARGET sound like the same speaker "
                      "in the same calm style as its neighbours, or does it stand out (pitch jump, other voice, odd "
                      "emotion, glitch, cut-off word)? Answer one line: 'OK' or 'STANDS OUT: <reason>'."}]
    for j in range(max(0, k - 1), min(len(rows), k + 2)):
        parts += [{"text": "TARGET:" if j == k else "neighbour:"}, clip(path(*rows[j][:2]))]
    return (ask(key, parts) or "(no answer)").strip()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lines", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--words", action="store_true", help="only the transcription check")
    args = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY is not set")
    rows = [(i, s, t) for i, (s, t) in enumerate(T.read_lines(args.lines), 1)]
    path = lambda i, seg_id: args.out / f"{i:02d}_{seg_id}.wav"
    missing = [s for i, s, _ in rows if not path(i, s).exists()]
    if missing:
        sys.exit(f"{len(missing)} line(s) have no audio yet, e.g. {missing[0]}")
    report = []
    for seg_id, ok, t, h, issue in words(key, rows, path):
        if not ok:
            report.append((seg_id, "words", issue, f"script: {t} | heard: {h}"))
    flagged = []
    tsv = args.out / "voice_check.tsv"
    if not args.words and tsv.exists():
        flagged = [l.split("\t")[0] for l in tsv.read_text().splitlines()[1:] if l.rstrip().endswith("!")]
        for seg_id in flagged:
            report.append((seg_id, "voice", stands_out(key, rows, path, seg_id), ""))
    (args.out / "verify.tsv").write_text("line\tcheck\tfinding\tdetail\n" + "".join("\t".join(r) + "\n" for r in report))
    n_words = sum(r[1] == "words" for r in report)
    n_out = sum(r[1] == "voice" and not r[2].startswith("OK") for r in report)
    print(f"verify: {len(rows)} lines; words differ in {n_words}; {n_out} of {len(flagged)} flagged lines stand out "
          f"(see verify.tsv)")
    for r in report:
        if r[1] == "words" or not r[2].startswith("OK"):
            print(f"  {r[0]} {r[1]}: {r[2]}" + (f"\n      {r[3]}" if r[3] else ""))


if __name__ == "__main__":
    main()
