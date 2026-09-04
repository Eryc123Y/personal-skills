---
description: Run a vault health check - grouped by severity, detects contradictions, concept gaps, stale claims, and structural issues
category: meta
triggers_en: ["vault health", "check vault", "audit vault", "vault diagnostics"]
triggers_es: ["salud del vault", "revisa el vault", "audita el vault", "diagnóstico del vault"]
triggers_pt: ["saúde do vault", "verifique o vault", "audite o vault", "diagnóstico do vault"]
triggers_zh: ["检查知识库健康状况", "给我的知识库做体检", "审计我的笔记库", "诊断知识库问题"]
---



# Vault health

Inspect the requested vault scope and return findings. This command is read-only unless the user requests specific repairs or a saved report; it does not append an operation log after an audit.

1. Resolve the vault, read its `AGENTS.md`, route map, and required context. Apply the vault's excluded runtime folders and the user's scope before scanning.
2. Choose a focused manual inspection or one appropriate scanner. Inspect the scanner's flags and side effects first. The bundled `scripts/vault_health.py --path <vault> --json` can supply structural findings when its exclusions and checks match this vault; it is optional, not a reason to install dependencies. Use an existing environment if available.
3. Triage relevant findings against actual notes and local conventions:
   - A wanted link can be an intentional future note. Report its context rather than creating a page to eliminate the count.
   - Confirm duplicates represent the same entity or claim; dated report series are not automatically duplicates.
   - Assess frontmatter and taxonomy against the vault's schemas. For code-fence-wrapped notes, a later authorized repair should unwrap the fence rather than add a second frontmatter block.
   - Distinguish dated overdue tasks from undated open work. Preserve conflicting claims with their sources and dates.
   - Use freshness or typed-edge checks only if relevant to the requested audit and the vault uses those conventions. Inspect helper side effects before execution; do not run provider-backed triage or remote research by default.
4. Group substantiated findings by severity and include note links, evidence, search limits, and proposed repairs. Adjust severity to the practical impact rather than automatically treating every formatting issue as critical.

For large or noisy results, narrow the current inspection using the route map and report the coverage. Do not change `.vault-config.json` or any persistent exclusion settings to make the report cleaner unless requested.

A single agent normally handles a bounded audit. Delegate disjoint read-only inspections only when delegation is authorized and useful; a category list is not a requirement to launch subagents.

If repairs are authorized, modify only that scope, follow [note operations](../references/codex-note-operations.md), and verify the actual changes. Apply existing user authorization without redundant confirmation. Report actions outside that scope rather than merging, archiving, rewriting claims, creating notes, or refreshing indexes automatically.
