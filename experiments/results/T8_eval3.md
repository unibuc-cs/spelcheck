# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T15:30:31)

24 specs, 72 runs scored; second reader: thelamapi/next-70b.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 13/21 | 9/9 | 4/12 | 5/18 | 66 | 18/36 | 5 | 20 |
| doubtful conflicts set aside | 13/21 | 9/9 | 4/12 | 0/18 | 2 | 18/36 | 5 | 20 |
| without step 6 (no questions, links unchecked) | 13/21 | 9/9 | 4/12 | 8/18 | 74 | 16/36 | 10 | 37 |
| without step 6, doubtful set aside | 13/21 | 9/9 | 4/12 | 0/18 | 2 | 16/36 | 10 | 37 |
| without link checks | 13/21 | 9/9 | 4/12 | 8/18 | 74 | 18/36 | 5 | 20 |
| translation needs 7 of 8 answers | 13/21 | 9/9 | 4/12 | 5/18 | 66 | 27/36 | 7 | 34 |
| second reader | 13/21 | 9/9 | 4/12 | 5/18 | 66 | 28/36 | 17 | 57 |
| second reader, without step 6 | 13/21 | 9/9 | 4/12 | 8/18 | 74 | 26/36 | 19 | 65 |
| second reader, 7 of 8 answers | 13/21 | 9/9 | 4/12 | 5/18 | 66 | 33/36 | 18 | 69 |
| without assumed facts and links | 7/21 | 6/9 | 1/12 | 0/18 | 1 | 18/36 | 5 | 20 |
| pairs of rules only | 13/21 | 9/9 | 4/12 | 5/18 | 66 | 18/36 | 5 | 20 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 1/9 | 8/9 | 3/9 | 6/9 |
| without step 6 (no questions, links unchecked) | 0/9 | 9/9 | 1/9 | 6/9 |
| translation needs 7 of 8 answers | 6/9 | 9/9 | 5/9 | 7/9 |
| second reader | 1/9 | 9/9 | 9/9 | 9/9 |
| second reader, without step 6 | 0/9 | 9/9 | 9/9 | 8/9 |
| second reader, 7 of 8 answers | 6/9 | 9/9 | 9/9 | 9/9 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| claims_ambiguity1 | 3 | none expected | none | 3 (planted): 1 |
| claims_ambiguity2 | 3 | none expected | none | 5: 2 |
| claims_clean | 3 | none expected | none | 5: 2 |
| claims_overlap | 3 | [3, 6]: 3/3 | none | 5: 1 |
| doors_ambiguity1 | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | none |
| doors_ambiguity2 | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | 1 (planted): 3 |
| doors_clean | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | none |
| doors_overlap | 3 | [2, 6]: 0/3, [3, 6]: 0/3 | [2, 5]: 3, [3, 5]: 3 | none |
| gym_ambiguity1 | 3 | none expected | none | 3 (planted): 1, 5: 1 |
| gym_ambiguity2 | 3 | none expected | none | 5 (planted): 3 |
| gym_clean | 3 | none expected | none | 5: 2 |
| gym_direct | 3 | [4, 6]: 3/3 | [1, 2]: 1, [5, 6]: 1 | 3: 3 |
| helpdesk_ambiguity1 | 3 | none expected | none | 1: 3, 4 (planted): 2 |
| helpdesk_ambiguity2 | 3 | none expected | none | 1: 2 |
| helpdesk_clean | 3 | none expected | none | 1: 1 |
| helpdesk_overlap | 3 | [1, 6]: 1/3 | none | 1: 3 |
| moderation_ambiguity1 | 3 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 3]: 1, [2, 4]: 2, [2, 5]: 2, [3, 4]: 2, [3, 5]: 2, [4, 5]: 2 | 2 (planted): 1 |
| moderation_ambiguity2 | 3 | none expected | [1, 3]: 1, [2, 4]: 2, [3, 4]: 1 | 3 (planted): 3 |
| moderation_clean | 3 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 4]: 2, [2, 5]: 2, [3, 4]: 2, [3, 5]: 2, [4, 5]: 2 | none |
| moderation_direct | 3 | [5, 6]: 3/3 | [1, 3]: 2, [2, 3]: 1, [2, 4]: 2, [3, 4]: 2 | none |
| streaming_ambiguity1 | 3 | none expected | none | 4 (planted): 2 |
| streaming_ambiguity2 | 3 | none expected | none | 5 (planted): 2 |
| streaming_clean | 3 | none expected | none | none |
| streaming_direct | 3 | [3, 6]: 3/3 | none | none |
