---
name: ftx-query
description: Query-trap reference for FTX MODEL-SIDE tables (rpt.ftx_nn_*, dwd.d_ad_ftx_*) — partition liveness, sentinels, join keys, double counting. Model-side only; business-side analysis queries route to chatbi's analysis/chatdb skills instead. Triggered by "raw_data", "lr_data", "fea_mapping", "查模型表".
---

# FTX Model-Side Query Traps

Consult before querying any `rpt.ftx_nn_*` or `dwd.d_ad_ftx_*` table. Business questions (profit, delivery diagnosis, DSP comparison) do NOT belong here — route them to the chatbi `analysis` / `chatdb` skills.

## Before any query — the liveness ritual

- **Registered ≠ readable.** Probe `SELECT ... FROM "schema.table$partitions"` first, then `count(*)` per partition. Orphan partitions (metadata registered, HDFS directory gone) throw `HIVE_FILE_NOT_FOUND` on trino and **silently drop data on presto** (an 88% silent loss has happened).
- **Two clusters are two independent pipelines**, not replicas: 阿里云 f-77 (presto) vs 腾讯云 T-157 (trino) normally agree within 0.14% but diverge 11× when a readiness gate halts one side. Reconcile daily row counts before any cross-cluster comparison; a halt can hit impression/click while model_feature stays healthy.
- **Partition-column aggregates never touch the base table.** `MAX(hour)`, `DISTINCT thisdate`, `COUNT(DISTINCT hour)` → `$partitions` / `SHOW PARTITIONS`. A single-day WHERE does not prevent the TB-scale scan.
- **No speculative WHERE.** Filters come from documented semantics, playbooks, or the user — never from plausible inference.

## rpt.ftx_nn_lr_raw_data

- **act rows land in the callback-arrival hour partition** → cross-hour conversions become `clk=0, act=1` orphan rows. Counting conversions with a `clk=1` filter loses ~13.6%. Correct: `sum(act)` filtered by `h` only (`h` on act rows is already the click hour); denominator stays `count(CASE WHEN clk=1 ...)`.
- **NN score encoding**: valid scores are probabilities in `[0,1)` read directly (no transform). Sentinels = unscored: `nn_cvr_raw = -1` (~42% of clicks), `nn_v2_ctr_raw = 0`. Filter sentinels before averaging. `nn_v2_ctr_raw` is actually a grayscale **CVR** v2 (~3% coverage) despite the name. `nn_cvr`/`nn_cvr_raw` are the multi-value (MV/DIN) model's output.
- Raw scores are uncalibrated: ~9× overestimate on cold devices; true-CVR checks need closed-loop full days.

## rpt.ftx_nn_lr_data (training table)

- **Always filter `thishour`**: partitions are `'00'..'23'` **plus `'daily'`** — unfiltered queries double-count (~×2).
- Training reads **only `thishour='daily'`** (`only_use_daily_files=True`); the daily partition materializes after day end → a new budget's first day is structurally priced at the default water line.
- Health assertion: full-table `daily/Σhour` is stable at **99.67–99.70% rows / 95.3–95.5% act**; deviation = failed backfill or duplicated hourly writes. (Per-DSP long-callback slices can invert this — don't assume daily ≥ Σhour.)
- **Feature columns are already `fea_id`** (post-mapping). Never re-translate through `feature_mapping`; `dsp_id`/`vendor_id` are identity mappings, so they can't reveal this mistake.
- **Ver-column sentinels changed 2026-08-21**: "unscored" merged `-1` → `0`; filters must be `<= 0`. CVR model updates ~05h daily, CTR ~03h; off-schedule releases happen. `nn_cvr_ver = 0` (unscored) is ~87.5% of impressions.

## rpt.ftx_nn_lr_fea_mapping

- **Append-only vocabulary**: `fea_id` never remaps across days (verified: 5 adjacent-day full joins, 70 features, 0 remapped) → cross-day PSI/drift can key on `fea_id` directly.
- **Four exceptions rebuilt daily**: `dsp_id`, `vendor_id`, `mix_vid_net`, `network_type` — a value disappearing from these means "no volume that day", not a data incident.
- `dsp_id`/`vendor_id`: `fea_val == fea_id` (read directly). `budget_id`/`order_id`/`slot_id`/etc. are renumbered — reverse-lookup for humans only.

## dwd.d_ad_ftx_response & model_feature_data

- `_response` keeps only **~5 days** (older partitions listed but files purged → `HIVE_FILE_NOT_FOUND`). Partition keys `thisdate/hour/dsp_rsp_success` are all **varchar**.
- Older "bid to media" questions: use `d_ad_ftx_model_feature_data` (≥10 days; every row with `seat_bid_price > 0` = final bid to media). Not in chatdb metadata — use `SHOW COLUMNS`.

## Join keys & event semantics

| Tables | Device/user key | DSP column |
|---|---|---|
| response / model_feature | `fancy_user_id` (device: `device_id`) | `dsp_id` (varchar) |
| click / common_track | `ext_user_id` (device: `ext_mobile_device_id`) | `ext_dsp_id` (int) |

- CAST to varchar before joining across the two groups. Click-row precise matching: `common_track.ext_request_id`.
- `common_track_data`: **callbacks duplicate ~3×** — count `DISTINCT ext_request_id`. Its `ext_timestamp` is a click-time copy; real arrival time is `timestamp`. 唤起 = `cpa_event_type=1`; 有效A = `is_cost=true`.
- **媒体配送 channel** (`vendor_id ≥ 10000` = base id + 10000): settlement-level only — zero rows in request/impression/click logs, can carry 75% of a DSP's clicks. Filter (`vendor_id < 10000` or ADX name not like '%媒体配送%') before reconciling with EasyReport/ClickHouse.
- **event8 has two complementary click families** (`fclk` ∪ `click_data`; boundary may be order_id-level). `fclk` alone matches only 22% as denominator. `fclk` exists on trino only from 2026-08-17; cross-day backfills go through presto.
- CVR **training set** is DSP-whitelisted (act>50 in 5 days) + `clk=1` — only ~12% of rows train. Any prior/statistics design must draw from unfiltered data, or it inherits an extreme bimodal composition.

## ods.o_ad_ftx_raw_log (SDK capture)

- `bid_data.device` is double-encoded JSON (unwrap twice). Deeplink lives at `response_data.ad[0].dp_url` (don't parse `dp_clk`). All 24 hour-partitions are pre-registered at day start — existence ≠ data.

<!-- Homegrown from fancy-model + chatbi-skills project memory. Maintained in light-skills. -->
