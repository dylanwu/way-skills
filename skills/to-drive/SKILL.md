---
name: to-drive
description: Coordinate multi-step work that fresh subagents implement, at a price that makes delegating worth it — the cost model, plan-as-state, per-dispatch model tiering, and review as a dispatch. Use when driving any delegated implementation loop. Triggered by "driver mode", "派发执行", "分派子代理".
---

# Driving Delegated Work

This session coordinates; fresh subagents implement. Everything below follows from one equation, and the equation is the reason to read the rest.

## The cost model

**Cost is turns times the driver's context, and the driver is the only context that accumulates.**

A subagent's context dies with it and is read once. The driver's is appended to forever and re-read on every later turn, at the session model's price. So the one place where accumulation is expensive is exactly where coordination lands — and coordination is what driving moves *into* the driver.

Measured on an 11-task run: 373 turns, 119M tokens, 96% of it the driver re-reading itself. Four fifths of that was accumulation; one fifth a fixed per-turn floor of ~64K that no discipline removes.

Two levers follow, and nothing else here matters as much: **take fewer driver turns**, since every one pays the full accumulated context, and **accumulate less** — which is structural, not vigilance.

## The plan is the state; the session is disposable

Grant the driver the disposability it already grants subagents. The plan file carries status, the decisions each unit forced, and findings still open; the conversation carries nothing that matters. A driver runs a few units, brings the plan current, hands off with `to-handoff`, and the next session resumes from the plan with its accumulation at zero.

Three or four sessions across one plan cost roughly half of one long driver. Past four, the floor dominates and the handoffs stop paying for themselves.

Nothing in this skill asks you to notice your context growing. That is the point of putting the state in a file.

## Dispatching

- **One unit of work per subagent.** The brief is its whole world and inherits nothing from this conversation: what to build, the files it may touch, and the command that proves it worked. It returns status, that command's output, and concerns — never a diff. Larger artifacts travel as file paths.
- **Name the model on every dispatch, implementers and reviewers alike.** An omitted model silently inherits the session's, usually the most capable and most expensive; that is how a quota goes at once. Transcription-grade work (the brief carries near-exact content, one or two files) → cheapest tier. Prose-driven or multi-file work → standard tier, because cheap models take 2–3× the turns there and cost more overall: turn count beats token price. Work whose *design* is still in question is not a dispatch at all.
- **A dispatch costs two driver turns, out and back; an inline edit costs one.** Amortise rather than multiply — several corrections of the same shape travel as one dispatch carrying the list, and work smaller than a unit is not worth dispatching.
- **If you edit implementation code, you have stopped driving.** `Edit` or `Write` against implementation is the trigger, not a judgement call: discard it and re-issue as a dispatch. Writing to the plan is the opposite — that is the job.
- **Parallelise only disjoint units**, never two implementers in the same files; isolate in worktrees if they must overlap.
- **Escalate, don't grind.** Resume the same agent with the findings once or twice; still stuck, a fresh agent one tier up; three failed fixes means the design is the problem, not the attempt (`to-debug`).

## Review is a dispatch too

Review each unit before opening the next — an unreviewed unit is not done. It is cheap here precisely because one unit's diff is small; a whole-branch pass costs what it costs by re-reading everything at once, and grows dearer the longer it is postponed.

Dispatch it rather than reading it: reviewing inline burns the context you need for driving, while a dispatched review keeps both the diff and the evaluation in the reviewer's context and returns only findings. Send it to a different agent than the one that wrote the unit, and price the two questions separately — *did it do what was asked and nothing more* is mechanical comparison against the brief, which the cheapest tier handles; *is this code you would keep* is judgement, and wants roughly the tier that would have designed it.

**The reviewer's brief carries the constraints, because the price is set by what it reads and re-runs.** Do the whole review yourself and never spawn a reviewer of your own: this process already grants every review seat the work gets, and a spawned one duplicates a seat at full cost while its verdict counts for nothing. The diff *is* your view of the change, so don't re-open changed files or crawl the codebase — step outside it only for a risk you can name, one focused check each, reporting both the risk and the check. Treat the implementer's test claims as unverified and check them against the diff instead of re-running the suite. Stay read-only on the checkout. Return the report alone: every line a verdict, a finding with `file:line`, or a check that was run. Skip anything tooling already enforces.

Sort findings instead of fixing as you read — fix now, fix before the next unit, write down — and never fix them in the driver session; send them back. Verify a finding before implementing it, since a reviewer can be wrong: "implement this properly" against something with no caller means delete it, not complete it.

**A re-review after a fix round is scoped and does not extend the loop.** Verdict each prior finding `ADDRESSED` or `NOT ADDRESSED` with file:line — *attempted* is not addressed — then inspect the fix diff alone for new breakage. Anything noticed outside it is an out-of-scope note for the end, never a blocker. Without that boundary every round costs a fresh review and the loop never terminates, because each pass finds something new.

## The end-of-branch pass

Some problems exist only at the scale of a whole change: one logical change forcing scattered edits, one module edited for unrelated reasons, the same switch recurring across files. Those get one pass at the end — **dispatched, with a named model and that short list as its entire brief.** If per-unit review did its job, the end pass is a narrow question, not a re-review of everything.

Do not hand it to the harness's own review command. Such a command has no tier of its own: it is the session model's shadow — confirm it the cheap way by switching the session's model and watching the review follow — and it fans out into several parallel agents on that model, arriving when the session is longest and the quota thinnest.

## Without dispatch

Some harnesses have none; Codex CLI has neither dispatch nor per-dispatch model selection. Then **never narrate a dispatch you did not make**, and: review is your own diff, read cold against the evidence by the same two questions; escalation becomes a design question, since there is no fresh agent to hand it to; units run serially, though the disjointness analysis still says which could be reordered. The cost model is unchanged and bites harder, because implementation lands in your context too — so plan-as-state matters more here, not less. Where the harness offers only a session-wide effort setting, that is the user's knob, not yours: say so before a long cheap stretch rather than after.

<!-- Source: distilled from superpowers v6.3.0 `subagent-driven-development`, `requesting-code-review`, `receiving-code-review` and mattpocock `code-review` (MIT), reorganised around a measured cost model. Maintained in way-skills. -->
