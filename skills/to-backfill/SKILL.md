---
name: to-backfill
description: Discipline for one-off data backfills in multi-layer pipelines — downstream propagation assertions, fill-holes-not-overwrite, archive layout. Triggered by "补数", "backfill", "回填".
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

## Fill holes, don't overwrite

When backfilling a column that multiple sources write, an unconditional overwrite erases other sources' truth. Default to **filling only empty cells**; overwriting non-empty values requires explicit sign-off, with a before/after count of values changed.

Audit source-table quirks before computing fill values: partitions may be rewritten rather than appended (history not reproducible from snapshots), ids may be truncated or prefixed, timestamp columns may be epoch-zero before some date, and a lost partition must be excluded rather than read as zeros.

## Archive discipline

One-off backfill scripts go into a dedicated per-task directory (dated, named), self-contained:

- `README.md` — background, parameters, execution order, current status
- runnable scripts (prep / backfill / downstream re-derivation), using `cd "$(dirname "$0")"` + relative paths
- the verification SQL that asserts propagation

Shared pieces go in a `common/` sibling. Never scatter one-off scripts into production script directories — stray backfill scripts once outnumbered the production SQL around them 16 to 9, unversioned. Follow the repo's existing backfill directory convention when one exists.

<!-- Source: homegrown, generalized from backfill incidents in project memory. Maintained in way-skills. -->
