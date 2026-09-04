---
description: Notebooklm for the user-requested vault task using available host tools.
category: research
triggers_en: ["notebooklm", "research grounded", "ground research in vault", "ask my notebook", "source-grounded research"]
triggers_es: ["notebooklm", "investigación fundamentada en mis notas", "basa esto en mi vault", "pregúntale a mis notas", "investigación con fuentes propias", "investiga en mis notas"]
triggers_pt: ["notebooklm", "pesquisa ancorada", "ancore a pesquisa no vault", "pergunte ao meu notebook", "pesquisa ancorada em fontes"]
triggers_zh: ["用我的资料做研究", "基于知识库回答", "问问我的笔记", "做有来源依据的研究", "用 NotebookLM 研究"]
---



# notebooklm

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Use an available NotebookLM integration when the user requests it, or analyze the provided sources directly when that satisfies the task. Do not substitute another product merely because its model is Gemini. State any unavailable integration. Ground claims in accessible sources and save to the vault only within the requested scope. No bundled Gemini File Search runtime is included.
