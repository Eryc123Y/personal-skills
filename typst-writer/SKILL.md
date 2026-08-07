---
name: typst-writer
description: Create, edit, debug, compile, and visually verify Typst documents using Eric's preferred remote Typst Universe packages and authoring conventions. Use for .typ files, Typst syntax or mathematics, Scholia study notes and source-editable exercise scaffolds, Unofficial Monash Touying presentations, CeTZ/CeTZ Plot/Fletcher diagrams, Codly code, Lovelace pseudocode, tables, bibliographies, templates, and Typst package selection.
---

# Typst Writer

Write idiomatic, compiling Typst that follows the target repository first and
Eric's personal defaults second.

## Start with the target

1. Inspect the target repository, its `AGENTS.md`, existing `.typ` files,
   `typst.toml`, imports, and native environments before choosing a template.
2. Preserve an existing repository-native template unless the user asks to
   migrate it.
3. Identify the artifact type and load only the relevant reference:
   - study notes, proof handouts, workbooks, or exercise scaffolds: read
     `references/scholia.md`;
   - Eric's academic or research slides: read
     `references/monash-slides.md`;
   - nontrivial formulas or notation conversion: read `references/math.md`;
   - editable figures, plots, graphs, automata, or trees: read
     `references/diagrams.md`;
   - package or version choice: read `references/packages.md`;
   - cross-project conventions or validation: read
     `references/personal-workflow.md`.

## Prefer remote Typst Universe imports

Import maintained packages directly from Typst Universe in every new document:

```typst
#import "@preview/scholia:0.1.0": *
```

```typst
#import "@preview/unofficial-monash-touying:0.1.2": *
```

Do not make generated documents import `.typ` files from this skill,
`~/.cc-switch/skills`, `.claude/skills`, or another absolute machine-local
path. Treat `assets/` as examples or explicit compatibility fallbacks, not
runtime dependencies. Use a local template only when the target repository
already owns it or the user explicitly asks to vendor or customize it.

## Route the document

- Use Scholia for new personal study notes, proof documents, revision notes,
  active-recall workbooks, and source-editable course scaffolds.
- Use Unofficial Monash Touying for Eric's new research and academic slides.
- Keep course-provided or project-provided templates when present; inspect
  their native environments before adding wrappers.
- Use the Typsidian/Lemmify compatibility pattern only for an existing document
  already built on that stack.
- Use plain Typst for artifacts that do not benefit from a maintained template.

## Author with semantic source

- Prefer native `proof`, `yourturn`, and `TODO` blocks in Scholia. Add `answer`
  or `solution` only as thin semantic aliases when useful.
- Keep answers and proofs editable in `.typ` source. Do not replace them with
  flattened screenshots or opaque boxes.
- Use native Typst math tokens instead of LaTeX commands or pasted Unicode
  logic symbols.
- Put a reference table inside a captioned `figure` when it should be numbered,
  cited, or treated as a study artifact.
- Use Codly for real source code and Lovelace for pseudocode or algorithm
  traces.
- Preserve substantive examples, citations, source URLs, and repository style.

## Validate both source and rendering

1. Compile the actual entrypoint with `typst compile` and the correct project
   root.
2. Read all diagnostics. Fix package resolution failures, unknown functions,
   missing assets, font warnings that alter the intended design, and overflow
   introduced by the change.
3. Render representative pages or slides to PNG and inspect them visually.
   For multipage output, use a page template such as `page-{p}.png`.
4. Validate the `.typ` source and generated PDF separately. A clean source
   parse does not prove good layout, and a rendered PDF does not prove the
   source follows the requested template conventions.
5. Keep generated build artifacts out of version control unless the repository
   intentionally tracks them.

## Bundled examples

- `assets/scholia-note.typ` demonstrates a direct remote Scholia import.
- `assets/monash-slides.typ` demonstrates a direct remote Monash Touying import.
- `assets/academic-note.typ` is a legacy Typsidian/Lemmify compatibility
  example.

Read or copy these examples when helpful, but reproduce their remote import
pattern in the target document instead of importing them from the installed
skill.
