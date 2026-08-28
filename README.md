# light-skills

A lightweight, self-maintained set of methodology skills for Claude Code. Skills live in this repo under `skills/<name>/` and are symlinked into `~/.claude/skills/`. No plugins, no hooks — each skill loads only when invoked, and every skill is both model-routable and user-invocable as `/<name>`.

**Two design principles:**

1. **Methodology only.** These skills carry transferable method, never business knowledge. Domain facts (table quirks, field semantics, repo paths) live in project memory and per-repo reference docs.
2. **One-word imperative names.** The roster reads like a command palette: `/grill`, `/spec`, `/handoff`, `/tdd`, `/debug`, `/review`, `/query`, `/backfill`.

## Roster

Ordered by where they sit in the work lifecycle:

| Name | Purpose | Origin |
|------|---------|--------|
| grill | Relentless interview to stress-test a plan or design before work starts | adapted from mattpocock/skills (MIT) |
| spec | Turn the current conversation into a spec saved to the repo's plans directory | adapted from mattpocock/skills (MIT) |
| handoff | Plan / handoff documents a fresh session can pick up, following repo conventions | homegrown, inspired by mattpocock handoff + superpowers writing-plans |
| tdd | Red-green TDD skeleton plus an ML appendix (fixture rules, traced-model release smoke gate) | skeleton from mattpocock/skills (MIT), ML appendix homegrown |
| debug | Root-cause-first debugging discipline with four phases | copied from the superpowers plugin v6.3.0 (MIT) |
| review | Pre-delivery self-review gate for analysis deliverables: generic checklist + causal-inference mines | homegrown from refuted-conclusion post-mortems |
| query | Query-hygiene methodology for partitioned warehouse tables (liveness, sentinels, joins, double counting) | homegrown from query-incident post-mortems |
| backfill | Backfill discipline for multi-layer pipelines: propagation assertions, fill-holes-not-overwrite, archiving | homegrown from backfill incidents |

## Install

Symlink each skill directory into `~/.claude/skills/`. New symlinks are picked up at the next Claude Code session start.

```bash
for n in grill spec handoff tdd debug review query backfill; do
  ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/$n/ ~/.claude/skills/$n
done
```

## Sources & licenses

Adapted files retain attribution comments at the bottom of each SKILL.md. mattpocock/skills and superpowers are both MIT-licensed. Homegrown skills distill this user's own post-mortems and have no upstream.

## Maintenance

- Homegrown skills grow by appending newly confirmed patterns when a real conclusion or pipeline dies in a new way — method only; the specific table/field/repo facts go to project memory instead.
- Adapted skills are frozen snapshots — sync upstream manually only if something breaks.
