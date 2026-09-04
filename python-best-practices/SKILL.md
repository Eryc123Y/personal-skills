---
name: python-best-practices
description: Use while implementing or reviewing Python code, pyproject.toml, or Python dependency configuration. Do not trigger for merely reading a Python file or for non-Python work.
---

# Python best practices

Apply these as proportionate implementation and review guidance. Follow the repository's local contract and the user's requested style first; this skill covers Python-specific decisions and does not replace project tests, security review, or domain guidance.

## Types and state

- Prefer precise annotations and small domain types. Use `Literal`, `NewType`, `Protocol`, and discriminated unions when they make invalid states harder to represent.
- Use frozen dataclasses for immutable value objects when mutation is not part of the design.
- Keep public functions explicit about inputs, outputs, and failure behavior. Avoid `Any` and untyped dictionaries at boundaries when a typed model is practical.

## Errors and logging

- Catch only errors you can handle. When translating an exception, preserve the cause with `raise ... from err`.
- Use a module-level logger and deferred `%s` formatting. Do not log secrets, tokens, or sensitive payloads.
- Prefer deterministic, side-effect-light functions; make I/O and external calls visible at the boundary.

## Verification

- Run the smallest meaningful formatter, linter, type checker, and tests required by the repository. Do not invent a tool or claim a check ran when it is unavailable.
- For `pyproject.toml` or dependency changes, inspect the project's supported Python version and lockfile workflow before editing.
- Use `uv`, `pyright`, `mypy`, `ruff`, or `ty` only when the project already uses them or the user requests them; do not install tools solely because this skill loaded.

These are defaults, not a reason to rewrite an existing module or force a style-only change during a read-only task.
