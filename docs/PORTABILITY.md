# Portability rules

The canonical skill bodies are shared by Claude Code, Codex, and Hermes Agent. Harness-specific syntax belongs in `adapters/`.

## Portable language

Skill bodies speak in actions ("dispatch a subagent", "create a task list", "read the file"), never in tool names. The action-to-tool translation lives per harness in `adapters/<harness>/TOOLS.md` (see [`CROSS-HARNESS-BOOTSTRAP.md`](CROSS-HARNESS-BOOTSTRAP.md)). Use ordinary project files, git, project test commands, documented CLIs, and explicit evidence. Say what to do when a capability is missing. Use `BLOCKED` or a read-only fallback instead of inventing a tool or agent.

## Bootstrap and triggering

aa-skills does not run a session-start bootstrap; triggering relies on each harness surfacing skill names and descriptions. That is a deliberate trade-off — see [`CROSS-HARNESS-BOOTSTRAP.md`](CROSS-HARNESS-BOOTSTRAP.md) for the consequences and the escalation path if guaranteed triggering is ever needed. Install paths always ride the harness's own install mechanism; never edit a user's global config files.

## Invocation

- Claude Code uses `disable-model-invocation: true` for human-only skills.
- Codex uses `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.
- Hermes uses explicit slash commands or bundles for human entry points, with normal skill metadata for discovery.

## Capabilities

Treat parallel agents, browser control, MCP, issue trackers, Graphite, scheduled execution, and model routing as optional. Detect them before use.

## Verification

A completion claim must cite a real command, test, runtime surface, diff, or artifact. A model's claim that it ran something is not proof by itself. Static validation proves structure only; behavior claims about skills (triggering, compliance) are covered by [`BEHAVIOR-EVALS.md`](BEHAVIOR-EVALS.md).
