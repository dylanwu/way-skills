# light-skills

A lightweight, self-maintained set of engineering-process and data-analysis skills for Claude Code. Skills live in this repo under `skills/<name>/` and are symlinked into `~/.claude/skills/`. No plugins, no hooks — each skill loads only when invoked.

## Roster

| Name | Purpose | Origin |
|------|---------|--------|
| grilling | Relentless interview to stress-test a plan or design before work starts | adapted from mattpocock/skills (MIT) |
| grill-me | User-invoked alias for grilling | adapted from mattpocock/skills (MIT) |
| to-spec | Turn the current conversation into a spec saved to the repo's plans directory | adapted from mattpocock/skills (MIT) |
| plan-handoff | Write plan / handoff documents that a fresh session can pick up, following each repo's existing conventions | homegrown, inspired by mattpocock handoff + superpowers writing-plans |
| systematic-debugging | Root-cause-first debugging discipline with four phases | copied from the superpowers plugin v6.3.0 (MIT) |
| tdd | Red-green TDD skeleton plus an ML appendix (fixture rules, traced-model release smoke gate) | skeleton from mattpocock/skills (MIT), ML appendix homegrown |
| analysis-review | Pre-delivery self-review gate for data analysis reports: generic checklist + causal-inference mines + Fancy domain appendix | homegrown from project memory |
| backfill | Fancy-model one-off data backfill discipline: archive layout + downstream propagation assertions | homegrown from project memory |
| ftx-query | Query-trap reference for FTX model-side tables (partitions, sentinels, join keys, double counting) | homegrown from project memory |

## Install

Symlink each skill directory into `~/.claude/skills/`. New symlinks are picked up at the next Claude Code session start.

```bash
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/grilling/ ~/.claude/skills/grilling
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/grill-me/ ~/.claude/skills/grill-me
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/to-spec/ ~/.claude/skills/to-spec
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/plan-handoff/ ~/.claude/skills/plan-handoff
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/systematic-debugging/ ~/.claude/skills/systematic-debugging
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/tdd/ ~/.claude/skills/tdd
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/analysis-review/ ~/.claude/skills/analysis-review
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/backfill/ ~/.claude/skills/backfill
ln -s /Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/light-skills/skills/ftx-query/ ~/.claude/skills/ftx-query
```

## Sources & licenses

Adapted files retain attribution comments at the bottom of each SKILL.md. mattpocock/skills and superpowers are both MIT-licensed. Homegrown skills encode this user's own project knowledge and have no upstream.

## Maintenance

- Domain skills (analysis-review, backfill, ftx-query, tdd appendix) grow by appending new confirmed mines from project memory.
- Adapted skills are frozen snapshots — sync upstream manually only if something breaks.
