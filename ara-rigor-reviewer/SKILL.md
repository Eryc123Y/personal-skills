---
name: ara-rigor-reviewer
description: Review an existing ARA for claim support, scope, exploration integrity, or methodological rigor when an evidence audit is requested.
metadata:
  author: ara-commons
  category: research-tooling
  version: "3.2.0"
---

# ARA Rigor Reviewer

Review the epistemic quality of an existing ARA. Findings describe observed
evidence and limitations; they are not a scientific certification or venue
acceptance decision.

## Preconditions and boundaries

- Establish the target and structural-validation status. If validation is absent
  or failing, identify the affected references and review the readable evidence.
  Do not claim a completed Level 2 validation while required Level 1 checks fail.
  Structural repair is a separate mutation and requires task authorization.
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
4. Default to evidence-linked findings and coverage gaps. Use the reference
   scoring rubric only if the user or project contract requests it; label scores
   as reviewer judgments, not calibrated measurements or acceptance decisions.
5. Produce `level2_report.json` at the target ARA root only when the requested
   review is meant to materialise an artifact; otherwise return the review to
   the user without modifying the ARA.

Be constructive and calibrated. Flag both over-claiming and under-claiming;
negative results and rejected routes are evidence of exploration integrity when
they are honestly documented.
