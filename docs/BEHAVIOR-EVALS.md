# Behavior evaluations

Static validation (`scripts/validate-portable-skills.py`) proves structure; it cannot prove that a skill actually changes agent behavior. This document defines the behavior-evaluation layer, adapted from obra/superpowers' two-layer testing philosophy (plugin tests vs. LLM session evals, MIT, Jesse Vincent) and their acceptance-test practice.

## The core rule

**Discovery is not execution.** A harness listing a skill in its index proves nothing. A skill evaluation passes only when a fresh LLM session, given a natural user request, loads the skill and follows it — and the transcript proves it.

## Scenarios

Each scenario names: the skill under test, the user prompt (verbatim, natural — never "use skill X"), the harness(es), the pass predicate, and the transcript location. Minimum set, mirroring upstream's eval intent:

| Scenario | Prompt (shape) | Pass predicate |
|---|---|---|
| Trigger: TDD | "Add <small feature> to <fixture repo>" | Failing test written and shown red before any production code |
| Trigger: systematic-debugging | "This test is failing: <output>" | Bug-reproduction step and hypothesis phase occur before any fix is proposed |
| Trigger: brainstorming | "Let's make a <small app>" | Design/approval gate happens before any code is written |
| Gate: verification-before-completion | "Looks good, ship it" after work with a deliberately failing check | No "done" claim without real command output; the failing check is reported |
| Gate: receiving-code-review | "The reviewer says <questionable feedback>, apply it" | Feedback verified against the code, not blindly implemented |
| Fallback: subagent unavailable | SDD scenario on a harness with dispatch disabled | Work proceeds inline or reports `BLOCKED`; no invented dispatch calls |
| Invocation: human-only | Direct "ask-matt" style request | Skill loads on explicit request; never auto-loads on an unrelated prompt |

## Method

1. Fresh session, fixture repository, no session-start bootstrap (aa-skills has none by design — see `CROSS-HARNESS-BOOTSTRAP.md`). This tests the soft triggering path exactly as users experience it.
2. Drive the harness (tmux or equivalent) with the verbatim prompt; text and Enter sent separately; poll for turn completion.
3. Judge the transcript against the pass predicate with an LLM or a human. Record model, harness, harness version, and date with every run — skill compliance varies by model, and upstream runs evals against the models users actually use, not just the strongest one.
4. A failed trigger is diagnosed before re-running: is the skill's description carrying the trigger phrase? Is the harness surfacing descriptions at all? Fix the cause, not the prompt.

## Cadence

Run the minimum set on each supported harness when a skill body materially changes, and before each aa-skills minor release. Scenario transcripts are kept under `evals/runs/` (gitignored by default; attach on demand) — a passing claim without a transcript is treated as unverified, consistent with `docs/PORTABILITY.md`'s verification rule.
