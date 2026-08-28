---
name: to-handoff
description: Compact the current session's state into a handoff document a fresh session can pick up. Use when pausing unfinished work or transferring context to a new session. Triggered by "handoff", "交接".
---

# Handoff Documents

Produce a document that lets a fresh agent (or future you) continue the work without this conversation. Synthesize from what is already known — do not interview the user.

## Where it goes

Follow the current repo's existing convention first; only fall back to the default when none exists:

1. A `HANDOFF.md` already sitting next to the work area → **update it in place**.
2. An existing plans/design-docs directory → follow its location and naming pattern.
3. A repeatable *operational procedure* is a **runbook**, not a handoff — if the repo has a runbooks directory, it goes there.
4. No convention found → `docs/plans/YYYY-MM-DD-<topic>-handoff.md`.

Never save to the OS temp directory — these documents are project artifacts and belong in the repo.

## Structure

1. **Goal** — one sentence: what this work builds or answers.
2. **Current state** — what is done and *verified* vs. done-but-unverified vs. not started. Never present unverified work as done.
3. **Key decisions and why** — each decision with the reason it was made; refuted alternatives named so they don't get re-litigated.
4. **Next steps** — a short ordered list inline. If the remaining work is substantial, write a proper plan via `to-plan` and link it here instead of inlining a weak one.
5. **Suggested skills** — which skills the next session should invoke.
6. **References** — link specs, plans, commits, dashboards, memory entries by path. Do NOT duplicate their content here.

Use absolute dates (2026-08-28), never "today" / "yesterday". Redact credentials and API keys.

<!-- Adapted from mattpocock/skills `handoff` (MIT License). Maintained in light-skills. -->
