# Evaluation (4 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-19T09:41:49)

3 specs, 12 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 20/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |
| doubtful conflicts set aside | 20/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |
| without step 6 (no questions, nothing checked) | 19/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| without step 6, doubtful set aside | 19/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| without checks of links and facts | 19/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |
| translation needs 7 of 8 answers | 20/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 7 |
| without assumed facts and links | 12/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |
| pairs of rules only | 20/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 4 | [1, 4]: 4/4, [3, 5]: 4/4 | none | 3: 2 |
| delete_property | 4 | [2, 4]: 4/4 | none | 4: 1 |
| order | 4 | [1, 5]: 4/4, [2, 3]: 4/4 | none | none |
