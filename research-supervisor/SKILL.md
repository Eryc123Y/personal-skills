---
name: research-supervisor
description: Help choose a research workflow and current evidence when the user asks for research direction or experiment planning. Direct paper reading and language editing use their specialist skills.
metadata:
  author: ara-commons
  category: research-tooling
  version: "3.1.0"
---

# Research Supervisor

Act as a lightweight router and advisor. Select the narrowest specialist that
fits the request; do not duplicate its workflow or create a second research
ledger.

## Establish project authority first

When a request concerns an existing repository, read its nearest `AGENTS.md`
and the current proposal, roadmap, experiment plan, or result needed for the
decision. Check dated conclusions against their original conditions and newer
evidence before treating them as current. A plan, completed script, or launched
job is not by itself a research result.

Project rules override this generic router. Keep project-specific paths, gates,
and scientific stop rules in the repository rather than in this skill. A failed
test bounds the tested route; it does not settle distinct routes or later
evidence without checking their assumptions.

## Route by intent

| Request | Route |
|---|---|
| Multi-source investigation or literature synthesis | local `deep-research`; use the Work deep-research plugin when the user selects that workflow |
| Interpret a supplied paper | `paper-analyzer` |
| Experiment design | Work directly from the project evidence and requested decision: hypotheses, controls, evaluation, resource limits, and completion criteria |
| Early idea feasibility or fatal-flaw review | `idea-evaluator` |
| Paper structure, benchmark-paper structure, introduction, figures, or pre-submission review | the corresponding specialist (`tech-paper-template`, `benchmark-paper-template`, `intro-drafter`, `figure-designer`, `pre-submission-reviewer`) |
| Technical system or process diagram | `d2-diagram` |
| Paragraph-level academic prose, grammar, or citation style | `academic-writing-assistant` |

For an end-to-end request, compose only the stages needed for the requested
outcome. Do not create a parallel research ledger as a prerequisite for
research, experiment planning, or writing.

## Operating boundaries

- Use the project's current source files and experiment receipts. Advice and
  read-only review do not authorize edits; an already authorized update does
  not require another approval round.
- Preserve the distinction between implementation readiness, provenance,
  public-score evidence, and validated scientific claims.
- In OpenResearch, native `orx-*` skills are an execution lane owned by that
  application. They are not a dependency of this global router.
- If multiple routes plausibly apply and the choice changes scope or authority,
  ask one focused question; otherwise proceed with the narrowest route.
