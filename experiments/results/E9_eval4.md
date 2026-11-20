# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T16:00:58)

24 specs, 72 runs scored; second reader: thelamapi/next-70b.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 21/21 | 9/9 | 12/12 | 6/18 | 29 | 14/36 | 7 | 22 |
| doubtful conflicts set aside | 21/21 | 9/9 | 12/12 | 0/18 | 1 | 14/36 | 7 | 22 |
| without step 6 (no questions, nothing checked) | 21/21 | 9/9 | 12/12 | 6/18 | 27 | 19/36 | 12 | 44 |
| without step 6, doubtful set aside | 21/21 | 9/9 | 12/12 | 0/18 | 2 | 19/36 | 12 | 44 |
| without checks of links and facts | 21/21 | 9/9 | 12/12 | 6/18 | 27 | 14/36 | 7 | 22 |
| translation needs 7 of 8 answers | 21/21 | 9/9 | 12/12 | 6/18 | 29 | 16/36 | 18 | 62 |
| second reader | 21/21 | 9/9 | 12/12 | 6/18 | 29 | 30/36 | 15 | 59 |
| second reader, without step 6 | 21/21 | 9/9 | 12/12 | 6/18 | 27 | 29/36 | 16 | 72 |
| second reader, 7 of 8 answers | 21/21 | 9/9 | 12/12 | 6/18 | 29 | 30/36 | 25 | 91 |
| without assumed facts and links | 18/21 | 6/9 | 12/12 | 1/18 | 8 | 14/36 | 7 | 22 |
| pairs of rules only | 21/21 | 9/9 | 12/12 | 6/18 | 29 | 14/36 | 7 | 22 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 4/9 | 3/9 | 2/9 | 5/9 |
| without step 6 (no questions, nothing checked) | 4/9 | 2/9 | 4/9 | 9/9 |
| translation needs 7 of 8 answers | 6/9 | 3/9 | 2/9 | 5/9 |
| second reader | 6/9 | 6/9 | 9/9 | 9/9 |
| second reader, without step 6 | 6/9 | 5/9 | 9/9 | 9/9 |
| second reader, 7 of 8 answers | 6/9 | 6/9 | 9/9 | 9/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 11 | 1 | 3 | 7 |
| other | 13 | 0 | 5 | 8 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| attendance_ambiguity1 | 3 | none expected | [1, 4]: 2, [2, 4]: 2, [3, 4]: 2 | 5: 3 |
| attendance_ambiguity2 | 3 | none expected | [1, 4]: 2, [2, 4]: 1 | 3 (planted): 1, 5: 2 |
| attendance_clean | 3 | none expected | none | 5: 1 |
| attendance_overlap | 3 | [3, 6]: 3/3 | none | 5: 2 |
| delivery_ambiguity1 | 3 | none expected | none | 1 (planted): 1, 2: 1 |
| delivery_ambiguity2 | 3 | none expected | none | 2 (planted): 1 |
| delivery_clean | 3 | none expected | none | none |
| delivery_direct | 3 | [3, 6]: 3/3 | none | 2: 1 |
| elevator_ambiguity1 | 3 | none expected | none | 4 (planted): 1 |
| elevator_ambiguity2 | 3 | none expected | [1, 2]: 3 | none |
| elevator_clean | 3 | none expected | [1, 2]: 3, [1, 3]: 3 | none |
| elevator_direct | 3 | [2, 6]: 3/3 | none | none |
| irrigation_ambiguity1 | 3 | none expected | [1, 3]: 1 | 1 (planted): 3 |
| irrigation_ambiguity2 | 3 | none expected | [1, 3]: 3 | 5: 1 |
| irrigation_clean | 3 | none expected | [1, 3]: 3 | 5: 3 |
| irrigation_direct | 3 | [3, 6]: 3/3 | none | 5: 2 |
| lockers_ambiguity1 | 3 | none expected | none | 3: 1 |
| lockers_ambiguity2 | 3 | none expected | [1, 3]: 3 | 3 (planted): 2 |
| lockers_clean | 3 | none expected | none | 4: 3 |
| lockers_overlap | 3 | [1, 6]: 3/3, [3, 6]: 3/3 | none | 4: 1 |
| printing_ambiguity1 | 3 | none expected | none | 5 (planted): 3 |
| printing_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| printing_clean | 3 | none expected | none | none |
| printing_overlap | 3 | [1, 6]: 3/3 | [2, 6]: 1 | 2: 1 |
