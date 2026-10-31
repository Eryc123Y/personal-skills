# Style guide

Adapted from the design notes of [figures4papers](https://github.com/ChenLiu-1996/figures4papers) (Chen Liu, CC BY-NC 4.0); see `../SOURCE.md` for what was changed.

## House style kept from figures4papers

- Minimal axes: no top or right spine, frameless legend, no grid unless reading exact values needs one.
- Sans-serif type (Arial, then Helvetica, then DejaVu Sans).
- One semantic palette:
  - `blue_main` / `blue_secondary` for the proposed method or key result;
  - greens for variants or improvements;
  - reds and pinks for baselines and contrasts;
  - `neutral` for reference or background.
- One highlight colour, used for one callout only.
- Black bar edges and hatches, so bars that differ only by hue still separate in grayscale print.
- For ablations, one hue with different hatches (or alpha) to show how complete each variant is.
- A dedicated legend panel when several panels share series.
- Limited curves per axis, with `fill_between` bands for uncertainty.

## Local changes and why

| Upstream habit | Here | Reason |
|---|---|---|
| Very large canvases (for example 45×12 in at 24 pt) scaled down in LaTeX | Canvas = column width (`figure_size`) at 8 pt | Scaling makes font sizes differ from figure to figure; at true size every figure matches the body text |
| `svg.fonttype = none` only | `pdf.fonttype = 42` as well | ACM and IEEE checks reject Type 3 fonts; TrueType embeds cleanly |
| y-limits tightened around the data, including for bars | Bars from zero; tighten line plots only | A truncated bar baseline exaggerates differences |
| `tight_layout(pad=2)` | Constrained layout | Long y-labels on neighbouring panels no longer collide |
| No error-bar helper | `errors=` on bars, `bands=` on trends | Seeds, raters and confidence intervals are standard in our results |
| — | `CB_SAFE_COLORS` (Okabe-Ito) | For more than four series, or when red and green must be told apart |

## Patterns by research need

| Need | Figure | Notes |
|---|---|---|
| Method vs baselines over a control (strength, budget, size) | `make_trend` with bands, one panel per metric, plus a legend panel | Shade the operating point with `axvspan`. Give every method the same x points |
| Ablation | `make_grouped_bar` with hatches and CI errors | Put the full method first; variants share its hue family |
| Preference / A/B results | Bars of win rate with 95% CI, plus a 0.5 reference line | Say how ties are counted and what unit the CI is over (raters or clips) |
| Breakdown by scene or condition | `make_heatmap(annotate=True)` | Use `viridis` for sequential data. For a diverging metric pass a diverging cmap and set `vmin`/`vmax` symmetric |
| Convergence and complexity (numerics) | `make_trend` plus log-log axes and dashed reference slopes | Label the slopes; put the error norm in the axis label |
| Distributions across seeds or clips | Box or violin via plain matplotlib, styled by `apply_publication_style` | More honest than a mean alone |

## Captions

State the data, the error-bar meaning, the number of seeds, clips or raters, and any axis truncation. Tag numbers that come from another paper.
