---
description: Create Command for the user-requested vault task using available host tools.
category: meta
triggers_en: ["create command", "new command", "add a command", "scaffold a command"]
triggers_es: ["crea un comando", "nuevo comando", "añade un comando", "hazme un comando nuevo", "arma un comando"]
triggers_pt: ["crie um comando", "novo comando", "adicione um comando", "gere um comando"]
triggers_zh: ["创建一个新命令", "新增 Obsidian 命令", "帮我写个命令", "生成命令模板"]
---



# create-command

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Create or update a procedure for the user-requested operation. Capture its trigger, input, expected output, read/write scope, and relevant resources. Follow the current host's skill format and the CC Switch managed source workflow. Preserve existing authorization and do not invent mandatory interviews. This package has no platform adapter builder; do not build or install commands into client directories automatically.
