# Exploration Tree YAML Specification

The exploration tree is the "git log" for research — a structured, traversable record of every
successful branch, failed attempt, and design decision that shaped the final result.

## Format

```yaml
# Exploration Tree — {paper_id}
# Research DAG: nested tree with cross-edges (also_depends_on) forming a DAG.
# Node types: question | experiment | dead_end | decision | pivot

tree:
  - id: N01
    type: question
    support_level: explicit
    source_refs: ["§1", "Table 2"]
    title: "{Central research question}"
    description: "{What question is being investigated}"
    children:

      - id: N02
        type: experiment
        support_level: explicit
        source_refs: ["Figure 4", "Table 2"]
        title: "{What was tried}"
        result: "{What was observed}"
        evidence: [C01, "Figure 3", "§2.2"]
        children:

          - id: N04
            type: decision
            support_level: inferred
            title: "{What was decided}"
            choice: "{The chosen approach}"
            alternatives:
              - "{Alternative 1}"
              - "{Alternative 2}"
            evidence: "{What informed this decision}"

      - id: N03
        type: dead_end
        support_level: inferred
        title: "{What was tried and failed}"
        hypothesis: "{What was expected}"
        failure_mode: "{Why it failed}"
        lesson: "{What was learned}"
```

## Node Types

### question
The root driver. What is being investigated?
- **Required fields**: `description`
- **Children**: experiments, decisions, other questions

### experiment
An attempt to answer a question or validate a decision.
- **Required fields**: `result`
- **Optional fields**: `evidence`
- **Children**: decisions, dead_ends, more experiments

### dead_end
A failed approach. THE MOST VALUABLE NODE TYPE for downstream agents.
- **Required fields**: `hypothesis`, `failure_mode`, `lesson`
- **NO children** — always a leaf node

### decision
A design choice with documented alternatives.
- **Required fields**: `choice`, `alternatives`

### pivot
A change in research direction.
- **Required fields**: `from`, `to`, `trigger`

## Rules

1. **Nested YAML**: Children appear inline under parent node's `children` list
2. **Valid DAG**: No cycles. All `also_depends_on` IDs must exist in the tree
3. **Target ~8+ nodes** covering the paper's key trajectory — but source-bounded, not a quota.
4. **dead_end / decision nodes**: include every one the paper actually reveals. If the paper exposes none, do NOT invent one.
5. **Every node has**: `id` (N01, N02...), `type`, `title`
6. **Every node has `support_level`**: `explicit` or `inferred`
7. **Explicit nodes should have `source_refs`**: table/figure/section references
8. **`also_depends_on`**: Only for DAG convergence (node has multiple parents beyond nesting)

## Extraction Strategy

When building from a PDF:
- **Central questions** → root nodes
- **"We tried X" / "We evaluated Y"** → experiment nodes
- **"We considered X but chose Y because..."** → decision nodes with alternatives
- **Ablation results showing X hurts** → dead_end nodes
- **"We initially pursued X but found..."** → pivot nodes

Support-level guidance:
- Mark a node `explicit` only if the paper directly reports it
- Mark a node `inferred` if you are reconstructing from narrative structure
- Prefer omission over fabricating a highly specific inferred node
