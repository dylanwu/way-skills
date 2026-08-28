---
name: to-query
description: Query-hygiene methodology for data-warehouse tables — partition liveness, metadata-vs-scan discipline, sentinels, join verification, double counting. Consult BEFORE writing SQL against partitioned warehouse tables. Triggered by "查数防雷", "query check", "分区探活".
---

# Query Hygiene

Generic trap-prevention for querying partitioned warehouse tables (Hive / Trino / Presto / ClickHouse and kin). Every rule here has drawn blood at least once. Domain-specific table facts (which table has which quirk) do NOT live here — they live in project memory and per-repo reference docs; this skill is the method.

## Before any query

- **Registered ≠ readable.** Partition metadata can list partitions whose files are gone (non-atomic writers, retention purges, mid-rewrite windows). Probe partition metadata first, then `count(*)` per partition to confirm liveness. Depending on the engine, a dead partition either throws (`HIVE_FILE_NOT_FOUND`) or — worse — **silently returns partial data**.
- **Partition-column aggregates never touch the base table.** `MAX(hour)`, `DISTINCT thisdate`, `COUNT(DISTINCT partition_col)`, `ORDER BY partition_col LIMIT 1` are metadata questions: answer them from `"table$partitions"` / `SHOW PARTITIONS`. A single-day WHERE does not make the base-table version safe — it still opens every file in the partition to read a value the metastore already has.
- **No speculative WHERE.** Filters come from documented table semantics, playbooks, or the user — never from plausible inference. Suggest optimizations instead of silently applying them; when unsure, run without the filter and flag the uncertainty.
- **Same-name table ≠ same data.** Two engines/clusters may hold independently produced copies that normally agree and diverge badly during incidents. Metadata can also differ per engine over one physical dataset. Reconcile row counts across engines before any cross-engine conclusion.

## Counting

- **Know the partition layout before aggregating.** Aggregate partitions (a `daily` rollup) can coexist with granular ones (24 hourly) in the same table — an unfiltered scan double-counts. Always constrain every partition dimension explicitly.
- **Know the grain before counting.** Event/callback tables can duplicate rows severalfold; count `DISTINCT` on the verified logical key, and verify the key is actually distinct per event (some id columns are constant).
- **Events land by arrival time, not event time.** A late-arriving event can fall into a different partition than its logical timestamp, orphaning it from the row it belongs with — joining or filtering across the pair silently loses the tail. Quantify the cross-partition fraction before trusting funnel ratios.

## Fields

- **Identify sentinels before aggregating.** "Unscored/missing" encodings (−1, 0, empty string) poison means and rates; filter them explicitly. Sentinel conventions **change over time** — a filter written as `= -1` breaks the day the sentinel migrates to `0`; prefer range predicates and re-verify after upstream releases.
- **A column's name is not its meaning.** Timestamps can be copies of a *different* event's time; a column named for metric A can carry grayscale metric B; encoded columns may already be post-mapping ids that must not be translated again. Verify semantics from the producing SQL or a reference doc, not the name.

## Joins

- **Verify key encoding on both sides.** Keys can silently carry versions/prefixes (versioned device ids, truncated ids) — a mismatched pair joins to ~0 rows with no error and reads as "no overlap". Spot-check match rate against a known-healthy pair first.
- **Check fan-out before joining.** Confirm the join key is unique on the dimension side (or aggregate first); a duplicated key multiplies metrics and the totals still look plausible.
- **Different tables, different keys.** The same logical entity can be keyed differently across tables (user id vs external user id); confirm the documented key pair for each table combination, casting types explicitly.

<!-- Homegrown methodology, generalized from query-incident post-mortems in project memory. Maintained in light-skills. -->
