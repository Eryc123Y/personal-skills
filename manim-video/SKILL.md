---
name: manim-video
description: Plan, write, render, and visually verify Manim Community Edition or ManimGX animations for math and science, including narrated explainers, silent animations, and clips embedded in existing videos. Use for a requested Manim or ManimGX scene, a 3Blue1Brown-style explanation, animated formulas, proofs, graphs, algorithms, or lit 3-D math surfaces. Clarify unresolved narration and integration needs before choosing the workflow. Not for ManimGL or general motion graphics without mathematical objects.
---

# Manim Video

Make the requested Manim animation (Manim CE, or ManimGX where it fits) and verify its rendered frames. Choose
narration, timing, and delivery steps from the user's requirements and the
existing project; a video request does not by itself require speech.

## Confirm the task before choosing the workflow

Read the request and relevant project files first. Reuse requirements already
specified or confirmed. If the choice is still unclear, ask one concise question
covering the material gaps before generating speech or committing to a timing
workflow:

- Is this a narrated explainer, a silent standalone animation, or a clip for an
  existing video?
- Is there existing narration or a timeline to follow? For an embedded clip,
  which project and time interval own it?
- What length and output are needed, if those materially affect the work (for
  example a loop, transparency, aspect ratio, or narration language)?

For example: "这次要带旁白的完整视频、独立无声动画，还是嵌入已有视频的片段？
如果有现成音频或时间线，我会沿用；预计多长、需要什么输出格式？"
Ask only the unanswered parts. An explicit "8-second silent loop" already
settles narration and duration; do not ask again or invent a speech requirement.
While awaiting a material answer, inspect the project and plan reusable visual
content, but leave dependent speech, timing, and final rendering decisions open.

| Task | Timing source and workflow |
|---|---|
| Narrated explainer | Existing or requested narration; align final visuals to real audio |
| Silent standalone animation | Requested duration and visual pacing; no speech, transcript, or subtitle prerequisite |
| Clip in an existing video | Host timeline and format; a silent export can still need exact narration synchronization |

## Establish the project

- Existing scripts, audio, timeline, palette, and visual specification govern an
  embedded clip. Match the host's resolution, frame rate, and style; reuse its
  engine and narration pipeline rather than creating another one.
- Choose the engine. The host project's engine wins. Otherwise Manim CE by default; ManimGX (GPU, CE's API,
  no TeX) for lit 3-D surfaces, long renders, or when the user asks for it. Stay on CE for `MarkupText`, custom
  TeX templates, or exact CE typography. Differences that matter: [ManimGX](references/manimgx.md).
- Run `python <skill>/scripts/doctor.py` (`--engine gx` for ManimGX) with the rendering interpreter. Resolve
  dependencies actually required by this clip; a silent scene does not need TTS,
  and a scene without TeX does not require TeX just to satisfy the checker. Reuse
  the project environment, or create a project-local Manim environment if needed.
- Read references only when relevant: [planning](references/planning.md),
  [narration timing](references/timing.md), [Manim code](references/manimce-0.21.md),
  [Chinese and formulas](references/cjk-and-tex.md),
  [visual design](references/visual-grammar.md),
  [review and delivery](references/qa-and-handoff.md), and [ManimGX](references/manimgx.md).

## Plan, code, and render

1. **Plan.** Establish the intended explanation or visual behavior, audience, and
   duration. Verify the numbers and identities that will appear. A short loop
   needs only a proportionate plan, not a narrated chapter structure.
2. **Set timing for the chosen mode.**
   - Narrated: prepare or reuse `lines.txt` and real audio; check the voice, then
     build timings with `scripts/timings.py` or adapt the host timeline. Estimated
     speech timings are for drafts, not final synchronization.
   - Silent: set animation durations and pauses from the requested visual effect.
     Do not generate audio, dummy narration, or a timing file solely to proceed.
   - Embedded: use the host's cues, whether they come from speech or editing.
     Deliver audio only if requested; do not regenerate an existing voice track.
3. **Code.** Give animations explicit `run_time`s. Use ordinary Manim `Scene` for
   an independent silent animation. Use `templates/timed_scene.py` when segment
   anchors are useful: `say(id)`, `beat(k)`, and `until(t)` follow the timeline
   without hand-summing durations. Keep `TimedScene`'s required timing file; it
   is a specialized template, not a mandatory base for every animation. On
   ManimGX use `templates/timed_scene_gx.py` (same calls; clip time is `now`).
4. **Preview.** `manim -ql --dry_run`, then `manim -ql --disable_caching`. On
   ManimGX: `manimgx inspect`, then `manimgx render -r 1280x720 --fps 30`.
5. **Inspect.** With segment timings, `scripts/check_frames.py` extracts boundary
   frames. Without timings, pass explicit `--at` timestamps for key visual states.
   Read the frames, correct defects, and re-render affected classes. For loops,
   inspect the wraparound motion as well as still frames.
6. **Deliver.** Render at final quality and inspect that output. For narrated
   chapters, assemble and mux when needed. For silent clips, deliver the requested
   video or transparent overlay without adding speech or subtitles.

## Verification boundaries

- In narration-synchronized work, finalize timings from real audio and align
  newly introduced elements to the speech or agreed host cues. These conditions
  do not require narration in an intentionally silent animation.
- When subtitles are requested, their text comes from the script, not a raw
  speech-recognition transcript.
- Check every number and formula, use Manim CE (or ManimGX) rather than ManimGL idioms, and
  inspect the final render. Report the actual frames or playback reviewed;
  extracting images alone is not visual verification.

## Bundled resources

- `templates/timed_scene.py`: segment-anchored `TimedScene`, `PALETTE`,
  `CJK_FONT`, and `cjk_tex()`; optional for silent standalone scenes.
- `templates/timed_scene_gx.py`: the same for ManimGX, with `mix_line()` for
  Chinese lines with formulas (Typst and mitex instead of ctex).
- `scripts/doctor.py`: local rendering-tool check (`--engine gx`: ManimGX and a GPU test render).
- `scripts/check_frames.py`: boundary or explicit-time frames and contact sheet;
  compares durations when a timing file is provided.
- Narrated workflows only: `scripts/tts_gemini.py`, `scripts/verify_voice.py`,
  `scripts/timings.py`, and `scripts/assemble.py`. See the timing reference for
  their current invocation and voice options; do not call them merely because
  this skill was selected.
