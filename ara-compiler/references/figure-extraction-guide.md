# Figure Extraction Guide — Reading Plots, Diagrams, and Samples

Load when an input contains figures whose information is not available as text. Goal: turn pixels
into structured ARA evidence **honestly**.

Governing rule (Critical Rule #11): read figures by looking at them, mark estimates as estimates,
never fabricate a data table for a figure that does not contain one.

---

## 0. Decide whether you need to crop

Try reading the figure from the rendered PDF page first. Only fall back to rendering/cropping when:
- too small or dense to read values reliably
- one panel in a multi-panel figure to isolate
- overlapping with text/other figures
- vector format needing higher resolution

---

## 1. Classify before you read

| Type | What it carries | Do NOT |
|------|-----------------|--------|
| `quantitative_plot` | numbers on axes (line/bar/scatter/box/hist/heatmap) | invent points you cannot see |
| `diagram` | structure: components + connections | build a numeric table |
| `qualitative_sample` | a demonstrated behavior/artifact | claim measurements |
| `mixed` | several types in one figure | collapse panels together |

If unsure: "could I read a number off an axis here?" If no → not a `quantitative_plot`.

---

## 2. Rendering and cropping (when needed)

### PyMuPDF — whole page

```python
import fitz
doc = fitz.open("paper.pdf")
page = doc[6]  # 0-indexed
pix = page.get_pixmap(dpi=200)
pix.save("page7.png")
```

### PyMuPDF — crop a figure region

```python
import fitz
doc = fitz.open("paper.pdf")
page = doc[6]
clip = fitz.Rect(60, 90, 540, 360)  # (x0, y0, x1, y1) in PDF points
pix = page.get_pixmap(dpi=300, clip=clip)
pix.save("fig4_cropped.png")
```

### pdf2image fallback

```python
from pdf2image import convert_from_path
pages = convert_from_path("paper.pdf", dpi=200, first_page=7, last_page=7)
pages[0].save("page7.png")
```

**Save every render as the evidence screenshot** next to its markdown file.

---

## 3. Reading a quantitative plot

1. **Axes first.** Record labels, units, and **scale (linear vs log)**. Log axis read as linear silently corrupts every value.
2. **Ranges and gridlines.** Note axis min/max.
3. **Prefer printed values.** Use data labels when available → `extraction method: exact_from_labels`.
4. **Otherwise estimate.** Mark each point `≈` → `extraction method: digitized_estimate`.
5. **Always capture the trend.** Monotonic? Plateau? Crossover? Variance bands?
6. **Series names from legend** exactly as shown.

Confidence rubric: `high` = clean axes/gridlines/labels; `medium` = interpolated; `low` = dense/blurred.

### Worked example

```markdown
# Figure 4: Validation accuracy vs. training epochs
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line
- **Axes**: X = epoch (count, linear), Y = top-1 accuracy (%, linear)

| Epoch | Ours (%) | Baseline (%) |
|-------|----------|--------------|
| 10    | ≈62      | ≈58          |
| 30    | ≈74      | ≈66          |
| 50    | ≈78      | ≈69          |

## Trend summary
Both rise monotonically, plateauing ~epoch 40. Ours above Baseline at every point; gap widens
from ≈4 pts (epoch 10) to ≈9 pts (epoch 50).
```

---

## 4. Reading a diagram

Do NOT build a data table. Capture structure, mirror into `architecture.md`.

```markdown
## Visual description
- **Components**: Tokenizer → Stage-A encoder (6 blocks) → Cross-attn bridge → Stage-B decoder → Head
- **Connections**: residual skip from Stage-A to bridge; dashed = optional auxiliary loss
- **Annotations**: blue = trainable, grey = frozen
- **What it conveys**: contribution sits in the cross-attn bridge
```

---

## 5. Reading a qualitative sample

```markdown
## Visual description
- **Shows**: 4 input/output pairs where model mislabels rotated objects
- **Demonstrates**: rotation-sensitivity failure mode
- **Supports**: G2 (robustness gap), qualitative basis for C04's limitation clause
```

---

## 6. Common traps

- **Log axes** read as linear — the single most damaging error. Check tick spacing.
- **Secondary Y-axis** — map each series to its correct scale.
- **Truncated axes** — note it in trend summary so claims aren't overstated.
- **Error bars / shaded bands** — capture them; they bound claim strength.
- **Color-only series** — name by legend text, not color.
- **Stacked vs grouped bars** — stacked totals are cumulative.

---

## 7. Honesty checklist

- [ ] Figure type classified; file format matches type
- [ ] `Extraction method` and `Reading confidence` set and consistent
- [ ] Every estimated number marked `≈`
- [ ] Axis scale (linear/log) recorded for plots
- [ ] No fabricated table for diagram or qualitative sample
- [ ] Unreadable figure stated as `reading confidence: low` with trend summary
- [ ] Diagram structure mirrored into `logic/solution/architecture.md`
- [ ] Qualitative sample tied to a claim or gap ID
