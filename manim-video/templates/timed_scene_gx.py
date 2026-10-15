"""Narration-timed ManimGX scene base: timed_scene.py for the GPU engine. Copy next to the film's scene file.

Same timings file and the same calls as the Manim CE template (see its docstring and references/timing.md):

    from timed_scene_gx import TimedScene, PALETTE, mix_line
    import manimgx as m

    class Taylor(TimedScene):
        TIMINGS = "timings/taylor.json"

        def construct(self):
            self.say("hook")
            self.play(m.Write(title), run_time=1.2)
            self.beat(0)
            ...
            self.finish()

    manimgx render scene.py Taylor -r 1280x720 --fps 30 -o draft.mp4     (preview: late beats only warn)
    manimgx render scene.py Taylor --fps 60 --crf 18 -o final.mp4        (1080p and up: late beats fail)

Differences from timed_scene.py (references/manimgx.md):
- the clip's time is `self.now`, not `self.clock`: ManimGX's Scene keeps its own `clock`;
- previews are told apart by resolution (ManimGX has no quality setting);
- no TeX templates: Chinese mixed with formulas is one Typst line (`mix_line`); MathTex alone needs nothing.
"""
from __future__ import annotations

import json
import warnings
from dataclasses import dataclass
from pathlib import Path

import manimgx as m

# One frame at the slowest preview rate; overruns smaller than this are frame rounding.
FRAME_TOLERANCE = 1 / 15
FINAL_HEIGHT = 1080       # renders at this height and above are finals

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
MATH_FONT = "New Computer Modern Math"
# Typst preamble for a line of Chinese with $...$ formulas: words in the CJK font, formulas in the maths font with
# the CJK font as fallback (Chinese inside \text{})
MIX_PREAMBLE = ('#import "@preview/mitex:0.2.7": mitex-scope\n'
                f'#set text(font: "{CJK_FONT}")\n'
                f'#show math.equation: set text(font: ("{MATH_FONT}", "{CJK_FONT}"))\n')
NO_GAP_BEFORE = "，。、；：？！）」》”’…,.;:?!)"       # punctuation that follows a formula directly


def _formula(latex: str) -> str:
    """Typst for one LaTeX formula, converted as MathTex converts it (mitex). ManimGX 0.1.1's own helpers;
    `{,}` becomes \\mathord{,}, since mitex otherwise leaves a space after the comma (10, 987)."""
    from manimgx import _engine
    from manimgx.drawing.typesetting import typst_string
    code = _engine.mitex_math(latex.replace("{,}", r"\mathord{,}"))
    return f'$display(#eval({typst_string(code)}, mode: "math", scope: mitex-scope))$'


def mix_line(s: str, font_size: float = 36, color: str = PALETTE["ink"], gap: str = "0.2em") -> m.Typst:
    """One line of Chinese with $...$ LaTeX formulas, e.g. mix_line("误差 $e(x)$ 的上界").

    Formulas are display style with `gap` on each side, as a ctex template sets them in Manim CE (no gap before
    full-width punctuation). The same font_size sets this line about 5 % smaller than CE's MathTex line."""
    from manimgx.drawing.typesetting import typst_string
    parts = s.split("$")
    if len(parts) % 2 == 0:
        raise ValueError(f"unbalanced $ in {s!r}")
    out = []
    for k, part in enumerate(parts):
        if k % 2:
            out.append(_formula(part))
            continue
        t = part.strip(" ")
        if t:
            lead = f"#h({gap})" if k > 0 and t[0] not in NO_GAP_BEFORE else ""
            trail = f"#h({gap})" if k < len(parts) - 1 else ""
            out.append(lead + "#" + typst_string(t) + trail)
    return m.Typst("".join(out), font_size=font_size, color=color, typst_preamble=MIX_PREAMBLE)


@dataclass(frozen=True)
class Segment:
    id: str
    text: str
    start: float
    end: float
    pauses: tuple[tuple[float, float], ...] = ()   # silences inside the line, seconds from its start

    @property
    def duration(self) -> float:
        return self.end - self.start


def load_timings(path: str | Path) -> tuple[dict[str, Segment], float]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    segments = [Segment(s["id"], s.get("text", ""), float(s["start"]), float(s["end"]),
                        tuple((float(a), float(b)) for a, b in s.get("pauses", [])))
                for s in data["segments"]]
    ids = [s.id for s in segments]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path}: duplicate segment ids")
    if any(b.start < a.end - 1e-6 for a, b in zip(segments, segments[1:])):
        raise ValueError(f"{path}: segments overlap or are out of order")
    duration = float(data.get("duration", segments[-1].end if segments else 0.0))
    return {s.id: s for s in segments}, duration


class TimedScene(m.Scene):
    TIMINGS: str = ""
    SUBTITLES: bool = True      # captions; `manimgx render` writes them beside the video as .srt
    OVERRUN_LIMIT: float = 0.3  # seconds a final render may run late before failing

    def setup(self) -> None:
        if not self.TIMINGS:
            raise ValueError(f"{type(self).__name__}.TIMINGS is not set")
        self.segments, self.clip_duration = load_timings(self.TIMINGS)
        self.camera.background_color = PALETTE["bg"]
        self._t0 = float(self.time)
        self.current: Segment | None = None
        self.overruns: list[tuple[str, float]] = []

    @property
    def now(self) -> float:
        """Seconds since this clip started."""
        return float(self.time) - self._t0

    def until(self, t: float, label: str = "") -> None:
        """Hold the current frame until clip time ``t``."""
        gap = t - self.now
        if gap >= 1 / m.config.frame_rate:   # sub-frame waits would be padded to a whole frame
            self.wait(gap)
        elif -gap > FRAME_TOLERANCE:
            self.on_overrun(label or f"t={t:.2f}", -gap)

    def say(self, seg_id: str) -> Segment:
        """Start a narration segment: pad to its start, then attach its caption."""
        seg = self.segments[seg_id]
        self.until(seg.start, label=f"before {seg_id}")
        if self.SUBTITLES and seg.text:
            self.add_subcaption(seg.text, duration=seg.duration)
        self.current = seg
        return seg

    def at(self, offset: float) -> None:
        """Hold until ``offset`` seconds into the current segment (a beat mid-sentence)."""
        self.until(self.current.start + offset, label=f"{self.current.id}+{offset:g}s")

    def beat(self, k: int, delay: float = 0.0) -> None:
        """Hold until pause ``k`` of the current segment ends, when its next phrase begins."""
        pauses = self.current.pauses
        if k >= len(pauses):
            raise IndexError(f"{self.current.id} has {len(pauses)} pauses; beat({k}) requested")
        self.until(self.current.start + pauses[k][1] + delay, label=f"{self.current.id} beat {k}")

    def hold(self, seg_id: str) -> None:
        """Pad to the end of a segment (use when the next beat should not start early)."""
        self.until(self.segments[seg_id].end, label=f"end of {seg_id}")

    def finish(self) -> None:
        self.until(self.clip_duration, label="clip end")
        if self.overruns:
            late = ", ".join(f"{label} +{s:.2f}s" for label, s in self.overruns)
            warnings.warn(f"{type(self).__name__}: {len(self.overruns)} late beat(s): {late}", stacklevel=2)

    def on_overrun(self, label: str, overrun: float) -> None:
        """Animations ran ``overrun`` seconds past an anchor that should already be due.

        Previews (below FINAL_HEIGHT) record and warn so one render shows every late beat. Final renders fail on
        overruns above OVERRUN_LIMIT; smaller ones are absorbed by the next anchor.
        """
        self.overruns.append((label, overrun))
        message = f"{type(self).__name__}: visuals {overrun:.2f}s late at {label}"
        if m.config.pixel_height >= FINAL_HEIGHT and overrun > self.OVERRUN_LIMIT:
            raise RuntimeError(message + " (shorten run_times or move a beat to the next segment)")
        warnings.warn(message, stacklevel=3)
