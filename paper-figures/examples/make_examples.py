"""Render example figures with synthetic data (not research results).

Run from the skill folder:
    uv run --no-project --with matplotlib --with numpy python examples/make_examples.py
Outputs go to examples/out/ (not tracked).
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import paperfig as pf  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
rng = np.random.default_rng(0)


def quality_vs_strength() -> None:
    """Two-panel double-column figure: metric curves over stereo strength, legend panel."""
    strength = np.array([0.0, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
    fig, axes = pf.create_subplots(1, 3, figsize=pf.figure_size("acm", "double", aspect=0.27),
                                   gridspec_kw={"width_ratios": [1, 1, 0.45]})
    methods = ["Ours", "Disparity scaling", "Diffusion baseline"]
    for ax, (ylabel, sign) in zip(axes[:2], [("LPIPS (lower is better)", 1), ("No-reference score", -1)]):
        series, bands = [], []
        for k in range(len(methods)):
            y = 0.08 + 0.05 * k + sign * 0.06 * strength**1.3 + rng.normal(0, 0.004, strength.size)
            series.append(y)
            bands.append((y - 0.01, y + 0.01))
        pf.make_trend(ax, strength, series, methods, bands=bands, markers=["o", "s", "^"],
                      xlabel="Stereo strength", ylabel=ylabel)
        ax.axvspan(0.55, 0.65, color=pf.PALETTE["neutral"], alpha=0.4, linewidth=0)
    pf.legend_panel(axes[2], axes[:2])
    pf.finalize_figure(fig, OUT / "quality_vs_strength")


def ablation_bars() -> None:
    """Single-column grouped bars with 95% CI error bars and hatches for grayscale print."""
    fig, (ax,) = pf.create_subplots(figsize=pf.figure_size("acm", "single", aspect=0.7))
    cats = ["Animation", "Indoor", "Outdoor"]
    values = [[0.71, 0.66, 0.69], [0.64, 0.61, 0.60], [0.58, 0.55, 0.57]]
    errors = [[0.03, 0.04, 0.03], [0.03, 0.03, 0.04], [0.04, 0.03, 0.03]]
    colors = [pf.PALETTE["blue_main"], pf.PALETTE["green_3"], pf.PALETTE["red_2"]]
    pf.make_grouped_bar(ax, cats, values, ["Full", "No gate", "Uniform"], ylabel="SIoU",
                        colors=colors, errors=errors, hatches=["", "//", "\\\\"])
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    pf.finalize_figure(fig, OUT / "ablation_bars")


def convergence_loglog() -> None:
    """Numerical-analysis style: error vs step size on log-log axes with reference slopes."""
    h = np.logspace(-3, -1, 8)
    fig, (ax,) = pf.create_subplots(figsize=pf.figure_size("acm", "single", aspect=0.75))
    errs = [0.8 * h, 2.0 * h**2 * (1 + rng.normal(0, 0.05, h.size)), 5.0 * h**4]
    pf.make_trend(ax, h, errs, ["Euler", "Heun", "RK4"], markers=["o", "s", "^"],
                  xlabel="Step size $h$", ylabel="Global error")
    ax.set_xscale("log")
    ax.set_yscale("log")
    for err, order in zip(errs, (1, 2, 4)):
        ref = 0.25 * err[-1] * (h[-3:] / h[-1]) ** order
        ax.plot(h[-3:], ref, color="black", linewidth=0.6, linestyle="--")
        ax.annotate(f"slope {order}", (h[-3], ref[0]), textcoords="offset points", xytext=(-4, -2),
                    ha="right", va="top", fontsize=6)
    ax.legend()
    pf.finalize_figure(fig, OUT / "convergence_loglog")


def heatmap() -> None:
    fig, (ax,) = pf.create_subplots(figsize=pf.figure_size("acm", "single", aspect=0.8))
    mat = np.clip(rng.normal(0.6, 0.15, (4, 5)), 0, 1)
    pf.make_heatmap(ax, mat, x_labels=[f"s={s}" for s in (0.4, 0.6, 0.8, 1.0, 1.4)],
                    y_labels=["Static", "Slow", "Fast", "Cuts"], cmap="viridis",
                    cbar_label="Win rate", annotate=True)
    pf.finalize_figure(fig, OUT / "heatmap")


if __name__ == "__main__":
    pf.apply_publication_style()
    quality_vs_strength()
    ablation_bars()
    convergence_loglog()
    heatmap()
    print("\n".join(sorted(p.name for p in OUT.iterdir())))
