# Evaluation (8 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T22:35:45)

3 specs, 24 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 9 |
| doubtful conflicts set aside | 32/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 9 |
| without step 6 (no questions, nothing checked) | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 10 |
| without step 6, doubtful set aside | 32/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 10 |
| without checks of links and facts | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 9 |
| translation needs 7 of 8 answers | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 14 |
| without assumed facts and links | 24/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 9 |
| pairs of rules only | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 8 | [1, 4]: 8/8, [3, 5]: 8/8 | none | 3: 8, 5: 1 |
| delete_property | 8 | [2, 4]: 8/8 | none | none |
| order | 8 | [1, 5]: 8/8, [2, 3]: 8/8 | none | none |
