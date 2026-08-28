# light-skills

A lightweight, self-maintained set of methodology skills for Claude Code. Skills live in this repo under `skills/<name>/` and are symlinked into `~/.claude/skills/`. No plugins, no hooks — each skill loads only when invoked, and every skill is both model-routable and user-invocable as `/<name>`.

**Two design principles:**

1. **Methodology only.** These skills carry transferable method, never business knowledge. Domain facts (table quirks, field semantics, repo paths) live in project memory and per-repo reference docs.
2. **Uniform `to-` prefix.** The prefix is a namespace: it avoids collisions with built-in commands and other skill sets, and makes the batch visually one family: `/to-grill`, `/to-spec`, `/to-plan`, `/to-handoff`, `/to-tdd`, `/to-debug`, `/to-review`, `/to-query`, `/to-backfill`.

## Roster

Ordered by where they sit in the work lifecycle:

| Name | Purpose | Origin |
|------|---------|--------|
| to-grill | Relentless interview to stress-test a plan or design before work starts | adapted from mattpocock/skills (MIT) |
| to-spec | Turn the current conversation into a spec saved to the repo's plans directory | adapted from mattpocock/skills (MIT) |
| to-plan | Implementation plans that decompose work into independently verifiable tasks | homegrown, inspired by superpowers writing-plans |
| to-handoff | Compact session state into a handoff document a fresh session can pick up | adapted from mattpocock/skills (MIT) |
| to-tdd | Red-green TDD skeleton plus an ML appendix (fixture rules, traced-model release smoke gate) | skeleton from mattpocock/skills (MIT), ML appendix homegrown |
| to-debug | Root-cause-first debugging discipline with four phases | copied from the superpowers plugin v6.3.0 (MIT) |
| to-review | Pre-delivery self-review gate for analysis deliverables: generic checklist + causal-inference mines | homegrown from refuted-conclusion post-mortems |
| to-query | Query-hygiene methodology for partitioned warehouse tables (liveness, sentinels, joins, double counting) | homegrown from query-incident post-mortems |
| to-backfill | Backfill discipline for multi-layer pipelines: propagation assertions, fill-holes-not-overwrite, archiving | homegrown from backfill incidents |

## Install

Symlink each skill directory into `~/.claude/skills/`. New symlinks are picked up at the next Claude Code session start.

```bash
for n in to-grill to-spec to-plan to-handoff to-tdd to-debug to-review to-query to-backfill; do
  ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/$n/ ~/.claude/skills/$n
done
```

## Sources & licenses

Adapted files retain attribution comments at the bottom of each SKILL.md. mattpocock/skills and superpowers are both MIT-licensed. Homegrown skills distill this user's own post-mortems and have no upstream.

## Maintenance

- Homegrown skills grow by appending newly confirmed patterns when a real conclusion or pipeline dies in a new way — method only; the specific table/field/repo facts go to project memory instead.
- Adapted skills are frozen snapshots — sync upstream manually only if something breaks.
