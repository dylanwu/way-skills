---
name: to-tdd
description: Red → green test-driven development with per-slice code review built into the loop, run in driver mode where the harness supports subagent dispatch (fresh subagent per slice, model matched to complexity) and solo otherwise. Use when building features or fixing bugs test-first, or when changing model training / feature encoding / calibration code that has a pure-function core. Triggered by "TDD", "红绿循环", "test-first".
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

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

Reaching for this skill means the work is feature-scale — **never run the loop on the default branch**. Set up isolation first:

1. **Already isolated?** If the session is already inside a linked worktree (harness-created or otherwise), use it — never nest another.
2. **Prefer the harness's native worktree tool** if it has one (Claude Code: `EnterWorktree`) — it owns placement, branching, and cleanup. Without one — Codex CLI has none — fall back to git, project-local:
   ```bash
   git check-ignore -q .worktrees || { echo ".worktrees/" >> .gitignore && git add .gitignore && git commit -m "ignore worktrees"; }
   git worktree add .worktrees/feature-<name> -b feature/<name>
   ```
   The worktree lives inside the project (`.worktrees/` at the repo root) and the directory must be git-ignored before anything is created in it.
3. **Verify a clean baseline** — run the existing test suite before writing the first red. A dirty baseline makes every later failure ambiguous.

Every slice — including any subagent dispatches — runs inside the worktree; the branch already exists when it's time to submit the MR/PR, and parallel slices that must touch overlapping files get their isolation for free (see Driver mode).

**After the MR merges**, clean up in the same motion as returning to the default branch — a merged worktree left behind is stale state, exactly like a merged branch:

```bash
git worktree remove .worktrees/feature-<name> && git branch -d feature/<name>
```

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** Review names what wants refactoring (see below); acting on it is a separate motion, not part of a red → green cycle. Whole-branch passes belong to the harness's own review (Claude Code: `/code-review`, `/simplify`; Codex: `$review-agent`) — once, at the end, not per slice.

## Reviewing a slice

Review every slice before opening the next one — an unreviewed slice is not green. This is cheap exactly because the diff is one slice; a whole-branch review costs what it costs because it re-reads everything at once, and it gets dearer the longer you postpone it. Paying per slice is how you avoid ever paying that bill.

The loop has already proved the behavior — red, then green. So review asks the two things the test cannot, and keeps them apart, because a slice can pass either one while failing the other:

- **Did it do what the slice asked, and nothing more?** Behavior beyond the failing test is scope creep however reasonable it looks. Check too that the test pins the *requirement*, not whichever implementation happened to satisfy it.
- **Is this code you would keep?** Judgement calls, never verdicts, and a documented project standard always overrides them. At slice scale the ones that can actually show up: a name that doesn't say what the thing does; logic duplicated from a hunk nearby; a function reaching into another object's data more than its own; the same few parameters travelling together, wanting to be a type; a primitive standing in for a domain concept; abstraction or parameters added for a need this slice doesn't have.

**Skip anything tooling already enforces.** Formatting, lint rules, type errors — spending review on what CI is about to say is pure waste.

Sort findings rather than fixing as you read: **fix now** (wrong behavior, broken build, security), **fix before the next slice** (real defects, not urgent), **write down** (everything else). That last tier is where review budgets die. Naming a smell is review; fixing it is refactoring, which is still not part of the loop.

**Verify a finding before implementing it.** A reviewer — human or agent — can be wrong about this codebase. Check it against reality and push back with reasoning instead of agreeing performatively. When a finding says to implement something properly, grep for a caller first: an unused thing gets deleted, not completed. If several findings arrive and any is unclear, settle all of them before implementing any — they are often related, and half-understood feedback implements the wrong thing.

Some smells only exist at the scale of a whole change: one logical change forcing scattered edits, one module edited for unrelated reasons, the same switch recurring across files. Those are what the harness's full review is for — once, at the end, not per slice.

## Driver mode (default where the harness supports it)

Run the loop as a **driver**: this session coordinates; fresh subagents implement. The driver's context stays clean for seam decisions and review, and each cycle's tool output stays out of it.

**First confirm the harness can dispatch subagents.** If it cannot — Codex CLI has no dispatch mechanism and no per-dispatch model selection — go to Solo mode below. Never narrate a dispatch you did not make.

- **Dispatch one slice per subagent.** The brief is the subagent's whole world — it inherits nothing from this conversation. It contains: the seam under test, the failing test's intent (or exact code), the files it may touch, and the command that proves red → green. The subagent returns status, the test command with its output, and concerns — not the full diff. Hand larger artifacts over as file paths, never pasted content.
- **Name the model explicitly, matched to slice complexity.** An omitted model silently inherits the session's — usually the most capable and most expensive. Transcription-grade slices (the brief carries the exact test and near-exact implementation, 1–2 files) → cheapest tier. Prose-driven implementation or multi-file integration → standard tier; cheap models take 2–3× the turns on multi-step prose work and cost more overall — turn count beats token price. Design judgment (the seam itself is in question) → not a dispatch at all; that is driver work, settled with the user.
- **Review between cycles — dispatch it, don't read it.** Reviewing the diff inline burns the context you need for driving; dispatched, the diff and the evaluation live in the reviewer's context and only the findings come back. Brief it with the slice's intent, the diff range and the test evidence — never this session's history. Never fix findings in the driver session; send them back.
- **Escalate a stuck slice, don't grind it.** Resume the same agent with the findings once or twice; still stuck → fresh agent, one model tier up. Three failed fixes → stop and question the design (`to-debug`'s architecture rule).
- **Parallelize only disjoint slices.** Slices on the same seam are serial by nature — each test responds to what the last cycle taught. Slices on different seams touching disjoint files may run concurrently; never two implementers in the same files, and isolate in worktrees if they must overlap.
- **Batch same-shape work.** Several tiny edits of the same kind (a rename, a constant, a field) are one dispatch carrying the list, not N dispatches.

## Solo mode (no subagent dispatch)

The same loop in one context. Unchanged: red before green, one slice at a time, seams confirmed up front, worktree isolation. What replaces dispatch:

- **Review between cycles still happens**, by the same two questions — but it is your own diff, so read it cold against the test evidence before opening the next slice, and say what you checked. Self-review that skips the diff is not review.
- **Cost control is a user-side knob, not yours.** With no model tiering, the only lever is the session's reasoning-effort setting (Codex: `model_reasoning_effort`), and you cannot change it mid-run. If a long stretch of transcription-grade slices is coming, say so and let the user dial it down before you start.
- **Escalation becomes a design question, not a retry.** With no fresh agent to hand the slice to, a slice that fails twice goes straight to `to-debug`'s architecture rule: stop and question the design with the user.
- **No parallel slices.** Run them serially. The disjointness analysis still earns its keep — it tells you which slices are independent enough to reorder.
- **Context hygiene is now yours.** Prefer file paths over pasted content, and do not carry a finished slice's tool output into the next one.

## ML appendix

### Where TDD pays off

The TDD sweet spot in ML code is the **pure-function layer**: feature encoding / mapping, dropout & mask rules, calibration computations. Pipeline SQL and training loops are poor TDD targets — their gates are different (see the `to-backfill` and `to-refute` skills).

**Test through the artifact you deploy, not the one you trained.** Logic that only takes effect at inference never runs during training-time checks, so a whole class of bug stays invisible until the first such rule ships. Exercise the exported model on a realistic batch shape — deployment-specific release gates themselves are project knowledge and belong in that project's docs, not here.

### Fixture iron rules

- **Encoding tests must use a feature whose mapped id ≠ raw value.** Identity-mapped features (mapped id == raw value) make a test pass even when the code confuses the two encoding domains — a Critical encoding bug once escaped unit tests exactly this way. Pick a fixture feature where the two domains are distinguishable.
- **Pin down which encoding domain each interface consumes.** If an input column is already post-mapping, a test must fail when consumer code translates it a second time.
- **Sentinel values belong in fixtures.** "Unscored/missing" sentinels must appear in test inputs, and sentinel conventions change over time (a real migration merged `-1` into `0`) — the right tests must fail when they do; prefer range predicates over equality on sentinels.

<!-- Source: skeleton adapted from mattpocock/skills `tdd` (MIT); driver mode distilled from superpowers `subagent-driven-development` (MIT); ML appendix homegrown from project post-mortems; slice review distilled from mattpocock `code-review` and superpowers `requesting-code-review` / `receiving-code-review` (MIT). Its two support files were absorbed here and dropped — all but two of their points already lived in this file, better stated. Maintained in way-skills. -->
