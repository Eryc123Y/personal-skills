---
name: paper-figures
description: >-
  Make publication-quality matplotlib data figures for papers, theses, reports
  and slides (grouped/ablation bars with error bars, trend and convergence
  curves with bands, heatmaps, scatter, multi-panel with a legend panel), sized
  at true column width with embedded TrueType fonts. Use when writing or
  revising plotting code for a paper/report figure, or when asked to match
  Eric's paper figure style. Not for web/artifact charts or dashboards
  (dataviz), pipeline or architecture diagrams (d2-diagram), or mathematical
  illustrations (Typst CeTZ/Fletcher, manim-video).
---

# Paper figures

This skill uses `scripts/paperfig.py`, a small helper module.

## Workflow

1. **Decide what the figure must show.** Fix the figure's claim, its panels, and which method is "ours" before writing code. When a figure's type or layout is not yet decided, use `figure-designer` first.
2. **Vendor the helper.** Copy `scripts/paperfig.py` into the project, for example `figures/paperfig.py`, so later edits to this skill do not silently change published figures. Reuse an existing copy if the project already has one.
3. **Write one script per figure.** Load the data from the experiment's results files. Never hard-code numbers that exist in a results file. Then:
   - call `apply_publication_style()` once (`SLIDE_STYLE` for slides);
   - take the canvas from `figure_size(venue, "single"|"double", aspect)`;
   - draw with the helpers;
   - save with `finalize_figure(fig, "figures/<name>")`, which writes PDF for the paper and PNG for preview.
4. **Look at the PNG before reporting.** Check that labels do not collide, the legend does not cover data, text is readable at print size, and the colours separate in grayscale where it matters. Run `pdffonts` on the PDF and confirm there are no Type 3 fonts.

## Helpers

| Helper | Use |
|---|---|
| `figure_size(venue, span, aspect)` | True print size. Venues: acm, ieee, cvpr, icml, neurips, a4, slide |
| `create_subplots(nrows, ncols, figsize)` | Constrained layout; returns a flat array of axes |
| `make_grouped_bar(..., errors=, hatches=, annotate=)` | Comparisons and ablations; errors are CI half-widths |
| `make_trend(..., bands=, markers=)` | Curves over a sweep or training, with uncertainty bands |
| `make_heatmap(..., annotate=)` | Matrices and grouped win rates |
| `make_scatter` | One scatter series |
| `legend_panel(ax, source_axes)` | A shared legend in its own panel for multi-panel figures |
| `annotate_bars` | Value labels on bars |
| `PALETTE`, `DEFAULT_COLORS`, `CB_SAFE_COLORS`, `HATCHES` | Semantic colours: blue for ours, green for variants, red for baselines, neutral for reference; Okabe-Ito when there are many series |

## Rules

- Bars start at zero. Set `ylim` only for a stated reason, and note the truncation in the caption.
- Report uncertainty whenever repeated runs or raters exist, and say in the caption what the error bar is (95% CI, std, number of seeds).
- Use at most four curves per axis. Keep a colour meaning the same method across every figure in the paper.
- Run headless with `matplotlib.use("Agg")` before importing pyplot. When no environment is set up: `uv run --no-project --with matplotlib --with numpy python <script>`.
- Ask before finalising when the panel count, method colours or data layout are ambiguous in a way that would change the figure.

Design rationale and patterns: [references/style-guide.md](references/style-guide.md). Rendered examples: `examples/make_examples.py`.
