# Legacy integrations and setup

Read this only for an explicit setup, migration, integration audit, or scheduling request. Loading this skill does not configure a runtime or activate a background process.

This package contains the Codex-oriented note workflow and selected local helpers. Claude hooks, adapter builds, installers, MCP and Telegram servers, provider research scripts, and semantic-search services are not included. Their upstream implementations are historical compatibility resources at [the upstream repository](https://github.com/eugeniughelbur/obsidian-second-brain), not local prerequisites or instructions to fetch and execute them.

SessionStart, PostCompact, and PostToolUse are Claude integration mechanisms, not Codex capabilities. Do not configure them, start a headless Claude subprocess, or alter permission settings during ordinary note work. An existing `_CLAUDE.md` in a vault can be an alias or older manual; prefer the current `AGENTS.md` and do not overwrite it from an old template.

CC Switch owns this installation's distribution and unified entrypoint. Preserve its configured source, enablement, and synchronization method. Do not replace client symlinks, install a second copy, or generate adapters into client directories unless that installation work is explicitly requested and reconciled with CC Switch.

For requested scheduling, use the host's supported interface and the user's cadence, scope, and notification preferences. Inspect an existing automation before creating a duplicate. The absence of a configured hook is not evidence of a running background process.
