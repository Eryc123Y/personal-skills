// Legacy compatibility example for existing Typsidian/Lemmify documents.
// New personal study notes should import Scholia directly from Typst Universe.

#import "@preview/typsidian:0.0.3" as typsidian
#import "@preview/lemmify:0.1.8": *
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.10": *
#import "@preview/lovelace:0.3.1": *

#let (
  theorem,
  lemma,
  corollary,
  remark,
  proposition,
  example,
  definition,
  proof,
  rules: note-theorem-rules,
) = default-theorems("note-theorems", lang: "en")

#let note-env(env) = (name, body) => env(name: name, body)

#let note-theorem = note-env(theorem)
#let note-lemma = note-env(lemma)
#let note-corollary = note-env(corollary)
#let note-remark = note-env(remark)
#let note-proposition = note-env(proposition)
#let note-example = note-env(example)
#let note-definition = note-env(definition)
#let note-proof(body) = proof(body)

#let note-pseudocode-list = pseudocode-list
#let note-pseudocode = pseudocode

#let academic-note(
  title: "Untitled Note",
  course: "",
  author: "",
  theme: "light",
  show-outline: false,
  body,
) = {
  show: typsidian.typsidian.with(
    title: title,
    course: course,
    author: author,
    theme: theme,
    show-index: false,
  )

  show: note-theorem-rules
  show: codly-init.with()
  codly(languages: codly-languages)

  typsidian.make-title(
    show-outline: show-outline,
    show-author: author != "",
    justify: "center",
  )

  body
}
