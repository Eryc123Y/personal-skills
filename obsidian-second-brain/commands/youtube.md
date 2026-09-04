---
description: Youtube for the user-requested vault task using available host tools.
category: research
triggers_en: ["summarize youtube", "youtube transcript", "extract video", "youtube to vault", "watch this video", "what's on screen in this video"]
triggers_es: ["resume este vídeo de youtube", "transcripción de youtube", "extrae este vídeo", "youtube al vault", "mira este vídeo", "qué se ve en este vídeo"]
triggers_pt: ["resuma este vídeo do youtube", "transcrição do youtube", "extraia este vídeo", "youtube para o vault", "assista a este vídeo", "o que aparece neste vídeo"]
triggers_zh: ["总结这个 YouTube 视频", "提取视频字幕", "把这个视频整理进知识库", "这个视频讲了什么", "看看视频画面里有什么"]
---



# youtube

Follow [the skill entrypoint](../SKILL.md), the current request, and the vault's applicable rules.

Inspect the requested video's available metadata, transcript, and relevant frames using supported host tools. Attribute transcript claims and distinguish them from direct visual observations. Match summary depth to the request. Explain unavailable video/transcript access without fabricating content. Save a routed vault note only when requested. The upstream media/provider scripts are not included.
