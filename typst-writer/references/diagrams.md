# Diagrams and plots

Choose the smallest remote package that matches the structure of the visual.

## Selection

- Use native Typst shapes and layout for a tiny static annotation.
- Use CeTZ `0.5.2` for coordinate drawings, axes, annotated geometry, custom
  curves, and explanatory mathematical figures.
- Use CeTZ Plot `0.1.3` for function- or data-driven plots and charts.
- Use Fletcher `0.5.8` for automatically arranged graphs, automata, trees,
  commutative diagrams, state machines, and relationship diagrams.

Prefer editable source over raster images when the figure remains reasonably
maintainable.

## CeTZ base pattern

```typst
#import "@preview/cetz:0.5.2" as cetz

#let blue = rgb("#2563eb")
#let muted = rgb("#64748b")

#figure(
  cetz.canvas(length: 0.7cm, {
    import cetz.draw: *
    line((-3, 0), (3, 0), mark: (end: "stealth"), stroke: muted + 0.7pt)
    line((0, -2), (0, 2), mark: (end: "stealth"), stroke: muted + 0.7pt)
    line((-2.5, -1.2), (-1, 0.2), (0.5, 1.1), (2.4, 1.5),
      stroke: blue + 1.4pt)
    content((2.6, -0.3), text(size: 8pt)[$x$])
    content((0.25, 1.8), text(size: 8pt)[$f(x)$])
  }),
  caption: [Illustrative function geometry.],
) <fig:function>
```

Use a stable named palette near the top of the document. Put labels in Typst
content or math so fonts and notation match the document.

## CeTZ Plot import

```typst
#import "@preview/cetz:0.5.2" as cetz
#import "@preview/cetz-plot:0.1.3": plot, chart
```

Read the current CeTZ Plot package documentation before using advanced plot
APIs; its abstractions are less stable than the base CeTZ drawing primitives.

## Fletcher pattern

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#diagram(
  spacing: 3em,
  node((0, 0), [Start]),
  edge("->"),
  node((1, 0), [Process]),
  edge("->"),
  node((2, 0), [Result]),
)
```

Use Fletcher instead of manually positioning nodes when graph structure and
edge routing are the core of the figure.

## Validation

- Compile the figure in its real document, not only in isolation.
- Inspect label collisions, clipping, line weights, legends, and readability at
  the final page or slide size.
- Keep important distinctions visible in grayscale when practical; do not rely
  on color alone.
- Avoid drawing decorative figures that do not clarify the argument.
