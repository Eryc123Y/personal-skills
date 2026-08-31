---
name: ara-rigor-reviewer
description: Perform a semantic, epistemic review of an already structurally valid Agent-Native Research Artifact (ARA). Use after Level 1 validation when the user asks to audit claim support, scope, exploration integrity, or methodological rigor.
metadata:
  author: ara-commons
  category: research-tooling
  version: "3.1.0"
---

# ARA Rigor Reviewer

Review the epistemic quality of an existing ARA. This is Seal Level 2: it does
not substitute for structural validation or invent missing evidence.

## Preconditions and boundaries

- Confirm that the target ARA and its Level 1 structural validation result are
  available. If validation has not passed, stop and route to structural repair.
- Read project guidance first. Preserve project-specific gates and avoid turning
  development-only or setup evidence into scientific claims.
- Treat a missing source, unresolved reference, or unavailable experiment as a
  finding, not as permission to infer a favourable result.

## Review procedure

1. Read the ARA in a coherent order: project problem and claims, experiments,
   solution constraints, trace, and representative evidence. Record what was
   actually read.
2. Evaluate the six dimensions in
   [review dimensions](references/review-dimensions.md): evidence relevance,
   falsifiability, scope calibration, argument coherence, exploration
   integrity, and methodological rigor.
3. For every finding, give a severity, target file/entity, observable evidence
   or explicit absence, reasoning, and a concrete remediation. Do not claim an
   exact source span unless it was observed.
4. Score each dimension from 1–5 and calculate the overall grade using the
   reference mapping. Explain any score that materially drives the grade.
5. Produce `level2_report.json` at the target ARA root only when the requested
   review is meant to materialise an artifact; otherwise return the review to
   the user without modifying the ARA.

Be constructive and calibrated. Flag both over-claiming and under-claiming;
negative results and rejected routes are evidence of exploration integrity when
they are honestly documented.
