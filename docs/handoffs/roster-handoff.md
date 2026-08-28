# way-skills roster — handoff

## Goal

Build and maintain **way-skills**: a 9-skill, methodology-only, self-maintained skill roster for Claude Code, symlinked into `~/.claude/skills/` (no plugins, no hooks).

## Current state (2026-08-28)

**Done and verified:**

- All 9 skills live and recognized by the harness: `to-grill, to-spec, to-plan, to-handoff, to-tdd, to-debug, to-review, to-query, to-backfill`. Symlinks in `~/.claude/skills/` point to `way-skills/skills/<name>/`.
- House style unified and lint-checked (frontmatter name == dir name, `# Title` + intent paragraph + sentence-case sections, English body with Chinese trigger phrases in descriptions, `Source:` attribution comment at file end, zero upstream-jargon leftovers).
- Business knowledge fully stripped — skills carry method only; domain facts remain in project memories (`fancy-model-gitlab`, `chatbi-skills`) and repo docs (`nn_model/backfill/README.md`).
- Repo renamed `light-skills` → `way-skills`, pushed to `github.com:dylanwu/way-skills` (branch `main`, upstream tracking set).
- Project memory migrated to the way-skills path key: `MEMORY.md` + 3 feedback entries (English-only SKILL.md; methodology-only + `to-` naming; cheap-model delegation).

**Done but unverified:**

- Only `to-handoff` has been exercised in a real session (once, in another session — it exposed the bare-root-HANDOFF.md naming bug, since fixed). `to-tdd` driver mode + worktree flow, `to-review`, `to-query`, `to-backfill` have never run end-to-end on real work.
- `to-tdd` ML appendix "four checks" release gate is an interpretation (traced-vs-eager, traced batch>1, sentinel inputs, mask-not-dropout); the user has not confirmed it matches their intended 四件套.

**Not started:**

- `chatbi-skills` repo still has the bare root `HANDOFF.md` from the other session; it should move to `docs/handoffs/ftx-consume-history-handoff.md`.
- superpowers plugin is still installed-but-disabled; its useful content (systematic-debugging + support files) is extracted, so it can be uninstalled.

## Key decisions and why

- **Self-maintain instead of installing plugins.** superpowers rejected for its SessionStart hook injection (invasive), mattpocock set for bulk redundancy. Adapted files are frozen snapshots; sync upstream only if something breaks.
- **Methodology only** (user rule): skills carry transferable method; table quirks / field semantics / repo paths / dated incidents go to project memory and per-repo docs. Refuted alternative: Fancy domain appendices inside skills (an earlier version had them; stripped).
- **English SKILL.md** (user rule): reduces routing ambiguity; Chinese trigger phrases stay in descriptions. Refuted: 中文化 (an earlier version was Chinese; reverted).
- **`to-` prefix namespace** after two naming rounds. Refuted: long descriptive names (looked un-batched), bare single words `grill/spec/...` (collision-prone with builtins and other skill sets).
- **`grill-me` alias merged into `to-grill`** — the alias bought only a command-name flavor; deleted.
- **`to-plan` and `to-handoff` split** — a plan is forward-looking for a zero-context executor; a handoff is state compaction at pause time. Refuted: the merged `plan-handoff` (one template served neither).
- **Handoff identity from path or name**: living doc updated in place; `<work-dir>/HANDOFF.md` or `docs/handoffs/<topic>-handoff.md`; bare root `HANDOFF.md` banned. Plans/specs are dated files in `docs/plans/` (`<topic>-plan.md`, `<feature>-spec.md`).
- **`to-tdd` defaults to driver mode** (distilled from superpowers subagent-driven-development): fresh subagent per slice, model named explicitly and matched to complexity (transcription → cheapest; prose/integration → standard — turn count beats token price; design judgment → driver + user), review between cycles, escalate a stuck slice one tier up, parallelize only disjoint slices, batch same-shape edits. Plus worktree-first: `.worktrees/<branch>` project-local (git-ignored, native tool like EnterWorktree preferred), baseline tests before the first red, `git worktree remove` + branch delete after the MR merges.
- **Not absorbed: `to-tickets`** (mattpocock) — its value is tracker integration + multi-agent parallel dispatch, which the current single-session workflow doesn't need. Worth stealing later: blocked-by edges for to-plan tasks, and the expand–contract sequencing for wide refactors.
- **Cheap-model delegation** (user rule): mechanical, fully-specified subtasks go to haiku-tier subagents; the main model orchestrates and verifies. Don't block on questions — take the recommended option and note it.

## Next steps

1. Move `chatbi-skills/HANDOFF.md` → `chatbi-skills/docs/handoffs/ftx-consume-history-handoff.md` (5 min, that repo not this one).
2. Optionally uninstall the superpowers plugin — content extracted, currently dead weight.
3. Dogfood pass: run `to-tdd` (driver + worktree) and `to-review` on real work; fix friction found. In particular have the user confirm the ML appendix's four release checks match their intended 四件套.
4. Grow the roster only by the two principles + `to-` naming; append newly confirmed mines to `to-review` / `to-query` / `to-backfill` from future post-mortems (method only; facts to memory).

## Suggested skills

- `to-grill` before any further roster-shape debate.
- Auto-recalled project memory carries the standing rules; check it before writing or renaming any skill here.

## References

- Repo: `/Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/way-skills` · remote `github.com:dylanwu/way-skills` · `README.md` holds the roster table, principles, install loop.
- `git log` (12 commits) documents every decision round with rationale in the messages.
- Project memory: `~/.claude/projects/-Users-dylanwu-NAS-bobodsm-Career-Fancy-Git-way-skills/memory/`
- Source material: superpowers 6.3.0 cache at `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/`; mattpocock/skills via `gh api repos/mattpocock/skills/...`.
- Domain knowledge stripped from earlier drafts lives in: fancy-model memory (`.../-Users-dylanwu-NAS-bobodsm-Career-Fancy-Git-fancy-model-gitlab/memory/`), chatbi-skills memory, `nn_model/backfill/README.md`.
