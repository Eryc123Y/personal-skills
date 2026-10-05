# Planning a math or science explainer

Plan before narration, and narration before code. The output is `plan.md`
in the film's working directory, unless the host project already keeps
outlines or scripts, in which case follow its documents.

## Settle these first

Ask only what the request and the project leave open:

- **Claim**: the one sentence a viewer should be able to repeat afterwards.
  If there are two, there are two videos.
- **Audience**: what they already know (school algebra, first-year calculus …).
  Every symbol beyond that needs an on-screen definition.
- **Length**: about 150 to 200 spoken Chinese characters per minute of a calm
  explainer. A 3-minute piece teaches one idea well.
- **Form**: standalone video, or a clip inside a larger film (then match its
  resolution, frame rate, palette and narration voice).

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

For each scene in `plan.md`:

```markdown
## 3 · remainder  (~35 s)
Purpose: show why the error shrinks near a and grows away from it
Narration ids: remainder_1 … remainder_4
Visual: sin x and P₃(x) on shared axes; shaded gap between them; tracker x moves away from a
Math on screen: R₃(x) = f(x) − P₃(x); the bound |R₃| ≤ M|x−a|⁴/4!
Transition in/out: P₃ curve carried over from scene 2; ends on the shaded gap only
```

Checks before writing narration:

- Every "so" or "therefore" has its premise on screen or in an earlier line.
- One visual idea per scene; one focus color at a time.
- The same object keeps the same name in narration, labels and subtitles.
- Every number and identity that will appear is verified (compute it, do not
  trust memory). A wrong number on screen is the worst failure.
- Concrete before abstract: show one example before the general formula.

Then write the narration as `lines.txt` (`id | text`), short spoken sentences,
and build timings (timing.md).
