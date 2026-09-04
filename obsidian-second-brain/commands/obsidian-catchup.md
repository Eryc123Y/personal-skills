---
description: Obsidian Catchup for the user-requested vault task using available host tools.
category: vault
triggers_en: ["catch up", "catchup", "what did I dump from telegram", "process my captures", "go through my telegram dumps", "anything new from the phone", "process my catchup", "review what I captured", "what did I capture on the go"]
triggers_es: ["ponme al día", "qué mandé por telegram", "procesa mis capturas", "revisa lo que capturé desde el móvil", "hay algo nuevo del móvil", "repasa mi cola de capturas"]
triggers_pt: ["coloque em dia", "catchup", "o que eu despejei do telegram", "processe minhas capturas", "passe pelas minhas capturas do telegram", "tem algo novo do telefone", "processe meu catchup", "revise o que capturei", "o que capturei na correria"]
triggers_zh: ["看看我从手机记了什么", "处理 Telegram 收集箱", "整理我路上记的东西", "整理待处理的随手记录", "把最近随手记的内容过一遍"]
---



# obsidian-catchup

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Review the existing capture queue the user identifies or the route map specifies. A request to inspect the queue is read-only. When asked to process captures, preserve source provenance, deduplicate against existing notes, and move or mark queue items only within the authorized scope after verifying their destination notes. Use available tools for supported attachments; report unsupported content. This package does not install a Telegram bot or process a queue in the background.
