# Visual grammar

Defaults, not a fixed house style. When a host project has a visual spec,
palette or motion rules, those win; match them so the clip cuts in cleanly.

## Frame and layout

The default frame is 14.2 × 8 units (16:9). Keep text at least 0.5 units from
every edge, and keep the bottom 1.2 units free when subtitles will be burned
in.

| Layout | Use |
|---|---|
| Visual centre, formula in the lower third | most explanation beats |
| Left / right split | two views of one idea, before and after |
| Title band on top, visual below | chapter openings only; do not keep a title on screen for a whole scene |
| One large statement, centred | the claim, the "aha", the conclusion |

## Color carries meaning

Assign roles once per film (see `PALETTE` in the template) and keep them:
primary object, verified result, current focus, error or counterexample,
muted context. At most two accent colors in a frame and one focus at a time.
Dim context instead of removing it: `set_opacity(0.25)` on surrounding parts
(on curves use `set_stroke(opacity=…)`).

## Motion

- **Transform, don't replace.** Carry an object into its next form
  (`TransformMatchingTex`, `ReplacementTransform`) so the viewer sees what
  became what. Fade-out/fade-in breaks that link.
- **Reveal progressively.** Build formulas term by term, each term entering
  as the narration names it, never before.
- **The camera follows the narration.** Zoom in when the voice turns to a
  detail, and always pull back to the whole before moving on. At most one
  camera move per beat.
- **Rhythm.** Quick setup moves (0.5 to 1 s), slow down for the key step
  (1.5 to 3 s), then hold still for at least 0.8 s so it can be read.
- **Restraint.** No bounce, spin-in or flash unless the content is itself a
  collision or an event. Motion that only decorates competes with the math.
- **Term tour.** To explain a formula part by part: dim the rest, color and
  frame the current part, narrate it, restore, move to the next part.

## Code on screen

Show code as an editor would, not as plain monospace text:

- Prefer real, runnable code over pseudocode, and run it (for example in the
  project's verification script) so what is on screen is known to work.
- Use Manim's `Code`: `Code(code_string=src, language="python",
  formatter_style="one-dark", background="window",
  paragraph_config={"font": "JetBrains Mono", "font_size": 24, "line_spacing": 0.85})`.
  This gives syntax colours, line numbers and window chrome. `one-dark` sits
  well on the default dark palette; dim `code.line_numbers` to about 0.45.
- Walk through it with a current-line bar: a translucent `FOCUS` rectangle
  (fill opacity about 0.13, no stroke) spanning the window, layered between
  the background and the text (`code.code_lines.set_z_index(2)`, bar at 1).
  Move it with the narration and dim the other lines to about 0.35.
- Keep lines short (about 75 characters) and the block under about 12 lines;
  `fit_width` it to about 12.6 units and check legibility on a 1080p frame.

## Endings

Close each scene on a frame that makes sense frozen: the result alone, or the
whole picture with the new piece highlighted. Hold it 1 to 1.5 s before the
transition.
