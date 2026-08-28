---
name: review
description: Pre-delivery self-review gate for data analysis reports, dashboards, and conclusions. Run BEFORE delivering any analysis deliverable. Generic checklist + causal-inference mines. Triggered by "交付前自查", "analysis review", "复查报告", "证伪".
---

# Review — the analysis delivery gate

Before any analysis report / dashboard / conclusion ships, walk every headline claim through this gate. For each claim: pass, or fix, or **downgrade the claim** (from conclusion to hypothesis). First-round conclusions die often — a single routine sweep once had 3 of its entity-level conclusions refuted on re-examination.

## Part 1 — Generic gate

1. **Conclusion–evidence chain.** Every headline claim traces to a specific query/number present in the report. No claim may rest on a filter you invented: WHERE conditions come only from documented table semantics, playbooks, or the user — never from plausible inference. A speculative filter can silently drop valid data and still look reasonable.
2. **Baseline legality.** Entity-level (account / campaign / segment) comparisons never use a single-day baseline — any day is somebody's anomaly day (alternate-day delivery, one-day spikes, budget rebuilds, holidays and promo days). Use a ~10-day series, median of several recent days as baseline, mark entities whose day/median ratio exceeds ~3× as baseline-anomalous, and check the baseline day itself for calendar events. Sparklines expose shapes (alternate-day patterns) that ratios can't.
3. **Composition / Simpson check.** Any ratio-metric group comparison must be stratified over known confounders (Mantel-Haenszel). Convergence test: adding one more stratification dimension should move Δ by < 0.5pp — "reported by dimension" does not exempt you from controlling the *other* dimensions inside each cell. Identify the structural dimensions known to differ (platform, channel, entity mix) and stratify by them by default; cross-day model comparisons stratify by the entity whose mix shifts.
4. **Sample size.** Small cells (n < ~100) are anecdotes, not findings — a "clear bias" once vanished when three thin morning hours were widened to the full day. Relative risks carry log-delta CIs, proportions carry Wilson intervals. Check the finding survives the full window, not a cherry-picked slice.
5. **Data liveness.** A registered partition is not a readable partition: probe partition metadata, then count per partition. Check retention windows before historical queries. If the same table exists on two engines/clusters, reconcile row counts before trusting either. Callback-based metrics need closed-loop complete windows — same-day data undercounts delayed events.
6. **Which side moved.** A two-sided ratio gap (ours vs theirs) never names a culprit by itself — numerator collapse and denominator inflation draw the same curve. Compare each side's *absolute* volume day-over-day against a healthy reference day first.
7. **Refutation pass.** For each surviving headline claim, spend one honest attempt to kill it: what confounder, data defect, or alternative mechanism would produce the same numbers? If you can't articulate the strongest counter-explanation, the claim isn't ready.

## Part 2 — Causal-inference mines

- **Multi-value features**: "has x vs lacks x" is contaminated when a dominant value exists — the "lacks x" group is a mixture of rows hitting *other* values, which can manufacture significant effects of the wrong sign. Use **"only x" vs "all empty"**, plus a dose table (hit 0/1/2/3 values) where monotonicity is independent evidence, plus MH stratification.
- **Channel confounding**: when two sub-populations differ structurally (integration type, platform, source), pooled effects can flip sign vs within-group effects — a real evaluation flipped from +4.2% pooled to −2.8% stratified. Split by the structural dimension by default; aggregate only via within-group stratification.
- **Placebo floor**: independently-trained or independently-measured arms need a placebo run to establish the noise floor — thresholds set without one can sit entirely inside noise.
- **Prospective signals**: a signal that is *pushed/deployed* validates on post-deployment data only; pre-deployment history can show the opposite sign, with the time break exactly at the deployment moment. Backtesting a forward-looking signal on its own past misjudges it.
- **Binary vs dose**: check whether an effect is binary before telling a dose-response story — presence/absence signals repeatedly masquerade as gradable ones.
- **Calibration O/E discipline**: compute observed/expected on the population the model actually scores, over closed-loop complete windows, with sentinel (unscored) rows filtered out first.

## Maintenance

This gate grows by subtraction from reality: every time a delivered or almost-delivered conclusion dies, its killer pattern gets appended here. Domain-specific mine lists (table quirks, field semantics) do NOT belong in this skill — they live in project memory and per-repo reference docs.

<!-- Homegrown methodology, distilled from refuted-conclusion post-mortems in project memory. Maintained in light-skills. -->
