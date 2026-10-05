#!/usr/bin/env python3
"""Build a clip timings file (references/timing.md) before writing scene code.

    timings.py estimate lines.txt -o timings/taylor.json [--cps 4.2] [--gap 0.35]
        Draft timings from text length, for layout work before audio exists.

    timings.py audio lines.txt --audio-dir voice/ -o timings/taylor.json [--gap 0.35]
        Real timings from one audio file per line (sorted by name, one per line of
        lines.txt). Measures each with ffprobe, records the pauses inside each
        line (phrase boundaries for mid-sentence beats), and writes the
        concatenated narration, with the gaps, next to the timings file as <clip>.wav.

    timings.py show timings/taylor.json
        Print each line's speech spans (numbered by the pause that precedes them)
        next to its phrases, to choose TimedScene.beat(k) for mid-sentence beats.

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


def speech_pauses(path: Path, duration: float) -> list[list[float]]:
    """Silences inside a clip (edge silence excluded), seconds from the clip start.

    Phrase boundaries are where mid-sentence beats belong (`TimedScene.at`).
    """
    log = subprocess.run(["ffmpeg", "-i", str(path), "-af", "silencedetect=n=-45dB:d=0.15", "-f", "null", "-"],
                         capture_output=True, text=True, check=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    return [[round(s, 2), round(e, 2)] for s, e in zip(starts, ends)
            if s > 0.05 and e < duration - 0.05 and e - s >= 0.05]


def layout(rows, durations, gap: float, pauses=None) -> list[dict]:
    segments, t = [], 0.0
    for i, ((seg_id, text), dur) in enumerate(zip(rows, durations)):
        seg = {"id": seg_id, "text": text, "start": round(t, 3), "end": round(t + dur, 3)}
        if pauses:
            seg["pauses"] = pauses[i]
        segments.append(seg)
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


def show(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for seg in data["segments"]:
        dur = seg["end"] - seg["start"]
        edges = [0.0] + [x for p in seg.get("pauses", []) for x in p] + [dur]
        print(f"{seg['id']}  [{seg['start']:.2f}-{seg['end']:.2f}]")
        for i in range(0, len(edges), 2):
            label = "start  " if i == 0 else f"beat({i // 2 - 1})"
            print(f"    {label} speech {edges[i]:5.2f}-{edges[i + 1]:5.2f}")
        for phrase in (x.strip() for x in re.split(r"(?<=[,.:;?!，。：；？！])\s*", seg["text"])):
            if phrase:
                print(f"    | {phrase}")


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "show":
        show(Path(sys.argv[2]))
        return
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
    pauses = None
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
        pauses = [speech_pauses(f, d) for f, d in zip(files, durations)]
        voice = args.out.with_suffix(".wav")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        concat_audio(files, args.gap, voice)
        payload["audio"] = voice.name

    segments = layout(rows, durations, args.gap, pauses)
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
