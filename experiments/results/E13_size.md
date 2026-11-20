# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-20T12:45:42)

4 specs, 12 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 6/6 | 3/3 | 3/3 | 3/3 | 12 | 0/0 | 7 | 22 |
| doubtful conflicts set aside | 6/6 | 3/3 | 3/3 | 0/3 | 0 | 0/0 | 7 | 22 |
| without step 6 (no questions, nothing checked) | 6/6 | 3/3 | 3/3 | 3/3 | 12 | 0/0 | 10 | 37 |
| without step 6, doubtful set aside | 6/6 | 3/3 | 3/3 | 0/3 | 0 | 0/0 | 10 | 37 |
| without checks of links and facts | 6/6 | 3/3 | 3/3 | 3/3 | 12 | 0/0 | 7 | 22 |
| translation needs 7 of 8 answers | 6/6 | 3/3 | 3/3 | 3/3 | 12 | 0/0 | 9 | 35 |
| without assumed facts and links | 3/6 | 3/3 | 0/3 | 0/3 | 0 | 0/0 | 7 | 22 |
| pairs of rules only | 6/6 | 3/3 | 3/3 | 3/3 | 12 | 0/0 | 7 | 22 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 15 | 0 | 0 | 15 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/3 | 0/3 | 0 | 9 |
| once for each event | 3/3 | 0/3 | 0 | 3 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| campsite_clean | 3 | none expected | [9, 11]: 3 | 3: 3, 4: 2, 10: 1, 16: 1 |
| campsite_direct | 3 | [30, 31]: 3/3 | [9, 11]: 3 | 3: 2, 4: 1 |
| campsite_gap | 3 | none expected | [8, 10]: 3 | 3: 3, 4: 2 |
| campsite_overlap | 3 | [12, 31]: 3/3 | [9, 11]: 3 | 3: 3, 4: 3, 16: 1 |
