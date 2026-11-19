# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-19T11:41:10)

9 specs, 27 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 16/24 | 0/6 | 3/3 | 3/9 | 5 | 0/0 | 0 | 10 |
| doubtful conflicts set aside | 16/24 | 0/6 | 3/3 | 0/9 | 0 | 0/0 | 0 | 10 |
| without step 6 (no questions, nothing checked) | 16/24 | 0/6 | 3/3 | 5/9 | 10 | 0/0 | 3 | 18 |
| without step 6, doubtful set aside | 16/24 | 0/6 | 3/3 | 0/9 | 0 | 0/0 | 3 | 18 |
| without checks of links and facts | 16/24 | 0/6 | 3/3 | 5/9 | 10 | 0/0 | 0 | 10 |
| translation needs 7 of 8 answers | 16/24 | 0/6 | 3/3 | 3/9 | 5 | 0/0 | 3 | 21 |
| without assumed facts and links | 10/24 | 0/6 | 0/3 | 0/9 | 0 | 0/0 | 0 | 10 |
| pairs of rules only | 16/24 | 0/6 | 3/3 | 3/9 | 5 | 0/0 | 0 | 10 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auctions_clean | 3 | none expected | [2, 3]: 1 | none |
| auctions_direct | 3 | [4, 6]: 0/3 | none | 6: 3 |
| auth_openspec | 3 | [1, 4]: 3/3, [3, 5]: 2/3 | none | 3: 3 |
| backup_clean | 3 | none expected | [3, 4]: 2 | none |
| backup_overlap | 3 | [5, 6]: 3/3 | none | none |
| delete_property | 3 | [2, 4]: 2/3 | none | 4: 1 |
| messages_clean | 3 | none expected | none | none |
| messages_direct | 3 | [3, 6]: 0/3 | [1, 4]: 1, [4, 5]: 1 | 6: 3 |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | none | none |
