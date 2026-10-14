# Planning a math or science explainer

Confirm unresolved narration, integration, duration, and output requirements
using the skill entrypoint before choosing the workflow. Reuse settled choices.
For narrated explainers, plan before narration and align final code to real
audio. For silent animations, plan visual states and durations without a script
or voice track. Embedded clips follow the host's cues even when exported silent.
Use the project's existing planning documents; a short standalone animation
can use a brief inline plan rather than requiring a separate `plan.md`.

## Settle these first

Ask only what the request and the project leave open:

- **Claim**: the one sentence a viewer should be able to repeat afterwards.
  A short silent loop can instead have a clear visual behavior to demonstrate.
- **Audience**: what they already know (school algebra, first-year calculus …).
  Every symbol beyond that needs an on-screen definition.
- **Length**: use the requested duration. For narrated work only, about 150 to
  200 spoken Chinese characters, or about 120 English
  words, per minute of a calm explainer (Gemini's Charon voice reads English
  at 120–125 wpm). Derivations need extra time on screen beyond the narration.
  A 3-minute piece teaches one idea well.
- **Form**: standalone video, or a clip inside a larger film (then match its
  resolution, frame rate, palette and any existing narration voice).

## Shape the argument

Pick one spine; combinations are fine:

| Spine | Use when |
|---|---|
| Puzzle → investigation → principle | a result looks wrong or surprising |
| Pieces → assembly → payoff | the idea is built from simple parts (Fourier, networks) |
| View A + view B → same thing | algebraic and geometric pictures coincide (dot product, determinant) |
| Naive → fails → repaired | a common misconception is the obstacle (limits, probability) |
| Example → pattern → generalisation | the abstraction is easier after one concrete case |
| How it was discovered | the history explains why the definition looks the way it does |

Emotional beats to place deliberately: curiosity (opening question),
friction (this is harder than it looks), partial clarity, the "aha", and a
resolved final frame.

## Plan per scene

For a narrated scene, the following is an optional planning format. For silent
scenes, replace narration IDs with visual events and their intended durations:

```markdown
## 3 · remainder  (~35 s)
Purpose: show why the error shrinks near a and grows away from it
Narration ids: remainder_1 … remainder_4
Visual: sin x and P₃(x) on shared axes; shaded gap between them; tracker x moves away from a
Math on screen: R₃(x) = f(x) − P₃(x); the bound |R₃| ≤ M|x−a|⁴/4!
Transition in/out: P₃ curve carried over from scene 2; ends on the shaded gap only
```

Checks before coding or writing narration, as applicable:

- Every "so" or "therefore" has its premise on screen or in an earlier line.
- One visual idea per scene; one focus color at a time.
- The same object keeps the same name in narration, labels and subtitles.
- Every number and identity that will appear is verified (compute it, do not
  trust memory). A wrong number on screen is the worst failure.
- Concrete before abstract: show one example before the general formula.

For narrated work, write or reuse `lines.txt` (`id | text`) and build timings
(timing.md). For silent work, proceed with the visual timing plan. For embedded
clips, reuse the host timeline and generate narration only when requested.
