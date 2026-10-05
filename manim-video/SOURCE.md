# Source and changes

Newly authored on 2026-10-05. No upstream file is redistributed: the
instructions, template and scripts were written for this repository. Three
public skills were reviewed as design references:

| Reviewed | Commit | License | What informed this skill |
|---|---|---|---|
| [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) (`manim-composer`, `manimce-best-practices`) | `cef04501` | MIT | Plan-before-code scene planning; narrative spines; topic coverage of the API rules |
| [Yusuke710/manim-skill](https://github.com/Yusuke710/manim-skill) | `0e9c9c86` | MIT | Narration → TTS → timings → code order; one class per scene with selective re-render; `add_subcaption` for sidecar subtitles |
| [liangdabiao/math-concept-film](https://github.com/liangdabiao/math-concept-film) | `e46ad0e4` | none stated | Ideas only: frame checks before and after each spoken cue, and the practice of keeping a pitfalls list. No text or code was copied |

Local design differences:

- Timing is anchored to absolute segment starts (`TimedScene.until`) instead of
  hand-summed budgets or a static simulator. This handles per-animation frame
  rounding, which differs between 15 fps previews and 60 fps finals.
- Chinese is first-class: `Text` with an explicit CJK font, and `MathTex` with
  a XeLaTeX + ctex template instead of avoiding LaTeX.
- The skill takes timings from the host project's own narration pipeline when
  one exists, and works as an embeddable component (silent or transparent clips).
- The pitfalls in `references/manimce-0.21.md` were re-verified on Manim CE 0.21.0.
  Upstream examples that use ManimGL APIs under a CE label were excluded.

This maintained version is distributed through personal-skills and installed
by CC Switch.
