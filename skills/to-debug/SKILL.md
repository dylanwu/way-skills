---
name: to-debug
description: Root-cause-first debugging discipline. Use when encountering any bug, test failure, or unexpected behavior — before proposing fixes. Triggered by "debug", "排查", "找根因".
---

# Systematic Debugging

Find the root cause before attempting any fix. Symptom fixes are failures. This applies hardest exactly when skipping feels justified: time pressure, an "obvious" quick fix, or several failed fixes already behind you — simple bugs have root causes too, and systematic is faster than guess-and-check thrashing.

**The iron law: no fixes without root-cause investigation first.** Complete each phase before the next.

## Phase 1 — Root-cause investigation

- **Read the error completely.** Stack traces, line numbers, error codes — they often contain the exact answer.
- **Reproduce consistently.** If you can't trigger it reliably, gather more data; don't guess.
- **Check recent changes.** Diffs, new dependencies, config and environment differences.
- **Instrument component boundaries.** In multi-component systems (CI → build → sign; API → service → DB), log what enters and exits each layer, run once, and let the evidence show *which* layer breaks — then investigate that layer.
- **Trace backward to the origin.** Where does the bad value first appear? Keep tracing up the call stack until you find the source; fix at the source, not at the symptom. Full technique: [root-cause-tracing.md](root-cause-tracing.md).

## Phase 2 — Pattern analysis

- Find working examples of the same pattern in this codebase.
- Read the reference implementation **completely** — partial understanding guarantees bugs.
- List every difference between working and broken, however small; don't assume "that can't matter".
- Understand the dependencies: settings, config, environment, assumptions.

## Phase 3 — Hypothesis and test

- State a single hypothesis: "I think X is the root cause because Y."
- Test it with the **smallest possible change** — one variable at a time.
- Confirmed → Phase 4. Refuted → form a new hypothesis; never stack another fix on top.
- If you don't understand something, say so and investigate — don't pretend.

## Phase 4 — Implementation

- Create the failing test first — simplest reproduction, automated if possible (use `to-tdd`).
- Implement **one** fix, at the root cause. No "while I'm here" improvements, no bundled refactoring.
- Verify with real output: test passes, nothing else broke, the issue is actually gone.
- **If the fix didn't work, count your attempts.** Fewer than 3 → return to Phase 1 with the new information. **3 or more → stop: this is an architecture problem, not a hypothesis problem.** Each fix revealing a new problem elsewhere is the signature. Question the pattern with the user before any fix #4.

## Red flags — stop and return to Phase 1

Catching yourself thinking any of these means the process has already been abandoned:

- "Quick fix for now, investigate later" / "just try changing X and see"
- "It's probably X, let me fix that" — proposing solutions before tracing data flow
- Multiple changes at once; skipping the test; "I'll verify manually"
- "I don't fully understand, but this might work"
- "One more fix attempt" — after two failures have already happened

## When there is no root cause

If systematic investigation shows the issue is truly environmental or timing-dependent: document what you investigated, implement appropriate handling (retry, timeout, clear error), and add monitoring. But most "no root cause" verdicts are incomplete investigations.

## Supporting techniques

- [root-cause-tracing.md](root-cause-tracing.md) — trace a bug backward through the call stack to its original trigger
- [defense-in-depth.md](defense-in-depth.md) — add validation at multiple layers *after* the root cause is found
- [condition-based-waiting.md](condition-based-waiting.md) — replace arbitrary timeouts with condition polling

<!-- Source: adapted from superpowers v6.3.0 `systematic-debugging` (MIT), restyled and condensed. Maintained in way-skills. -->
