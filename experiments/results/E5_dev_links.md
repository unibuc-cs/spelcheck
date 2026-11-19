# Evaluation (8 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-17T21:01:37)

3 specs, 24 runs scored.

## By configuration

| Configuration | Expected conflicts found | of which direct | overlap | Clean specs: runs with a false alarm | Unexpected conflicts, all specs | Planted ambiguities found | Other ambiguity flags |
|---|---|---|---|---|---|---|---|
| 1 symbol set (default) | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 13 |
| 1 symbol set, without assumed facts | 32/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 13 |
| 1 symbol set, pairs of rules only | 40/40 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 13 |

## By spec (1 symbol set (default))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 8 | [1, 4]: 8/8, [3, 5]: 8/8 | none | 3: 6 |
| delete_property | 8 | [2, 4]: 8/8 | none | 4: 7 |
| order | 8 | [1, 5]: 8/8, [2, 3]: 8/8 | none | none |
