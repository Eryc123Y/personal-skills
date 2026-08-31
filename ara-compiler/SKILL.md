---
name: ara-compiler
description: Compile user-supplied research papers, repositories, experiment logs, or notes into a grounded, validated Agent-Native Research Artifact (ARA). Use when the user explicitly asks to create or substantially reconstruct an ARA; do not use for ordinary summaries or to alter an existing project ledger without an explicit target.
metadata:
  author: ara-commons
  category: research-tooling
  version: "2.0.0"
---

# ARA Compiler

Create a source-bounded, reviewable ARA from material the user placed in scope.
The artifact must distinguish source facts, derived interpretation, missing
information, and proposed work.

## Choose the target safely

- For an existing repository, read its nearest `AGENTS.md` and research
  guidance before choosing an output path.
- Default a new compilation to a separate output directory such as
  `./ara-output/`. Do not overwrite an established project `ara/` without an
  explicit request naming that target.
- If the source is incomplete, compile what is supported and mark the gap as
  unavailable. Do not invent a claim, metric, experiment, decision, or history.
- Resolve material conflicts only when the source authority is clear; otherwise
  preserve the conflict and ask the user how to treat it.

## Evidence-first compilation

1. Inventory the supplied sources and their authority: papers, appendices,
   code, configs, datasets, logs, reports, and notes.
2. Extract exact facts before synthesising: equations, implementation details,
   datasets, seeds, hardware, numerical values, assumptions, negative results,
   and ablations.
3. Inspect visual evidence deliberately. Read every relevant table and figure;
   for plots, diagrams, or qualitative results, render or inspect the image as
   needed. Preserve extraction method and uncertainty. Use `≈` for estimates.
4. Keep complete, ordered evidence records. A derived subset is not the source
   table or figure unless it faithfully reproduces it.
5. Reconstruct an exploration graph only from explicit decisions, results, and
   documented alternatives. Never manufacture a plausible research history.

## Build and verify

Use the ARA schema and create only files the sources warrant. Bind claims to
experiments, evidence, and reproducibility artifacts; keep exact numbers in
evidence rather than inventing precision in narrative fields.

Read these references as needed:

- [ARA schema](references/ara-schema.md) for file-level fields and links.
- [Exploration tree specification](references/exploration-tree-spec.md) for
  trace-node structure.
- [Figure extraction guide](references/figure-extraction-guide.md) for visual
  evidence work.
- [Validation checklist](references/validation-checklist.md) before handoff.

Run the applicable structural validation, repair actual failures, and report:
the artifact location, sources read, gaps or conflicts, evidence coverage,
validation result, and any unverified interpretation. Do not call a plan or a
successful setup check an empirical result.
