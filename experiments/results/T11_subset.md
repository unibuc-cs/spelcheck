# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T23:09:04)

19 specs, 57 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 25/27 | 8/9 | 3/3 | 6/12 | 77 | 7/24 | 4 | 13 |
| doubtful conflicts set aside | 25/27 | 8/9 | 3/3 | 0/12 | 0 | 7/24 | 4 | 13 |
| without step 6 (no questions, nothing checked) | 24/27 | 8/9 | 3/3 | 6/12 | 72 | 10/24 | 5 | 25 |
| without step 6, doubtful set aside | 24/27 | 8/9 | 3/3 | 0/12 | 0 | 10/24 | 5 | 25 |
| without checks of links and facts | 24/27 | 8/9 | 3/3 | 6/12 | 72 | 7/24 | 4 | 13 |
| translation needs 7 of 8 answers | 25/27 | 8/9 | 3/3 | 6/12 | 77 | 15/24 | 11 | 32 |
| without assumed facts and links | 18/27 | 6/9 | 3/3 | 3/12 | 8 | 7/24 | 4 | 13 |
| pairs of rules only | 25/27 | 8/9 | 3/3 | 6/12 | 77 | 7/24 | 4 | 13 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if |
|---|---|---|---|
| default (1 symbol set) | 1/9 | 1/6 | 5/9 |
| without step 6 (no questions, nothing checked) | 3/9 | 2/6 | 5/9 |
| translation needs 7 of 8 answers | 4/9 | 3/6 | 8/9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| attendance_ambiguity1 | 3 | none expected | [1, 4]: 3, [2, 4]: 3 | 5: 2 |
| attendance_ambiguity2 | 3 | none expected | [1, 4]: 3, [2, 4]: 3 | 3 (planted): 3, 5: 2 |
| attendance_clean | 3 | none expected | [1, 4]: 1, [2, 4]: 1 | none |
| attendance_overlap | 3 | [3, 6]: 3/3 | [1, 4]: 1, [2, 4]: 1 | none |
| auth_openspec | 3 | [1, 4]: 2/3, [3, 5]: 3/3 | none | none |
| delete_property | 3 | [2, 4]: 3/3 | none | none |
| elevator_ambiguity1 | 3 | none expected | [1, 2]: 3, [1, 3]: 3 | 4 (planted): 1 |
| elevator_ambiguity2 | 3 | none expected | [1, 2]: 3, [1, 3]: 3 | 5: 1 |
| elevator_clean | 3 | none expected | none | 1: 2 |
| elevator_direct | 3 | [2, 6]: 2/3 | [1, 3]: 1 | 5: 1 |
| irrigation_ambiguity1 | 3 | none expected | [1, 3]: 2 | 1 (planted): 1, 5: 1 |
| irrigation_ambiguity2 | 3 | none expected | [1, 3]: 3 | 3 (planted): 1, 5: 1 |
| irrigation_clean | 3 | none expected | [1, 3]: 3 | 5: 2 |
| irrigation_direct | 3 | [3, 6]: 3/3 | none | 5: 1 |
| moderation_ambiguity1 | 3 | none expected | [1, 3]: 2, [1, 5]: 3, [2, 4]: 1, [2, 5]: 3, [3, 4]: 2, [3, 5]: 2, [4, 5]: 3 | none |
| moderation_ambiguity2 | 3 | none expected | [1, 3]: 3, [1, 5]: 2, [2, 5]: 2, [3, 4]: 3, [3, 5]: 2, [4, 5]: 2 | 3 (planted): 1 |
| moderation_clean | 3 | none expected | [1, 3]: 2, [1, 5]: 1, [2, 5]: 1, [3, 4]: 2, [3, 5]: 1, [4, 5]: 1 | none |
| moderation_direct | 3 | [5, 6]: 3/3 | [1, 3]: 1, [3, 4]: 1 | none |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | none | none |
