# Source and package notes

This skill is a Codex-oriented adaptation of [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain), distributed under the included [MIT license](LICENSE), copyright 2026 Eugeniu Ghelbur. The package was prepared from an installed upstream snapshot; its exact upstream commit is not recorded, so this is not represented as a pristine tagged release.

The adaptation shortens the entrypoint, makes the current vault's AGENTS.md and route map authoritative within host/user instructions, separates read-only requests from authorized writes, and replaces unconditional background activity with requested operations. Specialized command and schema material is retained as selectively loaded guidance. Provider-specific research and setup commands are adapted to available host tools instead of assuming an installed legacy runtime.

## Package boundary

Included: the entrypoint, 47 command references, relevant note/schema references, nine local Python helpers, and their license. The helpers retain upstream behavior; inspect flags, exclusions, and output destinations before using them. Some helpers write files or inspect Git history. Selecting a command does not authorize running a helper with side effects outside the user's request.

Not included: Claude hooks, client adapters, installers, integration servers, provider research runtimes, semantic-index runtimes, media assets, tests/fixtures, credentials, environment files, and caches. These are not needed for ordinary filesystem note work. Research and media operations use the host's available tools; no service is installed automatically. A missing integration is a capability limitation to explain, not a reason to claim the operation succeeded.

## Runtime requirements

The retained scripts require Python 3.10 or newer. `export_okf.py` and its dependent `merge_notes.py` require PyYAML; use an existing environment with `PyYAML>=6` when running them. Other selected helpers use the standard library and included sibling modules. The optional upstream `star_prompt` module is intentionally omitted; `vault_health.py` catches its `ImportError`, so the non-JSON star solicitation and its user-config marker write are skipped. Architecture and commit-decision inspection may require Git and an appropriate local repository. No dependency installation or helper execution is performed by loading this skill.

Validation for this package is structural: skill frontmatter, relative documentation links, Python syntax/import closure, retained-file license, and visible credential/path screening. No live vault workflow, provider call, scheduled task, or installer was run during packaging.

When maintained through CC Switch, change the configured source and synchronize through that manager. Do not maintain separate hand-edited client copies.
