---
description: Obsidian Reindex for the user-requested vault task using available host tools.
category: meta
triggers_en: ["reindex vault", "rebuild semantic index", "refresh semantic search", "update vault embeddings"]
triggers_es: ["reindexa el vault", "reconstruye el índice semántico", "actualiza la búsqueda semántica", "actualiza los embeddings del vault"]
triggers_pt: ["reindexe o vault", "reconstrua o índice semântico", "atualize a busca semântica", "atualize os embeddings do vault"]
triggers_zh: ["重建知识库索引", "刷新语义搜索", "更新笔记向量", "重新索引我的知识库"]
---



# obsidian-reindex

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Refresh an existing vault search index only when requested, using the actually configured indexing tool. Inspect its input scope, excluded folders, cache/output location, and side effects before running it. This package does not include a semantic-index service; if none is available, explain that limitation and use direct search for ordinary lookup. Do not install or create an index as a side effect of a read request.
