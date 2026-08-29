# Codex tool mapping

Skills in this repository speak in actions; on Codex they resolve as below. Structure adapted from obra/superpowers' per-harness tool mappings (MIT, Jesse Vincent); verify names against your installed Codex release — the CLI changes fast and trust your actual tool list over any table.

## Tools

| Action skills request | Codex mechanism |
|---|---|
| Read / create / edit files | file tools and `apply_patch`-style editing as exposed by your Codex version |
| Run a shell command | shell/exec tool |
| Search file contents / find files | grep/glob tooling as exposed by your version |
| Fetch a URL / web search | web tools if enabled in your configuration; degradeable — skip and say so if absent |
| Dispatch a subagent | multi-agent tools (`spawn_agent` / `followup_task` in current releases) — requires the feature flag below |
| Task tracking | a plan file or `TODO.md` unless your version exposes a native task tool |
| Invoke a skill | Codex discovers `SKILL.md` files natively; if a skill is not surfaced, read its `SKILL.md` directly — that is the documented mechanism, not a violation |

## Subagents require a user-set feature flag

Multi-agent tools are behind a Codex feature flag. The user sets it in their own `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

aa-skills never writes or scripts this file (see `docs/CROSS-HARNESS-BOOTSTRAP.md`, "install through the harness's own mechanism"). If the flag is off, subagent-dependent skills (`dispatching-parallel-agents`, `subagent-driven-development`, `code-review`'s parallel mode, `interrogate`, `reflect`, `arena`, `swarm`) degrade to inline work or report `BLOCKED`.

## Isolated forks for subagent-driven work

When the flag is on: spawn children with a clean context (`fork_turns: "none"` in current releases) rather than full-history forks — fresh context per task is what keeps a subagent focused. Resume an implementer with a follow-up message instead of dispatching a fresh one for fix rounds. Lifecycle and tool names vary by multi-agent version and model preset; check the real tool list in your session before relying on any of them.

## Environment detection

Skills that create worktrees or finish branches detect their environment with read-only git commands first (`git rev-parse --git-dir` vs `--git-common-dir`, `git branch --show-current`) — see `using-git-worktrees` Step 0 and `finishing-a-development-branch`. In sandboxed or externally managed environments (detached HEAD), commit the work and hand branch/push/PR steps to the user with exact commands to run.
