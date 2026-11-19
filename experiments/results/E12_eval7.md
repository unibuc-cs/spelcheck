# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-19T11:55:24)

24 specs, 72 runs scored; second reader: thelamapi/next-70b.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 13/18 | 7/9 | 6/9 | 0/18 | 3 | 17/36 | 5 | 27 |
| doubtful conflicts set aside | 13/18 | 7/9 | 6/9 | 0/18 | 1 | 17/36 | 5 | 27 |
| without step 6 (no questions, nothing checked) | 13/18 | 7/9 | 6/9 | 0/18 | 10 | 19/36 | 3 | 14 |
| without step 6, doubtful set aside | 13/18 | 7/9 | 6/9 | 0/18 | 6 | 19/36 | 3 | 14 |
| without checks of links and facts | 13/18 | 7/9 | 6/9 | 0/18 | 10 | 17/36 | 5 | 27 |
| translation needs 7 of 8 answers | 13/18 | 7/9 | 6/9 | 0/18 | 3 | 26/36 | 8 | 40 |
| second reader | 13/18 | 7/9 | 6/9 | 0/18 | 3 | 32/36 | 9 | 40 |
| second reader, without step 6 | 13/18 | 7/9 | 6/9 | 0/18 | 10 | 30/36 | 7 | 28 |
| second reader, 7 of 8 answers | 13/18 | 7/9 | 6/9 | 0/18 | 3 | 33/36 | 12 | 53 |
| without assumed facts and links | 3/18 | 0/9 | 3/9 | 0/18 | 0 | 17/36 | 5 | 27 |
| pairs of rules only | 13/18 | 7/9 | 6/9 | 0/18 | 3 | 17/36 | 5 | 27 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 2/9 | 6/9 | 1/9 | 8/9 |
| without step 6 (no questions, nothing checked) | 2/9 | 3/9 | 6/9 | 8/9 |
| translation needs 7 of 8 answers | 6/9 | 6/9 | 6/9 | 8/9 |
| second reader | 5/9 | 9/9 | 9/9 | 9/9 |
| second reader, without step 6 | 6/9 | 6/9 | 9/9 | 9/9 |
| second reader, 7 of 8 answers | 6/9 | 9/9 | 9/9 | 9/9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| canteen_ambiguity1 | 3 | none expected | none | 3 (planted): 1 |
| canteen_ambiguity2 | 3 | none expected | none | 1 (planted): 3 |
| canteen_clean | 3 | none expected | none | none |
| canteen_overlap | 3 | [1, 6]: 0/3 | none | none |
| fleet_ambiguity1 | 3 | none expected | [3, 5]: 1 | none |
| fleet_ambiguity2 | 3 | none expected | none | 5 (planted): 3 |
| fleet_clean | 3 | none expected | none | none |
| fleet_overlap | 3 | [1, 6]: 3/3 | [3, 5]: 1 | 4: 1 |
| lab_ambiguity1 | 3 | none expected | none | 4 (planted): 3 |
| lab_ambiguity2 | 3 | none expected | none | 4: 3 |
| lab_clean | 3 | none expected | none | 4: 2 |
| lab_direct | 3 | [5, 6]: 3/3 | none | 4: 3, 6: 3 |
| photos_ambiguity1 | 3 | none expected | none | 3 (planted): 2, 5: 3 |
| photos_ambiguity2 | 3 | none expected | none | 5: 3 |
| photos_clean | 3 | none expected | none | 5: 3 |
| photos_direct | 3 | [4, 6]: 1/3 | [5, 6]: 1 | 5: 3, 6: 3 |
| skipass_ambiguity1 | 3 | none expected | none | 4 (planted): 3 |
| skipass_ambiguity2 | 3 | none expected | none | none |
| skipass_clean | 3 | none expected | none | none |
| skipass_direct | 3 | [5, 6]: 3/3 | none | none |
| taxi_ambiguity1 | 3 | none expected | none | none |
| taxi_ambiguity2 | 3 | none expected | none | 4 (planted): 2 |
| taxi_clean | 3 | none expected | none | none |
| taxi_overlap | 3 | [1, 6]: 3/3 | none | none |
