---
name: manim-video
description: Plan, write, render, and visually verify narrated Manim Community Edition animations for math and science explainers, with Chinese text, LaTeX formulas, and visuals timed to real narration audio. Use when the user asks for a Manim scene or video, a 3Blue1Brown-style explanation, an animated derivation, proof, graph, or algorithm, or a math clip to embed in a larger video. Not for ManimGL, or for general motion graphics that do not need mathematical objects.
---

# Manim Video

Turn a concept into a narrated Manim CE clip whose visuals follow the voice,
then verify the rendered frames. The agent is planner, writer, programmer and
reviewer; this skill supplies the order of work, a timed scene base, and
verified Manim facts.

## Start with the target

1. Inspect the working project. If it already has a script, TTS, alignment
   timeline, palette or visual spec, those are authoritative. The Manim clip
   is then a component, so match its resolution, frame rate and style.
2. Run `python <skill>/scripts/doctor.py` with the interpreter that will
   render. Fix missing pieces before writing code. If there is no Manim
   environment, create one in the project (`uv venv`, `uv pip install manim`).
3. Load references only as needed:
   - concept, audience and scene plan: `references/planning.md`;
   - narration timings, anchors and subtitles: `references/timing.md`;
   - any Manim code: `references/manimce-0.21.md`;
   - Chinese text or formulas: `references/cjk-and-tex.md`;
   - layout, color and motion choices: `references/visual-grammar.md`;
   - review, muxing, or embedding in another engine: `references/qa-and-handoff.md`.

## Order of work

1. **Plan.** Fix the one-sentence claim, the audience and the length, then a
   scene-by-scene plan. Verify every number and identity that will appear.
2. **Narration, then timings.** Write `lines.txt` (`id | text`) and build a
   timings file from real audio (`scripts/timings.py`, or an adapter from the
   host timeline). Estimated timings are only for layout drafts.
3. **Code.** Copy `templates/timed_scene.py` next to the scene file. Subclass
   `TimedScene`, with one class per chapter. Place beats with `say(id)`, and
   mid-sentence beats with `beat(k)` at the recorded pauses
   (`scripts/timings.py show` lists them). Give every
   animation an explicit `run_time`. Never hand-sum durations into `wait()`
   calls.
4. **Preview.** `manim -ql --dry_run`, then `manim -ql --disable_caching`.
5. **Look.** `scripts/check_frames.py` extracts frames at every segment
   boundary. Read them, fix, and re-render only the affected classes.
6. **Final.** Render at final quality, check that render's frames again, then
   assemble and mux (`scripts/assemble.py` for several chapters) or hand over
   a silent or transparent clip (embedded).

## Non-negotiables

- Timings come from real narration audio before animation code is final.
- Subtitle text comes from the script, never from speech recognition.
- An element appears no earlier than the narration that introduces it.
- Every number and formula on screen has been checked.
- Write Manim CE (`from manim import *`), not ManimGL idioms.
- Only frames from the final render count as verified. Report which renders
  and frames were actually inspected.

## Bundled resources

- `templates/timed_scene.py`: `TimedScene` (`say`, `beat`, `at`, `hold`,
  `until`, `finish`), `PALETTE`, `CJK_FONT`, `cjk_tex()`.
- `scripts/doctor.py`: toolchain check (Manim, ffmpeg, TeX, ctex, CJK font).
- `scripts/tts_gemini.py`: one narration file per line via Gemini TTS, reading
  about five minutes per request (daily request quotas, even voice), with a
  per-line voice check and an optional Batch API mode; voice choice and quota
  facts are in `references/timing.md`.
- `scripts/timings.py`: timings (with in-sentence pauses) from per-line audio,
  or text estimates; `show` prints pauses beside phrases for choosing beats.
- `scripts/check_frames.py`: boundary frames, contact sheet, duration check.
- `scripts/assemble.py`: joins chapters with aligned narration and
  sentence-level subtitles.
