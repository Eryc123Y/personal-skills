---
name: skill-evaluation
description: Evaluate an existing skill with representative requests and observable
  outcomes when comparative testing or trigger-quality assessment is requested. Use
  the host skill-creator for ordinary skill creation and edits.
---

# Skill evaluation

Use the host's skill-creator for ordinary skill authoring. This supplementary skill covers comparative evaluation and trigger quality; a small edit does not automatically require a benchmark.

Select a few representative requests covering intended use, nearby requests that should not trigger, and a meaningful edge case. Judge task completion, correctness, scope, unnecessary questions, and tool use. Keep inputs and available tools comparable; record model/settings when known. Do not infer measured token or latency improvements from shorter Markdown alone.

Run bounded cases in an isolated workspace when behavioral execution is justified and authorized. For independent lookup or first-pass review, a user-preferred lightweight agent may help; the primary agent chooses cases and accepts results. Do not spawn a fixed batch of agents or prescribe a reasoning level for every evaluation. If execution cannot be performed, report a static review rather than a behavioral pass.

For an output review, compare actual artifacts against task requirements and cite the evidence for each failure. For an A/B comparison, hide the version labels from the reviewer when practical. Inspect differences after judging task completion, and separate style preferences from correctness. No external runners are bundled or required; use only the host's available execution tools.

Make changes supported by observed failures, then rerun affected cases. Report which behavior was actually exercised, unresolved failures, and any remaining uncertainty. Preserve the user's skill manager and source-of-truth layout when applying an approved change.
