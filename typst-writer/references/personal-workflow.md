# Personal workflow

Use these conventions after honoring the target repository's own rules.

## Defaults

- Import packages from Typst Universe with `@preview/...`; do not depend on an
  installed skill path.
- Use Scholia for new course notes, proof handouts, workbooks, and revision
  material.
- Use Unofficial Monash Touying for Eric's academic and research slides.
- Keep planning flexible: create a source-editable scaffold rather than filling
  every answer unless the user requests worked solutions.
- Inspect the chosen template's native environments before defining new ones.

## Source conventions

- Prefer semantic names and real package environments over hand-styled boxes.
- Keep `proof`, `yourturn`, and `TODO` editable in source.
- Use display equations for dense derivations; keep surrounding prose outside
  math mode.
- Use native math tokens instead of Unicode logic glyphs or LaTeX commands.
- Wrap a table in a captioned `figure` when it functions as a numbered or
  citable reference artifact.
- Preserve sources and URLs for adapted proofs, theorem statements, datasets,
  and external figures.

## Safe editing

1. Read the entrypoint and imported template before editing.
2. Keep package versions already established by the project unless a version
   change is part of the request.
3. Make the smallest coherent source change.
4. Compile using the repository's real root and entrypoint.
5. Inspect at least one representative rendered page or slide.
6. Check version-control status and avoid staging generated or unrelated files.

## Rendering commands

```sh
typst compile main.typ output.pdf --root .
typst compile main.typ "page-{p}.png" --root . --ppi 150
```

Use explicit paths appropriate to the project. Multipage PNG export requires a
page placeholder such as `{p}`.
