# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-19T09:54:54)

24 specs, 72 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 15/18 | 6/9 | 9/9 | 9/18 | 40 | 12/36 | 2 | 8 |
| doubtful conflicts set aside | 12/18 | 6/9 | 6/9 | 1/18 | 1 | 12/36 | 2 | 8 |
| without step 6 (no questions, nothing checked) | 15/18 | 6/9 | 9/9 | 11/18 | 57 | 17/36 | 1 | 16 |
| without step 6, doubtful set aside | 12/18 | 6/9 | 6/9 | 1/18 | 1 | 17/36 | 1 | 16 |
| without checks of links and facts | 15/18 | 6/9 | 9/9 | 11/18 | 57 | 12/36 | 2 | 8 |
| translation needs 7 of 8 answers | 15/18 | 6/9 | 9/9 | 9/18 | 40 | 18/36 | 11 | 39 |
| without assumed facts and links | 6/18 | 0/9 | 6/9 | 0/18 | 2 | 12/36 | 2 | 8 |
| pairs of rules only | 15/18 | 6/9 | 9/9 | 9/18 | 40 | 12/36 | 2 | 8 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 3/9 | 3/9 | 2/9 | 4/9 |
| without step 6 (no questions, nothing checked) | 7/9 | 0/9 | 4/9 | 6/9 |
| translation needs 7 of 8 answers | 5/9 | 4/9 | 5/9 | 4/9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| backup_ambiguity1 | 3 | none expected | none | none |
| backup_ambiguity2 | 3 | none expected | [3, 4]: 3 | none |
| backup_clean | 3 | none expected | none | none |
| backup_overlap | 3 | [5, 6]: 3/3 | none | none |
| cards_ambiguity1 | 3 | none expected | [3, 4]: 3 | none |
| cards_ambiguity2 | 3 | none expected | none | 4 (planted): 1 |
| cards_clean | 3 | none expected | [3, 4]: 3 | 3: 1 |
| cards_direct | 3 | [1, 6]: 3/3 | [3, 4]: 3 | none |
| hotel_ambiguity1 | 3 | none expected | none | 4 (planted): 3 |
| hotel_ambiguity2 | 3 | none expected | none | none |
| hotel_clean | 3 | none expected | none | 1: 1 |
| hotel_overlap | 3 | [1, 6]: 3/3 | none | none |
| messages_ambiguity1 | 3 | none expected | [1, 4]: 2, [4, 5]: 2 | 2 (planted): 1, 4: 1 |
| messages_ambiguity2 | 3 | none expected | [4, 5]: 2 | none |
| messages_clean | 3 | none expected | none | none |
| messages_direct | 3 | [3, 6]: 0/3 | none | 6: 1 |
| oven_ambiguity1 | 3 | none expected | [2, 4]: 3 | 1 (planted): 2, 3: 2 |
| oven_ambiguity2 | 3 | none expected | [1, 2]: 2, [2, 4]: 2 | 2 (planted): 1 |
| oven_clean | 3 | none expected | [1, 2]: 3, [2, 4]: 3 | none |
| oven_direct | 3 | [2, 6]: 3/3 | none | 4: 1 |
| polls_ambiguity1 | 3 | none expected | none | 4 (planted): 3 |
| polls_ambiguity2 | 3 | none expected | [4, 5]: 3 | 2 (planted): 1 |
| polls_clean | 3 | none expected | [4, 5]: 3 | none |
| polls_overlap | 3 | [1, 6]: 3/3 | [4, 5]: 3 | 5: 1 |
