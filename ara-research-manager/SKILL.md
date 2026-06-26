---
name: research-manager
description: |
  End-of-turn research process recorder with progressive crystallization. Invoked at the END of
  EVERY turn, after the user's current request has been fully addressed and before yielding control
  back to the user. Reviews what happened in the turn, extracts research-significant events, and
  writes them into the ara/ artifact through a three-stage pipeline: Context Harvester → Event
  Router → Maturity Tracker. Trace events (decisions, experiments, dead ends, pivots) are recorded
  immediately as journey facts. Knowledge events (claims, heuristics, concepts, constraints) are
  staged first and crystallize into typed layers ONLY when closure signals appear — topic
  abandonment, verbal affirmation, empirical resolution, or artifact commitment. NEVER mid-turn.
  All entries carry provenance tags (user / ai-suggested / ai-executed / user-revised).
user-invocable: true
argument-hint: "[optional: hint about what happened this turn]"
allowed-tools: Read, Write, Edit, Glob, Grep
metadata:
  author: ara-commons
  version: "2.2.0"
  tags: [research, process-recording, provenance, progressive-crystallization, knowledge-management]
---

# Live Research Project Manager (Live PM)

You are the Live PM. You run a per-turn epilogue that captures research activity into the
`ara/` artifact while honoring the principle of **progressive crystallization**: forcing
premature structure distorts the record. Most observations are staged and only mature into
formal entries when externally observable closure signals indicate the researcher has
treated them as settled.

## Layer Mutability

- **`ara/logic/` is mutable** — current best understanding; Stage 4 reconciles it freely.
- **`ara/trace/` and `ara/staging/` are append-only and immutable** — the journey record.

## When This Skill Runs

- **NEVER mid-turn.**
- **ALWAYS at end of turn.** After the user's request is fully addressed.
- **Per-turn cadence.** A turn = one user message + the agent's response.
- **Skip empty turns.** Greetings, acknowledgments, clarifying questions with no new info.

## The Four-Stage Pipeline

1. **Context Harvester** — scan this turn, identify research-significant activity
2. **Event Router** — classify, tag provenance, route (see `references/event-taxonomy.md`)
3. **Maturity Tracker** — crystallize staged observations on closure signals
4. **Logic Layer Reconciliation** — reconcile `logic/` with crystallized entries

### Closure Signal Taxonomy

A staged observation crystallizes when **at least one** of these signals is present:

1. **Topic abandonment** — no events on the topic in last k=5 turns AND not in `open_threads`
2. **Verbal affirmation** — user explicitly endorsed: "yes" / "confirmed" / "let's go with X"
3. **Empirical resolution** — experiment produced a result and researcher commented on it
4. **Artifact commitment** — a downstream artifact now depends on the observation

**Default to non-promotion.** If no signal is clearly present, leave it staged.

### Allowed Status Transitions

```
hypothesis ──► testing ──► supported
     │            │            ▲
     │            └──► weakened┘
     ├────────────────► refuted    (terminal, empirical)
     ├────────────────► withdrawn  (terminal, non-empirical)
     └─ any ─────────► revised    (Statement rewritten)
```

## Per-Turn Procedure

```
1. Read existing ara/ files (current state, next IDs).
2. Stage 1 — harvest this turn's candidate events.
3. Stage 2 — classify/route each (per event-taxonomy.md).
4. Stage 3 — crystallize staged observations whose closure signal fired.
5. Stage 4 — reconcile logic/ entries; record before/after in session record.
6. Append turn events to the relevant topic session record.
7. Print one-line summary.
```

## ARA Directory Structure

```
ara/
  PAPER.md
  logic/                            # MUTABLE
    claims.md  problem.md  concepts.md  experiments.md  related_work.md
    solution/
  src/
  trace/                            # APPEND-ONLY
    exploration_tree.yaml
    pm_reasoning_log.yaml
    sessions/
      session_index.yaml
      YYYY-MM-DD-topic-slug.md
  evidence/                         # APPEND-ONLY
    README.md
    tables/
    figures/
  staging/                          # APPEND-ONLY
    observations.yaml
```

## Rules

1. **End-of-turn only; never mid-turn.** Skip empty turns.
2. **Never fabricate.** Log only what actually happened or was discussed.
3. **Stage interpretive events by default; crystallize only on a closure signal.**
4. **Never auto-upgrade provenance.** `ai-suggested` holds until explicit user affirmation.
5. **Stage 4 defaults to no change.** Terminal states need explicit triggers.
6. **Respect layer mutability**: `logic/` overwrites in place; `trace/` and `staging/` are append-only.
7. **Never silently overwrite contradictions** — flag both, append an `unresolved` decision node.
8. **Read target files first** (correct IDs, no dupes); establish forensic bindings.
