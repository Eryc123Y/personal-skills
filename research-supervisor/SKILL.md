---
name: research-supervisor
description: Help choose a research workflow or evidence authority when the user asks for research direction, experiment planning, or ARA selection. Direct paper reading and language editing use their specialist skills.
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
and any project research adapter before giving consequential advice. Select the
project's declared ARA or evidence authority before interpreting results. A
plan, completed script, or launched job is not by itself a research result.

Project rules override this generic router. Keep project-specific paths, gates,
and scientific stop rules in the repository rather than in this skill.

## Route by intent

| Request | Route |
|---|---|
| Turn supplied papers, repositories, logs, or notes into a new ARA | `ara-compiler` |
| Capture a completed research-significant turn in an existing selected ARA | `ara-research-manager` |
| Audit an existing ARA for claim support and methodological rigor | `ara-rigor-reviewer` |
| Multi-source investigation or literature synthesis | local `deep-research`; use the Work deep-research plugin when the user selects that workflow |
| Interpret a supplied paper | `paper-analyzer` |
| Experiment design | Work directly from the project evidence and requested decision: hypotheses, controls, evaluation, resource limits, and completion criteria |
| Early idea feasibility or fatal-flaw review | `idea-evaluator` |
| Paper structure, benchmark-paper structure, introduction, figures, or pre-submission review | the corresponding specialist (`tech-paper-template`, `benchmark-paper-template`, `intro-drafter`, `figure-designer`, `pre-submission-reviewer`) |
| Technical system or process diagram | `d2-diagram` |
| Paragraph-level academic prose, grammar, or citation style | `academic-writing-assistant` |

For an end-to-end request, compose only the stages needed for the requested
outcome. Do not load a second orchestration suite or create an ARA unless the
user asks for one. ARA stores research evidence; it is not a prerequisite for
research, experiment planning, or writing.

## Operating boundaries

- Use the selected project ledger. Advice and read-only review do not authorize
  edits; an already authorized update does not require another approval round.
- Preserve the distinction between implementation readiness, provenance,
  public-score evidence, and validated scientific claims.
- In OpenResearch, native `orx-*` skills are an execution lane owned by that
  application. They are not a dependency of this global router.
- If multiple routes plausibly apply and the choice changes scope or authority,
  ask one focused question; otherwise proceed with the narrowest route.
