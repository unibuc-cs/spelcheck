# Evaluation (4 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T15:34:47)

3 specs, 12 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| doubtful conflicts set aside | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| without step 6 (no questions, links unchecked) | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 6 |
| without step 6, doubtful set aside | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 6 |
| without link checks | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| translation needs 7 of 8 answers | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 10 |
| without assumed facts and links | 12/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| pairs of rules only | 18/20 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 4 | [1, 4]: 4/4, [3, 5]: 4/4 | none | 3: 4 |
| delete_property | 4 | [2, 4]: 2/4 | none | none |
| order | 4 | [1, 5]: 4/4, [2, 3]: 4/4 | none | none |
