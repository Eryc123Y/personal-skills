---
name: d2-diagram
description: Create and revise editable D2 diagrams for architecture, processes, sequences, UML classes, schemas, and infrastructure. Use when the user requests D2 or when a structured diagram benefits from D2 source and a rendered export. Respect an existing diagram format or an explicitly selected tool; general requests for charts, illustrations, or animation do not by themselves require D2.
---

# D2 diagrams

Produce an editable `.d2` source and the requested rendered output. Follow the
project's diagram conventions and the user's chosen format, scope, and style.

## Choose the diagram

| Need | D2 representation |
|---|---|
| Architecture, infrastructure, or process | Nodes, meaningful containers, labeled connections |
| Time-ordered interactions | `shape: sequence_diagram` |
| Database schema | `shape: sql_table` |
| UML class diagram | `shape: class`; do not substitute a SQL table |
| State machine | Named states and labeled transitions |
| Roadmap | Grid containers and milestones; use a chart tool if scaled dates matter |

Read only the relevant reference:

- [Examples](references/d2-examples.md): complete architecture, sequence, schema,
  state, roadmap, and class diagrams.
- [Style guide](references/d2-style-guide.md): palettes, reusable classes,
  layout choices, and compile-ready syntax examples.
- [UML notation](references/uml-2.5.1-notation.md): relationship semantics and
  arrowheads for UML work.
- [Sequence checklist](references/sequence-diagram-checklist.md): participants,
  groups, spans, message order, and synchronous/asynchronous notation.

## Author and render

1. Identify what the diagram must explain and which relationships the source
   actually supports. Do not invent components or failure paths to fill a template.
2. Check `d2 --version` and the installed layout engines with `d2 layout`.
   Use ELK as a starting point for layered architecture; choose the layout that
   works for the actual diagram. Sequence diagrams have their own ordering rules.
3. Define important nodes and containers before connecting them. For sequences,
   predeclare participants, then keep messages, notes, and groups in chronological
   order; moving all messages to the bottom can change the meaning.
4. Match the requested palette. Use sketch styling only when it suits the
   deliverable. A small diagram does not need a palette or class framework.
5. Reuse classes when helpful. D2 supports multiple classes with
   `class: [service; highlighted]`. Use inline styles for genuine exceptions.
6. Quote labels containing syntax characters, such as `"GET /data/{id}"`.
   Separate same-line map entries with semicolons, and define variables before
   referencing them. Use integer `stroke-width` values supported by D2 v0.9.0.
7. For exact UML notation, check the reference's documented D2 limitations;
   do not present approximated open arrowheads as standards-compliant output.
8. Render and inspect the actual result. Check legibility, contrast, clipping,
   arrowheads, container boundaries, and message order. A successful compilation
   does not establish visual or semantic correctness.

```bash
# Architecture starting point; preserve a project's existing layout choice.
d2 --layout elk input.d2 output.svg

# Optional hand-drawn styling.
d2 --sketch --layout elk input.d2 output.svg
```

Use the host's available viewer or convert SVG to PNG for inspection. For a
large diagram, inspect readable crops as well as the overall layout. Remote
icons can fail to download; prefer available local assets or omit optional icons
when they prevent a reproducible render. Do not imply an icon is incompatible
with a shape without checking the actual output.

## Verify and deliver

Return the source and the requested export, describing any unresolved rendering
or notation limits. Do not start a watch server unless an interactive preview
is useful for the task.

When maintaining this skill, run the bundled example check:

```bash
python <skill-directory>/scripts/check_examples.py --output-dir <temporary-directory>
```

It compiles every D2 code block in this skill's Markdown files, preserving the
resulting source and SVG files for inspection. Compilation checks do not replace
visual review. Examples were checked with D2 v0.9.0; recheck the installed version
before relying on a version-specific limitation.
