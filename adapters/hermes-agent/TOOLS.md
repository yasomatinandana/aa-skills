# Hermes Agent tool mapping

Skills in this repository speak in actions ("dispatch a subagent", "create a task", "read the file"). On Hermes Agent those actions resolve to the tools below. Structure adapted from obra/superpowers' per-harness tool mappings (MIT, Jesse Vincent); names verified against the Hermes Agent toolset.

## Tools

| Action skills request | Hermes tool |
|---|---|
| Read a file | `read_file` |
| Create a new file | `write_file` |
| Edit a file (targeted patch) | `patch` |
| Run a shell command | `terminal` |
| Search file contents | `search_files` |
| Find files by name | `search_files` with `target="files"`, or `terminal` with `find` |
| Fetch a URL / read a webpage | `web_extract(urls=[...])` |
| Search the web | `web_search(query=...)` |
| Dispatch a subagent | `delegate_task(goal=..., context=...)` — background; the result returns on its own |
| Task tracking | `todo` tool |
| Invoke a skill | `skill_view("skill-name")`; list candidates with `skills_list` |
| Schedule later work | `cronjob` (optional; only skills that declare scheduling use it) |

## Instructions file

When a skill says "your instructions file" or "project context file", on Hermes Agent this is **`AGENTS.md`** in the project directory. Profile-global memory and skills live under `~/.hermes/`.

## Invoking skills

Hermes Agent has a `skills` toolset with `skill_view` and `skills_list`. To invoke a skill from this repo:

```
skill_view("test-driven-development")
skill_view("superpowers:...")  // not needed — aa-skills skills use flat names
```

If `skill_view` cannot find a skill, fall back to reading its `SKILL.md` directly with `read_file`. Reading the file is the documented fallback mechanism, not a rule violation.

## Subagent dispatch

`delegate_task` spawns isolated subagents; pass everything the child needs in `goal` and `context` (children see nothing from your session). Several tasks in one call run in parallel. If `delegate_task` is unavailable, do the work inline or report `BLOCKED` — never invent a dispatch call. Human-only skills are not dispatchable as subagent roles.

## Human-only skills

Skills with "user-invoked" behavior (routers like `ask-matt`, setup skills) are meant for explicit human invocation. On Hermes they are simply requested by name; there is no implicit-invocation flag to set.
