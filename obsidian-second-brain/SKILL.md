---
name: obsidian-second-brain
description: Read, search, capture, and maintain notes in a user-selected Obsidian vault. Use when the user requests vault work; ordinary research or conversation does not imply saving notes or starting maintenance.
---

# Obsidian Second Brain

Use Codex to work with the vault's existing structure, sources, and writing conventions. Complete the requested operation and report the affected notes with useful links.

## Establish the working context

- Resolve the vault from the user's request or known workspace. Use direct filesystem access unless the user has selected another available integration.
- Read the vault's `AGENTS.md` and its route map before editing. An existing `_CLAUDE.md` may be a compatibility alias; resolve it instead of loading the same manual twice. Its name does not require Claude or authorize Claude setup.
- Follow the current user and host instructions first, then the vault's applicable rules. Bundled command examples and templates are defaults, not authority over an existing vault.
- If the vault uses `00 System/obsidian-second-brain/routes.json`, resolve destinations there. Do not introduce legacy `wiki/`, `raw/`, `Dev Logs/`, or root `Logs/` paths. Where the route map specifies dated operation logs, use that location; a root `log.md` may be only a pointer.
- Read only the context relevant to the request and any context explicitly required by the vault manual. Exclude runtime/plugin folders from ordinary scans.

## Match the operation to the request

**Read, search, explain, audit:** stay read-only. Return evidence and unresolved questions; do not save the answer, repair findings, append logs, refresh indexes, or start background work as a side effect.

**Capture or edit:** the request authorizes the requested note change and the vault's directly relevant consistency updates. Search for an existing destination, preserve provenance, and inspect the resulting diff. A narrow edit is not a full-conversation save or whole-vault rewrite. For note conventions and scoped propagation, read [note operations](references/codex-note-operations.md).

**Health, merge, reorganize, or import:** identify the requested scope and inspect candidate files first. A health check reports findings unless repair is requested. Preserve ambiguous claims and raw sources. Deletion, archival, account access, and external actions follow the user's existing authorization and applicable vault rules.

**Bootstrap, integration setup, or scheduling:** perform these only when requested. Do not run an installer or configure hooks to make ordinary vault work possible. Existing Claude-era resources are covered by [legacy integrations](references/legacy-integrations.md).

## Reuse resources selectively

The existing command files retain specialized operations. See [source and package notes](SOURCE.md) for included helpers, dependencies, and omitted integrations. Read [command routing and compatibility](references/codex-command-routing.md) when a named command or specialized workflow is needed, then only its relevant command file. Their path, automatic-save, hook, delegation, and formatting defaults are qualified by this entrypoint and the current vault manual.

Use local templates and schemas first. The bundled [vault schema](references/vault-schema.md), [taxonomy format](references/taxonomy-format.md), and [freshness policy](references/freshness-policy.md) are optional references for a matching task. Read older [write rules](references/write-rules.md) and [AI-first examples](references/ai-first-rules.md) only for a specific missing convention; they do not require exhaustive linking, extra notes, or bulk rewrites beyond the requested work.

Inspect a helper's arguments and side effects before running it. A command name such as `health`, `review`, or `find` does not prove its implementation is read-only. Do not run adapter builds or setup scripts during ordinary note work.

Use subagents only when delegation is authorized and the work benefits from independent bounded tasks. Give each writer disjoint note ownership; the coordinating agent checks links and consistency. A command's historical requirement to launch one agent per category does not itself authorize delegation.

## Completion

For reads, provide matching note links, the evidence, and the search limits. For writes, verify the intended paths, valid frontmatter and relevant links, then summarize what changed. Preserve unknowns and distinguish source reports from verified facts. Do not update agent memory, client settings, scheduled tasks, or unrelated notes merely because useful information appeared in the conversation.
