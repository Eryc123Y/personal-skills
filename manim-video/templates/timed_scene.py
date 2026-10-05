"""Narration-timed Manim CE scene base. Copy next to the film's scene file.

Every segment time comes from a timings file (see references/timing.md):

    {"clip": "taylor", "audio": "voice.wav", "duration": 41.2,
     "segments": [{"id": "hook", "text": "...", "start": 0.0, "end": 3.4}, ...]}

Usage:

    from timed_scene import TimedScene, PALETTE, cjk_tex

    class Taylor(TimedScene):
        TIMINGS = "timings/taylor.json"

        def construct(self):
            self.say("hook")                      # waits for the segment, adds its subtitle
            self.play(Write(title), run_time=1.2)
            self.at(2.4)                          # 2.4 s into "hook", when the key word is spoken
            self.say("map")                       # pads to the next segment's start
            ...
            self.finish()                         # pads to the clip's duration

Time is anchored to absolute segment starts rather than summed run_times,
because Manim rounds each animation to whole frames: 0.7 s is 11 frames at
15 fps (0.733 s) but 42 frames at 60 fps (0.700 s). Summed budgets therefore
drift differently in preview and final renders; absolute anchors do not.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from manim import Scene, TexTemplate, config, logger

# One frame at the slowest preview rate; overruns smaller than this are frame rounding.
FRAME_TOLERANCE = 1 / 15
PREVIEW_QUALITIES = {"low_quality", "medium_quality"}

PALETTE = {
    "bg": "#16181d",
    "ink": "#ece8df",
    "muted": "#9a968c",
    "primary": "#5fb3d9",   # the main object
    "result": "#7cc48a",    # verified results, conclusions
    "focus": "#f2c14e",     # current focus; at most one at a time
    "warn": "#e0675c",      # errors, counterexamples
}

CJK_FONT = "PingFang SC"


def cjk_tex() -> TexTemplate:
    """XeLaTeX + ctex template for MathTex/Tex that contain Chinese."""
    return TexTemplate(
        tex_compiler="xelatex",
        output_format=".xdv",
        preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage[UTF8]{ctex}",
    )


@dataclass(frozen=True)
class Segment:
    id: str
    text: str
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


def load_timings(path: str | Path) -> tuple[dict[str, Segment], float]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    segments = [Segment(s["id"], s.get("text", ""), float(s["start"]), float(s["end"]))
                for s in data["segments"]]
    ids = [s.id for s in segments]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path}: duplicate segment ids")
    if any(b.start < a.end - 1e-6 for a, b in zip(segments, segments[1:])):
        raise ValueError(f"{path}: segments overlap or are out of order")
    duration = float(data.get("duration", segments[-1].end if segments else 0.0))
    return {s.id: s for s in segments}, duration


class TimedScene(Scene):
    TIMINGS: str = ""
    SUBTITLES: bool = True    # emit .srt via add_subcaption; never burn subtitles in
    OVERRUN_LIMIT: float = 0.3  # seconds a final render may run late before failing

    def setup(self) -> None:
        if not self.TIMINGS:
            raise ValueError(f"{type(self).__name__}.TIMINGS is not set")
        self.segments, self.clip_duration = load_timings(self.TIMINGS)
        self.camera.background_color = PALETTE["bg"]
        self._t0 = self.time
        self.current: Segment | None = None
        self.overruns: list[tuple[str, float]] = []

    @property
    def clock(self) -> float:
        """Seconds since this clip started."""
        return self.time - self._t0

    def until(self, t: float, label: str = "") -> None:
        """Hold the current frame until clip time ``t``."""
        gap = t - self.clock
        if gap >= 1 / config.frame_rate:   # sub-frame waits would be padded to a whole frame
            self.wait(gap)
        elif -gap > FRAME_TOLERANCE:
            self.on_overrun(label or f"t={t:.2f}", -gap)

    def say(self, seg_id: str) -> Segment:
        """Start a narration segment: pad to its start, then attach its subtitle."""
        seg = self.segments[seg_id]
        self.until(seg.start, label=f"before {seg_id}")
        if self.SUBTITLES and seg.text:
            self.add_subcaption(seg.text, duration=seg.duration)
        self.current = seg
        return seg

    def at(self, offset: float) -> None:
        """Hold until ``offset`` seconds into the current segment (a beat mid-sentence)."""
        self.until(self.current.start + offset, label=f"{self.current.id}+{offset:g}s")

    def hold(self, seg_id: str) -> None:
        """Pad to the end of a segment (use when the next beat should not start early)."""
        self.until(self.segments[seg_id].end, label=f"end of {seg_id}")

    def finish(self) -> None:
        self.until(self.clip_duration, label="clip end")
        if self.overruns:
            late = ", ".join(f"{label} +{s:.2f}s" for label, s in self.overruns)
            logger.warning(f"{type(self).__name__}: {len(self.overruns)} late beat(s): {late}")

    def on_overrun(self, label: str, overrun: float) -> None:
        """Animations ran ``overrun`` seconds past an anchor that should already be due.

        Previews (-ql, -qm) record and warn so one render shows every late beat.
        Final renders fail on overruns above OVERRUN_LIMIT; smaller ones are
        absorbed by the next anchor.
        """
        self.overruns.append((label, overrun))
        message = f"{type(self).__name__}: visuals {overrun:.2f}s late at {label}"
        if config.quality not in PREVIEW_QUALITIES and overrun > self.OVERRUN_LIMIT:
            raise RuntimeError(message + " (shorten run_times or move a beat to the next segment)")
        logger.warning(message)
