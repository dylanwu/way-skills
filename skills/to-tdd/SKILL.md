---
name: to-tdd
description: Red → green test-driven development, run in driver mode by default (fresh subagents implement each slice, model matched to slice complexity). Use when building features or fixing bugs test-first, or when changing model training / feature encoding / calibration code that has a pure-function core. Triggered by "TDD", "红绿循环", "test-first".
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

## Before the first red

Reaching for this skill means the work is feature-scale — **never run the loop on the default branch**. Create a feature branch first, preferably in a **worktree** so the main checkout stays clean and usable:

```bash
git worktree add ../<repo>-<feature> -b feature/<name>
```

Every slice — including subagent dispatches — runs inside it. This also means the branch already exists when it's time to submit the MR/PR, and parallel slices that must touch overlapping files get their isolation for free (see Driver mode).

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (use the built-in `/code-review` or `/simplify`), not the red → green implementation cycle.

## Driver mode (default)

Run the loop as a **driver**: this session coordinates; fresh subagents implement. The driver's context stays clean for seam decisions and review, and each cycle's tool output stays out of it.

- **Dispatch one slice per subagent.** The brief is the subagent's whole world — it inherits nothing from this conversation. It contains: the seam under test, the failing test's intent (or exact code), the files it may touch, and the command that proves red → green. The subagent returns status, the test command with its output, and concerns — not the full diff. Hand larger artifacts over as file paths, never pasted content.
- **Name the model explicitly, matched to slice complexity.** An omitted model silently inherits the session's — usually the most capable and most expensive. Transcription-grade slices (the brief carries the exact test and near-exact implementation, 1–2 files) → cheapest tier. Prose-driven implementation or multi-file integration → standard tier; cheap models take 2–3× the turns on multi-step prose work and cost more overall — turn count beats token price. Design judgment (the seam itself is in question) → not a dispatch at all; that is driver work, settled with the user.
- **Review between cycles.** Read the diff and the test evidence before starting the next slice — a slice the driver hasn't reviewed isn't green. Never fix findings in the driver session; send them back.
- **Escalate a stuck slice, don't grind it.** Resume the same agent with the findings once or twice; still stuck → fresh agent, one model tier up. Three failed fixes → stop and question the design (`to-debug`'s architecture rule).
- **Parallelize only disjoint slices.** Slices on the same seam are serial by nature — each test responds to what the last cycle taught. Slices on different seams touching disjoint files may run concurrently; never two implementers in the same files, and isolate in worktrees if they must overlap.
- **Batch same-shape work.** Several tiny edits of the same kind (a rename, a constant, a field) are one dispatch carrying the list, not N dispatches.

## ML appendix

### Where TDD pays off

The TDD sweet spot in ML code is the **pure-function layer**: feature encoding / mapping, dropout & mask rules, calibration computations. Pipeline SQL and training loops are poor TDD targets — their gates are different (see the `to-backfill` and `to-review` skills).

### Fixture iron rules

- **Encoding tests must use a feature whose mapped id ≠ raw value.** Identity-mapped features (mapped id == raw value) make a test pass even when the code confuses the two encoding domains — a Critical encoding bug once escaped unit tests exactly this way. Pick a fixture feature where the two domains are distinguishable.
- **Pin down which encoding domain each interface consumes.** If an input column is already post-mapping, a test must fail when consumer code translates it a second time.
- **Sentinel values belong in fixtures.** "Unscored/missing" sentinels must appear in test inputs, and sentinel conventions change over time (a real migration merged `-1` into `0`) — the right tests must fail when they do; prefer range predicates over equality on sentinels.

### Release smoke gate (the four checks)

Before deploying ANY model change, all four must pass:

1. **Traced vs eager parity** — traced model output matches eager `forward()` element-wise on a real batch.
2. **Traced batch > 1** — `jit.trace` freezes python ints (`torch.ones(batch_size)` becomes batch=1 forever; use `torch.ones_like(x[:, 0])`). Any *new eval-time in-model logic* must be exercised through the **traced** graph with batch > 1 — train-only logic never enters the traced graph, so tracing bugs hide until the first eval-time rule lands.
3. **Sentinel inputs** — unscored / sentinel rows through the traced model produce defined outputs, not garbage.
4. **Channel-off uses a deterministic mask, never dropout with p=1.0** — dropout is train-only; p=1.0 leaves the embedding untrained yet *read at inference*, producing a seed-dependent bias. A mask is deterministic on both ends (verifiable bit-exact).

<!-- Source: skeleton adapted from mattpocock/skills `tdd` (MIT); driver mode distilled from superpowers `subagent-driven-development` (MIT); ML appendix homegrown from project post-mortems. Maintained in light-skills. -->
