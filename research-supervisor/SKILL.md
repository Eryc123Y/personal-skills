---
name: research-supervisor
description: Main entrypoint for Eric's academic research supervision workflow. Use when the user asks for Research Supervisor, research supervisor, 研究导师, research planning, FYP or paper direction advice, idea evaluation, paper logic, paper skeleton, benchmark paper planning, Introduction structure, academic figure design, pre-submission review, or AI-assisted research workflow routing. This skill routes to the HKUSTDial/Supervisor-Skills research skills and keeps deep-research, academic-writing-assistant, humanizer, and data-visualization as support skills only when needed.
license: local
---

# Research Supervisor

Use this as a lightweight router, not as a replacement for the specialist skills.

## Route

- Early research idea, feasibility, novelty, or fatal-flaw check: use `idea-evaluator`.
- Technical paper structure, method-paper logic, paper skeleton, or advisor meeting preparation: use `tech-paper-template`.
- Benchmark, dataset, evaluation framework, or empirical capability boundary paper: use `benchmark-paper-template`.
- Introduction outline or story flow: use `intro-drafter`.
- Figure 1, methodology figure, or experiment figure design: use `figure-designer`.
- Final paper audit before submission: use `pre-submission-reviewer`.
- AI-assisted research workflow and tool routing: use `vibe-research-workflow`.

## Support Skills

- Use `deep-research` only for external literature/source gathering and verified multi-source synthesis.
- Use `academic-writing-assistant` only for language polish, citation style, and paragraph-level rewriting.
- Use `humanizer` only for final naturalness and AI-tone cleanup.
- Use `data-visualization` only for implementing charts or Python plotting.
- Avoid `academic-research-suite` unless the user explicitly asks for ARS or its command aliases.