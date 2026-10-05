#!/usr/bin/env python3
"""Join rendered chapters into one narrated film with sentence-level subtitles.

    assemble.py chapters.txt -o film.mp4

chapters.txt lists one chapter per line, in order: `<video.mp4> <timings.json>`
(paths relative to chapters.txt; # comments allowed). Each timings file's
"audio" (written by timings.py audio) is that chapter's narration, starting at
the chapter's first frame.

Each chapter's narration is padded with silence to that chapter's measured
video duration before concatenation, so audio and picture stay aligned across
chapter boundaries (a chapter's video is longer than its voice by its tail and
frame rounding). Subtitles come from the timings text (the script), split into
sentences and clauses of at most 90 characters, with cue boundaries snapped to
recorded pauses. Writes film.mp4, film.srt and film_narration.wav, then prints
the durations, which must agree.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_CHARS = 90


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def srt_time(t: float) -> str:
    ms = round(t * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunk_text(text: str) -> list[str]:
    """Sentences first, then clauses, each at most MAX_CHARS where possible."""
    chunks = []
    for sent in (x for x in re.split(r"(?<=[.?!。？！])\s*", text) if x.strip()):
        if len(sent) <= MAX_CHARS:
            chunks.append(sent.strip())
            continue
        cur = ""
        for part in (x for x in re.split(r"(?<=[,:;，：；])\s*", sent) if x.strip()):
            if cur and len(cur) + 1 + len(part) > MAX_CHARS:
                chunks.append(cur)
                cur = part.strip()
            else:
                cur = f"{cur} {part}".strip()
        if cur:
            chunks.append(cur)
    return chunks


def segment_cues(seg: dict) -> list[tuple[float, float, str]]:
    """Time each chunk by its share of characters, snapping boundaries to the nearest recorded pause."""
    start, end = seg["start"], seg["end"]
    chunks = chunk_text(seg["text"])
    total = sum(len(c) for c in chunks) or 1
    pauses = [start + (a + b) / 2 for a, b in seg.get("pauses", [])]
    cues, t0, acc = [], start, 0
    for i, chunk in enumerate(chunks):
        acc += len(chunk)
        if i == len(chunks) - 1:
            t1 = end
        else:
            guess = start + (end - start) * acc / total
            near = min(pauses, key=lambda p: abs(p - guess)) if pauses else guess
            t1 = near if abs(near - guess) < 1.5 and near > t0 + 0.5 else guess
        cues.append((t0, t1, chunk))
        t0 = t1
    return cues


def read_chapters(listing: Path) -> list[tuple[Path, Path]]:
    chapters = []
    for raw in listing.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            video, timings = line.split()
            chapters.append((listing.parent / video, listing.parent / timings))
    missing = [str(p) for pair in chapters for p in pair if not p.exists()]
    if missing:
        sys.exit("missing:\n" + "\n".join(missing))
    return chapters


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapters", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()

    chapters = read_chapters(args.chapters)
    timings = [json.loads(t.read_text(encoding="utf-8")) for _, t in chapters]
    audios = [t.parent / data["audio"] for (_, t), data in zip(chapters, timings)]
    durs = [duration(v) for v, _ in chapters]
    voice = args.out.with_name(args.out.stem + "_narration.wav")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        padded = []
        for i, (audio, d) in enumerate(zip(audios, durs)):
            out = tmp / f"a{i:03d}.wav"
            run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-af", "apad", "-t", f"{d:.6f}",
                 "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(out)])
            padded.append(out)
        vlist, alist = tmp / "v.txt", tmp / "a.txt"
        vlist.write_text("".join(f"file '{v.resolve()}'\n" for v, _ in chapters), encoding="utf-8")
        alist.write_text("".join(f"file '{a}'\n" for a in padded), encoding="utf-8")
        picture = tmp / "picture.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(vlist), "-c", "copy", str(picture)])
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(alist), "-c", "copy", str(voice)])
        run(["ffmpeg", "-v", "error", "-y", "-i", str(picture), "-i", str(voice), "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(args.out)])

    entries, offset = [], 0.0
    for data, d in zip(timings, durs):
        for seg in data["segments"]:
            entries += [(offset + a, offset + b, text) for a, b, text in segment_cues(seg)]
        offset += d
    srt = "".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{text}\n\n" for i, (a, b, text) in enumerate(entries, 1))
    args.out.with_suffix(".srt").write_text(srt, encoding="utf-8")

    print(f"{len(chapters)} chapters, {len(entries)} subtitles")
    print(f"sum of chapters {sum(durs):.3f}s | film {duration(args.out):.3f}s | narration {duration(voice):.3f}s")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(f"ffmpeg/ffprobe failed: {exc}")
