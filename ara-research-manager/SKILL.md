---
name: ara-research-manager
description: Record completed research-significant decisions, results, pivots, or evidence updates in an already selected ARA. Use only at the end of a research turn with a valid project ARA; skip ordinary discussion, planning, read-only audits, and non-research work.
metadata:
  author: ara-commons
  category: research-tooling
  version: "3.0.0"
---

# ARA Research Manager

Maintain a selected ARA as an honest, append-only research ledger with
progressive crystallisation. This skill is a narrow end-of-turn recorder, not a
universal memory system and not a reason to create research state.

## Eligibility gate

Write only when all conditions hold:

1. The turn produced a research-significant fact: an explicit decision,
   completed experiment or evidence audit, documented dead end, pivot, or
   material evidence change.
2. The target ARA is already present and has been selected by project guidance
   or the user.
3. The event can be grounded in files, commands, user statements, or other
   durable evidence available in the turn.

Skip greetings, general advice, planning-only work, clarifying questions,
read-only audits, implementation setup without a result, and any turn where
the target ARA is ambiguous. Never initialise `ara/` implicitly.

## Authority and mutability

Read the nearest project `AGENTS.md` and ARA contract first. Project rules
choose the ARA root and may add gates. In the absence of a more specific
contract:

- `trace/`, `staging/`, and `evidence/` are append-only;
- `logic/` is a current-state view and changes only after a closure signal;
- interpretations stage by default; promote them only after explicit user
  affirmation, empirical resolution, topic abandonment, or artifact commitment;
- never silently erase contradictions. Record the conflict and leave it
  unresolved until authority or evidence settles it.

Use `references/event-taxonomy.md` when classifying an event or deciding
whether it belongs in the exploration tree, session record, or staging.

## Single-writer procedure

1. Re-read the target files immediately before writing. Determine the current
   identifier sequence and existing session record from the files, not memory.
2. Record only what actually occurred; label provenance accurately. AI-suggested
   content remains AI-suggested until the user explicitly adopts it.
3. A subagent or OpenResearch worker may propose events, but the current primary
   agent is the only writer. Merge proposals only after checking their evidence.
4. For any `logic/` change, preserve the before/after rationale in the relevant
   session record and keep historical trace entries intact.
5. Parse modified YAML and run the repository's ARA validator before handoff.
   If validation fails, repair the record or report it as incomplete; do not
   claim successful capture.

Report one concise line naming the selected ARA, record(s) changed, and
validation outcome. Do not record a new event solely because this skill ran.
