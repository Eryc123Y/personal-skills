# Chinese text and LaTeX

## Which object for which content

| Content | Object | Notes |
|---|---|---|
| Chinese prose, titles, labels | `Text("…", font=CJK_FONT)` | Pango; set the font explicitly so Chinese never falls back to boxes |
| Math | `MathTex(r"…")` | default LaTeX template |
| Math containing Chinese | `MathTex(r"\text{余项}~R_N(x)", tex_template=cjk_tex())` | XeLaTeX + ctex |
| A sentence with inline math | `VGroup(Text(...), MathTex(...)).arrange(RIGHT, buff=0.12)` | align on the baseline by eye; check the frame |

`CJK_FONT` and `cjk_tex()` live in `templates/timed_scene.py`. On macOS,
`PingFang SC` is present; Linux typically has `Noto Sans CJK SC`.

## Pitfalls

- Inside `\text{}` under ctex, a space after a Chinese character is dropped:
  `\text{余项 }R` renders as 余项R. Use `~` or `\,`.
- Chinese inside `MathTex` without `cjk_tex()` fails to compile or drops
  characters. Pass the template to each object; do not change the global
  default, which slows every formula.
- `Text` measures in Manim units. Long lines overflow silently, so cap
  widths: `t.set(width=min(t.width, config.frame_width - 1.5))`.
- Pango spacing for Latin text is uneven. For English prose next to math,
  `Tex` often looks better than `Text`.
- `DecimalNumber` and `Integer` render through LaTeX. Without TeX, format
  numbers with `Text(f"{v:.2f}")`.

## Without LaTeX

If `scripts/doctor.py` reports no TeX and installing it is not an option, use
Unicode math in `Text` (x², √, ∑, ∫, ≈, →) for short expressions. Do not
attempt fractions, matrices or multi-line derivations this way; say that the
video needs TeX for them.
