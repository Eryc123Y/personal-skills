---
description: Record decisions - lightweight by default (logged to project notes), or a full ADR record with --formal
category: thinking
triggers_en: ["extract decisions", "log decisions", "what did we decide", "log this decision", "ADR", "record decision", "decision record"]
triggers_es: ["saca las decisiones de esta conversación", "registra las decisiones", "¿qué decidimos?", "anota esta decisión", "ADR", "acta de decisión formal"]
triggers_pt: ["extraia decisões", "registre decisões", "o que decidimos", "registre esta decisão", "adr", "registrar decisão", "registro de decisão"]
triggers_zh: ["记录这个决定", "我们刚才决定了什么", "把这些决策整理出来", "生成决策记录", "写一份 ADR"]
---



# Decision records

Use the current [skill entrypoint](../SKILL.md) and the vault's routes and conventions.

A request such as "what did we decide?" asks for an answer and remains read-only. A request to record a decision authorizes that specified decision and destination. Do not extract unrelated decisions from the whole conversation or update other notes solely because the command was selected.

## Lightweight record

1. Identify the requested decision, its date, rationale, and source. Separate an accepted decision from a proposal or unresolved option.
2. Search for its existing project or decision note. Use the user-specified destination when provided; otherwise resolve the appropriate note through the vault's routes and conventions.
3. Add or update a concise dated entry in that note, preserving the earlier history where the decision supersedes something. Link relevant existing notes and sources; do not invent alternatives or outcomes.
4. Apply only directly relevant consistency updates that fall within the user's authorized scope and vault rules. An "only this file" instruction means no daily note, index, operation log, or board change; mention any necessary follow-up outside that scope.
5. Verify the intended diff and report the note link and decision recorded. For a read-only question, return the answer with supporting note links instead.

## Formal record

Use a fuller ADR when the user asks for `--formal`, an ADR, or equivalent detail. Read an existing local ADR template if available. Capture context, options considered, the decision, rationale, consequences, status, and sources to the extent the evidence supports them. Missing information remains explicitly unknown; the template is a guide rather than a reason to invent details or require another round of questions.

A formal record does not automatically authorize an additional index, daily entry, log, or structure change. Use the requested destination and the same scope and verification rules as the lightweight record.
