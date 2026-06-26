# ARA Directory Schema — Complete Field-Level Reference

## Directory Structure

`✓` = mandatory core (always present). Everything else is created **only when the paper's content
warrants it** — there is no domain template to fill; you decide which method/artifact files
genuinely represent the work. The layout below is illustrative, not prescriptive.

```
PAPER.md                            # ✓ Root manifest + layer index
logic/
  problem.md                        # ✓ Why: observations → gaps → key insight
  claims.md                         # ✓ Falsifiable assertions
  concepts.md                       # ✓ Key technical terms (one ## per term)
  experiments.md                    # ✓ Declarative verification/analysis plans (NOT scripts)
  solution/
    constraints.md                  # ✓ Boundary conditions + assumptions + limitations
    <method files>                  # as warranted: architecture / algorithm / method /
                                    #   study_design / formalization / results / proofs /
                                    #   design / heuristics … — whatever fits THIS work
  related_work.md                   # ✓ Typed dependency graph (RDO)
src/
  environment.md                    # ✓ Data/software/hardware/protocols/seeds
  configs/                          # as warranted: hyperparameters / inference / deployment
  execution/{module}.py             # as warranted: grounded code stub (or absent — see below)
  prompts/, ...                     # as warranted: prompt templates, etc.
data/                               # as warranted: dataset.md + preprocessing.md
trace/
  exploration_tree.yaml             # ✓ Research DAG: nested YAML tree with typed nodes
evidence/
  README.md                         # ✓ Index mapping every evidence file to claims
  tables/                           # ✓ every numbered Table: tableN.md + tableN.png
  figures/                          # ✓ every numbered Figure: figureN.md + figureN.png
  proofs/                           # as warranted: derivations / proofs
rubric/requirements.md              # (Only if a rubric is provided)
```

Every numbered table and figure in the source gets BOTH a markdown file and a screenshot `.png`
(see the evidence specs below).

## Progressive Disclosure (3 Levels)

- **Level 1 — PAPER.md** (~200 tokens): Frontmatter + layer index. Agent reads ONLY this to decide relevance.
- **Level 2 — Layer files** (problem.md, claims.md, experiments.md, evidence/README.md): Loaded on demand.
- **Level 3 — Detail files** (algorithm.md, code stubs, individual evidence tables): Loaded when drilling in.

---

## PAPER.md

YAML frontmatter MUST include:
```yaml
---
title: "{full paper title}"
authors: [{author list}]
year: {year}
venue: "{venue}"
doi: "{DOI or arXiv ID}"
ara_version: "1.0"
domain: "{research domain — free text}"
keywords: [{5-10 keywords}]
claims_summary:
  - "{one-line summary of each main claim}"
abstract: "{paper abstract}"
---
```

Body MUST include a Layer Index — a table for each layer listing every file actually generated.

---

## logic/problem.md

```markdown
# Problem Specification

## Observations

### O{N}: {title}
- **Statement**: {precise empirical fact with numbers}
- **Evidence**: {source — figure, table, measurement, citation}
- **Implication**: {what this means for the problem}

## Gaps

### G{N}: {title}
- **Statement**: {what's missing or broken}
- **Caused by**: {which observations, e.g., O1, O2}
- **Existing attempts**: {what's been tried}
- **Why they fail**: {specific failure mode}

## Key Insight
- **Insight**: {the creative leap, stated precisely}
- **Derived from**: {which observations}
- **Enables**: {what solution approach this unlocks}

## Assumptions
- A1: {assumption}
- A2: {assumption}
```

---

## logic/claims.md

Each claim MUST have ALL fields:
```markdown
## C{NN}: {Short title}
- **Statement**: {Precise, falsifiable assertion}
- **Status**: {hypothesis|supported|refuted}
- **Falsification criteria**: {What would disprove this}
- **Proof**: [{experiment IDs: E01, E02}]
- **Evidence basis**: {What the cited evidence directly shows}
- **Interpretation**: {Optional broader reading}
- **Dependencies**: {other claim IDs, if any}
- **Tags**: {comma-separated keywords}
```

---

## logic/concepts.md

Target ≥5 concepts, but capture the paper's *genuine* technical terms. One section per concept:
```markdown
## {Term Name}
- **Notation**: {LaTeX or symbolic notation, or "—" if none}
- **Definition**: {Formal definition}
- **Boundary conditions**: {When it applies/not}
- **Related concepts**: {other concept names}
```

---

## logic/experiments.md

≥3 experiments. Declarative plans, NOT scripts. NO exact numerical results.

```markdown
## E{NN}: {Short title}
- **Verifies**: {claim IDs, e.g., C01, C02}
- **Setup**:
  - Model: {model name and size}
  - Hardware: {GPU type, count, memory}
  - Dataset: {dataset name, size, source}
- **Procedure**:
  1. {Step 1}
  2. {Step 2}
- **Metrics**: {what to measure, with units}
- **Expected outcome**:
  - {directional/relative ONLY}
  - NEVER exact numbers (those go in evidence/)
- **Baselines**: {methods to compare against}
- **Dependencies**: {other experiment IDs, or "none"}
```

---

## logic/solution/heuristics.md

Include only heuristics the paper actually states:
```markdown
## H{NN}: {Short description}
- **Rationale**: {Why this trick is needed}
- **Sensitivity**: {low|medium|high — or "Not specified in paper"}
- **Bounds**: {acceptable range or limits — or "Not specified in paper"}
- **Code ref**: [{path to src/execution/ file, or "Not specified"}]
- **Source**: {Section/table in the paper}
```

---

## logic/related_work.md

```markdown
## RW{NN}: {Author et al., Year}
- **DOI**: {DOI or arXiv ID}
- **Type**: {imports|bounds|baseline|extends|refutes}
- **Delta**:
  - What changed: {specific technical delta}
  - Why: {motivation}
- **Claims affected**: {claim IDs}
- **Adopted elements**: {what was kept}
```

---

## src/environment.md (mandatory core)

```markdown
# Environment
- **Language/runtime**: {Python version, R version, or "analytical — none"}
- **Framework**: {framework versions}
- **Hardware**: {GPU/CPU type, count, memory — or "n/a"}
- **Data sources**: {datasets/cohorts}
- **Key dependencies**: {list with versions}
- **Protocols**: {analysis protocol / preregistration, if any}
- **Random seeds**: {if specified}
```

---

## evidence/tables/{file}.md (+ screenshot)

Every numbered table gets BOTH a markdown file AND a screenshot `tableN.png`.

```markdown
# Table {N} - {Caption or short description}

**Source**: Table {N} in {paper/report title}
**Caption**: {verbatim or near-verbatim caption}
**Screenshot**: tableN.png
**Extraction type**: raw_table

| ... | ... |
| --- | --- |
| ... | ... |
```

---

## evidence/figures/{name}.md (+ screenshot)

Every numbered figure gets BOTH a markdown file AND a screenshot `figureN.png`.

```markdown
# Figure N: {Title}
- **Source**: Figure N, Section X.Y
- **Caption**: "{verbatim or near-verbatim caption}"
- **Screenshot**: figureN.png
- **Figure type**: {quantitative_plot | diagram | qualitative_sample | mixed}
- **Extraction method**: {exact_from_labels | digitized_estimate | visual_description}
- **Reading confidence**: {high | medium | low}
```

### quantitative_plot
```markdown
- **Plot kind**: {line | bar | scatter | box | histogram | heatmap}
- **Axes**: X = {label, units, scale: linear|log}, Y = {label, units, scale: linear|log}

| X | Y (Series A) | Y (Series B) |
|---|-------------|-------------|
| v | ≈v          | ≈v          |

## Trend summary
{Directional reading}
```

### diagram
```markdown
## Visual description
- **Components**: {boxes/modules}
- **Connections**: {arrows / data flow}
- **What it conveys**: {the structural claim}
```

### qualitative_sample
```markdown
## Visual description
- **Shows**: {what the panel depicts}
- **Demonstrates**: {the qualitative point}
- **Supports**: {claim ID(s) or gap ID(s)}
```

---

## evidence/README.md

```markdown
# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/{name}.md](tables/{name}.md) | Table N, §X.Y | C01, C02 | {one sentence} |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/{name}.md](figures/{name}.md) | Figure N, §X.Y | C03 | {one sentence} |
```

---

## trace/exploration_tree.yaml

```yaml
tree:
  - id: N01
    type: question
    support_level: explicit | inferred
    source_refs: ["Table 2", "§4.1"]
    title: "{...}"
    description: "{...}"
```

- `support_level: explicit` = directly grounded in provided source material
- `support_level: inferred` = reconstruction, not a literal session record
