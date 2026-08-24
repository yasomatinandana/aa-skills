# Codex adapter

This adapter uses Agent Skills-compatible directories and `agents/openai.yaml` metadata. Keep `AGENTS.md` as the project instruction entry point.

Human-only skills must carry `policy.allow_implicit_invocation: false`. Use Codex-native sandbox, worktree, execution, and delegation behavior. Do not assume a native Codex plugin API exists; verify the installed Codex release before adding one.
