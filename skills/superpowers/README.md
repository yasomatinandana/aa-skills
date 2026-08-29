# Superpowers

Selected, adapted skills from Jesse Vincent's **Superpowers** (obra/superpowers), an MIT-licensed agentic skills framework. This is an independent adaptation and is not endorsed by the upstream author.

- Source: https://github.com/obra/superpowers
- License: MIT — Copyright (c) 2025 Jesse Vincent, preserved at `upstream/superpowers-LICENSE`
- Source revision: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (v6.3.0, `main`)
- Imported as a full-repository clone at the sibling import location; skills copied from `skills/` of that tree.

## Included skills (12 of 14)

| Skill | Responsibility |
|---|---|
| [brainstorming](./brainstorming/SKILL.md) | Explore intent and design before any implementation work; three-path classification (spike / bounded / architectural) with a hard approval gate. |
| [writing-plans](./writing-plans/SKILL.md) | Turn an approved design into an implementation plan with exact test evidence per task. |
| [executing-plans](./executing-plans/SKILL.md) | Execute a written plan inline in one session with batch checkpoints. |
| [subagent-driven-development](./subagent-driven-development/SKILL.md) | Execute a plan by dispatching a fresh implementer subagent per task with per-task and whole-branch reviews. |
| [dispatching-parallel-agents](./dispatching-parallel-agents/SKILL.md) | Fan out one subagent per independent problem domain. |
| [requesting-code-review](./requesting-code-review/SKILL.md) | Request a two-axis code review (spec compliance, code quality) from a subagent. |
| [receiving-code-review](./receiving-code-review/SKILL.md) | Respond to review feedback with technical rigor instead of performative agreement. |
| [finishing-a-development-branch](./finishing-a-development-branch/SKILL.md) | Decide integration for a finished branch: merge, PR, or stay. |
| [systematic-debugging](./systematic-debugging/SKILL.md) | Four-phase root-cause debugging before any fix is proposed. |
| [test-driven-development](./test-driven-development/SKILL.md) | Enforced red-green-refactor: no production code without a failing test first. |
| [using-git-worktrees](./using-git-worktrees/SKILL.md) | Ensure an isolated workspace: detect existing isolation, prefer native tools, git worktree fallback. |
| [verification-before-completion](./verification-before-completion/SKILL.md) | Evidence-before-assertions gate before any "done" claim. |

## Excluded upstream skills (2 of 14)

- **using-superpowers** — the upstream plugin's own router/entry skill. It exists to bootstrap the upstream plugin installation; the aa-skills harness adapters provide the equivalent entry points.
- **writing-skills** — authoring guidance for upstream-plugin skills. Responsibility overlaps this repo's `writing-for-agents` (Matt Pocock source), and the upstream body is written against the upstream plugin's test machinery.

## Adaptations from upstream

Changes are limited to portability reconciliation; the workflow bodies are upstream content.

1. Cross-skill references rewritten from upstream's `superpowers:<name>` namespaced form to aa-skills' flat names (15 references across `executing-plans`, `subagent-driven-development`, `systematic-debugging`, `writing-plans`).
2. `executing-plans` note about subagent availability rephrased to name harnesses generically instead of pointing at upstream's per-platform reference files (`../using-superpowers/references/`), which are not shipped.
3. `test-driven-development/writing-good-tests.md` — removed a parenthetical reference to upstream's `writing-skills` skill (not shipped).
4. `brainstorming` — removed a sentence naming other upstream-plugin skills (`frontend-design`, `mcp-builder`) as forbidden terminal states; the rule (only `writing-plans` follows brainstorming on the architectural path) is preserved without them.
5. `systematic-debugging` development-log and adversarial test fixtures (`CREATION-LOG.md`, `test-academic.md`, `test-pressure-*.md`) are upstream development artifacts and are not shipped.

## Relationship to the other aa-skills sources

No name collisions with the pstack or Matt Pocock material. Closest neighbors, kept distinct by responsibility:

- **test-driven-development (superpowers)** is the enforcement loop (fail → pass → refactor, rationalization table). **tdd (Matt Pocock)** is test-quality guidance (seams, good tests, mocking). Both load together without conflict.
- **systematic-debugging (superpowers)** is the process loop (phases and gates). **diagnosing-bugs (Matt Pocock)** is the feedback-loop construction discipline. Complementary.
- **requesting-code-review / receiving-code-review (superpowers)** are orchestration prompts around review dispatch. **code-review (Matt Pocock)** is the two-axis review rubric a reviewer consumes.
- **using-git-worktrees (superpowers)** overlaps pstack `poteto-mode`'s worktree playbooks at the mechanism level, but poteto-mode remains the pstack style profile's own path; no reconciliation needed.
- **brainstorming / writing-plans (superpowers)** precede and complement `grill-with-docs`, `to-spec`, and `wayfinder`, which cover grilling and issue-tracker publication rather than design-to-plan handoff.
