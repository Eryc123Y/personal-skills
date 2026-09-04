# Command routing and compatibility

Load only the command that matches the user's requested operation. These are bundled procedure references, not a requirement to install slash commands or an assumption that those commands exist in the active client.

## Scope before procedure

The current [skill entrypoint](../SKILL.md), user request, host permissions, and vault `AGENTS.md` qualify every command below. Older instructions to save automatically, write logs after reads, propagate everywhere, start agents, use Claude hooks, or impose an AI-first-only style do not expand scope. Read/search/audit requests remain read-only. Use the actual route map instead of the paths in examples.

Resolve bare `references/...`, `scripts/...`, and `commands/...` references from the skill root, not the vault or current shell directory. A tool or integration mentioned in a command must actually be available before it can be used. Do not install it implicitly.

- Ordinary lookup or a small edit can be completed from the entrypoint without loading a command.
- For specialized note operations, select the corresponding `obsidian-*` procedure below.
- Research/media procedures apply when the user requests that work for the vault. They do not require that unrelated research be saved, or authorize remote calls and expenses beyond the task.
- Bootstrap, scheduling, and command-generation procedures require the corresponding explicit request; consult [legacy integrations](legacy-integrations.md) before runtime changes.

## Available procedures

- [`create-command`](../commands/create-command.md): Create a new obsidian-second-brain command via interview - zero markdown editing required
- [`idea-discovery`](../commands/idea-discovery.md): Surface 3-5 next-direction candidates by reading ungraduated ideas, open project questions, and orphan research notes - what is worth working on next
- [`notebooklm`](../commands/notebooklm.md): Perform the requested source-grounded vault research using an available compatible integration; inspect legacy provider examples before use.
- [`obsidian-architect`](../commands/obsidian-architect.md): Scan a codebase and write a maintained set of architecture notes into the vault - overview, per-module notes, key decisions. Re-run to refresh without clobbering your edits
- [`obsidian-board-hygiene`](../commands/obsidian-board-hygiene.md): Inspect a board and perform only the requested triage or repairs; preserve unconfirmed task status.
- [`obsidian-board`](../commands/obsidian-board.md): Show or update a kanban board - flags overdue items, updates from conversation
- [`obsidian-brainstorm`](../commands/obsidian-brainstorm.md): Multi-turn Socratic brainstorm - one question per turn until the idea converges, then a design note with named alternatives and one recommendation
- [`obsidian-calendar`](../commands/obsidian-calendar.md): One calendar command with four modes - agenda (read a snapshot), reconcile (vault vs calendar gaps), meeting (event to note), schedule (task to event)
- [`obsidian-capture`](../commands/obsidian-capture.md): Capture the requested idea using the vault destination and authorized consistency updates.
- [`obsidian-catchup`](../commands/obsidian-catchup.md): Review and process everything captured on the go from the Telegram journal bot - voice, text, images, PDFs, links - waiting in the catchup queue. You pull it when you are back at the laptop; nothing is processed autonomously.
- [`obsidian-challenge`](../commands/obsidian-challenge.md): Red-team your current idea against your own vault history - finds contradictions, past failures, and flawed assumptions
- [`obsidian-connect`](../commands/obsidian-connect.md): Bridge two unrelated domains using your vault's link graph - forces creative friction to spark new ideas
- [`obsidian-daily`](../commands/obsidian-daily.md): Create or update today's daily note - pulls calendar events, overdue tasks, and conversation context
- [`obsidian-decide`](../commands/obsidian-decide.md): Answer a decision query read-only, or record the specified decision; use ADR detail when requested.
- [`obsidian-distill`](../commands/obsidian-distill.md): Condense a long note or source into key claims, each tagged with provenance back to the exact source block it came from
- [`obsidian-emerge`](../commands/obsidian-emerge.md): Surface unnamed patterns from your recent notes - recurring themes, hidden connections, and conclusions you haven't explicitly stated
- [`obsidian-export`](../commands/obsidian-export.md): Export a clean structured snapshot of the vault that any agent or tool can consume - flat JSON, markdown index, or an OKF (Open Knowledge Format) bundle
- [`obsidian-find`](../commands/obsidian-find.md): Smart vault search - returns results with context, not just filenames
- [`obsidian-graduate`](../commands/obsidian-graduate.md): Promote an idea fragment into a full project spec with tasks, board entries, and structure
- [`obsidian-health`](../commands/obsidian-health.md): Inspect the requested vault scope read-only and report substantiated findings; repair only when authorized.
- [`obsidian-ingest`](../commands/obsidian-ingest.md): Import the requested source with provenance; propose or apply related updates within the authorized scope.
- [`obsidian-init`](../commands/obsidian-init.md): Initialize a vault manual and supporting files when requested; use AGENTS.md and the existing routes, with legacy setup examples adapted before use.
- [`obsidian-learn`](../commands/obsidian-learn.md): Review recorded learnings and patterns; change or retire notes only within the requested scope.
- [`obsidian-log`](../commands/obsidian-log.md): Log this work or dev session to the vault - infers project from context
- [`obsidian-merge`](../commands/obsidian-merge.md): Merge two near-duplicate notes found by /obsidian-health into one - dry run by default, redirects the retired note rather than deleting it
- [`obsidian-panel`](../commands/obsidian-panel.md): Convene a panel of distinct perspectives on a decision - one independent verdict per lens, then a synthesis. A multi-persona complement to /obsidian-challenge
- [`obsidian-person`](../commands/obsidian-person.md): Create or update a person note from conversation context
- [`obsidian-project`](../commands/obsidian-project.md): Create or update the requested project note with relevant authorized consistency updates.
- [`obsidian-projects`](../commands/obsidian-projects.md): Live project status from git + local docs - infers all context from vault notes, no config required
- [`obsidian-recap`](../commands/obsidian-recap.md): Summarize a time period from the vault - today, week, or month
- [`obsidian-reconcile`](../commands/obsidian-reconcile.md): Find conflicting claims and their provenance; resolve only evidence-supported changes within the requested scope.
- [`obsidian-recurring`](../commands/obsidian-recurring.md): Track a recurring obligation (payment, filing, ops) with a cadence and a computed next-due date
- [`obsidian-reindex`](../commands/obsidian-reindex.md): Refresh the vault's semantic search index and report coverage before and after
- [`obsidian-retrieval-eval`](../commands/obsidian-retrieval-eval.md): Measure how well vault search finds the right note for a natural-language question - recall@k and MRR, with the concrete failures
- [`obsidian-review`](../commands/obsidian-review.md): Generate a structured weekly or monthly review note from vault history
- [`obsidian-save`](../commands/obsidian-save.md): Save the specified conversation material to the vault; a narrow save does not imply all-conversation capture.
- [`obsidian-synthesize`](../commands/obsidian-synthesize.md): Find patterns for the requested topic; write synthesis notes only when the user requests a saved result.
- [`obsidian-task`](../commands/obsidian-task.md): Record the requested task on the appropriate board; preserve uncertainty in priority and due date.
- [`obsidian-visualize`](../commands/obsidian-visualize.md): Generate a visual canvas map of your vault - see the shape of your second brain and how knowledge connects
- [`obsidian-world`](../commands/obsidian-world.md): Load your identity, values, priorities, and current state in one shot - with progressive context levels to avoid burning tokens
- [`podcast`](../commands/podcast.md): Extract requested podcast metadata, transcript, or summary; save a vault note when requested.
- [`research-deep`](../commands/research-deep.md): Research the requested vault topic with available authorized sources; save findings only within the requested scope.
- [`research`](../commands/research.md): Web research with citations - Perplexity Sonar when an API key is set, free key-less sources (Wikipedia, HackerNews, arXiv, Reddit, and more) otherwise. Deep dossier with summary, facts, timeline, players, contrarian views, open questions
- [`vault-deep-synthesis`](../commands/vault-deep-synthesis.md): Deep cross-reference of everything the vault knows about one topic - agreements, contradictions, stale claims, and coverage gaps. Pure vault, no network
- [`x-pulse`](../commands/x-pulse.md): Scan X for what's trending in a topic - themes, voices, hooks, and post ideas powered by Grok x_search
- [`x-read`](../commands/x-read.md): Deep-read an X (Twitter) post via Grok x_search - verbatim post, thread, TL;DR, claims, reply sentiment, voices to watch
- [`youtube`](../commands/youtube.md): Inspect a requested YouTube video using available tools; save a vault note when requested, with visual analysis when relevant.
