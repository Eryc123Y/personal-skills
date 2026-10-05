# Manim CE 0.21 facts and pitfalls

Each item was checked on Manim Community 0.21.0 (macOS, 2026-10-05). After a
Manim upgrade, re-check an item before relying on it. `pip show manim` gives the
installed version.

## Community Edition, not ManimGL

The two share names but not APIs. Training data and many examples mix them.

| Looks like | Is | CE equivalent |
|---|---|---|
| `from manimlib import *`, `manimgl` CLI | ManimGL | `from manim import *`, `manim` CLI |
| `self.frame.reorient(...)`, `frame.animate.reorient` | ManimGL | `ThreeDScene.move_camera(phi=, theta=)` or `MovingCameraScene` with `self.camera.frame.animate` |
| `Tex` for formulas, `t2c` everywhere | ManimGL habits | `MathTex` for math; `Tex` for LaTeX text |
| `ShowCreation` | ManimGL / old | `Create` |

## Removed or renamed

| Fails in 0.21 | Use |
|---|---|
| `FRAME_WIDTH`, `FRAME_HEIGHT` (NameError) | `config.frame_width`, `config.frame_height` |
| `Dot(opacity=0.5)`, any constructor `opacity=` (TypeError) | `fill_opacity=` / `stroke_opacity=` |
| `Axes(ticks=[])` (TypeError) | `axis_config={"include_ticks": False}` |
| `self.wait(0)` or negative waits (ValueError) | `TimedScene.until()`, which skips zero gaps |

## Behaviour that surprises

- `mob.set_opacity(x)` also sets **fill** opacity. On a plotted curve
  (fill 0 by default) this fills the closed path. To dim a curve, use
  `curve.set_stroke(opacity=x)`.
- `axes.plot(f)` smooths through samples. For step, square or other
  discontinuous functions pass `use_smoothing=False` (forwarded to
  `ParametricFunction`), plus `discontinuities=[...]` where the function jumps.
- Animations are rounded to whole frames (see timing.md). Low-quality previews
  (15 fps) and finals (60 fps) differ by up to one frame per animation.
- A crashed render leaves `partial_movie_files/`. Locate outputs by their exact
  path `media/videos/<file>/<quality>/<Scene>.mp4`, never by globbing `*.mp4`.
- `--disable_caching` avoids stale partials while iterating on one scene.

## Rendering commands

```bash
manim -ql scene.py Taylor           # 480p15 preview
manim -qh scene.py Taylor           # 1080p60 final
manim -qk scene.py Taylor           # 2160p60
manim -ql -s scene.py Taylor        # last frame only, as PNG
manim -qh -t scene.py Taylor        # transparent background -> .mov (qtrle, argb)
manim -ql --dry_run scene.py Taylor # runs construct without writing video (fast API check)
```

Quality flags set resolution and frame rate. Override with
`--resolution 1920,1080 --frame_rate 30` when the host film uses 30 fps.

## Patterns that work

- `TransformMatchingTex(a, b)` for algebra steps. Split formulas into
  substrings (`MathTex(r"f(x)", "=", r"x^2")`) so parts can be colored and
  matched.
- `ValueTracker` plus `always_redraw` for anything driven by a parameter
  (a tangent line, a moving point, an area). Animate the tracker, not the
  drawing.
- `VGroup(...).arrange(DOWN, aligned_edge=LEFT, buff=0.3)` for derivations.
- Fix pseudo-random layouts with `np.random.default_rng(seed)`.
- 3D: `ThreeDScene`; set the camera with `set_camera_orientation`, move it only
  with `move_camera`; keep text readable with `add_fixed_in_frame_mobjects`.
