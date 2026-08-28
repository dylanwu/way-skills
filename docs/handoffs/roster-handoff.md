# way-skills roster — handoff

## Goal

Build and maintain **way-skills**: a methodology-only, self-maintained skill roster that runs under both Claude Code and Codex, symlinked into each harness's skills directory (no plugins, no hooks).

## Current state (2026-08-28)

**Done and verified:**

- **10 skills live in both harnesses**, in lifecycle order: `to-explore, to-grill, to-spec, to-plan, to-handoff, to-tdd, to-debug, to-refute, to-query, to-backfill`. Symlinks in `~/.claude/skills/` and `~/.codex/skills/` both point at `way-skills/skills/<name>/`.
- **Dual-harness support** (PR #1, merged as `39f2f0a`). Codex reads the same `SKILL.md` format, so one copy serves both. Verified on `codex-cli 0.150.0-alpha.12.2` by driving `codex exec`: every skill loads, multi-file skill dirs resolve through the symlink, cross-skill references work.
  - Codex **silently ignores** `disable-model-invocation`. `to-spec` needs *both* that frontmatter field and `agents/openai.yaml` → `policy.allow_implicit_invocation: false`. Claude Code ignores the `agents/` dir; Codex ignores the field. Verified both ways: `to-spec` is absent from Codex's implicit list and still loads via `$to-spec`.
  - Codex CLI has **no subagent dispatch and no per-dispatch model selection**, which made to-tdd's driver mode inert there. Driver mode is now gated on the harness having dispatch, with a **Solo mode** section for when it does not. Verified: Codex reads the gate and routes itself to Solo mode.
- **House style holds** across all 10: frontmatter `name` == dir name, `# Title` + intent paragraph + sentence-case sections, English body with Chinese trigger phrases in descriptions, `Source:` attribution comment at file end.
- **Methodology only** — no business knowledge in any skill; domain facts live in project memory (`fancy-model-gitlab`, `chatbi-skills`) and repo docs (`nn_model/backfill/README.md`).

**Done but unverified:**

- `to-explore` (added 2026-08-28) and the `to-review` → `to-refute` rename are **uncommitted** in the working tree. Both are symlinked and load in both harnesses, but neither has run on real work.
- Only `to-handoff` has been exercised in real sessions (twice; the first exposed the bare-root-`HANDOFF.md` naming bug, since fixed). `to-explore`, `to-grill`, `to-tdd` (driver *and* solo), `to-refute`, `to-query`, `to-backfill` have never run end-to-end.

**Not started:**

- `chatbi-skills` repo still has a bare root `HANDOFF.md`; it should move to `docs/handoffs/ftx-consume-history-handoff.md`.
- superpowers plugin is installed-but-disabled; its useful content is extracted (systematic-debugging → `to-debug`, driver mode → `to-tdd`, brainstorming → `to-explore`), so it can be uninstalled.
- `~/.codex/AGENTS.md` is a 0-byte file. The global Claude Code rules (local-HTML-dashboard output, `提交MR` / `切回主分支` shortcuts) have no Codex equivalent. The user **declined** syncing them for now — do not do it unprompted.

## Key decisions and why

- **Self-maintain instead of installing plugins.** superpowers rejected for its SessionStart hook injection; mattpocock set for bulk redundancy. Adapted files are frozen snapshots; sync upstream only if something breaks.
- **Methodology only** (user rule): skills carry transferable method; table quirks, field semantics, repo paths and dated incidents go to project memory and per-repo docs. Refuted: Fancy domain appendices inside skills.
- **English SKILL.md** (user rule): reduces routing ambiguity; Chinese trigger phrases stay in descriptions. Refuted: 中文化.
- **`to-` prefix namespace** after two naming rounds. Refuted: long descriptive names (looked un-batched), bare single words (collision-prone). A name must also survive collision with the *harness's* built-ins — `to-review` became **`to-refute`** on 2026-08-28 because it read as code review next to `/code-review`, `/simplify`, and Codex's `$review-agent`, when its job is falsifying analysis claims.
- **One file tree, two harnesses.** Differences are carried in-tree by files the other harness ignores, rather than forking. Any future skill that must not be model-routed needs both mechanisms.
- **Split skills by direction of work, not by topic.** `to-explore` is divergent (the model proposes 2–3 genuinely different candidates); `to-grill` is convergent (the model interrogates an existing position). Merging them was refuted on the same grounds as the earlier merged `plan-handoff`: one template serves neither. Same reason `to-plan` (forward-looking, zero-context executor) stays separate from `to-handoff` (state compaction at pause time).
- **`to-tdd` defaults to driver mode where dispatch exists**: fresh subagent per slice, model named explicitly and matched to complexity (transcription → cheapest; prose/integration → standard, since turn count beats token price; design judgment → driver + user), review between cycles, escalate a stuck slice one tier up, parallelize only disjoint slices. Worktree-first: `.worktrees/<branch>` project-local and git-ignored, baseline tests before the first red, cleanup after the MR merges.
- **Handoff identity from path or name**: living doc updated in place; `<work-dir>/HANDOFF.md` or `docs/handoffs/<topic>-handoff.md`; bare root `HANDOFF.md` banned. Plans/specs are dated files in `docs/plans/`.
- **Adoption is not a copy.** Upstream material is stripped to method and restyled before it lands. `to-debug` carried four unconverted superpowers support files (636 lines of another project's TypeScript case study, with dated incident numbers) until 2026-08-28, when they were absorbed into an abstract Techniques section and deleted; the directory going from 697 lines to 63 is the size of the gap. A skill directory much heavier than its neighbours is the tell.
- **The ML release gate was removed from `to-tdd`, not fixed** (2026-08-28). It listed four checks; an evidence review against fancy-model memory found exactly one traceable to a real post-mortem (verify traced `batch>1` for any new eval-time in-model logic — recorded verbatim in `feedback_embed_dropout_p1_trap.md`), one restatement of a design rule (channel-off uses a deterministic mask, not dropout `p=1.0`), and two invented to reach the number four (traced-vs-eager parity, sentinel inputs — the latter already covered correctly under Fixture iron rules). The name was itself a mis-transcription: 四件套 in this user's vocabulary means 身份四件套 = `dsp/budget/order/task`, four identity features, not a checklist. Deployment gates are project knowledge and live in fancy-model memory; `to-tdd` keeps only the universal kernel (test the artifact you deploy, not the one you trained). **Do not re-add.**
- **Not absorbed: `to-tickets`** (mattpocock) — its value is tracker integration + multi-agent dispatch, which this single-session workflow doesn't need. Worth stealing later: blocked-by edges for to-plan tasks, expand–contract sequencing for wide refactors.
- **Cheap-model delegation** (user rule): mechanical, fully-specified subtasks go to haiku-tier subagents; the main model orchestrates and verifies. Don't block on questions — take the recommended option and note it.

## Next steps

1. Commit and PR the working-tree changes: `to-explore` + the `to-refute` rename (the user asked for one PR covering both).
2. Dogfood pass — the roster's main open risk. Run `to-explore` → `to-grill` on a real design question, and `to-tdd` (solo mode under Codex, driver under Claude Code) plus `to-refute` on real work; fix the friction found.
3. Move `chatbi-skills/HANDOFF.md` → `chatbi-skills/docs/handoffs/ftx-consume-history-handoff.md` (that repo, not this one).
4. Optionally uninstall the superpowers plugin — content extracted, currently dead weight.
5. Grow the roster only by the two principles + `to-` naming; append newly confirmed mines to `to-refute` / `to-query` / `to-backfill` from future post-mortems (method only; facts to memory).

## Suggested skills

- `to-explore` before proposing any new roster shape; `to-grill` before committing to one.
- Auto-recalled project memory carries the standing rules — check it before writing or renaming any skill here.

## References

- Repo: `/Users/dylanwu/NAS/bobodsm/Career/Fancy/Git/way-skills` · remote `github.com:dylanwu/way-skills` · `README.md` holds the roster table, the two principles, the dual install loop, and the Codex compatibility table.
- `git log` documents every decision round with rationale in the messages; PR #1 carries the Codex evidence in its description.
- Project memory: `~/.claude/projects/-Users-dylanwu-NAS-bobodsm-Career-Fancy-Git-way-skills/memory/`
- Codex CLI for testing: `/Applications/ChatGPT.app/Contents/Resources/codex` (not on `PATH`; the npm `@openai/codex` install is broken — missing vendor binary). Non-interactive check: `codex exec --ephemeral -s read-only`.
- Source material: superpowers 6.3.0 cache at `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/`; mattpocock/skills via `gh api repos/mattpocock/skills/...`.
