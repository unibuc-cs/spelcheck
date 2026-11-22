# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-22T16:10:40)

4 specs, 12 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 6/6 | 3/3 | 3/3 | 1/3 | 2 | 0/0 | 4 | 24 |
| doubtful conflicts set aside | 6/6 | 3/3 | 3/3 | 1/3 | 2 | 0/0 | 4 | 24 |
| without step 6 (no questions, nothing checked) | 6/6 | 3/3 | 3/3 | 1/3 | 4 | 0/0 | 10 | 44 |
| without step 6, doubtful set aside | 6/6 | 3/3 | 3/3 | 1/3 | 4 | 0/0 | 10 | 44 |
| without checks of links and facts | 6/6 | 3/3 | 3/3 | 1/3 | 4 | 0/0 | 4 | 24 |
| translation needs 7 of 8 answers | 6/6 | 3/3 | 3/3 | 1/3 | 2 | 0/0 | 10 | 60 |
| without assumed facts and links | 3/6 | 3/3 | 0/3 | 0/3 | 0 | 0/0 | 4 | 24 |
| pairs of rules only | 6/6 | 3/3 | 3/3 | 1/3 | 2 | 0/0 | 4 | 24 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 9 | 2 | 1 | 6 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/3 | 0/3 | 0 | 9 |
| once for each event | 3/3 | 0/3 | 12 | 15 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| ferry_clean | 3 | none expected | [1, 4]: 1 | 4: 1, 21: 3 |
| ferry_direct | 3 | [9, 101]: 3/3 | [1, 4]: 1 | 4: 1, 6: 1, 21: 3, 53: 1 |
| ferry_gap | 3 | none expected | none | 4: 2, 20: 2 |
| ferry_overlap | 3 | [26, 101]: 3/3 | none | 4: 1, 6: 1, 21: 3, 30: 1, 63: 1, 75: 1, 76: 1, 83: 1 |
