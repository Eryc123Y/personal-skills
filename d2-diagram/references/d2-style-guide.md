# D2 style and layout guide

These examples are self-contained. Adapt them to the target project rather than
adding every feature to every diagram. The installed D2 version and the actual
render determine compatibility; these examples are checked with v0.9.0.

Official references: [styles](https://d2lang.com/tour/style/),
[classes](https://d2lang.com/tour/classes/),
[layouts](https://d2lang.com/tour/layouts/), and
[icons](https://d2lang.com/tour/icons/).

## Palette and reusable classes

Choose light or dark styling from the surrounding document and user preference.
Define only colors and classes used by the diagram. A palette alone does not
establish accessibility compliance: check each foreground/background pair and
label size in the rendered output.

### Light

```d2
vars: {
  d2-config: {theme-id: 0; layout-engine: elk}
  surface: "#F3F4F6"
  text: "#111827"
  primary: "#2563EB"
  accent: "#7C3AED"
}
classes: {
  service: {style: {fill: ${surface}; font-color: ${text}; stroke: ${primary}; border-radius: 8}}
  highlighted: {style.stroke: ${accent}; style.stroke-width: 3}
}
api: API {class: [service; highlighted]}
worker: Worker {class: service}
api -> worker: dispatches
```

### Dark

```d2
vars: {
  d2-config: {theme-id: 200; layout-engine: elk}
  surface: "#162646"
  text: "#D6D6DA"
  primary: "#739BCF"
  accent: "#F5871F"
}
classes: {
  service: {style: {fill: ${surface}; font-color: ${text}; stroke: ${primary}; border-radius: 8}}
  highlighted: {style.stroke: ${accent}; style.stroke-width: 3}
}
api: API {class: [service; highlighted]}
worker: Worker {class: service}
api -> worker: dispatches
```

Multiple classes are applied in order; later classes can override earlier
properties. Inline styles are appropriate for exceptions. Sketch styling is
optional (`d2 --sketch`), not a requirement for engineering diagrams.

## Node and connection styles

Use semantic shapes when they clarify meaning: cylinders for data stores,
queues for messages, people for actors, and plain rectangles for services.
Do not assume every hosted service needs a cloud or every microservice a hexagon.

```d2
service: API {
  style: {
    fill: "#F3F4F6"
    stroke: "#2563EB"
    font-color: "#111827"
    stroke-width: 2
    border-radius: 8
    font-size: 18
    bold: true
  }
}
store: Database {shape: cylinder}
service -> store: queries {
  style: {stroke: "#2563EB"; stroke-width: 2; font-size: 16}
}
```

In D2 v0.9.0, use integer stroke widths. Features such as shadows, multiple
outlines, and 3D effects are optional and shape-dependent; render before adding
them to a reusable class.

## Connectors and legends

Outside UML, pick a clear convention for sync calls, events, data flow, and
monitoring. State that convention when the reader might infer a different one.
Inside UML, follow the UML reference rather than borrowing architecture styles.
A dashed line alone does not make a message asynchronous in UML.

```d2
producer: API
queue: Events {shape: queue}
worker: Worker
producer -> queue: publishes event {
  style: {stroke: "#7C3AED"; stroke-width: 2}
  target-arrowhead.shape: arrow
}
queue -> worker: delivers event {
  style: {stroke: "#7C3AED"; stroke-width: 2}
  target-arrowhead.shape: arrow
}
```

Animated edges (`style.animated: true`) can help interactive SVGs, but do not
carry essential meaning only through motion; static exports lose it.

## Containers, boundaries, and layout

Use nesting for meaningful ownership or trust boundaries, not a fixed number of
levels. Keep one main level of detail when possible, and label purposeful
cross-level views. Do not invent compliance or classification labels.

ELK is a useful architecture starting point. Dagre or another installed engine
may produce a better result. Sequence diagrams preserve source order through
their specialized layout; do not describe that behavior as a dagre fallback.
Use node-relative positioning only with an engine that supports it.

```d2
vars: {d2-config: {layout-engine: elk}}
direction: right
client: Client
service: Application boundary {
  style: {fill: "#F3F4F6"; stroke: "#6B7280"; stroke-dash: 4}
  api: API
  db: Database {shape: cylinder}
  api -> db: reads
}
client -> service.api: HTTPS
```

Avoid hard-coded widths and heights until the natural layout has been inspected.
Node dimensions and container sizing behave differently across engines.

## Grids and roadmaps

A grid orders cards; it does not make their positions proportional to dates.
Use a chart tool when elapsed time or durations must be encoded quantitatively.

```d2
roadmap: {
  grid-columns: 3
  grid-gap: 16
  discovery: Discovery
  implementation: Implementation
  review: Review
}
```

## Labels containing syntax

Quote labels with braces, colons, or other D2 syntax. Use a real quoted newline
escape when a message needs a second line.

```d2
client -> api: "GET /data/{id}\nAuthorization: Bearer token"
```

## Globs

Use globs when a class would obscure a simple shared property. Declare useful
nodes first so the example also demonstrates the effect.

```d2
vpc: {
  api: API
  worker: Worker
  api -> worker: sends job
}
vpc.*.style.border-radius: 8
vpc.**.style.font-color: "#111827"
(* -> *)[*].style.stroke-width: 2
```

## Icons and output review

Use official icons only when they clarify the system. Prefer project-local
assets for repeatable builds. Rectangles often leave more room for an icon and
label; other shapes can also work with suitable sizing. Inspect the export for
overlap and legibility instead of imposing a universal shape ban.

For infrastructure, show only the actual region, network, namespace, service,
and workload boundaries supported by the source. Avoid turning every diagram
into a complete vendor inventory.

Check contrast, labels, arrow direction, meaningful boundaries, and the intended
reading order. Exporting successfully does not prove that a diagram communicates
the intended system correctly.
