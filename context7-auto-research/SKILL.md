---
name: context7-auto-research
description: Use for an explicit request to check current documentation, API usage, or version-specific behavior of a named library or framework. Do not trigger for ordinary file reading, general coding, or an unscoped create/build request.
metadata:
  version: 1.0.3
  author: BenedictKing
  user-invocable: true
---

# Context7 documentation lookup

Use this skill when the user names a library/framework and asks for current documentation, API details, setup guidance, or a code example whose correctness depends on the current version. A mere `.py`, `package.json`, or repository mention is not enough. Prefer the official documentation or an available Context7 MCP tool when it is discoverable in the current session.

## Routing

1. Identify the library, requested API/topic, and version if supplied.
2. Check whether a Context7 tool is actually available. Do not invent a tool name or assume an MCP server is installed.
3. If the local helper exists, use it as a fallback:

```bash
node <skill-directory>/context7-api.cjs search "<library>" "<query>"
node <skill-directory>/context7-api.cjs context "<library-id>" "<query>"
```

The helper supports only `search` and `context`; inspect its output and select the returned library ID before requesting context. Keep queries focused and do not expose secrets in them.

4. If the tool/helper is unavailable, errors, or returns no useful result, say so briefly and use an authoritative source available in the session or clearly label knowledge as potentially stale. Never claim a Context7 lookup occurred when it did not.
5. Apply the documentation to the user's question, preserving version qualifiers and linking/citing the source when the interface permits it.

Mere reading or editing of a local file does not itself require a lookup; fetch when the user requests it or correctness depends on an uncertain or version-sensitive API. Do not write files, install packages, or change project configuration merely because this skill triggered.
