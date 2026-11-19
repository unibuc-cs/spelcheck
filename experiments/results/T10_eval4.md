# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T22:50:32)

24 specs, 72 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 21/21 | 9/9 | 12/12 | 6/18 | 43 | 14/36 | 4 | 15 |
| doubtful conflicts set aside | 21/21 | 9/9 | 12/12 | 0/18 | 3 | 14/36 | 4 | 15 |
| without step 6 (no questions, nothing checked) | 21/21 | 9/9 | 12/12 | 5/18 | 43 | 22/36 | 8 | 42 |
| without step 6, doubtful set aside | 21/21 | 9/9 | 12/12 | 0/18 | 5 | 22/36 | 8 | 42 |
| without checks of links and facts | 21/21 | 9/9 | 12/12 | 5/18 | 43 | 14/36 | 4 | 15 |
| translation needs 7 of 8 answers | 21/21 | 9/9 | 12/12 | 6/18 | 43 | 22/36 | 15 | 52 |
| without assumed facts and links | 18/21 | 6/9 | 12/12 | 3/18 | 10 | 14/36 | 4 | 15 |
| pairs of rules only | 21/21 | 9/9 | 12/12 | 6/18 | 43 | 14/36 | 4 | 15 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 4/9 | 3/9 | 1/9 | 6/9 |
| without step 6 (no questions, nothing checked) | 6/9 | 4/9 | 5/9 | 7/9 |
| translation needs 7 of 8 answers | 6/9 | 4/9 | 6/9 | 6/9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| attendance_ambiguity1 | 3 | none expected | [1, 4]: 3, [2, 4]: 3, [3, 4]: 3 | 5: 1 |
| attendance_ambiguity2 | 3 | none expected | [1, 4]: 3, [2, 4]: 3 | 3 (planted): 1 |
| attendance_clean | 3 | none expected | [1, 4]: 1, [2, 4]: 1, [3, 4]: 2 | 5: 1 |
| attendance_overlap | 3 | [3, 6]: 3/3 | none | 5: 2 |
| delivery_ambiguity1 | 3 | none expected | none | 1 (planted): 1 |
| delivery_ambiguity2 | 3 | none expected | none | 2 (planted): 2, 4: 1 |
| delivery_clean | 3 | none expected | none | none |
| delivery_direct | 3 | [3, 6]: 3/3 | none | none |
| elevator_ambiguity1 | 3 | none expected | none | 1: 1 |
| elevator_ambiguity2 | 3 | none expected | [1, 2]: 3, [1, 3]: 3 | 3: 1 |
| elevator_clean | 3 | none expected | [1, 2]: 1, [1, 3]: 1 | 5: 1 |
| elevator_direct | 3 | [2, 6]: 3/3 | [1, 3]: 3, [4, 5]: 2 | 6: 1 |
| irrigation_ambiguity1 | 3 | none expected | [1, 3]: 1 | 1 (planted): 2 |
| irrigation_ambiguity2 | 3 | none expected | [1, 3]: 3 | none |
| irrigation_clean | 3 | none expected | [1, 3]: 3 | 5: 2 |
| irrigation_direct | 3 | [3, 6]: 3/3 | none | 5: 1, 6: 1 |
| lockers_ambiguity1 | 3 | none expected | none | 4: 1, 5 (planted): 1 |
| lockers_ambiguity2 | 3 | none expected | [1, 3]: 3 | 3 (planted): 2 |
| lockers_clean | 3 | none expected | none | none |
| lockers_overlap | 3 | [1, 6]: 3/3, [3, 6]: 3/3 | none | none |
| printing_ambiguity1 | 3 | none expected | none | 5 (planted): 2 |
| printing_ambiguity2 | 3 | none expected | none | 1 (planted): 3, 2: 1 |
| printing_clean | 3 | none expected | none | none |
| printing_overlap | 3 | [1, 6]: 3/3 | [2, 6]: 1 | none |
