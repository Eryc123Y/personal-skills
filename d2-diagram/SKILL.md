---
name: d2-diagram
description: "Generate production-quality D2 diagrams for system and process visualization. Use this skill whenever the user asks to diagram, draw, sketch, visualize, or map out system architecture, flowcharts, sequence diagrams, ER/database schemas, network topology, CI/CD pipelines, cloud infrastructure (AWS/GCP/Azure), Kubernetes, data flows, state machines, org charts, class diagrams, or roadmaps/timelines. Also activate when the user says 'show me how X connects to Y', 'make this visual', or 'create a diagram' for a structured system or workflow."
---

# D2 Diagram Skill

## Design Philosophy

1. **Semantic shapes first** — cylinders for databases, clouds for managed services, queues for message buses, hexagons for microservices, person for actors
2. **Palette matches context** — dark/navy for engineering audiences; light/minimal for presentations and docs; infer from context or ask
3. **Sketch by default** — hand-drawn aesthetic for exploratory and engineering diagrams; disable for formal print-ready output
4. **ELK by default** — use `layout-engine: elk` for every diagram unless D2 forces `sequence_diagram` to use dagre internally
5. **Typed connectors** — every edge communicates meaning (sync vs async, data-flow vs monitoring, boundary-crossing)
6. **Classes for consistency** — define style classes once, apply everywhere; never repeat inline styles
7. **Structure before connections** — declare all containers and nodes first, then draw all edges at the bottom

## Diagram Type Selection

| Type | D2 Approach | Key Config |
| ---- | ----------- | ---------- |
| **System Architecture** | Nested containers + typed edges | `direction: right`, ELK |
| **Sequence Diagram** | `shape: sequence_diagram` | D2 falls back to dagre internally |
| **ER / Schema** | `shape: sql_table` with constraints | `direction: right`, ELK |
| **Flowchart / Decision** | `diamond` + `step` + `oval` shapes | `direction: down`, ELK |
| **State Machine** | Nodes as states, labeled transition edges | `circle` for start/end terminals |
| **Org Chart** | `person` shapes + containers | `direction: down`, ELK |
| **Class Diagram** | `sql_table` approximation | Fields + methods as rows |
| **CI/CD Pipeline** | `step` shapes + grid layout | `direction: right` |
| **Data Flow / ETL** | Animated edges + pipeline-step class | `animated: true` |
| **Cloud Infra** | Account/VPC/subnet containers, vendor icons | 5-level nesting |
| **K8s Topology** | Cluster → namespace → deployment | `multiple: true` for replicas |
| **Network / Security** | Trust zones + boundary-crossing edges | `security-boundary` class |
| **Roadmap / Timeline** | `grid-rows` + `grid-columns` per quarter | `step` shapes per item |

For complete renderable examples of every type, see `references/d2-examples.md`.

## Required Source Checks

Before generating diagrams where notation correctness matters, consult the bundled sources first:

- **UML diagrams**: read `references/uml-2.5.1-notation.md` before generating class, object, package, component, or relationship-accurate diagrams.
- **Sequence diagrams**: read `references/sequence-diagram-checklist.md` before generating or revising any non-trivial sequence diagram.

## UML Mode

When the user explicitly asks for UML, class diagrams, object diagrams, or relationship-accurate notation, switch into **strict UML mode**:

- Follow UML 2.5.1 notation concepts.
- Prefer D2's native UML support where available (`shape: class`).
- Use correct relationship markers.

Relationship rules:
- **Association**: plain solid line
- **Aggregation**: hollow diamond on the whole side
- **Composition**: filled diamond on the whole side
- **Generalization**: solid line with hollow triangle pointing to parent
- **Realization**: dashed line with hollow triangle
- **Dependency**: dashed line with open arrow

See `references/uml-2.5.1-notation.md` for D2 patterns.

## Sequence Diagram Mode

Before drawing the final diagram, read `references/sequence-diagram-checklist.md`.

- Predeclare actors at the top level to control ordering
- Use groups for meaningful interaction fragments
- Use spans when activation / in-flight work matters
- Use notes for operational context
- Preserve message order deliberately

## Palette Options

### Dark (engineering / technical audiences)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg:      "#1C2F4A"   surface:  "#162646"   text:      "#D6D6DA"
  primary: "#385FAF"   accent:   "#9CADD7"   highlight: "#F5871F"
  muted:   "#739BCF"   success:  "#4CAF80"   danger:    "#E24B4A"
  text-light: "#FFFFFF"
}
```

### Light (presentations / mixed audiences)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 0; layout-engine: elk }
  bg:      "#FFFFFF"   surface:  "#F3F4F6"   text:      "#111827"
  primary: "#2563EB"   accent:   "#7C3AED"   highlight: "#F59E0B"
  muted:   "#6B7280"   success:  "#16A34A"   danger:    "#DC2626"
  text-light: "#FFFFFF"
}
```

For additional palettes, see `references/d2-style-guide.md` → Palette Options.

## Core Template

```d2
# DIAGRAM TYPE: <Architecture | Sequence | ER | Flowchart | ...>
# AUDIENCE: <who reads this>
# Shows: <one sentence>

direction: right

vars: {
  d2-config: {
    sketch: true
    theme-id: 200
    layout-engine: elk
  }
  # palette vars here
}

classes: {
  # See references/d2-style-guide.md > "Default Class Library"
}

# 1. Top-level standalone nodes (actors, external systems)
# 2. Container hierarchy (outermost → innermost)
# 3. All connections grouped by semantic type
```

## Render Commands

```bash
# Dark + sketch (default)
d2 --sketch --theme 200 --layout elk input.d2 output.svg

# Light mode
d2 --theme 0 --layout elk input.d2 output.svg

# Watch mode
d2 --layout elk -w input.d2 output.svg
```

## Key Rules

- **Connections always last** — define structure first, then draw connections
- **Default to ELK** — always pass `layout-engine: elk` or `--layout elk`
- **`sequence_diagram` is the only exception** — D2 uses dagre internally for sequences
- **Classes over inline styles** — never repeat fill/stroke/font-color on individual nodes
- **One `class` per node** — D2 supports only one; use `class` for shape, `style` block for colors
- **Integer `stroke-width` only** — D2 v0.7.x rejects decimal values
- **Icons on rectangular shapes only** — hexagon, diamond, person, circle distort icons

## References

- **`references/d2-style-guide.md`** — Complete D2 syntax: all style properties, shape catalog, palette options, icon library, ELK config, grid layouts, animation patterns.
- **`references/d2-examples.md`** — Full renderable examples for every diagram type.
- **`references/uml-2.5.1-notation.md`** — UML 2.5.1 relationship notation quick reference.
- **`references/sequence-diagram-checklist.md`** — D2 sequence diagram checklist.
