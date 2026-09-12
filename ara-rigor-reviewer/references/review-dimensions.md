# Level 2 Review Dimensions — Scoring Anchors and Check Inventory

Six dimensions of epistemic quality. Apply checks to the claim type and evidence
actually in scope; mark inapplicable checks rather than forcing a defect.
Numerical anchors and the historical grade mapping below are optional, only for
a requested scoring workflow. They are uncalibrated reviewer judgments, not
certification, empirical quality measurements, or predictions of venue acceptance.

---

## D1. Evidence Relevance

**Question**: Does the cited evidence actually support each claim in substance?

| Check | What to verify | Severity |
|-------|---------------|----------|
| Relevance | Experiment addresses what the claim actually asserts | major |
| Type-aware entailment | Design matches claim type (causal→ablation, generalization→heterogeneous, improvement→baseline) | major |
| Evidence sufficiency | Is a single experiment enough? | suggestion |

| Score | Description |
|-------|-------------|
| 5 | Type-appropriate, relevant evidence for every claim |
| 4 | Evidence relevant for all claims, minor type mismatches |
| 3 | Most pairs relevant, 1-2 weak matches |
| 2 | Multiple claims where experiments don't address the claim |
| 1 | Majority of claims cite irrelevant experiments |

---

## D2. Falsifiability Quality

**Question**: Are claims genuinely falsifiable with meaningful, actionable criteria?

| Check | What to verify | Severity |
|-------|---------------|----------|
| Actionability | Independent researcher could execute? Threshold and conditions specified? | major |
| Non-triviality | More than a tautology? | major |
| Scope match | Criterion addresses same scope as Statement? | major |
| Independence | Testable without proprietary data? | minor |

---

## D3. Scope Calibration

**Question**: Do claims assert exactly what evidence supports?

| Check | What to verify | Severity |
|-------|---------------|----------|
| Over-claiming | Universal scope while evidence is narrow | critical/major |
| Under-claiming | Evidence not captured by any claim | minor |
| Assumption explicitness | Key assumptions stated in problem.md/constraints.md | major |
| Generalization boundaries | What claims do NOT apply to is stated | minor |

---

## D4. Argument Coherence

**Question**: Does the argument follow a coherent path from problem to evidence?

| Check | What to verify | Severity |
|-------|---------------|----------|
| Observation → Gap derivation | Gaps follow logically from observations | major |
| Gap → Insight connection | Key insight addresses the gaps | major |
| Insight → Solution alignment | Solution implements the insight | major |
| Cross-layer consistency | Claims, tree, and evidence tell the same story | major |
| Gap coverage | Every gap addressed by at least one claim | major |

---

## D5. Exploration Integrity

**Question**: Does the exploration tree faithfully document the research journey?

| Check | What to verify | Severity |
|-------|---------------|----------|
| Dead-end specificity | failure_mode is concrete, lesson is transferable | major |
| Decision rationale quality | WHY chosen path preferred over real alternatives | major |
| Rebutted-branch consistency | No claim advocates a dead_end approach | critical |
| Exploration breadth | Document actual alternatives when the sources report them; absence alone does not establish poor exploration | minor |
| Honesty signal | Tree documents genuine negatives, not post-hoc justification | suggestion |

---

## D6. Methodological Rigor

**Question**: Are experiments well-designed with adequate baselines?

| Check | What to verify | Severity |
|-------|---------------|----------|
| Baseline adequacy | Right things compared? Recent and relevant? | major |
| Ablation coverage | Multi-component claims have isolating experiments | major |
| Statistical reporting | Variance, CI, runs, tests mentioned | major |
| Metric-claim alignment | Metric measures what claim asserts | major |
| Reproducibility signals | Setup specific enough for replication | minor |

---

## Overall Grade Mapping

| Grade | Condition |
|-------|-----------|
| **Strong Accept** | mean ≥ 4.5 AND no dimension < 3 |
| **Accept** | mean ≥ 3.8 AND no dimension < 2 |
| **Weak Accept** | mean ≥ 3.0 AND no dimension < 2 |
| **Weak Reject** | mean ≥ 2.0 AND (mean < 3.0 OR any dimension < 2) |
| **Reject** | mean < 2.0 OR any dimension = 1 |

## Finding Severity Definitions

| Severity | Meaning |
|----------|---------|
| `critical` | Fundamental epistemic flaw; claim cannot stand as written |
| `major` | Significant weakness that undermines a claim or dimension |
| `minor` | Noticeable issue that doesn't invalidate the work |
| `suggestion` | Constructive improvement opportunity, not a flaw |
