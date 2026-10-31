import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import paperfig as pf  # noqa: E402


@pytest.fixture(autouse=True)
def _style():
    pf.apply_publication_style()
    yield
    matplotlib.pyplot.close("all")


def test_style_embeds_truetype_and_hides_spines():
    assert matplotlib.rcParams["pdf.fonttype"] == 42
    assert matplotlib.rcParams["axes.spines.top"] is False
    assert matplotlib.rcParams["legend.frameon"] is False


def test_figure_size_uses_venue_width():
    assert pf.figure_size("acm", "single", aspect=0.5) == (3.33, 1.665)
    assert pf.figure_size("ieee", "double")[0] == 7.16
    with pytest.raises(ValueError):
        pf.figure_size("unknown")
    with pytest.raises(ValueError):
        pf.figure_size("acm", "triple")


def test_grouped_bar_shapes_and_zero_baseline():
    fig, (ax,) = pf.create_subplots()
    containers = pf.make_grouped_bar(
        ax, ["A", "B", "C"], [[0.8, 0.7, 0.9], [0.6, 0.65, 0.7]], ["Ours", "Base"],
        errors=[[0.02] * 3, [0.03] * 3], hatches=["", "//"], annotate=True,
    )
    assert len(containers) == 2 and len(containers[0]) == 3
    assert ax.get_ylim()[0] == 0


def test_grouped_bar_rejects_mismatched_inputs():
    fig, (ax,) = pf.create_subplots()
    with pytest.raises(ValueError):
        pf.make_grouped_bar(ax, ["A", "B"], [[1, 2, 3]], ["X"])
    with pytest.raises(ValueError):
        pf.make_grouped_bar(ax, ["A"], [[1], [2]], ["X"])
    with pytest.raises(ValueError):
        pf.make_grouped_bar(ax, ["A", "B"], [[1, 2]], ["X"], errors=[[0.1]])


def test_trend_with_band_and_length_check():
    fig, (ax,) = pf.create_subplots()
    x = np.linspace(0, 1, 5)
    pf.make_trend(ax, x, [x, x**2], ["lin", "sq"], bands=[(x - 0.1, x + 0.1), None], markers=["o", "s"])
    assert len(ax.get_lines()) == 2
    with pytest.raises(ValueError):
        pf.make_trend(ax, x, [x[:3]], ["short"])


def test_heatmap_label_checks():
    fig, (ax,) = pf.create_subplots()
    pf.make_heatmap(ax, np.eye(3), x_labels=list("abc"), y_labels=list("xyz"), annotate=True, cbar_label="r")
    with pytest.raises(ValueError):
        pf.make_heatmap(ax, np.eye(3), x_labels=["a"])


def test_finalize_writes_vector_and_preview(tmp_path):
    fig, (ax,) = pf.create_subplots()
    pf.make_scatter(ax, [0, 1, 2], [1, 0, 2], label="pts")
    saved = pf.finalize_figure(fig, tmp_path / "sub" / "demo")
    assert {p.suffix for p in saved} == {".pdf", ".png"}
    assert all(p.stat().st_size > 0 for p in saved)
    pdf = (tmp_path / "sub" / "demo.pdf").read_bytes()
    assert b"/FontFile2" in pdf and b"/Type3" not in pdf


def test_finalize_rejects_unknown_format(tmp_path):
    fig, _ = pf.create_subplots()
    with pytest.raises(ValueError):
        pf.finalize_figure(fig, tmp_path / "x", formats=["docx"])


def test_legend_panel_collects_unique_labels():
    fig, axes = pf.create_subplots(1, 3, figsize=pf.figure_size("acm", "double", 0.3))
    for ax in axes[:2]:
        ax.plot([0, 1], [0, 1], label="Ours")
        ax.plot([0, 1], [1, 0], label="Base")
    pf.legend_panel(axes[2], axes[:2])
    texts = [t.get_text() for t in axes[2].get_legend().get_texts()]
    assert texts == ["Ours", "Base"]
