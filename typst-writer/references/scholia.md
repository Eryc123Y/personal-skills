# Scholia notes and workbooks

Use Scholia for Eric's new study notes, proof handouts, revision documents,
active-recall workbooks, and source-editable exercise scaffolds.

## Remote preamble

```typst
#import "@preview/scholia:0.1.0": *

#set document(title: "Document Title", author: "Eric")
#show: scholia.with(
  theme: "light",
  prose: "notes",
  paper: "a4",
)
```

Use `prose: "book"` for connected exposition with first-line indentation. Use
`prose: "notes"` for handouts and workbooks with separated paragraphs.

## Native grammar

- `cover(...)`: title page.
- `note[...]`: intuition, scope, or reading guidance.
- `definition`, `theorem`, `lemma`, `proposition`, `corollary`: formal content.
- `proof[...]`: source-editable proof body with the package's ending marker.
- `example[...]`: worked model.
- `yourturn[...]`: learner response or active-input area.
- `TODO[...]`: an explicit source-editable missing step.
- `fillin(...)` and `workspace(...)`: print-oriented blanks and ruled space.
- `remark[...]`, `sidenote[...]`, and `recall[...]`: supporting commentary.

Inspect the package API or the Scholia repository skill when a task specifically
requires the full active-recall method. Do not duplicate or override native
styling in ordinary course documents.

## Source-editable answers

Use native blocks directly when their names fit:

```typst
#proof[
  State the proof here and leave #TODO[the key implication] when appropriate.
]

#yourturn[
  Type the response here.
]
```

When a course scaffold benefits from answer-oriented names, use thin aliases:

```typst
#let answer(body) = yourturn(body)
#let solution(body) = answer(body)
```

Do not introduce a new visual box for these aliases.

## Typical document opening

```typst
#cover(
  "Week 2 Workbook",
  subtitle: "Logic and formal languages",
  author: "Eric",
  date: "Semester 2, 2026",
)

#note[
  *How to use this document.* Write directly in each `proof`, `answer`, or
  `solution` body and replace the `TODO` prompt.
]

#outline(title: "Contents", depth: 2)
#pagebreak()
```

## Tables

Use native `table`. When a table is a named reference artifact, wrap it:

```typst
#figure(
  table(
    columns: (1fr, 2fr),
    table.header[*Symbol*][*Meaning*],
    [$Sigma$], [Alphabet],
    [$Sigma^*$], [All finite words over $Sigma$],
  ),
  caption: [Notation used in the exercises.],
) <tab:notation>
```

## Optional packages

Import extra packages only when used:

```typst
#import "@preview/cetz:0.5.2" as cetz
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.10": *
#import "@preview/lovelace:0.3.1": *
```

Keep all imports remote. Prefer CeTZ for editable mathematical figures, Codly
for source code, and Lovelace for pseudocode.
