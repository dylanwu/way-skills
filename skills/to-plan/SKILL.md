---
name: to-plan
description: Write an implementation plan that decomposes multi-step work into independently verifiable tasks for a zero-context executor. Use before starting substantial work, typically after to-grill / to-spec. Triggered by "写个 plan", "排个计划", "implementation plan".
---

# Implementation Plans

Turn agreed scope (a spec, a settled discussion) into a plan that a skilled executor with **zero context** — no access to this conversation, limited taste — can follow task by task.

## Where it goes

Follow the repo's existing plans/design-docs convention if one exists; otherwise default to `docs/plans/`. Filename: `YYYY-MM-DD-<topic>-plan.md` with today's actual date.

## Plan structure

- **Goal** — one sentence: what this builds.
- **Approach** — 2–3 sentences; link the spec it implements (the plan argues from the spec, so the spec travels with it).
- **Global constraints** — project-wide requirements copied verbatim (version floors, naming rules); every task implicitly includes them.
- **Tasks** — ordered, checkbox syntax (`- [ ]`) for tracking. Each task states: exact files to create/modify, what earlier tasks it consumes and what later tasks rely on (exact names and signatures), the change itself, and the command that proves it worked with its expected output.

## Quality rules

- **Right-sized tasks**: the smallest unit that carries its own verify cycle. Fold setup/scaffolding into the task whose deliverable needs them; split only where a reviewer could reject one task while approving its neighbor.
- **No placeholders**: "TBD", "add proper error handling", "similar to task N", "fill in details" are plan failures. Every step carries the actual content the executor needs — code steps show the code.
- **Zero-context executor**: if a step relies on something only this conversation knows, write it into the plan.
- **Self-review before saving**: (1) does every spec requirement map to a task? (2) scan for placeholder patterns; (3) do names, paths, and signatures used in later tasks match earlier ones?

To capture *session state* when pausing work, use `to-handoff` instead — a plan is forward-looking; it carries no "current state".

<!-- Homegrown; structure inspired by superpowers `writing-plans` (MIT). Maintained in light-skills. -->
