# way-skills

A lightweight, self-maintained set of methodology skills for **Claude Code and Codex** — both harnesses read the same `SKILL.md` format, so one copy serves both. Skills live in this repo under `skills/<name>/` and are symlinked into `~/.claude/skills/` and `~/.codex/skills/`. No plugins, no hooks — each skill loads only when invoked, and every skill is both model-routable and user-invocable (`/<name>` in Claude Code, `$<name>` in Codex).

**Two design principles:**

1. **Methodology only.** These skills carry transferable method, never business knowledge. Domain facts (table quirks, field semantics, repo paths) live in project memory and per-repo reference docs.
2. **Uniform `to-` prefix.** The prefix is a namespace: it avoids collisions with built-in commands and other skill sets, and makes the batch visually one family: `to-explore`, `to-grill`, `to-spec`, `to-plan`, `to-handoff`, `to-tdd`, `to-debug`, `to-refute`, `to-query`, `to-backfill`.

## Roster

Ordered by where they sit in the work lifecycle:

| Name | Purpose | Origin |
|------|---------|--------|
| to-explore | Two-way exploration of an open idea into 2-3 genuinely different candidate approaches | distilled from superpowers brainstorming (MIT) |
| to-grill | Relentless interview to stress-test a plan or design before work starts | adapted from mattpocock/skills (MIT) |
| to-spec | Turn the current conversation into a spec saved to the repo's plans directory | adapted from mattpocock/skills (MIT) |
| to-plan | Implementation plans that decompose work into independently verifiable tasks | homegrown, inspired by superpowers writing-plans |
| to-handoff | Compact session state into a handoff document a fresh session can pick up | adapted from mattpocock/skills (MIT) |
| to-tdd | Red-green TDD in driver mode (subagents implement, model by complexity), solo fallback where the harness has no dispatch, plus an ML appendix | mattpocock skeleton + superpowers driver mode (MIT), ML appendix homegrown |
| to-debug | Root-cause-first debugging discipline with four phases | copied from the superpowers plugin v6.3.0 (MIT) |
| to-refute | Adversarial self-check that tries to kill every headline claim before an analysis ships: generic gate + causal-inference mines | homegrown from refuted-conclusion post-mortems |
| to-query | Query-hygiene methodology for partitioned warehouse tables (liveness, sentinels, joins, double counting) | homegrown from query-incident post-mortems |
| to-backfill | Backfill discipline for multi-layer pipelines: propagation assertions, fill-holes-not-overwrite, archiving | homegrown from backfill incidents |

## Install

Symlink each skill directory into the harness's skills directory. New symlinks are picked up at the next session start.

```bash
REPO=/Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/way-skills
SKILLS="to-explore to-grill to-spec to-plan to-handoff to-tdd to-debug to-refute to-query to-backfill"

for n in $SKILLS; do ln -s $REPO/skills/$n ~/.claude/skills/$n; done   # Claude Code
for n in $SKILLS; do ln -s $REPO/skills/$n ~/.codex/skills/$n;  done   # Codex
```

## Codex compatibility

Verified on `codex-cli 0.150.0-alpha.12.2` (2026-08-28): all ten load through the symlinks, multi-file skill directories resolve through the symlink, and cross-skill references work. Two harness differences are handled in-tree, so the same files serve both:

| | Claude Code | Codex |
|---|---|---|
| Explicit invocation | `/<name>` | `$<name>` |
| Suppress model routing | frontmatter `disable-model-invocation: true` | `agents/openai.yaml` → `policy.allow_implicit_invocation: false` |
| Project instructions | `CLAUDE.md` | `AGENTS.md` |
| Review command | `/code-review`, `/simplify` | `$review-agent` |
| Subagent dispatch | yes, with per-dispatch model choice | **none** — to-tdd falls back to Solo mode |

Codex silently ignores `disable-model-invocation`, which is why `to-spec` carries both that field and an `agents/openai.yaml`; Claude Code ignores the `agents/` directory in turn. Any future skill that must not be model-routed needs both.

## Sources & licenses

Adapted files retain attribution comments at the bottom of each SKILL.md. mattpocock/skills and superpowers are both MIT-licensed. Homegrown skills distill this user's own post-mortems and have no upstream.

## Maintenance

- Homegrown skills grow by appending newly confirmed patterns when a real conclusion or pipeline dies in a new way — method only; the specific table/field/repo facts go to project memory instead.
- Adapted skills are frozen snapshots — sync upstream manually only if something breaks.
- A skill with a discovery phase needs an entry condition. Written only as a forward procedure, it restarts at step one every time it loads — including when the work is already done and the user just wants it described. State up front what to do when the artifact already exists.
- No shell positional parameters (`$0`, `$1`, …) anywhere in a skill body — the harness substitutes them with the invocation's arguments at load time, silently rewriting the text the model reads. Phrase around them.
- Adoption is not a copy. Upstream material gets stripped to method and restyled before it lands: no other project's identifiers, dated incidents, or house style. `to-debug` shipped with four unconverted support files (636 lines of a TypeScript case study) until they were absorbed into its Techniques section on 2026-08-28 — a skill directory that is much heavier than its neighbours is the tell.
