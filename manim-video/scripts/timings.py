#!/usr/bin/env python3
"""Build a clip timings file (references/timing.md) before writing scene code.

    timings.py estimate lines.txt -o timings/taylor.json [--cps 4.2] [--gap 0.35]
        Draft timings from text length, for layout work before audio exists.

    timings.py audio lines.txt --audio-dir voice/ -o timings/taylor.json [--gap 0.35]
        Real timings from one audio file per line (sorted by name, one per line of
        lines.txt). Measures each with ffprobe and writes the concatenated
        narration, with the gaps, next to the timings file as <clip>.wav.

lines.txt holds one narration segment per non-empty line, either "id | text"
or plain text (ids become s01, s02, ...). Lines starting with # are ignored.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
CJK = re.compile(r"[㐀-鿿豈-﫿]")


def read_lines(path: Path) -> list[tuple[str, str]]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        seg_id, sep, text = line.partition("|")
        rows.append((seg_id.strip(), text.strip()) if sep else ("", line))
    if not rows:
        raise SystemExit(f"{path}: no narration lines")
    rows = [(seg_id or f"s{i:02d}", text) for i, (seg_id, text) in enumerate(rows, 1)]
    ids = [seg_id for seg_id, _ in rows]
    if len(set(ids)) != len(ids):
        raise SystemExit(f"{path}: duplicate ids")
    return rows


def spoken_units(text: str) -> float:
    """CJK characters count one each; other words count as 1.6 characters."""
    cjk = len(CJK.findall(text))
    words = len(re.findall(r"[A-Za-z0-9]+", CJK.sub(" ", text)))
    return cjk + 1.6 * words


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def layout(rows, durations, gap: float) -> list[dict]:
    segments, t = [], 0.0
    for (seg_id, text), dur in zip(rows, durations):
        segments.append({"id": seg_id, "text": text, "start": round(t, 3), "end": round(t + dur, 3)})
        t += dur + gap
    return segments


def concat_audio(files: list[Path], gap: float, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        silence = Path(tmp) / "gap.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        "anullsrc=r=48000:cl=mono", "-t", f"{gap:.3f}", str(silence)], check=True)
        parts = []
        for i, f in enumerate(files):
            norm = Path(tmp) / f"{i:03d}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-ar", "48000", "-ac", "1",
                            str(norm)], check=True)
            parts.append(norm)
            if gap > 0 and i < len(files) - 1:
                parts.append(silence)
        listing = Path(tmp) / "list.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                        "-c", "copy", str(out)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["estimate", "audio"])
    ap.add_argument("lines", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--audio-dir", type=Path)
    ap.add_argument("--cps", type=float, default=4.2, help="estimate: spoken units per second")
    ap.add_argument("--gap", type=float, default=0.35, help="seconds of silence between segments")
    ap.add_argument("--tail", type=float, default=1.0, help="hold after the last segment")
    args = ap.parse_args()

    rows = read_lines(args.lines)
    clip = args.out.stem
    payload = {"clip": clip}
    if args.mode == "estimate":
        durations = [max(1.2, spoken_units(text) / args.cps) for _, text in rows]
        payload["estimated"] = True
    else:
        if not args.audio_dir:
            raise SystemExit("audio mode needs --audio-dir")
        files = sorted(p for p in args.audio_dir.iterdir() if p.suffix.lower() in AUDIO_EXTS)
        if len(files) != len(rows):
            raise SystemExit(f"{len(rows)} lines but {len(files)} audio files in {args.audio_dir}")
        durations = [probe_duration(f) for f in files]
        voice = args.out.with_suffix(".wav")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        concat_audio(files, args.gap, voice)
        payload["audio"] = voice.name

    segments = layout(rows, durations, args.gap)
    payload["duration"] = round(segments[-1]["end"] + args.tail, 3)
    payload["segments"] = segments
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{args.out}: {len(segments)} segments, {payload['duration']:.2f} s"
          + (" (estimated)" if payload.get("estimated") else ""))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(f"ffmpeg/ffprobe failed: {exc}")
