---
name: ara-research-manager
description: Update an existing, selected ARA with grounded research decisions or results when the user or project instructions authorize recording. Skip ordinary discussion and read-only review.
metadata:
  author: ara-commons
  category: research-tooling
  version: "3.1.0"
---

# ARA Research Manager

Maintain a selected ARA as an honest, append-only research ledger with
progressive crystallisation. This skill is a narrow end-of-turn recorder, not a
universal memory system and not a reason to create research state.

## Eligibility gate

Write only when all conditions hold:

1. The user or applicable project instructions authorize this ledger update.
   An existing authorization covers routine recording within its scope.

2. The turn produced a research-significant fact: an explicit decision,
   completed experiment, an evidence audit selected for recording, documented
   dead end, pivot, or material evidence change.
3. The target ARA is already present and has been selected by project guidance
   or the user.
4. The event can be grounded in files, commands, user statements, or other
   durable evidence available in the turn.

Skip greetings, general advice, planning-only work, clarifying questions,
read-only audits without a recording request, implementation setup without a
research result, and any turn where the target ARA is ambiguous. Never initialise `ara/` implicitly.

## Authority and mutability

Read the nearest project `AGENTS.md` and ARA contract first. Project rules
choose the ARA root and may add gates. In the absence of a more specific
contract:

- `trace/`, `staging/`, and `evidence/` are append-only;
- `logic/` is a current-state view and changes only after a closure signal;
- interpretations stage by default; promote a claim only when its evidence
  supports the stated scope. User adoption, committing a file, or abandoning a
  topic may close a decision but does not establish empirical truth;
- never silently erase contradictions. Record the conflict and leave it
  unresolved until authority or evidence settles it.

Use [event taxonomy](references/event-taxonomy.md) when classifying an event or deciding
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
