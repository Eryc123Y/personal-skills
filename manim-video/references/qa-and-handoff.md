# Review and hand-off

## Review loop

1. `manim -ql --dry_run scene.py Clip` catches API errors and overruns
   without encoding video.
2. `manim -ql --disable_caching scene.py Clip` gives a 480p15 preview.
3. Choose frame extraction for the confirmed mode:
   - With segment timings: `python <skill>/scripts/check_frames.py Clip.mp4 timings/clip.json -o check/clip`.
   - Without timings: `python <skill>/scripts/check_frames.py Clip.mp4 -o check/clip --at 0 2 4`.
     Choose timestamps within the actual clip at meaningful visual changes;
     no timing file or audio track is required.
   Then **look at** `contact.png` and the extracted frames:
   - `<id>_in` for synchronized work: nothing introduced later by the narration or host cues appears prematurely.
   - `<id>_out`: the segment's intended result is on screen and legible.
   - `at_*` for silent work: the planned visual state is present and legible.
     Inspect loop wraparound playback when relevant; stills cannot prove continuity.
   - Overflow past the frame, overlaps, a subtitle zone covering labels,
     colors that break their roles, unreadable small text.
4. Fix, then re-render only the affected scene classes.
5. Render the final at `-qh` (or the host's resolution and fps) and run
   `check_frames.py` on that file too. The final render is the only thing
   that counts as checked; a clean preview does not prove the final is clean.

Report what was looked at: "frames checked at every segment boundary of the
1080p60 render" is a claim; "lint passed" is not a visual review.

## Standalone delivery

For a silent animation, deliver the rendered video in the requested format.
Do not require a voice track or subtitles. Check its measured duration against
the requested length. The commands below apply only to narrated delivery:

```bash
ffmpeg -y -f concat -safe 0 -i chapters.txt -c copy picture.mp4      # several scene files, in order
ffmpeg -y -i picture.mp4 -i timings/clip.wav -map 0:v -map 1:a \
       -c:v copy -c:a aac -b:a 192k -movflags +faststart final.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4  # ≈ timings duration
```

Do not pass `-shortest` when the picture deliberately holds after the voice
ends. Keep `<Scene>.srt` as a sidecar; burn it in only if the platform needs
that.

## Clip inside a larger film

- Render at the host's resolution and frame rate
  (`--resolution 1920,1080 --frame_rate 30`).
- Match the host palette and fonts; ask the host project for its tokens.
- Use the host's timeline for the segment times (timing.md, option 1) and let
  the host own the narration audio. Deliver a silent picture.
- Transparent overlay: `manim -qh -t` writes `.mov` (qtrle, argb). Composite
  it with `ffmpeg -i bg.mp4 -i clip.mov -filter_complex overlay`. In an HTML
  engine, convert to WebM with alpha (`-c:v libvpx-vp9 -pix_fmt yuva420p`)
  or to a PNG sequence when the engine seeks frame by frame.
- Run the host's own QA on the composited result as well.
