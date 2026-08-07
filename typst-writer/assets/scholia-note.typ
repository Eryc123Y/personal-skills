// Example only. New documents should reproduce this remote import rather than
// importing this file from the installed skill.

#import "@preview/scholia:0.1.0": *
#import "@preview/cetz:0.5.2" as cetz

#set document(title: "Study Workbook", author: "Eric")
#show: scholia.with(theme: "light", prose: "notes", paper: "a4")

#let answer(body) = yourturn(body)
#let solution(body) = answer(body)

#cover(
  "Study Workbook",
  subtitle: "Definitions, proofs, and practice",
  author: "Eric",
  date: "2026",
)

#note[
  Write directly in each `proof`, `answer`, or `solution` body. Replace the
  `TODO` prompt when completing a scaffolded step.
]

= Core idea

#definition[Invariant][
  A property preserved by every permitted transition.
]

#theorem[Preservation][
  If the invariant holds initially and each transition preserves it, then it
  holds after every finite sequence of transitions.
]

#proof[
  Proceed by induction on the number of transitions and complete
  #TODO[the induction step].
]

#example[One transition][
  Check the property before and after a single transition.
]

#answer[
  Restage the check here in your own words.
]

#figure(
  cetz.canvas(length: 0.65cm, {
    import cetz.draw: *
    line((-2, 0), (2, 0), mark: (end: "stealth"), stroke: rgb("#64748b") + 0.7pt)
    circle((-1, 0), radius: 0.12, fill: rgb("#2563eb"), stroke: none)
    circle((1, 0), radius: 0.12, fill: rgb("#059669"), stroke: none)
    content((-1, 0.45), [$s_0$])
    content((1, 0.45), [$s_1$])
  }),
  caption: [One state transition.],
)
