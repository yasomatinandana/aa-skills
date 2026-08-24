# Claude Code adapter

This adapter exposes the shared Agent Skills package through Claude Code's plugin and project skill mechanisms.

Use `.claude-plugin/plugin.json` as the manifest template. Preserve `disable-model-invocation: true` for human-only entry points. Replace references to Cursor `Task`, `AskQuestion`, Cursor model rules, Cursor `/loop`, Graphite, and Cursor UI controls with Claude-native mechanisms. Never enable `--dangerously-skip-permissions` by default.

The skill bodies remain in `skills/`; this file documents the adapter boundary.
