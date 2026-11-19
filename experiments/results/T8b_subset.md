# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T15:42:41)

15 specs, 45 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 19/27 | 3/3 | 3/9 | 6/9 | 74 | 9/18 | 2 | 14 |
| doubtful conflicts set aside | 19/27 | 3/3 | 3/9 | 0/9 | 5 | 9/18 | 2 | 14 |
| without step 6 (no questions, links unchecked) | 19/27 | 3/3 | 3/9 | 6/9 | 74 | 6/18 | 4 | 20 |
| without step 6, doubtful set aside | 19/27 | 3/3 | 3/9 | 0/9 | 5 | 6/18 | 4 | 20 |
| without link checks | 19/27 | 3/3 | 3/9 | 6/9 | 74 | 9/18 | 2 | 14 |
| translation needs 7 of 8 answers | 19/27 | 3/3 | 3/9 | 6/9 | 74 | 11/18 | 3 | 24 |
| without assumed facts and links | 15/27 | 3/3 | 3/9 | 0/9 | 0 | 9/18 | 2 | 14 |
| pairs of rules only | 19/27 | 3/3 | 3/9 | 6/9 | 74 | 9/18 | 2 | 14 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 2/6 | 4/6 | 0/3 | 3/3 |
| without step 6 (no questions, links unchecked) | 0/6 | 4/6 | 0/3 | 2/3 |
| translation needs 7 of 8 answers | 2/6 | 5/6 | 1/3 | 3/3 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 3 | [1, 4]: 3/3, [3, 5]: 3/3 | none | 3: 2 |
| delete_property | 3 | [2, 4]: 1/3 | none | 4: 1 |
| doors_ambiguity1 | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | 3 (planted): 1 |
| doors_ambiguity2 | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | 1 (planted): 3 |
| doors_clean | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | none |
| doors_overlap | 3 | [2, 6]: 0/3, [3, 6]: 0/3 | [2, 5]: 3, [3, 5]: 3 | 2: 1 |
| helpdesk_ambiguity1 | 3 | none expected | none | 1: 1, 3: 1, 4 (planted): 1 |
| helpdesk_ambiguity2 | 3 | none expected | none | 1: 2 |
| helpdesk_clean | 3 | none expected | none | 1: 2 |
| helpdesk_overlap | 3 | [1, 6]: 3/3 | none | 1: 3 |
| moderation_ambiguity1 | 3 | none expected | [1, 3]: 2, [1, 5]: 1, [2, 3]: 1, [2, 4]: 2, [2, 5]: 2, [3, 4]: 2, [3, 5]: 2, [4, 5]: 1 | 2 (planted): 1, 3: 1 |
| moderation_ambiguity2 | 3 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 4]: 2, [2, 5]: 2, [3, 4]: 2, [3, 5]: 1, [4, 5]: 2 | 3 (planted): 3 |
| moderation_clean | 3 | none expected | [1, 3]: 3, [1, 5]: 2, [2, 3]: 1, [2, 4]: 2, [2, 5]: 2, [3, 4]: 3, [3, 5]: 2, [4, 5]: 2 | none |
| moderation_direct | 3 | [5, 6]: 3/3 | [1, 3]: 3, [2, 4]: 1, [3, 4]: 3 | none |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | none | none |
