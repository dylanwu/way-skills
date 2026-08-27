---
name: tdd
description: Test-driven development. Use when building features or fixing bugs test-first, mentions of "red-green-refactor", or when changing model training / feature encoding / calibration code that has a pure-function core.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read the project's CLAUDE.md and existing docs so test names and interface vocabulary match the project's domain language.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (use the built-in `/code-review` or `/simplify`), not the red → green implementation cycle.

## ML appendix (fancy-model)

### Where TDD pays off

The TDD sweet spot in training code is the **pure-function layer**: feature encoding / mapping, dropout & mask rules, calibration computations. Pipeline SQL and training loops are poor TDD targets — their gates are different (see the `backfill` and `analysis-review` skills).

### Fixture iron rules

- **Encoding tests must use a feature whose `fea_val ≠ fea_id`** (e.g. `budget_id`). `dsp_id` / `vendor_id` have identity mappings (`fea_val == fea_id`), so a test built on them will pass even when the code confuses the two encoding domains — a Critical prior-anchor bug escaped unit tests exactly this way.
- **`lr_data` / `raw_data` feature columns are already mapped `fea_id`.** Consumer-side code (calibration grouping, prior statistics, offline scoring) must not translate them through `feature_mapping` again; tests must pin this down.
- **Sentinel values belong in fixtures.** Unscored sentinels (`-1` and `0`) must appear in test inputs. A sentinel migration is a real event (2026-08-21: ver columns' "-1 = unscored" merged into "0") — filters written as `= -1` must be `<= 0`, and the right tests must fail when a sentinel convention changes.

### Release smoke gate (the four checks)

Before deploying ANY model change, all four must pass:

1. **Traced vs eager parity** — traced model output matches eager `forward()` element-wise on a real batch.
2. **Traced batch > 1** — `jit.trace` freezes python ints (`torch.ones(batch_size)` becomes batch=1 forever; use `torch.ones_like(x[:, 0])`). Any *new eval-time in-model logic* must be exercised through the **traced** graph with batch > 1 — train-only logic never enters the traced graph, so tracing bugs hide until the first eval-time rule lands.
3. **Sentinel inputs** — unscored / sentinel rows through the traced model produce defined outputs, not garbage.
4. **Channel-off uses `mode:"mask"`, never `embed_dropout p=1.0`** — dropout is train-only; p=1.0 leaves the embedding untrained yet *read at inference*, producing a +0.02 seed-dependent bias. Mask is deterministic on both ends (verified bit-exact zero diff).

<!-- Skeleton adapted from mattpocock/skills `tdd` (MIT License); ML appendix homegrown from fancy-model project memory. Maintained in light-skills. -->
