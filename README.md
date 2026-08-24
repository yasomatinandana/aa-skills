# aa-skills

Portable engineering workflows for Claude Code, Codex, and Hermes Agent.

This repository combines selected, adapted skill content from pstack and Matt Pocock's Skills for Real Engineers. The canonical source material lives under `skills/`. Harness-specific installation and behavior live under `adapters/`.

## Sources and attribution

Read [`docs/UPSTREAM-ATTRIBUTION.md`](docs/UPSTREAM-ATTRIBUTION.md) before redistributing or modifying this material. The upstream MIT license texts are preserved under `upstream/`.

- pstack: Lauren Tan, from the `pstack/` directory of https://github.com/cursor/plugins
- Matt Pocock's skills: https://github.com/mattpocock/skills

This project is an independent adaptation. It is not endorsed by the upstream authors, Cursor, Anthropic, OpenAI, or Nous Research.

## Layout

- `skills/engineering/` and `skills/productivity/` contain the selected Matt Pocock skills.
- `skills/pstack/` contains pstack principles and workflow profiles.
- `adapters/` contains harness-specific guidance.
- `docs/` contains portability and provenance policy.
- `upstream/` preserves source license files.

## Scope of this initial port

The initial port intentionally does not include pstack's Benny automation, Graphite-specific shipping, Cursor UI controls, or vendor-specific model mappings. Those belong in optional adapters after the portable core is evaluated.

## License

See [`upstream/pstack-LICENSE`](upstream/pstack-LICENSE) and [`upstream/mattpocock-LICENSE`](upstream/mattpocock-LICENSE). New aa-skills adapter and documentation code is MIT licensed unless a file says otherwise.
