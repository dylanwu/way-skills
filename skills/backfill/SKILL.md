---
name: backfill
description: One-off data backfill (补数) discipline for the fancy-model NN training pipeline — archive layout, downstream propagation assertions, fill-holes-not-overwrite. Triggered by "补数", "backfill", "回填". Scope is fancy-model only.
---

# Backfill Discipline (fancy-model)

The NN training data is a three-layer chain — a backfill is not done until it has propagated to the bottom:

```
dwd.d_ad_ftx_{impression,click,common_track}_data  +  rpt.ftx_nn_lr_model_feature_data
  → rpt.ftx_nn_lr_raw_data      (nn_model/sql/ftx_nn_raw_data.hql)
  → rpt.ftx_nn_lr_data          (nn_model/sql/ftx_nn_data.hql — the training table)
```

## Iron rule: backfill does not propagate by itself

Filling `model_feature_data` does **not** re-run `raw_data` / `lr_data`. Real incident: upstream had 71k rows, downstream had 0 — the model then trained on ~10 samples for that DSP and priced at the network's default water line (predicted 18.2% vs real 2.1%, O/E 0.117).

After any backfill:

1. Re-run `ftx_nn_raw_data.hql` + `ftx_nn_data.hql` for every backfilled date.
2. Assert with a **downstream ÷ upstream ratio** per (date, DSP) — below ~90% means not propagated. Never conclude success from upstream row counts alone. (Reference SQL: `nn_model/eval/bili_laxin_cvr_calib/sql/22`.)
3. Check `lr_data` with `thishour = 'daily'` — training reads only the daily partition.
4. Close the loop on the *consequence*: retrain, then verify O/E recovered (the 1325 case went 0.126 → 1.126 after propagation + retrain, zero model-code changes).

Also run the ratio check when a new budget/DSP ramps up — insufficient samples in the training window causes default-water-line pricing even without any backfill.

## Fill holes, don't overwrite

When backfilling a dimension that multiple sources write (e.g. RTA `ref_dim_infos` fed by several device lists), an unconditional overwrite erases other sources' truth — the 闲鱼 backfill would have wiped 910-list values present in 31% of rows. Default to **filling only empty cells**; overwriting non-empty values requires explicit sign-off.

Beware of source-table quirks before computing fill values: partitions can be non-append (history gets rewritten), ids can be truncated (8-char `"99700081"`), timestamp columns can be epoch-zero before a given date, and one HDFS-lost partition must be excluded rather than read as zeros.

## Archive layout (mandatory)

One-off backfill scripts go to `nn_model/backfill/<YYYY-MM>_<task-name>/`, each task self-contained:

```
README.md                    # background / parameters / execution order / status
run_prep.sh
run_backfill.sh
run_lr_data_daily.sh
sql/{evt_daily_tmp,snapshot,stage,publish,cums_check}.hql
```

- File names inside a task dir carry no task prefix (the directory disambiguates).
- Cross-task reusable SQL goes to `backfill/common/`.
- Scripts keep `cd "$(dirname "$0")"` + relative `-f sql/xxx.hql`, so always cd into the task dir to run.
- Never drop `run_*_backfill.sh` into `nn_model/sql/` or the `nn_model/` root — 16 stray scripts once buried the 9 production SQLs there.
- Methodology and past pitfalls: `nn_model/backfill/README.md`.

<!-- Homegrown from fancy-model project memory. Maintained in light-skills. -->
