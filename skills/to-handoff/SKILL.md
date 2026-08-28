---
name: to-handoff
description: Compact the current session's state into a handoff document a fresh session can pick up. Use when pausing unfinished work or transferring context to a new session. Triggered by "handoff", "交接".
---

# Handoffs

Produce a document that lets a fresh agent (or future you) continue the work without this conversation. Synthesize from what is already known — do not interview the user.

## Where it goes

A handoff is a **living document, updated in place** — not a dated archive entry. Its identity must come from its path or its name:

1. A handoff for *this* workstream already exists (`HANDOFF.md` next to the work area, or `docs/handoffs/<topic>-handoff.md`) → update it in place.
2. Work scoped to a module/directory → `<work-dir>/HANDOFF.md` — the path carries the topic.
3. Work not tied to one directory → `docs/handoffs/<topic>-handoff.md`, with the slug named after the scenario (e.g. `docs/handoffs/ftx-consume-history-handoff.md`). Never a bare `HANDOFF.md` at the repo root — it carries no topic identity, and the next unrelated handoff would collide with it.
4. A repeatable *operational procedure* is a **runbook**, not a handoff — if the repo has a runbooks directory, it goes there.

Dated documents belong to `to-spec` / `to-plan` in the plans directory; don't file handoffs there. Never save to the OS temp directory — a handoff is a project artifact and belongs in the repo.

## Structure

1. **Goal** — one sentence: what this work builds or answers.
2. **Current state** — what is done and *verified* vs. done-but-unverified vs. not started. Never present unverified work as done.
3. **Key decisions and why** — each decision with the reason it was made; refuted alternatives named so they don't get re-litigated.
4. **Next steps** — a short ordered list inline. If the remaining work is substantial, write a proper plan via `to-plan` and link it here instead of inlining a weak one.
5. **Suggested skills** — which skills the next session should invoke.
6. **References** — link specs, plans, commits, dashboards, memory entries by path. Do not duplicate their content here.

## Rules

- Use absolute dates (2026-08-28), never "today" / "yesterday".
- Redact credentials, API keys, and personal data.
- Prune superseded state on each update — a handoff that accretes history stops being readable; history lives in git.

<!-- Source: adapted from mattpocock/skills `handoff` (MIT). Maintained in way-skills. -->
