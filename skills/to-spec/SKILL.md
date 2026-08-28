---
name: to-spec
description: "Turn the current conversation into a spec saved to the repo's plans directory: no interview, just synthesis of what you've already discussed. User-invoked only — never trigger it on your own."
disable-model-invocation: true
---

# Specs

Turn the current conversation context and codebase understanding into a spec. Do not interview the user — synthesize what you already know.

## Where it goes

Follow the repo's existing plans/design-docs convention if one exists; otherwise default to `docs/plans/`. Filename: `YYYY-MM-DD-<feature-name>-spec.md` with today's actual date. Do not publish it anywhere online.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's established vocabulary (CLAUDE.md / AGENTS.md, existing docs) throughout the spec, and respect any documented architecture decisions in the area you're touching.

2. Sketch out the **seams** at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better — the ideal number is one. Check with the user that these seams match their expectations.

3. Write the spec using the template below, then save it (see "Where it goes").

## Template

Emit the spec with these sections, as `##` headings in the saved file. The block below is the template, not this skill's own structure:

```markdown
## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories, each in the form:

1. As an <actor>, I want a <feature>, so that <benefit>

  (e.g. As a mobile bank customer, I want to see balance on my accounts,
   so that I can make better informed decisions about my spending)

Cover every capability the feature actually requires — completeness of coverage,
not length. A story you would argue against in review does not belong in the spec.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do not include specific file paths or code snippets. They may end up being
outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more
precisely than prose can (state machine, reducer, schema, type shape), inline it
within the relevant decision and note briefly that it came from a prototype.
Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- What makes a good test here (external behavior only, never implementation
  details — see the `to-tdd` skill)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.
```

<!-- Source: adapted from mattpocock/skills `to-spec` (MIT); issue-tracker publishing replaced with a local plans-dir save. Maintained in way-skills. -->
