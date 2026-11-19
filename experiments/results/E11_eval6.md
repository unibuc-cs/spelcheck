# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-19T10:12:31)

24 specs, 72 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 15/18 | 3/6 | 12/12 | 8/18 | 25 | 19/36 | 2 | 14 |
| doubtful conflicts set aside | 15/18 | 3/6 | 12/12 | 0/18 | 0 | 19/36 | 2 | 14 |
| without step 6 (no questions, nothing checked) | 15/18 | 3/6 | 12/12 | 9/18 | 33 | 16/36 | 5 | 22 |
| without step 6, doubtful set aside | 15/18 | 3/6 | 12/12 | 0/18 | 0 | 16/36 | 5 | 22 |
| without checks of links and facts | 15/18 | 3/6 | 12/12 | 9/18 | 33 | 19/36 | 2 | 14 |
| translation needs 7 of 8 answers | 15/18 | 3/6 | 12/12 | 8/18 | 25 | 30/36 | 12 | 43 |
| without assumed facts and links | 12/18 | 3/6 | 9/12 | 0/18 | 0 | 19/36 | 2 | 14 |
| pairs of rules only | 15/18 | 3/6 | 12/12 | 8/18 | 25 | 19/36 | 2 | 14 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 4/9 | 7/9 | 3/9 | 5/9 |
| without step 6 (no questions, nothing checked) | 3/9 | 6/9 | 1/9 | 6/9 |
| translation needs 7 of 8 answers | 9/9 | 8/9 | 7/9 | 6/9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auctions_ambiguity1 | 3 | none expected | [1, 5]: 1 | 5: 1 |
| auctions_ambiguity2 | 3 | none expected | none | 2: 1, 3 (planted): 2 |
| auctions_clean | 3 | none expected | [2, 3]: 2 | none |
| auctions_direct | 3 | [4, 6]: 0/3 | [2, 3]: 1 | 2: 1, 6: 3 |
| bikes_ambiguity1 | 3 | none expected | [4, 5]: 3 | 4 (planted): 3 |
| bikes_ambiguity2 | 3 | none expected | [4, 5]: 3 | 3 (planted): 2 |
| bikes_clean | 3 | none expected | [2, 5]: 2, [4, 5]: 1 | 4: 2 |
| bikes_direct | 3 | [3, 6]: 3/3 | [2, 5]: 3 | 4: 3 |
| carwash_ambiguity1 | 3 | none expected | none | 5 (planted): 2 |
| carwash_ambiguity2 | 3 | none expected | none | 1 (planted): 1, 5: 1 |
| carwash_clean | 3 | none expected | none | none |
| carwash_overlap | 3 | [3, 6]: 3/3 | none | none |
| charging_ambiguity1 | 3 | none expected | none | 5 (planted): 3 |
| charging_ambiguity2 | 3 | none expected | none | 4 (planted): 3 |
| charging_clean | 3 | none expected | none | none |
| charging_overlap | 3 | [1, 6]: 3/3 | none | none |
| tickets_ambiguity1 | 3 | none expected | none | 4 (planted): 2 |
| tickets_ambiguity2 | 3 | none expected | none | 1 (planted): 1, 5: 1 |
| tickets_clean | 3 | none expected | none | none |
| tickets_overlap | 3 | [3, 6]: 3/3 | none | none |
| warehouse_ambiguity1 | 3 | none expected | none | none |
| warehouse_ambiguity2 | 3 | none expected | [3, 5]: 3 | none |
| warehouse_clean | 3 | none expected | [3, 5]: 3 | none |
| warehouse_overlap | 3 | [3, 6]: 3/3 | [3, 5]: 3 | 5: 1 |
