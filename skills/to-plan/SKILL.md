---
name: to-plan
description: Write a plan or handoff document that a fresh session can pick up and execute. Use when pausing unfinished work, transferring context to a new session, or laying out a multi-step implementation. Triggered by "handoff", "交接", "写个 plan", "落个文档".
---

# Plan / Handoff Documents

Produce a document that lets a fresh agent (or future you) continue the work without this conversation. Synthesize from what is already known — do not interview the user.

## Where it goes

Follow the current repo's existing convention first; only fall back to the default when none exists:

1. A `HANDOFF.md` already sitting next to the work area → **update it in place**.
2. An existing plans/design-docs directory (look for `docs/plans/`, module-level `docs/plans/`, or date-prefixed design docs) → follow its location and naming pattern.
3. A repeatable *operational procedure* is a **runbook**, not a handoff — if the repo has a runbooks directory, it goes there.
4. No convention found → `docs/plans/YYYY-MM-DD-<topic>.md`.

Never save to the OS temp directory — these documents are project artifacts and belong in the repo.

## Handoff structure

1. **Goal** — one sentence: what this work builds or answers.
2. **Current state** — what is done and *verified* vs. done-but-unverified vs. not started. Never present unverified work as done.
3. **Key decisions and why** — each decision with the reason it was made; refuted alternatives named so they don't get re-litigated.
4. **Next steps** — concrete, ordered tasks (see plan quality rules below).
5. **Suggested skills** — which skills the next session should invoke.
6. **References** — link specs, plans, commits, dashboards, memory entries by path. Do NOT duplicate their content here.

Use absolute dates (2026-08-28), never "today" / "yesterday". Redact credentials and API keys.

## Plan quality rules

- **Bite-sized tasks**: each task is independently executable and verifiable, with exact file paths and the command that proves it worked.
- **No placeholders**: "TBD", "add proper error handling", "similar to task N", "fill in details" are plan failures. Every step carries the actual content the executor needs.
- **Zero-context executor**: assume the reader is skilled but knows nothing about this codebase or the conversation. If a step relies on something only this conversation knows, write it into the document.
- **Self-review before saving**: (1) does every goal/requirement map to a task? (2) scan for placeholder patterns; (3) do names, paths, and signatures used in later tasks match earlier ones?

<!-- Homegrown; structure inspired by mattpocock/skills `handoff` and superpowers `writing-plans` (both MIT). Maintained in light-skills. -->
