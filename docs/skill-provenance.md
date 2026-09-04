# Maintained skill provenance

CC Switch installs these customizations from `Eryc123Y/personal-skills`, branch
`main`. This repository is the source of truth; installed copies are deployment
outputs. Do not point an installed customization back at its historical upstream
and expect local edits to survive an upstream update.

## Independently maintained instruction-only entries

The following folders contain newly authored instructions and do not redistribute
historical upstream scripts, templates, prompts, or other resources:

- `pdf`, `docx`, `pptx`: scoped document operations. The old Anthropic bundles are
  not included. Ordinary authoring uses the current host's document skills.
- `skill-creator`: the `skill-evaluation` entry; no legacy Claude runner is bundled.
- `deep-research`: evidence-backed investigation with task-dependent scope.
- `paper-analyzer`, `paper-comic`, `paper-deck`: paper interpretation and visual
  deliverables using capabilities available in the current host.

The historical installations were associated with `anthropics/skills`,
`199-biotechnologies/claude-deep-research-skill`, and
`zsyggg/paper-craft-skills`. Those repositories remain independent upstreams.
The restrictive document-bundle terms and unconfirmed licensing of the research
and paper-craft resources are why those resources are not redistributed here.

## Attributed adaptations

| Folder | Upstream | License and changes |
|---|---|---|
| `context7-auto-research` | [BenedictKing/context7-auto-research](https://github.com/BenedictKing/context7-auto-research) | MIT; narrower trigger and host-aware tool routing; retained helper |
| `python-best-practices` | [alleneubank/claude-code](https://github.com/alleneubank/claude-code) (formerly `0xbigboss/claude-code`) | Apache-2.0; condensed implementation/review guidance |
| `vibe-research-workflow` | [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | CC BY-NC-SA 4.0; scoped workflow selection, Codex-oriented tools, fewer unconditional steps |
| `obsidian-second-brain` | [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | MIT; scoped vault operations, adapted command entrypoints, reduced runtime dependencies |

Each adapted folder includes its license and `SOURCE.md`, which identify the
upstream and describe the local changes. The noncommercial/share-alike terms of
`vibe-research-workflow` apply to that adaptation, not indiscriminately to the
other independent folders. Do not remove these notices when packaging skills.

## Repository-to-client verification

After an authorized push, update through CC Switch and compare each installed
skill directory with its repository counterpart. Check source registration,
client enablement, and content together. A local commit alone is not publication;
a push alone is not proof that clients installed the new revision.

A future upstream revision is first reviewed and incorporated here, retaining
license notices and local behavior. CC Switch then updates from this maintained
repository. Other third-party skills not customized here retain their original
upstream registrations.
