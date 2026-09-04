---
description: Obsidian Find for the user-requested vault task using available host tools.
category: vault
triggers_en: ["find in vault", "search my notes", "where is", "what did I write about"]
triggers_es: ["busca en el vault", "busca en mis notas", "dónde está", "qué escribí sobre", "tengo algo sobre"]
triggers_pt: ["encontre no vault", "pesquise minhas notas", "onde está", "o que eu escrevi sobre"]
triggers_zh: ["在知识库里找一下", "搜索我的笔记", "我之前在哪篇笔记里写过", "我写过关于这个吗"]
---



# obsidian-find

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Search the requested vault scope using file names, aliases, note titles, and relevant content. Follow the route map and exclude runtime folders. Read the strongest matches, try focused synonyms if needed, and return note links with supporting context. Explain the search scope before claiming absence. This operation is read-only; do not create notes, refresh indexes, log the search, or configure an integration. MCP and semantic-index servers are not included.
