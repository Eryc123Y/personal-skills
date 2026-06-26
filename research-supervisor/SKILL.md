---
name: research-supervisor
description: >
  Central router for all of Eric's academic research workflows. Activate when
  the user mentions research supervision, FYP, paper planning, idea evaluation,
  literature review, paper writing, figure design, pre-submission review,
  knowledge extraction from papers, structural analysis, or experiment planning.
  Also activate on: 研究导师, 研究规划, 文献综述, 论文写作, 论文审阅, 实验规划,
  ARA 编译, 结构分析.
  Routes to: HKUSTDial/Supervisor-Skills, academic-research-suite (ARS),
  ara-compiler, ara-research-manager, ara-rigor-reviewer, prism-*, d2-diagram,
  and support skills. Works in Claude Code, Claude Desktop, and any Claude-
  compatible environment.
---

# Research Supervisor

Lightweight router. Read the task, pick the most specific skill, hand off immediately.
Never duplicate what the specialist skill does.

---

## 1 — Knowledge Capture (structuring existing material)

| Task | Skill |
|------|-------|
| Convert a paper, repo, experiment log, or raw notes into a structured ARA | `ara-compiler` |
| Record what happened during this research session (run end-of-turn) | `ara-research-manager` |
| Epistemic quality review of an ARA (Seal Level 2, 6 dimensions) | `ara-rigor-reviewer` |

---

## 2 — Active Research (exploring and gathering)

| Task | Skill |
|------|-------|
| Deep research, systematic review, meta-analysis, PRISMA, evidence synthesis | `academic-research-suite` → `ars/deep-research/WORKFLOW.md` |
| Vague topic, no clear research question yet, need Socratic guidance | `academic-research-suite` socratic mode → `ars/deep-research/WORKFLOW.md` |
| Quick literature scan comparing papers by WHY / HOW / WHAT | `academic-research-suite` three-way-scan mode (`/ars-3w`) |
| Fact-checking specific claims against primary sources | `academic-research-suite` fact-check mode |
| Experiment planning, statistical interpretation, reproducibility | `academic-research-suite` → `ars/experiment-agent/WORKFLOW.md` |
| Full research-to-paper pipeline with integrity gates | `academic-research-suite` → `ars/academic-pipeline/WORKFLOW.md` |

---

## 3 — Paper Writing

| Task | Skill |
|------|-------|
| Early idea: feasibility, novelty check, fatal-flaw detection | `idea-evaluator` |
| Technical paper structure, method logic, skeleton, advisor prep | `tech-paper-template` |
| Benchmark / dataset / evaluation framework / empirical-capability paper | `benchmark-paper-template` |
| Introduction outline and story flow | `intro-drafter` |
| Full paper writing: outline → draft → revision → citation check | `academic-research-suite` → `ars/academic-paper/WORKFLOW.md` |
| Figure 1, methodology diagram, experiment figure | `figure-designer` |
| System or architecture diagram (D2 code) | `d2-diagram` |
| Peer review simulation, editorial decision letter, reviewer calibration | `academic-research-suite` → `ars/academic-paper-reviewer/WORKFLOW.md` |
| Final paper audit before submission | `pre-submission-reviewer` |

---

## 4 — Structural Analysis (code, artifacts, text, strategy)

| Task | Skill |
|------|-------|
| Discover all angles worth analyzing for a given artifact | `prism-discover` |
| Quick structural scan with dynamically chosen cognitive lenses | `prism-scan` |
| Three orthogonal passes: WHERE (structure) / WHEN (dynamics) / WHY (causality) | `prism-3way` |
| What does the analysis itself conceal? Conservation law + constraint report | `prism-reflect` |
| Maximum depth: multi-pass with mandatory adversarial self-correction | `prism-full` |

---

## 5 — Support Skills (use only when the primary skill explicitly calls for them)

| Need | Skill |
|------|-------|
| Language polish, citation style, paragraph-level rewriting | `academic-writing-assistant` |
| Final AI-tone cleanup and naturalness pass | `humanizer` |
| Python chart or data visualization implementation | `data-visualization` |

---

## Routing Logic

1. **Specific request → direct route.** No need to clarify further if the task maps clearly to a single row above.
2. **Vague or multi-phase request → ask one scoping question** before routing:
   - "Do you already have a research question, or do you need to develop one?"
   - "Are you starting from scratch or do you have papers/materials to work from?"
3. **Never load the full ARS pipeline** (`ars/academic-pipeline`) unless the user explicitly asks for a full research-to-paper run or says "full pipeline."
4. **ARA and ARS are complementary, not redundant.** `ara-compiler` extracts knowledge from material you already have. ARS actively gathers and writes new material.
5. **Prism skills work on any artifact** — code, paper drafts, strategy documents, business plans. Not limited to research.
