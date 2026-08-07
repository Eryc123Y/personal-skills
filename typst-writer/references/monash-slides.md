# Unofficial Monash Touying slides

Use Eric's package for new academic talks, research updates, FYP presentations,
and Monash-aligned teaching decks.

## Remote preamble

```typst
#import "@preview/unofficial-monash-touying:0.1.2": *

#set text(font: ("Arial", "New Computer Modern"))

#show: monash-theme.with(
  config-info(
    title: [Presentation Title],
    short-title: [Short Title],
    subtitle: [Subtitle],
    author: [Eric Yang],
    institution: [Monash University],
    date: datetime.today(),
  ),
)

#show: show-monash-frames
#title-slide()
```

Do not import Touying separately for normal use. The package re-exports the
common authoring API.

## Authoring model

- Level-one headings create sections and section dividers.
- Level-two headings create ordinary slides.
- Use `#slide[...]` for one-off manual layouts.
- Use `#pause`, `#uncover`, `#only`, and `#meanwhile` through the package export.
- Use `definition`, `theorem`, `lemma`, `corollary`, `proof`, `remark`, `note`,
  and `warning` for academic frames.
- Set `toc: false` in `monash-theme.with(...)` when the deck should not insert
  an outline after the title slide.

## Two columns

```typst
#slide(composer: (1fr, 1fr))[
  *Question*

  What changes under distribution shift?
][
  *Evaluation*

  - compare with the baseline
  - show one failure case
  - state one takeaway
]
```

## Title graphics

Pass project-owned assets as content. Do not reference an image inside the
installed skill:

```typst
#let title-background = image(
  "assets/title-background.png",
  width: 100%,
  height: 100%,
  fit: "cover",
)

#show: monash-theme.with(
  titlegraphic: title-background,
  config-info(title: [Presentation Title]),
)
```

Use only logos or marks the project is authorized to use.

## Slide discipline

- Keep one main claim per slide.
- Prefer a strong heading and one visual or compact evidence block over dense
  prose.
- Use the package's square and nested triangle bullets instead of redefining
  list markers.
- Use `show-monash-frames.with(numbering: false)` only when visible frame
  numbering is undesirable.
- Verify title slides, section dividers, content slides, two-column layouts,
  code blocks, and frame-heavy slides in the rendered PDF.
