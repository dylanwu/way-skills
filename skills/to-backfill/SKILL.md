---
name: to-backfill
description: Discipline for one-off data backfills in multi-layer pipelines — downstream propagation assertions, verification gates that can actually fail, fill-holes-not-overwrite, archive layout. Triggered by "补数", "backfill", "回填".
---

# Backfill Discipline

A backfill into a multi-layer pipeline is not done until it has propagated to the layer consumers actually read. Every rule here comes from a real incident.

## Iron rule: backfill does not propagate by itself

Filling an upstream table does **not** re-derive its downstream tables. Real incident: upstream showed 71k backfilled rows, downstream had 0 — the consumer (a model) then trained on ~10 samples and produced default-level outputs in production.

After any backfill:

1. **Re-run every downstream derivation** for the backfilled dates, layer by layer, down to the table consumers read.
2. **Assert with a downstream ÷ upstream ratio** per (date, entity) — a ratio far below ~90% means not propagated. Never conclude success from upstream row counts alone.
3. **Know which partition the consumer reads** (e.g. a daily rollup vs hourly partitions) and check that one specifically.
4. **Close the loop on the consequence**, not just the rows: re-run the consumer (retrain, recompute) and verify its output metric recovered.

Run the same ratio check when a new entity ramps up — a thin training/derivation window produces the same default-output failure with no backfill involved.

## Every check must be able to fail

A backfill is only as good as the assertions guarding it, and a wrong assertion is worse than none: it launders an unchecked write into a "checked" one. Three questions before trusting any check in this skill, the propagation ratio above included — every specific trap here is an instance of failing one of them.

- **Does it assert the property, or only something the property implies?** "No marker came back non-zero" and "the row counts match" are both implied by success without implying it back. State the property positively and completely: *every* expected marker present and zero; *every* non-target column identical.
- **What does it do when it receives nothing?** Empty output, a renamed marker, a job that died after printing half its results, a failure swallowed by a pipe — each yields an *absence* of failure signal, so a check that reads absence as success passes hardest exactly when the run went worst. Missing evidence is a failure, never a pass.
- **Have you watched it fail?** Perturb the thing it exists to catch — drop a row, alter one column, truncate the output — and confirm it blocks. A check never seen failing is decoration. This is `to-tdd`'s red-green discipline pointed at the gate.

**Structure the run so a gate can exist at all.** Produce the new data somewhere non-destructive, verify it there, and make the production write a separate step the gate stands in front of — stage, check, publish. A check cannot guard a write that already happened.

In shell specifically: use `set -eo pipefail`, because plain `set -e` sees only the last command of a pipeline and `check | tee log` reports `tee`'s success; and when one run covers N partitions, assert the marker appears N times, because `grep | tail -1` reads only the last.

## Fill holes, don't overwrite

When backfilling a column that multiple sources write, an unconditional overwrite erases other sources' truth. Default to **filling only empty cells**; overwriting non-empty values requires explicit sign-off, with a before/after count of values changed.

**When the write rewrites whole rows to change only some columns**, equal row counts prove nothing about the columns you did not mean to touch. Assert they are untouched: hash the non-target columns per row, group by (hash, +1 for before / −1 for after), and require every group to sum to zero. Generate the column list from the live schema instead of transcribing it, and have a test assert the generated list matches that schema exactly — a hand-copied list of a hundred columns fails silently, in production only.

Audit source-table quirks before computing fill values: partitions may be rewritten rather than appended (history not reproducible from snapshots), ids may be truncated or prefixed, timestamp columns may be epoch-zero before some date, and a lost partition must be excluded rather than read as zeros.

## Archive discipline

One-off backfill scripts go into a dedicated per-task directory (dated, named), self-contained:

- `README.md` — background, parameters, execution order, current status
- runnable scripts (prep / backfill / downstream re-derivation) that cd to their own directory before anything else, then reference SQL by relative path
- the verification SQL that asserts propagation

Shared pieces go in a `common/` sibling. Never scatter one-off scripts into production script directories — stray backfill scripts once outnumbered the production SQL around them 16 to 9, unversioned.

Copy **structure, never invocations.** Layout, naming and file roles are what an earlier task is good for; its binary names, conf flags and cluster parameters were frozen the day it was archived and rot from there. Prefer the most recent task over any older one, and confirm every command you copy still exists in the repo today. Before writing a verification helper, grep for one — an earlier task has often solved the same problem, and its version has already survived review.

<!-- Source: homegrown, generalized from backfill incidents in project memory. Maintained in way-skills. -->
