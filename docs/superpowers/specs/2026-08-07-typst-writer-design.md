# Typst Writer Skill Design

## Goal

Make `Eryc123Y/personal-skills` the repository source for Eric's
`typst-writer` skill while keeping CC Switch as the live installation and
cross-client synchronization authority.

The revised skill must encode Eric's actual Typst workflow rather than a broad
language tutorial. It should help an agent choose and use Eric's Scholia and
Unofficial Monash Touying packages, write idiomatic native Typst mathematics,
select appropriate drawing packages, and verify rendered output.

## Authority and Distribution

- Store the maintained skill at `personal-skills/typst-writer/`.
- Register or refresh it through CC Switch as
  `Eryc123Y/personal-skills:typst-writer`.
- Treat `~/.cc-switch/skills/typst-writer/` and the CC Switch database as the
  live installed state.
- Let CC Switch synchronize enabled clients. Do not manually copy files into
  `.claude/skills`, `.codex/skills`, or other client directories.
- Preserve CC Switch backups and avoid direct database mutation when the app's
  normal repository refresh/install workflow is available.

## Skill Structure

Keep the entrypoint concise and route detailed material through one-level
references:

```text
typst-writer/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── personal-workflow.md
│   ├── scholia.md
│   ├── monash-slides.md
│   ├── math.md
│   ├── diagrams.md
│   └── packages.md
└── assets/
    ├── scholia-note.typ
    ├── monash-slides.typ
    └── academic-note.typ
```

`SKILL.md` will contain the trigger description, document-type routing,
authoring workflow, resource-loading rules, and validation gates. It will not
repeat a general Typst manual.

## Routing Rules

Choose the authoring base from the requested artifact:

1. Use `@preview/scholia:0.1.0` for course notes, proof handouts, revision
   notes, source-editable exercise scaffolds, and active-recall workbooks.
2. Use `@preview/unofficial-monash-touying:0.1.2` for Eric's academic and
   research presentations.
3. Use a repository-native template when an existing course or project already
   provides one. Inspect its native environments before adding aliases or
   wrappers.
4. Use the legacy `academic-note.typ` stack only when compatibility with an
   existing Typsidian/Lemmify document is required. Scholia is the default for
   new personal study material.
5. Use plain Typst only when the artifact does not benefit from one of the
   maintained templates.

## Personal Authoring Conventions

- Keep answer areas source-editable. Prefer Scholia's native `proof`,
  `yourturn`, and `TODO`; introduce `answer` or `solution` only as thin semantic
  aliases when the document benefits from those names.
- Inspect package-native environments before creating custom boxes.
- Use display mathematics for math-rich material where inline rendering or
  readability is unreliable.
- Write Typst-native math tokens instead of pasted Unicode or LaTeX commands.
- Put tables in captioned `figure` elements when they are reference artifacts
  that should be numbered or cited.
- Preserve substantive examples, citations, and source URLs.
- Prefer editable Typst diagrams to raster images when the diagram is simple
  enough to maintain in source.

## Mathematics Reference

Build `references/math.md` around real recurring needs from FIT2014, MTH2051,
FIT3181, and research notes:

- logic and sets: quantifiers, implication, equivalence, membership,
  complements, subsets, and set builders;
- algebra and linear algebra: matrices, vectors, norms, inner products,
  eigenvalues, Jacobians, hats, calligraphic and blackboard-bold symbols;
- calculus and numerical analysis: limits, derivatives, integrals, sums,
  asymptotic notation, error expressions, and aligned derivations;
- probability and ML: expectations, distributions, losses, gradients, and
  indexed parameters;
- reliable translations from common LaTeX habits into native Typst syntax.

Examples must compile and should favor the notation already found in Eric's
documents.

## Diagram Selection

- Use CeTZ `0.5.2` as the default for coordinate drawings, annotated geometry,
  axes, explanatory curves, and custom mathematical illustrations.
- Use CeTZ Plot when a plot is generated from functions or data and benefits
  from plot-level abstractions.
- Use Fletcher for automatically laid-out graphs, automata, trees, and
  relationship diagrams.
- Use native Typst shapes and layout for very small diagrams where a package
  would add unnecessary complexity.
- Keep a stable palette and label text using Typst math/content inside the
  drawing.

## Package Policy

`references/packages.md` will distinguish:

- personal defaults: Scholia, Unofficial Monash Touying, CeTZ, Codly,
  Codly Languages, and Lovelace;
- conditional packages: CeTZ Plot, Fletcher, and template-specific
  dependencies;
- legacy compatibility: Typsidian and Lemmify.

Pin versions in starter assets. Before changing a version, verify the current
package manifest or authoritative package source and compile the affected
starter.

## Assets

- `scholia-note.typ`: minimal note/workbook starter using native Scholia
  environments and a source-editable answer area.
- `monash-slides.typ`: minimal presentation starter using the package's public
  Touying exports, title slide, frames, and a two-column example.
- `academic-note.typ`: retain and validate the existing compatibility template;
  label it legacy rather than the default for new notes.

Do not vendor the Scholia or Monash package implementation into the skill. The
assets demonstrate stable public APIs and remain small enough to copy into a
new project.

## Validation

1. Run the skill-creator `quick_validate.py` check.
2. Compile all three assets with the installed Typst compiler in an isolated
   temporary directory.
3. Render representative pages or slides to PNG and inspect them visually.
4. Scan compiler diagnostics and reject unknown functions, package errors,
   overflow caused by the starter, or missing required assets.
5. Forward-test realistic Scholia, Monash slides, math, and diagram prompts if
   a clean subagent evaluation is available.
6. Commit the repository changes intentionally.
7. Refresh the repository in CC Switch and confirm the installed skill has the
   repository-backed ID, expected content hash, and enabled client flags.
8. Confirm CC Switch, not a manual copy, propagated the update to the clients.

## Failure Handling

- If CC Switch cannot refresh the private GitHub repository, diagnose its
  repository authentication and 404 response without rewriting its database.
- If a package version cannot resolve, verify the package manifest and use the
  last repository-confirmed version rather than guessing.
- If a starter compiles but renders poorly, treat visual inspection as failed
  validation and revise the asset.
- Preserve unrelated files and existing CC Switch-managed skills throughout.

## Success Criteria

- `personal-skills` contains a valid, modular `typst-writer` skill.
- New study-note tasks default to Scholia; new Eric presentation tasks default
  to Unofficial Monash Touying.
- The skill gives concise, compiling guidance for native Typst mathematics and
  CeTZ-centered drawing.
- Starter assets compile and render acceptably.
- CC Switch identifies and distributes the repository-backed skill without
  manual client-directory synchronization.
