# ARA Structural Validation

Validate the selected project contract first. This checklist is a fallback for
new artifacts using the bundled paper-oriented schema; it does not migrate or
invalidate a different established ARA layout.

## Structure and coverage

- Parse YAML/frontmatter and check the fields required by the selected schema.
- Ensure the manifest indexes the files actually produced, including the source
  set, requested coverage, omissions, and unavailable evidence.
- For the default layout, check PAPER.md, the applicable logic files, source
  environment, trace, and evidence index. A section with no source support may
  state that limitation; do not manufacture content to populate a template.
- There are no minimum counts for concepts, experiments, alternatives, or trace
  nodes. Code files are required only when the requested artifact includes code.

## Claim and protocol bindings

- Each claim has a statement, status, scope, evidence basis, and falsification
  criteria appropriate to its type. Separate supported findings from hypotheses.
- Referenced claim and experiment identifiers resolve to the intended entities.
- Experiment protocols distinguish proposed work from completed evaluations;
  exact measured results retain source bindings in evidence.
- Conditions needed to interpret a result (split, baseline, configuration,
  metric, uncertainty) are recorded when available, otherwise marked missing.

## Visual and tabular evidence

- Each included object has a precise source locator and extraction method.
- Preserve complete source tables when claiming full extraction; label subsets.
- Preserve figure images/crops when available, with type and reading uncertainty.
  If an image is unavailable, record the limitation instead of fabricating one.
- Quantitative estimates use approximate notation and an identified extraction
  method. Qualitative images and diagrams do not require invented numeric tables.
- For full-paper coverage, inventory every numbered table and figure. For partial
  coverage, name the included scope and exclusions. Uninspected evidence is not
  verified merely because its caption or reference is present.

## Trace and provenance

- Parse trace YAML, resolve cross-edges, and reject duplicate IDs or cycles.
- Check fields for each applicable node type against the selected schema.
- Historical decisions, pivots, failures, and experiments have direct source
  support. Ablation weakness alone does not establish that a route was abandoned.
- Keep AI interpretations visibly distinct from observed or user-adopted events.
- An empty trace is acceptable when the available sources reveal no journey.

## Verification and reporting

- Check local file references and observed line locations; do not invent locators.
- Recompute derived values when inputs are available and relevant to the claim.
- Run the project's validator when available, recording its scope and outcome.
  A manual checklist is not an executed validator or scientific validation.
- Repair failures within the authorized artifact work. Report unresolved errors,
  missing dependencies, incomplete coverage, and unverified interpretations.
  Do not describe an artifact as passing checks that were not completed.
