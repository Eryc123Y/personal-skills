---
description: Obsidian Retrieval Eval for the user-requested vault task using available host tools.
category: meta
triggers_en: ["evaluate retrieval", "how good is my vault search", "retrieval eval", "test vault search quality", "measure find quality"]
triggers_es: ["evalúa la búsqueda", "qué tal funciona la búsqueda de mi vault", "evaluación de recuperación", "prueba la calidad de la búsqueda", "comprueba si encuentra bien mis notas"]
triggers_pt: ["avalie a recuperação", "quão boa é a busca do meu vault", "avaliação de recuperação", "teste a qualidade da busca do vault", "meça a qualidade da busca"]
triggers_zh: ["测试知识库搜索效果", "评估检索质量", "看看我的笔记好不好找", "测量语义搜索召回率", "检查搜索能不能找到正确笔记"]
---



# obsidian-retrieval-eval

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Evaluate the actual available vault search against representative questions and known relevant notes. Agree on or use the requested scope, preserve excluded folders, and report ranking failures with recall or reciprocal-rank measures only when the test data supports them. Store cases and results only at an authorized location; never put private vault excerpts in a distributable skill package. The upstream MCP search and evaluation runtime are not included; a bounded manual evaluation is valid when clearly labeled.
