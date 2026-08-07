// Example only. New decks should reproduce this remote import rather than
// importing this file from the installed skill.

#import "@preview/unofficial-monash-touying:0.1.2": *

#set text(font: ("Arial", "New Computer Modern"))

#show: monash-theme.with(
  toc: false,
  config-info(
    title: [Research Update],
    short-title: [Update],
    subtitle: [Question, evidence, and next decision],
    author: [Eric Yang],
    institution: [Monash University],
    date: datetime.today(),
  ),
)

#show: show-monash-frames
#title-slide()

= Motivation

== Research question

State one question and one reason it matters.

- keep the claim visible
- show the strongest evidence
- name the remaining uncertainty

== Method and evaluation

#slide(composer: (1fr, 1fr))[
  *Method*

  - define the intervention
  - isolate the changed component
][
  *Evaluation*

  - compare with the baseline
  - include one failure case
]

== Formal claim

#definition[Evaluation gate][
  A condition that must pass before the next experiment is justified.
]

#warning[Interpretation][
  Separate confirmed evidence from an uncommitted protocol recommendation.
]
