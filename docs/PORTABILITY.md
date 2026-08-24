# Portability rules

The canonical skill bodies are shared by Claude Code, Codex, and Hermes Agent. Harness-specific syntax belongs in `adapters/`.

## Portable language

Use ordinary project files, git, project test commands, documented CLIs, and explicit evidence. Say what to do when a capability is missing. Use `BLOCKED` or a read-only fallback instead of inventing a tool or agent.

## Invocation

- Claude Code uses `disable-model-invocation: true` for human-only skills.
- Codex uses `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.
- Hermes uses explicit slash commands or bundles for human entry points, with normal skill metadata for discovery.

## Capabilities

Treat parallel agents, browser control, MCP, issue trackers, Graphite, scheduled execution, and model routing as optional. Detect them before use.

## Verification

A completion claim must cite a real command, test, runtime surface, diff, or artifact. A model's claim that it ran something is not proof by itself.
