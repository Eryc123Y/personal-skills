# ARA Seal Level 1 — Validation Checklist

Fix ALL failures before reporting success.

## 1. Directory Existence

Mandatory-core dirs — all must exist: `logic/`, `logic/solution/`, `src/`, `trace/`, `evidence/`.

## 2. Mandatory File Existence (non-empty, >10 bytes)

- `PAPER.md`
- `logic/problem.md`
- `logic/claims.md`
- `logic/concepts.md`
- `logic/experiments.md`
- `logic/solution/constraints.md`
- `logic/related_work.md`
- `src/environment.md`
- `trace/exploration_tree.yaml`
- `evidence/README.md`
- An evidence file for every numbered table and figure

## 3. PAPER.md Checks

- Starts with `---` (YAML frontmatter); valid YAML mapping
- Contains keys: `title`, `authors`, `year`
- Body contains "Layer Index" section

## 4. Field-Level Checks

### logic/claims.md
- Has `## C\d+` blocks (at least one claim)
- Contains `**Statement**`, `**Status**`, `**Falsification criteria**`, `**Proof**`, `**Evidence basis**`, `**Interpretation**`

### logic/problem.md
- Has `### O\d+` blocks (observations)
- Has `### G\d+` blocks (gaps)
- Has Key Insight section

### logic/experiments.md
- Has `## E\d+` blocks (at least 3)
- Contains `**Verifies**`, `**Setup**`, `**Procedure**`, `**Expected outcome**`

### logic/solution/heuristics.md (when present)
- Has `## H\d+` blocks with `**Rationale**`, `**Sensitivity**`, `**Bounds**`

### logic/related_work.md
- Has `## RW\d+` blocks with `**Type**`, `**Delta**`

### logic/concepts.md
- Has `## ` sections (at least 5) with `**Definition**`

## 5. Count Checks

Counts are **source-bounded targets, not quotas** — never pad with invented items.

- `logic/concepts.md`: aim ≥5 concept sections
- `logic/experiments.md`: aim ≥3 experiment blocks
- `src/execution/`: ≥1 `.py` file only when the work has concrete code

## 6. Evidence Quality

For each file in `evidence/tables/*.md` and `evidence/figures/*.md`:
- Must contain `**Source**` field
- **Must have a sibling screenshot `.png`** with a `**Screenshot**` field
- Table files must contain a Markdown table

For `evidence/figures/*.md`:
- Must declare `**Figure type**` in {quantitative_plot, diagram, qualitative_sample, mixed}
- Must declare `**Extraction method**` and `**Reading confidence**`
- `quantitative_plot` must contain a data table OR explicit unreadable statement with trend summary
- `diagram` and `qualitative_sample` must have visual description, NOT a fabricated numeric table
- Estimated readings marked `≈` with extraction method `digitized_estimate`

## 7. evidence/README.md

- Must contain a Markdown table (file index)
- All numbered tables and figures reflected

## 8. Exploration Tree (YAML)

- Parses as valid YAML
- Has top-level `tree` key
- All node types in {question, decision, experiment, dead_end, pivot}
- Every node has `id`, `type`, `support_level`
- Type-specific required fields: question:`description`, experiment:`result`, dead_end:`hypothesis,failure_mode,lesson`, decision:`choice,alternatives`, pivot:`from,to,trigger`
- Explicit nodes include `source_refs`

## 9. Cross-Layer Binding

- Every `E\d+` in a claim's `**Proof**` must exist in experiments.md
- Every `C\d+` in an experiment's `**Verifies**` must exist in claims.md
- Any `C\d+` in a tree node's `evidence` field must exist in claims.md
- Trace hygiene: no dead_end/decision/experiment nodes unsupported by source

## 10. Citation Verification

- Every repo path / `file:line` referenced exists
- No fact about a repo artifact transcribed from paper without checking

## 11. Evidence Ledger Completeness

- **Every numbered `Table N` and `Figure N` is filed** with BOTH markdown and screenshot `.png`
- Any deliberately not filed object listed in `evidence/README.md` with reason

## 12. Self-Consistency

- ARA-authored derived numbers recompute correctly
- `PAPER.md` declared counts match actual files
- Tree `evidence:` references are claim IDs (`C\d+`), not observation IDs
