---
name: analysis-review
description: Pre-delivery self-review gate for data analysis reports, dashboards, and conclusions. Run BEFORE delivering any analysis deliverable. Generic checklist + causal-inference mines + Fancy domain appendix. Triggered by "交付前自查", "analysis review", "复查报告", "证伪".
---

# Analysis Review — the delivery gate

Before any analysis report / dashboard / conclusion ships, walk every headline claim through this gate. For each claim: pass, or fix, or **downgrade the claim** (from conclusion to hypothesis). History says first-round conclusions die often — one routine sweep had 3 of its DSP-level conclusions refuted, and the memory corpus carries 10+ refuted findings that once looked solid.

## Part 1 — Generic gate (any project, any report)

1. **Conclusion–evidence chain.** Every headline claim traces to a specific query/number present in the report. No claim may rest on a filter you invented: WHERE conditions come only from documented table semantics, playbooks, or the user — never from plausible inference (a speculative `err_code = 0` once silently dropped valid data).
2. **Baseline legality.** Entity-level (DSP / order / budget) comparisons never use a single-day baseline — any day is somebody's anomaly day (one sampled day had ≥5 DSPs in abnormal state; another randomly chosen baseline landed on 七夕). Use a 10–11 day series, median of T-5..T-2 as baseline, mark entities with day/median ≥ 3× as baseline-anomalous, and check the baseline day for holidays/promos. Sparklines expose alternate-day delivery patterns that ratios can't.
3. **Composition / Simpson check.** Any ratio-metric group comparison must be stratified over known confounders (MH). Convergence test: adding one more stratification dimension moves Δ by < 0.5pp. "Reported by dimension" does not exempt you from controlling the *other* dimensions inside each cell (信息流 case: +9.58pp → +2.79pp after adding DSP). Cross-day model comparisons stratify by order_id — order mix shifts masquerade as model drift.
4. **Sample size.** Small cells (n < ~100) are anecdotes, not findings (a "biased order" was n=75 in three morning hours; full-day bias was −0.001). RRs carry log-delta CIs, proportions carry Wilson intervals. Check the finding survives the full day/window, not a cherry-picked hour.
5. **Data liveness.** A registered partition is not a readable partition: probe `$partitions` then count per partition; check retention windows before historical queries; if the table exists on two clusters, reconcile row counts before trusting either. Callback-based metrics (CVR/act) need closed-loop full days — same-day data undercounts conversions.
6. **Which side moved.** A two-sided ratio gap (ours vs theirs) never names a culprit by itself — numerator collapse and denominator inflation draw the same curve. Compare each side's *absolute* volume day-over-day against a healthy day first.
7. **Refutation pass.** For each surviving headline claim, spend one honest attempt to kill it: what confounder, data defect, or alternative mechanism would produce the same numbers? If you can't articulate the strongest counter-explanation, the claim isn't ready.

## Part 2 — Causal-inference mines

- **Multi-value features**: "has x vs lacks x" is contaminated when a dominant value exists — the "lacks x" group is a mixture of other hits (produced fake significant negatives, RR 0.79–0.89, that flipped to positive). Use **"only x" vs "all empty"**, plus a dose table (hit 0/1/2/3) where monotonicity is independent evidence, plus MH stratification (raw 1.81× → MH 1.60×).
- **Channel is a confounder**: FTX effect analyses split SDK (`vendor.name LIKE '%mpSDK%'`) / API by default, and per-DSP. Pooling flipped a verdict from +4.2% to −2.8%. Aggregate only via within-channel stratification (MH).
- **Placebo floor**: independently-trained arms need a placebo run to establish the noise floor — thresholds set without one can sit entirely inside noise (prior-anchor c2/c3 case).
- **Prospective signals**: a pushed list/feature validates on post-push data only; pre-push history showed −13% where post-push reality was +14% (time break exactly at push).
- **Binary vs dose**: check whether an effect is binary before telling a dose story (device lists repeatedly proved binary, not dose-responsive).
- **O/E discipline**: CVR calibration O/E is computed on click rows; raw scores are probabilities in [0,1) read directly — after filtering sentinels.

## Part 3 — Fancy domain appendix (quick mines)

- 媒体配送 channel (`vendor_id ≥ 10000`): zero impressions/cost, absent from request-level logs entirely; filter before reconciling with EasyReport (can be 75% of clicks; CVR differs 7×).
- `raw_data` orphan partitions: registered-but-no-directory partitions throw `HIVE_FILE_NOT_FOUND` on trino and *silently drop data* on presto — probe per `thishour` on both.
- `lr_data` double counting: always filter `thishour` (`'daily'` + 24 hourly partitions ≈ ×2); training reads `daily` only; new budgets have no daily partition until day end.
- act rows land in the callback-arrival hour partition: summing act with `clk=1` filter loses ~13.6% of conversions.
- Sentinel migration 2026-08-21: "unscored" merged from `-1` into `0` — filters must be `<= 0`; ver columns dominate PSI rankings after such events, remove them before reading drift reports.
- `geo_code = 156001000000` is the IP-library default value, not Beijing.
- FTX `os` field: 1 = iOS, 2 = Android (inverted vs intuition).
- `common_track_data` duplicates callbacks ~3×: count via `DISTINCT ext_request_id`; its `ext_timestamp` is a *click-time copy*, arrival time is `timestamp`.
- ick impression tracking has 30–60 min write latency — do not read fresh minutes as a drop.
- CAID joins: the 41-char prefix encodes version date; mismatched versions join to ~0 silently.
- Partition-column aggregates (`MAX(hour)`, `DISTINCT thisdate`) go to `$partitions` / `SHOW PARTITIONS`, never the base table — a single-day WHERE does not make the scan safe.

## Maintenance

This gate grows by subtraction from reality: every time a delivered or almost-delivered conclusion dies, its killer pattern gets appended here.

<!-- Homegrown, distilled from fancy-model + chatbi-skills project memory. Maintained in light-skills. -->
