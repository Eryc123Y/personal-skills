# Timing: narration first, then code

Visual timing is derived from real narration audio. Writing animations against
guessed durations is the most common cause of audio/visual drift and full
re-renders.

## The timings file

One JSON file per clip. Times are seconds from the clip's first frame.

```json
{
  "clip": "taylor",
  "audio": "taylor.wav",
  "duration": 41.2,
  "segments": [
    {"id": "hook", "text": "用一个多项式，吻住一条曲线。", "start": 0.0, "end": 3.4, "pauses": [[1.21, 1.52]]},
    {"id": "map",  "text": "只要知道函数在一点的信息……", "start": 3.75, "end": 9.1}
  ]
}
```

- `id` is stable and meaningful (`hook`, `derive_2`, `remainder`), so scene
  code survives re-recording. `text` is the subtitle and must come from the
  script, never from speech recognition, which garbles terminology.
- `start`/`end` are when the voice is actually speaking; `duration` adds a tail.
- `pauses` (written by `timings.py audio`) are silences inside the line, in
  seconds from the line's start; they mark phrase boundaries.
- `"estimated": true` marks draft timings. Never ship a render cut to them.

## Getting timings

Prefer what the host project already has:

1. **Host project timeline.** If the project has its own TTS and alignment
   (for example an `audio/timeline.json` with scenes, lines and cues), write a
   ten-line adapter that slices one scene into this format, subtracting the
   scene's start time. Do not run a second TTS.
2. **One audio file per line.** `scripts/timings.py audio lines.txt --audio-dir voice/ -o timings/<clip>.json`
   measures each file and writes the concatenated `<clip>.wav`.
3. **No audio yet.** `scripts/timings.py estimate lines.txt -o timings/<clip>.json`
   gives draft timings (about 4.2 Chinese characters per second) for layout
   work. Replace them with real audio before the final render.

## Choosing a voice

Use the first option that applies; none of these needs a GPU.

| Option | When | How |
|---|---|---|
| Host project's narration | the clip belongs to a film that already has a voice | reuse its pipeline and timeline; never mix two voices in one film |
| Gemini 3.8 TTS (`gemini-3.8-flash-lite-tts`, or `gemini-3.8-flash-tts` for more nuance) | default for finished narration, Chinese or English; needs `GEMINI_API_KEY` | `python <skill>/scripts/tts_gemini.py lines.txt voice/` then `timings.py audio`. Set `VOICE` (default `Charon`) and `STYLE` (delivery instruction). Verified 2026-10-05: 18/18 English lines first try |
| edge-tts | drafts without a key, or when the API is unavailable | `uvx edge-tts --voice en-US-AndrewNeural` / `zh-CN-YunxiNeural --text "..." --write-media NN_id.mp3` per line |

Pace: Gemini's Charon voice reads English at about 120–125 words per minute,
calmer than many explainers. For a brisker read, ask for it in `STYLE`, or
speed every line up uniformly with `ffmpeg -af atempo=1.1` (pitch preserved;
about 135 wpm) before running `timings.py audio`. Decide the pace before
writing beats, and tell the user if you change it.

Write numbers, symbols and formulas in lines.txt the way they should be
spoken ("one point five seven", "h squared"), not as digits or LaTeX. Read
every number on screen against the narration that names it.

A local or GPU model (for example a larger open TTS on Colab) is only worth
it when the API voices are unsuitable; load the model once and synthesise
every line in the same process.

When narration changes, regenerate timings first, then update the code.
Segment ids that still exist keep their scene code.

## Anchoring animations in code

`templates/timed_scene.py` provides `TimedScene`:

| Call | Effect |
|---|---|
| `self.say("id")` | holds until the segment starts, then attaches its subtitle |
| `self.beat(k)` | holds until pause `k` of the current segment ends, when its next phrase starts |
| `self.at(2.4)` | holds until 2.4 s into the current segment (when no pause fits) |
| `self.hold("id")` | holds until the segment ends |
| `self.until(t)` | holds until clip time `t` |
| `self.finish()` | holds until the clip's `duration` |
| `self.clock` | seconds since the clip started |

Write animations between anchors with explicit `run_time`s. Do not sum
run_times by hand and compute `wait(budget - spent)`:

- Manim rounds every animation to whole frames, so `run_time=0.7` lasts
  0.733 s at 15 fps and 0.700 s at 60 fps. Hand-written budgets drift
  differently in the preview and final renders.
- `self.wait(0)` or a negative wait raises `ValueError` in Manim 0.21.
- Anchors absorb the rounding. An anchor that is already overdue by more than
  one preview frame calls `on_overrun`: previews (`-ql`, `-qm`) log a warning
  and keep going, so one render lists every late beat; final renders raise
  when a beat is more than `OVERRUN_LIMIT` (0.3 s) late. `finish()` logs a
  summary of all late beats.

Placing beats inside a sentence: a phrase starts at the end of a pause, so put
`self.beat(k)` before the animation that shows what that phrase names.
`python <skill>/scripts/timings.py show timings/<clip>.json` lists each line's
speech spans, labelled `beat(k)`, next to its phrases. Prefer `beat(k)` to
`at(seconds)`: pause indices survive re-recording or a tempo change, hard-coded
offsets do not. A segment-level anchor alone lets an element appear seconds
before its word is spoken; checking beats against pauses caught about twenty
early beats in a 2.5-minute clip.

Fitting a beat into its segment: the animations between two anchors must fit
in the time available. Trim `run_time`s or move a beat to the next segment.
Do not speed the narration up to fit the visuals.

## Subtitles

`say()` calls `add_subcaption`, so Manim writes `<Scene>.srt` next to the
video, one cue per narration line; that is fine for previews. For delivery,
`scripts/assemble.py` writes the film's subtitles from the timings text,
split into sentences and clauses of at most 90 characters. Burn subtitles in only at the final mux, and only if the delivery needs
it (`ffmpeg -vf subtitles=Scene.srt`). Never draw subtitles as mobjects; they
then cannot be edited, translated or turned off.

## Multi-scene films

Use one `TimedScene` subclass per chapter, each with its own lines file,
narration audio and timings file. Each class renders to its own file and can
be re-rendered alone.

To join them, list `<video> <timings.json>` per chapter in order in a text
file and run `python <skill>/scripts/assemble.py chapters.txt -o film.mp4`. It
pads each chapter's narration to that chapter's measured video length before
concatenating (a chapter's picture runs longer than its voice by the tail and
frame rounding; plain concatenation drifts more with every chapter), muxes the
narration, writes the subtitles, and prints the film, narration and summed
chapter durations, which must agree.
