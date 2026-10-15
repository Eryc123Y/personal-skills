# ManimGX

ManimGX (academa-labs/manimgx) is a Rust and wgpu engine with Manim CE's authoring API. Notes checked on
v0.1.1 (2026-10-15), Apple M4, against Manim CE 0.21. Its own docs: <https://manimgx.academa.ai/reference/> and the
agent primer <https://manimgx.academa.ai/llms.txt>.

## When to use it

- Choose ManimGX for real 3-D (lit surfaces, materials, a turning scene), for fast renders, or when the project
  already uses it. Ordinary 2-D scenes rendered 14–25× faster than CE in our trial; the last frames of 56
  scenes took 5 s instead of 238 s (CE with a cold TeX cache; 26 s warm).
- Stay on CE when the host project renders with CE (reuse its engine), or the scene needs `MarkupText` (Pango
  markup), a LaTeX package or TeX template mitex cannot convert, or exact CE typography.
- Scenes that rebuild thousands of shapes in Python every frame gain little (one was slower than on CE): write
  them as real 3-D objects or as geometry derived from a `ValueTracker` first.

## Install

- Python 3.13 or newer; Typst, mitex, fonts (CJK included) and the video encoder come with the package, no TeX.
- Its own environment, version pinned (upgrades change behaviour):
  `uv venv .venv-gx -p 3.14 && uv pip install --python .venv-gx/bin/python manimgx==0.1.1`
- Licence: source MIT; the wheels include x264 and are GPL as a whole. Rendered videos are not affected.
- The GPU worked inside Claude Code's macOS sandbox without extra permissions.

## Write

- `import manimgx as m`; `m.Scene`, `m.ThreeDScene`; `play`, `wait`, `add` as in CE.
- Narration timing: `templates/timed_scene_gx.py` (same timings file and calls as `timed_scene.py`; clip time is
  `self.now`).
- Names the Scene owns, which a subclass must not define: `clock`, `_recording` (a method), `_events` (a dict).
  Read the time with `float(self.time)`.
- Missing names: `MarkupText`, `tempconfig`, `TexTemplate`, the `rate_functions` module (the functions are at top
  level: `m.smooth`, `m.ease_in_out_sine`).

## Text and formulas

- `MathTex` and `Tex` take LaTeX; mitex converts it to Typst. Differences seen on 6038 formulas (99.9 % set as
  is): subscripts sit a little lower; `\ldots` and `\ ` are a little tighter; a thousands separator `10{,}987`
  gets a space after the comma, so write `\mathord{,}`.
- Chinese inside a formula needs a CJK fallback font for the maths: pass
  `typst_preamble='#show math.equation: set text(font: ("New Computer Modern Math", "PingFang SC"))'`.
- A line of Chinese with formulas is one `m.Typst` run, not a ctex `MathTex`: `mix_line()` in the template.
- Sizes at one `font_size`: `MathTex` and `DecimalNumber` match CE; `Text` is about 6 % smaller in PingFang SC
  and 8 % in a monospace font; a mixed line about 5 % smaller than CE's ctex line. Scale by these factors when
  one project mixes engines.

## Time and motion

- Updaters that take `dt` run at `config.simulation_rate` (60 a second by default), whatever the frame rate: at
  30 fps each runs twice a frame. When updaters read the time rather than `dt`, set
  `m.config.simulation_rate = m.config.frame_rate`.
- Clips are variable frame rate: a frame the picture holds is written once and shown longer. Before joining
  ManimGX clips with constant-rate ones in ffmpeg's concat, re-encode them:
  `ffmpeg -i in.mp4 -vf fps=30 -c:v libx264 -crf 18 -pix_fmt yuv420p -video_track_timescale 15360 out.mp4`
  (15360 is CE's time base). Otherwise the join loses their length. Frame grabs: use `-vf fps=30`, not `-ss`.
- A clip comes out a frame or two longer than its timeline; mux by measured length.

## Three dimensions

- `ThreeDScene.set_camera_orientation(phi=..., theta=..., frame_center=[...])`; text that explains goes in with
  `add_fixed_in_frame_mobjects`.
- Light: `m.SunLight(direction, intensity=1.5, shadows=False)` and `m.AmbientLight(intensity=0.3)`. Turn
  shadows off when labels stand over a surface (they cast them on it).
- Surface: `m.Surface(f, u_range, v_range, resolution=(84, 50))`,
  `.set_fill_by_value(axes, colorscale=[(dark, z0), (light, z1)])`, `.set_material(m.Material(roughness=0.65,
  reflectance=0.35))` for a matte look on a dark background.
- Labels in the scene: stand them upright (`.rotate(PI / 2, axis=RIGHT)`) and move them with the turn in an
  updater. Labels lying flat on the floor read upside down halfway round.
- To keep a layout (figure left, text right), keep the camera still and turn the objects about their own
  vertical axis.

## Check and render

- Still frame: `scene.render(frames=lambda f: last.__setitem__(0, f.pixels()))`, then
  `PIL.Image.frombytes("RGBA", (m.config.pixel_width, m.config.pixel_height), last[0])`. There is no `-s`.
- `manimgx inspect scene.py Cls` writes a storyboard and flags sampled 2-D layout problems. It is generic: it
  also flags intended designs (a title on a card border, a highlight band behind text), and 3-D scenes get only
  the storyboard. A project's own layout check wins; look at full-size frames either way.
- `manimgx render scene.py Cls -r 1280x720 --fps 30 -o draft.mp4`; the default is 1920×1080 at 60 fps. It writes
  the storyboard and, with captions, an `.srt` beside the video.

## Projects using both engines

numerics (`~/Movies/video-projects/numerics`) picks the engine per slide (`engine="gx"`): a compatibility layer
`shared/gx/manim` gives the series' CE code ManimGX, with the font factors, mitex fixes and time names above;
see its `shared/deck/README.md`.
