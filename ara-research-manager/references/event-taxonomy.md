# Event Taxonomy & Routing Rules

Canonical reference for **Stage 2 (Event Router)** of the Live PM pipeline.

## Direct-Routed Events (Journey Layer)

Write to `trace/exploration_tree.yaml` immediately at end of turn.

| Type | Signals | Required payload |
|------|---------|------------------|
| `question` | Research direction opened | `description` |
| `decision` | User chose between alternatives | `choice`, `alternatives`, `evidence` |
| `experiment` | Code ran a test/benchmark | `result`, `evidence` |
| `dead_end` | Approach abandoned | `hypothesis`, `failure_mode`, `lesson` |
| `pivot` | Major direction change | `from`, `to`, `trigger` |

## Staged-Routed Events (Interpretive)

Write to `staging/observations.yaml` first.

| Candidate Event | Crystallizes To | `potential_type` |
|-----------------|-----------------|------------------|
| Falsifiable assertion | `logic/claims.md` | `claim` |
| Implementation rule with rationale | `logic/solution/heuristics.md` | `heuristic` |
| New term defined | `logic/concepts.md` | `concept` |
| Boundary condition | `logic/solution/constraints.md` | `constraint` |
| System design statement | `logic/solution/architecture.md` | `architecture` |
| Untyped | (stays staged) | `unknown` |

## Routing Decision Tree

```
Journey fact (something that happened)?
  Choice between alternatives? → decision [DIRECT]
  Code/test produced a result? → experiment [DIRECT]
  Approach abandoned? → dead_end [DIRECT]
  Major direction change? → pivot [DIRECT]
  Research question opened? → question [DIRECT]
  AI performed an action? → ai-action [session record only]

Interpretation (something asserted to be true)?
  Falsifiable assertion? → STAGE as claim
  Implementation rule? → STAGE as heuristic
  Term definition? → STAGE as concept
  Boundary condition? → STAGE as constraint
  System-design statement? → STAGE as architecture
  Doesn't fit? → STAGE as unknown
```

## Skip Filter (no record)

- Routine file reads with no downstream decision
- Typo fixes, formatting changes, lint passes
- Git status checks, dependency installs, environment setup
- Greetings, acknowledgments, "thanks"
- Clarifying questions whose answer added no new content

## Provenance Assignment

```
User said it directly → provenance: user
AI inferred from context → provenance: ai-suggested
AI performed an action → provenance: ai-executed
User modified an AI suggestion → provenance: user-revised
Uncertain? → provenance: ai-suggested (conservative default)
```

## ID Conventions

| Type | Prefix | Scope |
|------|--------|-------|
| Exploration node | N | Global |
| Claim | C | Global; assigned at crystallization |
| Heuristic | H | Global; assigned at crystallization |
| Experiment plan | E | Global |
| Observation | O | Global; assigned at staging |

Always read the target file to find the highest existing ID before assigning a new one.

## Forensic Binding Checklist

- **Claim → Proof**: what evidence supports/refutes it?
- **Experiment → Claim**: which claim does this experiment test?
- **Heuristic → Code**: where in the codebase is this implemented?
- **Decision → Evidence**: which exploration nodes motivated it?
- **Dead End → Lesson**: what was learned?
- **Observation → Bound nodes**: list `bound_to: [N{XX}, ...]` at staging time.
