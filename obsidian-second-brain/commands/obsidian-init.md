---
description: Obsidian Init for the user-requested vault task using available host tools.
category: meta
triggers_en: ["init vault", "bootstrap vault", "setup vault", "scan vault"]
triggers_es: ["inicializa el vault", "arranca el vault", "configura el vault", "escanea el vault", "inicia el vault", "deja listo el vault"]
triggers_pt: ["inicialize o vault", "bootstrap do vault", "configure o vault", "escaneie o vault"]
triggers_zh: ["初始化知识库", "为这个知识库生成初始配置", "扫描并配置我的知识库", "生成知识库操作手册"]
---



# obsidian-init

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Initialize a vault only when explicitly requested. Inspect existing files, user preferences, and any route map first. Create or update AGENTS.md and only the supporting index/templates the requested setup needs; preserve existing content and the manager's runtime directories. Use local templates where available. Do not bootstrap legacy folders, overwrite a manual, install hooks, migrate logs, or create schedules automatically. For integration boundaries read [legacy integrations](../references/legacy-integrations.md).
