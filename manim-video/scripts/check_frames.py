#!/usr/bin/env python3
"""Pull review frames at segment boundaries or explicit visual timestamps.

    check_frames.py media/videos/film/480p15/Taylor.mp4 timings/taylor.json -o check/taylor
    check_frames.py clip.mp4 timings.json -o check/ --at 12.4 30.1    # extra moments
    check_frames.py silent.mp4 -o check/silent --at 0 1.5 3          # no timing file

For every segment it extracts two frames:
  <id>_in.png   0.4 s after the segment starts  (nothing that is said later may be visible)
  <id>_out.png  0.1 s before the segment ends   (everything said so far must be visible)
then tiles all frames into contact.png and compares the clip and timings durations.
Without a timing file, --at is required and no expected duration is inferred.
Read the frames; a passing run of this script is not a visual review.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def ffprobe(path: Path, entries: str, stream: str | None = None) -> str:
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()


def grab(video: Path, t: float, out: Path, width: int) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", str(video),
                    "-frames:v", "1", "-vf", f"scale={width}:-2", str(out)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("timings", type=Path, nargs="?", help="optional segment timeline JSON")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--at", type=float, nargs="+", default=[], help="timestamps in seconds relative to the clip (plus --offset)")
    ap.add_argument("--width", type=int, default=640)
    ap.add_argument("--offset", type=float, default=0.0, help="clip start inside the video")
    args = ap.parse_args()

    if args.timings is None and not args.at:
        ap.error("provide a timing file or at least one --at timestamp")
    if any(not math.isfinite(t) or t < 0 for t in [args.offset, *args.at]):
        ap.error("timestamps and offset must be finite and non-negative")
    if args.width < 2:
        ap.error("width must be at least 2 pixels")
    timings = json.loads(args.timings.read_text(encoding="utf-8")) if args.timings else None
    duration = float(ffprobe(args.video, "format=duration"))
    args.out.mkdir(parents=True, exist_ok=True)

    shots: list[tuple[str, float]] = []
    segments = timings["segments"] if timings is not None else []
    for seg in segments:
        start, end = float(seg["start"]), float(seg["end"])
        if not all(math.isfinite(t) for t in [start, end]) or start < 0 or end <= start:
            ap.error(f"invalid segment interval: {seg['id']}")
        shots.append((f"{seg['id']}_in", start + min(0.4, (end - start) / 2)))
        shots.append((f"{seg['id']}_out", max(start, end - 0.1)))
    shots += [(f"at_{t:07.2f}", t) for t in args.at]

    contact = args.out / "contact.png"
    contact.unlink(missing_ok=True)
    frames, cols = [], 4
    for name, t in shots:
        t += args.offset
        if t >= duration:
            print(f"skip {name}: {t:.2f}s is past the video end ({duration:.2f}s)")
            continue
        frame = args.out / f"{name}.png"
        frame.unlink(missing_ok=True)
        grab(args.video, t, frame, args.width)
        if not frame.is_file() or not frame.stat().st_size:
            print(f"skip {name}: no frame decoded at {t:.2f}s")
            continue
        frames.append(frame)

    if not frames:
        ap.error("no review frames were extracted; choose timestamps inside the clip")
    if len(frames) == 1:
        shutil.copyfile(frames[0], contact)
    else:
        inputs = sum((["-i", str(f)] for f in frames), [])
        pads = "".join(f"[{i}:v]" for i in range(len(frames)))
        layout = "|".join(f"{'+'.join(['w0'] * (i % cols)) or '0'}_{'+'.join(['h0'] * (i // cols)) or '0'}"
                          for i in range(len(frames)))
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                        f"{pads}xstack=inputs={len(frames)}:layout={layout}:fill=black",
                        "-frames:v", "1", str(contact)], check=True)

    expected = None
    if timings is not None:
        if "duration" in timings:
            expected = float(timings["duration"])
        elif segments:
            expected = float(segments[-1]["end"])
    has_audio = bool(ffprobe(args.video, "stream=codec_type", "a"))
    print(f"frames: {len(frames)} in {args.out} (contact.png, {cols} columns)")
    if args.offset:   # a chapter inside a longer film: the totals are not comparable
        print(f"clip at {args.offset:.2f}s inside a {duration:.2f}s video; audio stream: {'yes' if has_audio else 'no'}")
    elif expected is not None:
        print(f"video {duration:.2f}s vs timings {expected:.2f}s (diff {duration - expected:+.2f}s); "
              f"audio stream: {'yes' if has_audio else 'no'}")
    else:
        print(f"video {duration:.2f}s; no expected timing duration supplied; "
              f"audio stream: {'yes' if has_audio else 'no'}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(f"ffmpeg/ffprobe failed: {exc}")
