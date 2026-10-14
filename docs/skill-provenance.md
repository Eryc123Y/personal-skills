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
- `weekly-attendance-check-in`: current-semester unit discovery and verified
  attendance submission from the user's authenticated Monash course sources.
- `manim-video`: narrated, silent, and host-timed Manim CE animations. Three public Manim skills
  were reviewed as design references only; `manim-video/SOURCE.md` lists them.

The historical installations were associated with `anthropics/skills`,
`199-biotechnologies/claude-deep-research-skill`, and
`zsyggg/paper-craft-skills`. Those repositories remain independent upstreams.
The restrictive document-bundle terms and unconfirmed licensing of the research
and paper-craft resources are why those resources are not redistributed here.

## Attributed adaptations

| Folder | Upstream | License and changes |
|---|---|---|
| `python-best-practices` | [alleneubank/claude-code](https://github.com/alleneubank/claude-code) (formerly `0xbigboss/claude-code`) | Apache-2.0; condensed implementation/review guidance |
| `obsidian-second-brain` | [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | MIT; scoped vault operations, adapted command entrypoints, reduced runtime dependencies |

Each adapted folder includes its license and `SOURCE.md`, which identify the
upstream and describe the local changes. Preserve these notices when packaging
skills. The `vibe-research-workflow` adaptation and its bundled references were
removed on 2026-10-14; its historical source and license remain in Git history.
The `context7-auto-research` wrapper and fallback helper were also removed on
2026-10-14. Context7 remains available through the connected tool; no separate
personal wrapper is maintained. Historical attribution remains in Git history.

## Repository-to-client verification

After an authorized push, update through CC Switch and compare each installed
skill directory with its repository counterpart. Check source registration,
client enablement, and content together. A local commit alone is not publication;
a push alone is not proof that clients installed the new revision.

A future upstream revision is first reviewed and incorporated here, retaining
license notices and local behavior. CC Switch then updates from this maintained
repository. Other third-party skills not customized here retain their original
upstream registrations.
