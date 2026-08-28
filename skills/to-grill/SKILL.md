---
name: to-grill
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking. Triggered by "grill", "逼问我", "拷问".
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. The deliverable is a fully explored decision space — nothing silently assumed.

## The design tree

Map the discussion as a **design tree**: every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you haven't heard yet.

## Rounds

Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each answered round reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

## Facts are yours, decisions are the user's

Finding facts is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, data tables, tool output), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait — ask the rest of the frontier now. The decisions are the user's: put each to them and wait.

## Done when

The frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on the plan until the user confirms you have reached a shared understanding.

<!-- Source: adapted from mattpocock/skills `grilling` (MIT). Maintained in way-skills. -->
