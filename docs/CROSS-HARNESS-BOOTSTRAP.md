# Cross-harness bootstrap and distribution

How aa-skills skills get discovered and loaded on each harness, and how to add a new harness. The design adapts the integration invariants from obra/superpowers' `docs/porting-to-a-new-harness.md` (MIT, Jesse Vincent, at revision `b36e082`); the structures here are aa-skills'.

## The invariant

Skill bodies are written in actions, never tool names: "read the file", "dispatch a subagent", "create a task list". Per-harness tool names live only in `adapters/<harness>/TOOLS.md`. A skill body that names a harness-specific tool is a bug — move the name to the tool mapping.

The second invariant is upstream's rule 2, adopted here: **every install path ships through the harness's own install mechanism. Nothing in this repository documents, script-assists, or tolerates editing a user's global config files** (`~/.hermes/SOUL.md`, `~/.codex/config.toml`, `~/.claude/CLAUDE.md`) to load aa-skills.

## Integration shapes

Upstream classifies harnesses by how a session-start bootstrap reaches the model (shell hook / in-process plugin / instructions file). aa-skills takes a deliberately different position, consistent with `docs/PORTABILITY.md`: **aa-skills does not run a session-start bootstrap.** Skill triggering on every harness here relies on the harness surfacing skill names and descriptions at session start — what upstream calls the "surfaced skill index" path, and treats as the weakest bootstrap. That is an accepted trade-off: aa-skills is a shared skill collection alongside other content, not an opinionated framework that owns the session. Two consequences, taken directly from upstream's analysis of this path:

1. **Triggering is softer.** There is no `<EXTREMELY_IMPORTANT>` wrapper, no dedup guard, no re-injection after compaction. Skill descriptions must carry rich trigger phrasing ("Use when...", concrete situations), and the acceptance test in each harness is the only structural guarantee.
2. **The tool mapping must be reachable, not merely present.** Because nothing injects it, each `adapters/<harness>/TOOLS.md` must be discoverable by a model that has loaded a skill — the human-only router skills point at it (see "Tool mapping" below), and this file documents the path.

If a future release wants guaranteed triggering, upstream's escalation order applies: a manifest-declared context file the installer preserves is the strongest clean bootstrap; hand-editing user config is never acceptable.

## Capability matrix

Required, degradable, and optional capabilities, with the documented fallback when a capability is absent. This is upstream's capability checklist with aa-skills' fallbacks filled in.

| Capability | Used by | If absent |
|---|---|---|
| File read/write/edit | nearly all skills | Essential; no fallback. |
| Shell commands | TDD, verification, debugging, git skills | Essential; no fallback. |
| Skill discovery + invocation | all | Native skill tool, or reading the `SKILL.md` as the documented mechanism — state which in the harness's `TOOLS.md`. |
| Subagent dispatch | `dispatching-parallel-agents`, `subagent-driven-development`, `code-review`, `interrogate`, `reflect`, `arena`, `swarm` | Degradeable: do the work inline, or report `BLOCKED`. Never invent a dispatch call. |
| Todo / task tracking | planning and execution skills | Degradeable: fall back to a plan file or `TODO.md`. |
| Web fetch / search | `research`, `ask-matt` | Degradeable. |
| Issue tracker / MCP / browser / scheduling | `triage`, `to-tickets`, `wayfinder`, `brainstorming` visual companion | Optional: detect before use; the skill documents its fallback. |

A skill that silently assumes a degradable capability exists — instead of falling back per this table — is a portability bug.

## Definition of done for a new harness adapter

Adapted from upstream Part 3, minus the bootstrap requirement, plus the reconciliation gate aa-skills adds:

1. An `adapters/<harness>/README.md` documents install path, skill discovery mechanism, invocation metadata convention, and which capabilities degrade.
2. An `adapters/<harness>/TOOLS.md` maps every action in the shared action vocabulary (read/edit/create files, shell, search, fetch, dispatch, todos, invoke-skill) to real tool names — taken from the harness's own docs or a live session, never invented.
3. The harness can discover the skills through its own install mechanism, and a fresh session can load a skill (natively or via the documented read-`SKILL.md` path).
4. Human-only skills carry the harness's human-only metadata (Claude: `disable-model-invocation: true`; Codex: `agents/openai.yaml` policy) and are not implicitly triggered.
5. **Overlap reconciliation is reviewed** (per the skill library's porting procedure): the new harness's skill-selection implications are checked against existing bundles before skills are listed in the manifests.
6. The acceptance test passes in a fresh session: an ambiguous feature request auto-loads `brainstorming` before code is written; a "this is done" claim is challenged by `verification-before-completion` unless real command output exists. Save the transcript next to this doc's evaluation record.
7. Manifests list the bundle's skills, and `scripts/validate-portable-skills.py` passes.

## Distribution notes

- Hermes Agent: skills load from the repo checkout, a versioned skill tap, or the `adapters/hermes-agent/plugin.json` bundle. Human-only entry points are invoked explicitly; there is no session-start hook to configure.
- Claude Code: install via the marketplace/plugin mechanism referencing `adapters/claude-code/plugin.json`; skills and invocation metadata ride the plugin.
- Codex: skills install as an Agent Skills-compatible directory; `agents/openai.yaml` beside each skill carries picker metadata. Subagent-dependent skills additionally require the multi-agent feature flag in the user's own Codex config — that flag is the user's to set; document it, never script it.
- New harness: follow the definition of done above. If the harness cannot install skills through its own mechanism without user-config edits, say so and stop — that is a limitation to surface, not to work around.
