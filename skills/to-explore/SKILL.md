---
name: to-explore
description: Explore an open-ended idea into 2-3 candidate approaches through two-way dialogue — you propose options, not just questions. Use when the shape of the solution is still open, before to-grill hardens one. Triggered by "探索方案", "brainstorm", "有哪些做法", "怎么做比较好".
---

# Exploring Approaches

The divergent half of design. The deliverable is **two or three live candidates** with honest trade-offs and your recommendation — not consensus, not a decision, not a plan. You are a participant here, not an examiner: a session where you only asked questions has failed this skill.

## This or to-grill

Use `to-explore` when the shape of the solution is still open — the user has an idea, a problem, or a direction, but no position yet. Use `to-grill` once a position exists and needs stress-testing.

The tell that you picked wrong: you are interrogating a plan the user has not actually formed. Stop and switch. Interrogation only works against a frame; when there is no frame yet, questions land as pressure instead of clarification.

## Scope check first

Before spending any questions on detail, size the request. If it is really several independent subsystems, say so immediately and help decompose: what are the separable pieces, how do they depend on each other, which one goes first. Then explore only the first piece. Questions spent refining a project that needs decomposing first are wasted questions, and the design they produce is worse for having assumed the whole.

## The loop

1. **Read the context yourself** — files, docs, recent commits — before the first question. Finding facts is your job, never the user's; when a question needs something the environment can answer, go look, and dispatch a subagent for it if the harness has one.
2. **Ask one question at a time.** In exploration the answer changes which question comes next, so a batch commits you to a frame the user has not confirmed. (This is the opposite of `to-grill`'s batched frontier, and deliberately so — there, the frame is already agreed.) Aim at purpose, constraints, and what "done well" would look like.
3. **Propose approaches** once you can state the problem in the user's terms. See below.
4. **Present the chosen one in sections** scaled to their complexity — a few sentences when it is straightforward, a few paragraphs when it is not — and check after each section that it still looks right. Be ready to reopen an earlier section rather than patching around it.

## Proposing approaches

- **Two or three, never one.** A single option is a decision wearing a question's clothes. More than three and you are listing rather than thinking.
- **They must be genuinely different.** One idea at three sizes is one approach — if the candidates differ only in scope or polish, you have not found alternatives yet. Different means a different mechanism, a different place to put the complexity, or a different thing being traded away.
- **Lead with your recommendation and say why.** Ranking is part of the work; an unranked menu pushes the decision back onto the user untouched.
- **Every candidate states what it costs**, not just what it does. An approach with no named downside has not been thought through — find the downside or drop the candidate.
- **Include the option the user did not ask for** when it is genuinely live: the smaller version, the existing tool, the thing they already have, doing nothing. Say plainly when doing nothing is defensible.
- **YAGNI each candidate before showing it.** Strip everything the stated goal does not require. Do not present a feature you would argue against.

## Rules

- **Nothing gets built before the user picks.** Not a scaffold, not a "quick prototype to show the idea". The artifact scales with the task; the approval gate never does. If a question can only be settled by trying something, say so and get a nod for that probe specifically — its output is an answer, and anything it produces stays labeled throwaway.
- **Announce a reopen.** Complexity found later that invalidates the chosen approach goes back to the user as a reopened decision, never as a quiet patch to keep the choice alive.
- **The decision is the user's.** Recommend as hard as you like, then wait.

## Done when

The user picks an approach. This skill writes no files. From here: `to-grill` to stress-test the choice before committing to it, or straight to `to-spec` when the choice is small enough that grilling would be ceremony.

<!-- Source: distilled from superpowers v6.3.0 `brainstorming` (MIT) — its three-path classification, red-flags table, visual companion, and spec-path conventions dropped as ceremony this roster covers elsewhere. Maintained in way-skills. -->
