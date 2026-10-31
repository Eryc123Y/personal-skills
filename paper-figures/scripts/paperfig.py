"""Publication-style matplotlib helpers for paper, report, and slide figures.

Copy this file into a project (for example ``figures/paperfig.py``) so that
figures stay reproducible even if the skill changes later.

Design rules follow the figures4papers house style (semantic blue/green/red
palette, open spines, frameless legends) with three local changes: figures are
sized at true print width, PDF fonts are embedded as TrueType, and bar axes
start at zero unless a limit is set explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure

PALETTE: dict[str, str] = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "neutral_dark": "#767676",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}

DEFAULT_COLORS: tuple[str, ...] = (
    PALETTE["blue_main"],
    PALETTE["green_3"],
    PALETTE["red_strong"],
    PALETTE["teal"],
    PALETTE["violet"],
    PALETTE["neutral_dark"],
)

# Okabe-Ito order, for figures where many series must stay distinct for
# colour-blind readers.
CB_SAFE_COLORS: tuple[str, ...] = (
    "#0072B2",
    "#E69F00",
    "#009E73",
    "#D55E00",
    "#CC79A7",
    "#56B4E9",
    "#F0E442",
    "#000000",
)

HATCHES: tuple[str, ...] = ("", "//", "\\\\", "..", "xx", "--")

# Text-block widths in inches for common venues: (single column, full width).
COLUMN_WIDTHS_IN: dict[str, tuple[float, float]] = {
    "acm": (3.33, 7.00),
    "ieee": (3.50, 7.16),
    "cvpr": (3.25, 6.875),
    "neurips": (5.50, 5.50),
    "icml": (3.25, 6.75),
    "a4": (6.30, 6.30),
    "slide": (11.0, 11.0),
}

SAVE_FORMATS = frozenset({"pdf", "svg", "eps", "png", "jpg", "jpeg", "tif", "tiff"})


@dataclass(frozen=True)
class FigureStyle:
    """Typography and line weights; defaults suit a figure printed at true size."""

    font_size: float = 8.0
    axes_linewidth: float = 0.8
    line_width: float = 1.5
    use_tex: bool = False
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")


PAPER_STYLE = FigureStyle()
SLIDE_STYLE = FigureStyle(font_size=16.0, axes_linewidth=1.6, line_width=2.5)


def apply_publication_style(style: FigureStyle | None = None) -> FigureStyle:
    """Set rcParams for publication figures and return the style used."""
    style = style or PAPER_STYLE
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": list(style.font_family),
            "font.size": style.font_size,
            "axes.titlesize": style.font_size,
            "axes.labelsize": style.font_size,
            "xtick.labelsize": style.font_size * 0.9,
            "ytick.labelsize": style.font_size * 0.9,
            "legend.fontsize": style.font_size * 0.9,
            "axes.linewidth": style.axes_linewidth,
            "xtick.major.width": style.axes_linewidth,
            "ytick.major.width": style.axes_linewidth,
            "lines.linewidth": style.line_width,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "axes.prop_cycle": matplotlib.cycler(color=list(DEFAULT_COLORS)),
            "text.usetex": style.use_tex,
            "mathtext.fontset": "custom",
            "mathtext.rm": style.font_family[0],
            "mathtext.it": f"{style.font_family[0]}:italic",
            "mathtext.bf": f"{style.font_family[0]}:bold",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
        }
    )
    return style


def figure_size(venue: str = "acm", span: str = "single", aspect: float = 0.62) -> tuple[float, float]:
    """Return (width, height) in inches for a venue column ('single' or 'double')."""
    key = venue.lower()
    if key not in COLUMN_WIDTHS_IN:
        raise ValueError(f"Unknown venue {venue!r}; choose from {sorted(COLUMN_WIDTHS_IN)}")
    if span not in ("single", "double"):
        raise ValueError("span must be 'single' or 'double'")
    if aspect <= 0:
        raise ValueError("aspect must be positive")
    single, double = COLUMN_WIDTHS_IN[key]
    width = single if span == "single" else double
    return width, round(width * aspect, 3)


def create_subplots(
    nrows: int = 1,
    ncols: int = 1,
    figsize: tuple[float, float] | None = None,
    **kwargs,
) -> tuple[Figure, np.ndarray]:
    """Create a figure and return its axes as a flat 1-D array.

    Uses constrained layout unless ``layout`` is passed, so axis labels of
    neighbouring panels do not collide.
    """
    if nrows < 1 or ncols < 1:
        raise ValueError("nrows and ncols must be at least 1")
    kwargs.setdefault("layout", "constrained")
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize or figure_size(), squeeze=False, **kwargs)
    return fig, axes.ravel()


def finalize_figure(
    fig: Figure,
    out_path: str | Path,
    formats: Iterable[str] | None = None,
    dpi: int = 300,
    close: bool = True,
    pad: float = 0.02,
) -> list[Path]:
    """Save ``fig`` in each format and return the written paths.

    Without ``formats``, the suffix of ``out_path`` is used; with no suffix,
    the figure is saved as PDF (vector, for the paper) and PNG (preview).
    """
    out_path = Path(out_path)
    if formats is None:
        suffix = out_path.suffix.lstrip(".").lower()
        formats = [suffix] if suffix else ["pdf", "png"]
    formats = [f.lower().lstrip(".") for f in formats]
    unknown = sorted(set(formats) - SAVE_FORMATS)
    if unknown:
        raise ValueError(f"Unsupported formats {unknown}; choose from {sorted(SAVE_FORMATS)}")

    stem = out_path.with_suffix("") if out_path.suffix else out_path
    stem.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for fmt in formats:
        target = stem.with_suffix(f".{fmt}")
        fig.savefig(target, dpi=dpi, bbox_inches="tight", pad_inches=pad)
        saved.append(target)
    if close:
        plt.close(fig)
    return saved


def _as_1d(values: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be 1-D, got shape {arr.shape}")
    return arr


def _as_2d(values: Sequence[Sequence[float]], name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be 2-D (series x categories), got shape {arr.shape}")
    return arr


def _pick_colors(colors: Sequence[str] | None, n: int) -> list[str]:
    palette = list(colors) if colors is not None else list(DEFAULT_COLORS)
    if len(palette) < n:
        raise ValueError(f"Need {n} colours, got {len(palette)}")
    return palette[:n]


def make_grouped_bar(
    ax: Axes,
    categories: Sequence[str],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    ylabel: str = "Value",
    colors: Sequence[str] | None = None,
    errors: Sequence[Sequence[float]] | None = None,
    hatches: Sequence[str] | None = None,
    annotate: bool = False,
    fmt: str = "{:.2f}",
    ylim: tuple[float, float] | None = None,
) -> list[BarContainer]:
    """Draw grouped bars: one group per category, one bar per series.

    ``errors`` has the same shape as ``series`` (symmetric half-widths, e.g. a
    95% CI). Bars start at zero unless ``ylim`` is given; a truncated bar axis
    exaggerates differences, so set it only with a reason stated in the caption.
    """
    values = _as_2d(series, "series")
    n_series, n_cats = values.shape
    if n_cats != len(categories):
        raise ValueError(f"series has {n_cats} columns but there are {len(categories)} categories")
    if len(labels) != n_series:
        raise ValueError(f"{n_series} series but {len(labels)} labels")
    err = _as_2d(errors, "errors") if errors is not None else None
    if err is not None and err.shape != values.shape:
        raise ValueError(f"errors shape {err.shape} must match series shape {values.shape}")
    if hatches is not None and len(hatches) < n_series:
        raise ValueError(f"Need {n_series} hatches, got {len(hatches)}")
    palette = _pick_colors(colors, n_series)

    x = np.arange(n_cats)
    width = 0.8 / n_series
    containers = []
    for i in range(n_series):
        offset = (i - (n_series - 1) / 2) * width
        bars = ax.bar(
            x + offset,
            values[i],
            width=width,
            color=palette[i],
            edgecolor="black",
            linewidth=plt.rcParams["axes.linewidth"],
            hatch=hatches[i] if hatches is not None else None,
            yerr=err[i] if err is not None else None,
            capsize=2 if err is not None else 0,
            error_kw={"elinewidth": plt.rcParams["axes.linewidth"]},
            label=labels[i],
        )
        containers.append(bars)
        if annotate:
            annotate_bars(ax, bars, fmt=fmt)
    ax.set_xticks(x, categories)
    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(*ylim)
    return containers


def annotate_bars(
    ax: Axes,
    bars: BarContainer,
    fmt: str = "{:.2f}",
    fontsize: float | None = None,
    padding: float = 2,
) -> None:
    """Write each bar's value just above it."""
    ax.bar_label(bars, labels=[fmt.format(b.get_height()) for b in bars], padding=padding,
                 fontsize=fontsize or plt.rcParams["font.size"] * 0.8)


def make_trend(
    ax: Axes,
    x: Sequence[float],
    y_series: Sequence[Sequence[float]],
    labels: Sequence[str],
    colors: Sequence[str] | None = None,
    bands: Sequence[tuple[Sequence[float], Sequence[float]] | None] | None = None,
    markers: Sequence[str] | None = None,
    ylabel: str | None = None,
    xlabel: str | None = None,
) -> None:
    """Plot several lines over a shared x, with optional (lower, upper) bands."""
    xs = _as_1d(x, "x")
    if len(y_series) != len(labels):
        raise ValueError(f"{len(y_series)} series but {len(labels)} labels")
    if bands is not None and len(bands) != len(y_series):
        raise ValueError("bands must have one entry (or None) per series")
    palette = _pick_colors(colors, len(y_series))
    for i, y in enumerate(y_series):
        ys = _as_1d(y, f"y_series[{i}]")
        if len(ys) != len(xs):
            raise ValueError(f"y_series[{i}] has length {len(ys)}, x has {len(xs)}")
        marker = markers[i] if markers is not None else None
        ax.plot(xs, ys, color=palette[i], marker=marker, markersize=3.5, label=labels[i])
        band = bands[i] if bands is not None else None
        if band is not None:
            lo, hi = _as_1d(band[0], "band lower"), _as_1d(band[1], "band upper")
            if len(lo) != len(xs) or len(hi) != len(xs):
                raise ValueError(f"band for series {i} must match x length")
            ax.fill_between(xs, lo, hi, color=palette[i], alpha=0.18, linewidth=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)


def make_heatmap(
    ax: Axes,
    matrix: Sequence[Sequence[float]],
    x_labels: Sequence[str] | None = None,
    y_labels: Sequence[str] | None = None,
    cmap: str = "magma",
    cbar_label: str | None = None,
    annotate: bool = False,
    fmt: str = "{:.2f}",
    vmin: float | None = None,
    vmax: float | None = None,
):
    """Draw a matrix as a heatmap with an optional colour bar label and cell text."""
    data = _as_2d(matrix, "matrix")
    if x_labels is not None and len(x_labels) != data.shape[1]:
        raise ValueError("x_labels must match the number of columns")
    if y_labels is not None and len(y_labels) != data.shape[0]:
        raise ValueError("y_labels must match the number of rows")
    image = ax.imshow(data, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    cbar = ax.figure.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    cbar.outline.set_visible(False)
    if cbar_label:
        cbar.set_label(cbar_label)
    if x_labels is not None:
        ax.set_xticks(np.arange(data.shape[1]), x_labels)
    if y_labels is not None:
        ax.set_yticks(np.arange(data.shape[0]), y_labels)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    if annotate:
        norm = image.norm
        for (r, c), value in np.ndenumerate(data):
            shade = image.cmap(norm(value))
            luminance = 0.299 * shade[0] + 0.587 * shade[1] + 0.114 * shade[2]
            ax.text(c, r, fmt.format(value), ha="center", va="center",
                    color="black" if luminance > 0.5 else "white",
                    fontsize=plt.rcParams["font.size"] * 0.75)
    return image


def make_scatter(
    ax: Axes,
    x: Sequence[float],
    y: Sequence[float],
    label: str | None = None,
    color: str | None = None,
    size: float = 12,
    alpha: float = 0.7,
) -> None:
    """Draw one scatter series."""
    xs, ys = _as_1d(x, "x"), _as_1d(y, "y")
    if len(xs) != len(ys):
        raise ValueError(f"x has length {len(xs)}, y has {len(ys)}")
    ax.scatter(xs, ys, s=size, alpha=alpha, color=color or PALETTE["blue_main"],
               edgecolors="none", label=label)


def legend_panel(ax: Axes, source_axes: Sequence[Axes], ncol: int = 1, loc: str = "center") -> None:
    """Turn ``ax`` into a legend-only panel collecting unique entries from ``source_axes``."""
    handles, labels, seen = [], [], set()
    for src in source_axes:
        for handle, label in zip(*src.get_legend_handles_labels()):
            if label not in seen:
                seen.add(label)
                handles.append(handle)
                labels.append(label)
    ax.set_axis_off()
    ax.legend(handles, labels, ncol=ncol, loc=loc)
