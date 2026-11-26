# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T09:39:38)

24 specs, 72 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 17/18 | 8/9 | 9/9 | 2/18 | 24 | 18/36 | 4 | 22 |
| doubtful conflicts set aside | 17/18 | 8/9 | 9/9 | 0/18 | 18 | 18/36 | 4 | 22 |
| without step 6 (no questions, nothing checked) | 17/18 | 8/9 | 9/9 | 1/18 | 24 | 20/36 | 1 | 8 |
| without step 6, doubtful set aside | 17/18 | 8/9 | 9/9 | 0/18 | 19 | 20/36 | 1 | 8 |
| without checks of links and facts | 17/18 | 8/9 | 9/9 | 1/18 | 24 | 18/36 | 4 | 22 |
| translation needs 7 of 8 answers | 17/18 | 8/9 | 9/9 | 2/18 | 24 | 23/36 | 8 | 35 |
| without assumed facts and links | 3/18 | 0/9 | 3/9 | 0/18 | 0 | 18/36 | 4 | 22 |
| facts vote without the parentheses repair | 17/18 | 8/9 | 9/9 | 2/18 | 24 | 18/36 | 4 | 22 |
| without the questions about outcomes | 12/18 | 6/9 | 6/9 | 2/18 | 7 | 18/36 | 4 | 22 |
| without the questions about outcomes, doubtful set aside | 12/18 | 6/9 | 6/9 | 0/18 | 3 | 18/36 | 4 | 22 |
| pairs of rules only | 17/18 | 8/9 | 9/9 | 2/18 | 24 | 18/36 | 4 | 22 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 4/9 | 3/9 | 5/9 | 6/9 |
| without step 6 (no questions, nothing checked) | 3/9 | 4/9 | 4/9 | 9/9 |
| translation needs 7 of 8 answers | 6/9 | 3/9 | 7/9 | 7/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 14 | 0 | 4 | 10 |
| other | 18 | 7 | 0 | 11 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/0 | 0/0 | 0 | 31 |
| once for each event | 0/0 | 0/0 | 6 | 24 |
| once for each event, doubtful set aside | 0/0 | 0/0 | 6 | 24 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| canteen_ambiguity1 | 3 | none expected | none | 3 (planted): 1 |
| canteen_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| canteen_clean | 3 | none expected | none | none |
| canteen_overlap | 3 | [1, 6]: 3/3 | [2, 3]: 2, [3, 6]: 2 | none |
| fleet_ambiguity1 | 3 | none expected | [3, 4]: 2, [3, 5]: 2 | 1 (planted): 1 |
| fleet_ambiguity2 | 3 | none expected | none | 5 (planted): 3 |
| fleet_clean | 3 | none expected | [3, 5]: 2 | none |
| fleet_overlap | 3 | [1, 6]: 3/3 | [4, 6]: 1 | none |
| lab_ambiguity1 | 3 | none expected | none | 4 (planted): 2 |
| lab_ambiguity2 | 3 | none expected | [1, 5]: 2 | 1 (planted): 1, 4: 1 |
| lab_clean | 3 | none expected | none | 4: 1 |
| lab_direct | 3 | [5, 6]: 3/3 | none | 4: 2, 6: 3 |
| photos_ambiguity1 | 3 | none expected | none | 3 (planted): 1, 5: 3 |
| photos_ambiguity2 | 3 | none expected | none | 5: 3 |
| photos_clean | 3 | none expected | none | 5: 3 |
| photos_direct | 3 | [4, 6]: 2/3 | [5, 6]: 2 | 5: 3, 6: 3 |
| skipass_ambiguity1 | 3 | none expected | none | 4 (planted): 1 |
| skipass_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| skipass_clean | 3 | none expected | none | none |
| skipass_direct | 3 | [5, 6]: 3/3 | [3, 6]: 3 | none |
| taxi_ambiguity1 | 3 | none expected | none | 5 (planted): 2 |
| taxi_ambiguity2 | 3 | none expected | none | 4 (planted): 2 |
| taxi_clean | 3 | none expected | none | none |
| taxi_overlap | 3 | [1, 6]: 3/3 | [3, 6]: 3, [5, 6]: 3 | none |
