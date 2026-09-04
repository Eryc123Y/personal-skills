---
name: vibe-research-workflow
description: Plan an AI-assisted research workflow when the user asks how to organize
  coding, figures, or writing with agents. Do not trigger for every research session
  or an ordinary coding or writing task.
license: CC-BY-NC-SA-4.0
---
# Vibe Research Workflow

## Overview

Vibe Research is the modern research workflow where large language
models and AI coding tools handle mechanical tasks (implementation,
figure rendering, language polish) while the researcher retains
full ownership of research direction, problem framing, experimental
design, and factual accuracy. The goal is a two-to-five times
productivity gain on routine tasks without compromising academic
integrity.

The skill has three sub-flows: **Vibe Coding** (AI-assisted code),
**Vibe Figure** (AI-assisted figure production), **Vibe Writing**
(AI-assisted prose polish). Each is governed by six behavioural
rules that draw a hard line between acceptable use (mechanical
acceleration, auxiliary suggestions, style correction) and
academic misconduct (fabricated citations, outsourced scientific
judgment, hidden AI authorship).

This skill is a meta-skill that orchestrates tool selection, flow
design, and integrity enforcement across a research session. It
consolidates the the curriculum's Vibe Research section into a
single invocable procedure.

## When to use this skill

- The user requests a plan for an AI-assisted coding, figure, or writing workflow.
- The user asks 'how to use AI for research', 'Vibe Coding tips',
  'AI-assisted writing workflow', 'which AI tool for this'.
- The user is choosing tools or dividing work between Codex and occasional Gemini/Antigravity use.
- The user wants a workflow plan for a multi-day project
  involving AI.
- The user suspects AI output has drifted into unacceptable
  territory (fabricated citations, outsourced reasoning).

## When NOT to use this skill

- The user wants paper prose drafted. That is legitimate under this
  plugin's evidence discipline and belongs to the drafting skills:
  use an available drafting skill such as `academic-writing-assistant` or `intro-drafter`
  (Introductions), whose rules forbid fabricated substance (every
  factual claim traces to the user's materials, verified retrieval,
  or field common knowledge). Remind the user that venue and school
  AI-disclosure policies still apply, and that they remain
  responsible for verifying every drafted passage against their
  actual research. What stays forbidden is fabrication, not
  drafting.
- The user wants a code implementation done. This skill guides
  the process; it does not replace the implementation itself.
- The user wants to evaluate research direction. Use
  `idea-evaluator` (see handbook 2.3 for disruptive-innovation deep-dive).

## Core procedure

### Step 1: Phase classification

Decide which phase the user is in: coding, figure, writing, or
mixed.

### Step 2: Behavioural rules (brief when relevant)

See: references/behavior-guidelines.md for the full six-rule set.

State only the rules relevant to the current phase; give the full six-rule recap when the user asks for a workflow plan or when integrity risk is material:

1. AI-assisted work is permitted for literature search and
   organisation, code and debugging support, language and
   expression polish.
2. Research ideas, problems, designs, technical paths,
   experimental plans, core conclusions, and novelty must be the
   user's own and fully understood. Drafting assistance is
   legitimate within that boundary: the substance belongs to the
   user; the linguistic realization may be AI-assisted; the
   verification duty (rule 3) is unchanged.
3. Every AI-generated or AI-assisted passage is verified by the
   user against the actual research process, experimental
   results, and facts.
4. No fabricated citations; references come from the user's own
   reading and confirmation.
5. No academic misconduct, including fabricated data,
   experimental results, or plagiarism concealment.
6. Venue or school AI-disclosure requirements are honoured.

These rules are non-negotiable and enforced in the integrity
gate.

### Step 3: Phase-specific procedure

For Vibe Coding, see: references/vibe-coding.md.

For Vibe Figure, see: references/vibe-figure.md.

For Vibe Writing, see: references/vibe-writing.md.

Each phase has its own core techniques (Plan Mode, Small Steps,
Clear Requirements for coding; four-step figure workflow; red-line
rules for writing).

### Step 4: Tool selection

Codex is the primary agent in this workspace; Gemini through Antigravity is optional when selected by the user. Do not recommend installing or configuring Claude. Use the currently available tools for the requested output.

For bounded lookup, inventory, or first-pass review, use the user's preferred lightweight subagent when delegation is authorized and useful; the primary agent owns synthesis and acceptance. Do not force delegation or a fixed reasoning level for every task.

For scientific figures, use data-backed plotting and verify the exported artifact. For writing, preserve the user's authoring format and distinguish language editing from scientific claims. The historical tool matrix in references/tool-selection.md is background only; consult it only for a specifically requested comparison and verify current capabilities.

### Step 5: Integrity gate

Before closing the session, run the checks in the Integrity gate
section below.

### Step 6: Output

Emit the workflow plan in the Output format below.

## Integrity gate

This skill is a behavioural nudge, not a verification engine. Most
bullets are tagged [user-attest] because the LLM cannot actually
observe the user's private verification work. [inspection] tags
apply only to checks the LLM can confirm from its own outputs and
the user's session history.

Before ending the session:

1. **[inspection]** The six behavioural rules have been stated at
   the start of the session.
2. **[user-attest]** No fabricated citation has been introduced or
   accepted. (The LLM cannot verify citations without web access;
   the user confirms via DBLP or arXiv.)
3. **[user-attest]** The user's research direction, framing, and
   contributions are owned by the user, not by AI.
4. **[user-attest]** Every AI-generated code block has been
   reviewed and tested by the user.
5. **[user-attest]** Every AI-drafted paragraph has been rewritten
   or at minimum sentence-by-sentence verified by the user.
6. **[attestation]** Venue or school AI-disclosure rules have been
   checked. The skill asks the user to name the venue and
   surfaces known policy types; the user confirms compliance.
7. **[user-attest]** The user's own expertise is still driving the
   project; AI is an accelerator, not a replacement.

Pause only for an observed red-line violation (fabricated evidence,
plagiarism concealment, or an unverified core claim presented as fact).
Routine reminders and user-attested items should not interrupt otherwise
authorized work.

## Output format

### 1. Phase
- Primary phase: <coding or figure or writing or mixed>
- Secondary phases: <list>

### 2. Behavioural rules recap
- Rule 1-6 (see references/behavior-guidelines.md): acknowledged

### 3. Workflow plan
| Time block | Phase | Activity | Tool | User check |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### 4. Tool recommendations
| Phase | Primary tool | Alternative | Reason |
|---|---|---|---|
| Coding | ... | ... | ... |
| Figure | ... | ... | ... |
| Writing | ... | ... | ... |

### 5. Red-line reminders
- ... (from references/vibe-writing.md)

### 6. Integrity gate plan
- Verification points: ...
- AI-disclosure requirements for the target venue: ...
