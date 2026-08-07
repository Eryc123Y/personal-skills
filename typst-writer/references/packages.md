# Personal package policy

Import packages from Typst Universe. Pin the version in source and verify the
authoritative manifest before upgrading.

## Personal defaults

| Package | Version | Use |
|---|---:|---|
| `scholia` | `0.1.0` | New study notes, proofs, revision, and workbooks |
| `unofficial-monash-touying` | `0.1.2` | Eric's academic and research slides |
| `cetz` | `0.5.2` | Editable mathematical and explanatory drawings |
| `codly` | `1.3.0` | Source-code blocks |
| `codly-languages` | `0.1.10` | Codly language colors and icons |
| `lovelace` | `0.3.1` | Pseudocode and algorithm traces |

## Conditional packages

| Package | Version | Use only when |
|---|---:|---|
| `cetz-plot` | `0.1.3` | A figure is a data/function plot rather than a custom drawing |
| `fletcher` | `0.5.8` | A graph, automaton, tree, or relationship diagram needs layout |

## Legacy compatibility

| Package | Version | Use only when |
|---|---:|---|
| `typsidian` | `0.0.3` | Maintaining an existing Typsidian document |
| `lemmify` | `0.1.8` | Maintaining theorem environments in that legacy stack |

Do not choose Typsidian/Lemmify over Scholia for new personal study material.

## Remote import examples

```typst
#import "@preview/scholia:0.1.0": *
#import "@preview/cetz:0.5.2" as cetz
```

```typst
#import "@preview/unofficial-monash-touying:0.1.2": *
```

```typst
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.10": *
#import "@preview/lovelace:0.3.1": *
```

## Version changes

1. Check the target repository's current imports.
2. Check the package's Typst Universe entry, manifest, or official repository.
3. Read migration notes when changing a minor or major version.
4. Compile every affected starter and at least one real document.
5. Avoid upgrading unrelated packages during a focused edit.

Never invent a package version from memory. Keep a confirmed older version
rather than guessing a newer one.
