# Source and changes

Design conventions are adapted from [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers), reviewed at commit `b709de1` (2026-10-19). That repository is licensed CC BY-NC 4.0; its license is included as [LICENSE-figures4papers](LICENSE-figures4papers). The parts derived from it are `references/style-guide.md` (rewritten from the upstream `design-theory.md` and `common-patterns.md`) and the palette values in `PALETTE`. These derived parts are shared under the same non-commercial terms, with attribution.

Local work, 2026-10-31:

- `scripts/paperfig.py` was written independently against the upstream API description. No upstream plotting script was copied; the upstream repository ships no helper module.
- Main changes from the upstream style:
  - figures are sized at true column width;
  - PDF fonts are embedded as TrueType;
  - bars start at zero;
  - layout is constrained;
  - error bars and bands are added;
  - an Okabe-Ito palette is added.
  The reasons are in `references/style-guide.md`.
- The skill entrypoint, tests and examples are new.

Do not use the derived material in commercial products. Review upstream changes before adopting them here.
