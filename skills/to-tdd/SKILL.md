---
name: to-tdd
description: Red → green test-driven development — what a good test is, the seams to test at, the anti-patterns, and the rules of the loop. Use when building features or fixing bugs test-first, or when changing model training / feature encoding / calibration code that has a pure-function core. Triggered by "TDD", "红绿循环", "test-first".
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read the project's CLAUDE.md / AGENTS.md and existing docs so test names and interface vocabulary match the project's domain language.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure. One logical assertion per test — a test that checks several things names none of them when it fails.

**Mock at system boundaries, nowhere else.** The legitimate targets are the things you don't control: external APIs, time and randomness, the filesystem, and databases (prefer a real test database where you can). Your own modules and internal collaborators are never mock targets; mocking them is precisely what couples a test to structure.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Before the first red

Reaching for this skill means the work is feature-scale — **never run the loop on the default branch.** If the session is already inside a linked worktree, use it and never nest another; otherwise prefer the harness's native worktree tool (Claude Code: `EnterWorktree`), which owns placement, branching and cleanup. Without one — Codex CLI has none — fall back to git, keeping the worktree project-local and git-ignored before anything is created in it:

```bash
git check-ignore -q .worktrees || { echo ".worktrees/" >> .gitignore && git add .gitignore && git commit -m "ignore worktrees"; }
git worktree add .worktrees/feature-<name> -b feature/<name>
```

Then **run the existing suite before writing the first red** — a dirty baseline makes every later failure ambiguous. When the MR merges, remove the worktree and delete the branch in the same motion; a merged worktree left behind is stale state exactly like a merged branch.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** Review names what wants refactoring; acting on it is a separate motion, never part of a red → green cycle.
- **Review every slice before opening the next.** An unreviewed slice is not green.

## Running the loop with subagents

Where the harness can dispatch, run the loop as a driver and read **`to-drive`** for how: the cost model that makes delegation worth it, the plan-as-state structure, a named model on every dispatch, review as a dispatch, and the end-of-branch pass. Every slice — dispatches included — runs inside the worktree from *Before the first red*.

Two things are specific to TDD. The **slice is the unit**: one seam, one test, one implementation, dispatched with the failing test's intent or exact code and the command that proves red → green. And red → green has **already settled behaviour**, so the review's first question narrows from *does it work* to *did it do only what the slice asked* — plus whether the test pins the requirement rather than whichever implementation happened to satisfy it.

## ML appendix

### Where TDD pays off

The TDD sweet spot in ML code is the **pure-function layer**: feature encoding / mapping, dropout & mask rules, calibration computations. Pipeline SQL and training loops are poor TDD targets — their gates are different (see the `to-backfill` and `to-refute` skills).

**Test through the artifact you deploy, not the one you trained.** Logic that only takes effect at inference never runs during training-time checks, so a whole class of bug stays invisible until the first such rule ships. Exercise the exported model on a realistic batch shape — deployment-specific release gates themselves are project knowledge and belong in that project's docs, not here.

### Fixture iron rules

- **Encoding tests must use a feature whose mapped id ≠ raw value.** Identity-mapped features (mapped id == raw value) make a test pass even when the code confuses the two encoding domains — a Critical encoding bug once escaped unit tests exactly this way. Pick a fixture feature where the two domains are distinguishable.
- **Pin down which encoding domain each interface consumes.** If an input column is already post-mapping, a test must fail when consumer code translates it a second time.
- **Sentinel values belong in fixtures.** "Unscored/missing" sentinels must appear in test inputs, and sentinel conventions change over time (a real migration merged `-1` into `0`) — the right tests must fail when they do; prefer range predicates over equality on sentinels.

<!-- Source: skeleton adapted from mattpocock/skills `tdd` (MIT); ML appendix homegrown from project post-mortems; the driver, review and cost material extracted to `to-drive`. Maintained in way-skills. -->
