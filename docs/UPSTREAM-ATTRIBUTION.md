# Upstream attribution

This repository combines and adapts material from the following MIT-licensed upstream projects. Their licenses are preserved under `upstream/`.

## pstack

- Author: Lauren Tan (poteto).
- Source: https://github.com/cursor/plugins/tree/main/pstack
- Imported as a subdirectory of `cursor/plugins`.
- Source revision used for this initial port: `46125561306434d8a1d7745d540d8932ab0cd2a2`.
- Copyright and license text: `upstream/pstack-LICENSE`.
- Adapted material includes pstack principles, `poteto-mode` playbooks, multi-agent workflow patterns, and selected helper references.

## Matt Pocock's Skills

- Author: Matt Pocock.
- Source: https://github.com/mattpocock/skills
- Source revision used for this initial port: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`.
- Copyright and license text: `upstream/mattpocock-LICENSE`.
- Adapted material includes the engineering and productivity skill buckets, their references, templates, and Codex metadata.

## Superpowers

- Author: Jesse Vincent (obra).
- Source: https://github.com/obra/superpowers
- Source revision used for this import: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (tag v6.3.0, default branch `main`).
- Copyright and license text: `upstream/superpowers-LICENSE`.
- Adapted material includes 12 of the upstream repository's 14 skills, copied from its `skills/` tree into `skills/superpowers/`. The excluded skills (`using-superpowers`, `writing-skills`) and the exact adaptation list are recorded in `skills/superpowers/README.md`.
- Additionally adapted: cross-harness integration concepts from the upstream repository's `docs/porting-to-a-new-harness.md` and per-harness tool-mapping references (`skills/using-superpowers/references/`), re-expressed in `docs/CROSS-HARNESS-BOOTSTRAP.md`, `docs/BEHAVIOR-EVALS.md`, and the `adapters/*/TOOLS.md` files. These are structural ideas re-authored for aa-skills' no-bootstrap design, not copies.

## Adaptation policy

Upstream authors retain attribution and copyright in their original material. New adapter code, reconciliation edits, evaluation fixtures, and documentation in this repository are authored by the aa-skills maintainers. Each adapted skill should retain an `Upstream:` note in its local provenance record when it is materially changed.

Do not imply endorsement by Lauren Tan, Cursor, Matt Pocock, or Anthropic.
