# Hermes Agent adapter

Hermes consumes the same `SKILL.md` content through `~/.hermes/skills/`, external skill directories, or a portable Agent Plugins v1 package. Use native Hermes plugins only for runtime tools, hooks, commands, or setup logic.

Hermes-specific workflows may use `delegate_task`, `cronjob`, profiles, worktrees, memory, MCP, browser, and computer-use tools when declared as optional capabilities.
