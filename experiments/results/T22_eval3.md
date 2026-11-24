# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T13:44:40)

24 specs, 72 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 21/21 | 9/9 | 12/12 | 11/18 | 95 | 14/36 | 6 | 15 |
| doubtful conflicts set aside | 21/21 | 9/9 | 12/12 | 3/18 | 33 | 14/36 | 6 | 15 |
| without step 6 (no questions, nothing checked) | 21/21 | 9/9 | 12/12 | 14/18 | 98 | 17/36 | 11 | 29 |
| without step 6, doubtful set aside | 21/21 | 9/9 | 12/12 | 6/18 | 36 | 17/36 | 11 | 29 |
| without checks of links and facts | 21/21 | 9/9 | 12/12 | 14/18 | 98 | 14/36 | 6 | 15 |
| translation needs 7 of 8 answers | 21/21 | 9/9 | 12/12 | 11/18 | 95 | 21/36 | 11 | 36 |
| without assumed facts and links | 10/21 | 6/9 | 4/12 | 3/18 | 12 | 14/36 | 6 | 15 |
| facts vote without the parentheses repair | 21/21 | 9/9 | 12/12 | 11/18 | 95 | 14/36 | 6 | 15 |
| without the questions about outcomes | 15/21 | 9/9 | 6/12 | 9/18 | 85 | 14/36 | 6 | 15 |
| without the questions about outcomes, doubtful set aside | 15/21 | 9/9 | 6/12 | 1/18 | 25 | 14/36 | 6 | 15 |
| pairs of rules only | 21/21 | 9/9 | 12/12 | 11/18 | 95 | 14/36 | 6 | 15 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 10 | 0 | 0 | 10 |
| other | 14 | 1 | 0 | 13 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/0 | 0/0 | 0 | 42 |
| once for each event | 0/0 | 0/0 | 15 | 33 |
| once for each event, doubtful set aside | 0/0 | 0/0 | 15 | 33 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| claims_ambiguity1 | 3 | none expected | [2, 3]: 3 | none |
| claims_ambiguity2 | 3 | none expected | [2, 5]: 1 | 2 (planted): 2 |
| claims_clean | 3 | none expected | [2, 3]: 2 | 5: 1 |
| claims_overlap | 3 | [3, 6]: 3/3 | [2, 3]: 1 | none |
| doors_ambiguity1 | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | none |
| doors_ambiguity2 | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | 1 (planted): 3 |
| doors_clean | 3 | none expected | [2, 5]: 3, [3, 5]: 3 | none |
| doors_overlap | 3 | [2, 6]: 3/3, [3, 6]: 3/3 | [2, 5]: 3, [3, 5]: 3 | none |
| gym_ambiguity1 | 3 | none expected | [1, 2]: 3, [3, 5]: 1 | 3 (planted): 1 |
| gym_ambiguity2 | 3 | none expected | [1, 2]: 3 | 5 (planted): 2 |
| gym_clean | 3 | none expected | [1, 2]: 3 | 5: 1 |
| gym_direct | 3 | [4, 6]: 3/3 | [1, 2]: 3, [3, 6]: 1 | none |
| helpdesk_ambiguity1 | 3 | none expected | none | 4 (planted): 1 |
| helpdesk_ambiguity2 | 3 | none expected | none | 1: 1 |
| helpdesk_clean | 3 | none expected | none | none |
| helpdesk_overlap | 3 | [1, 6]: 3/3 | none | 1: 2, 6: 1 |
| moderation_ambiguity1 | 3 | none expected | [1, 3]: 3, [1, 5]: 3, [2, 3]: 1, [2, 4]: 3, [2, 5]: 3, [3, 4]: 3, [3, 5]: 3, [4, 5]: 1 | 3: 1 |
| moderation_ambiguity2 | 3 | none expected | [1, 3]: 2, [1, 5]: 3, [2, 4]: 3, [2, 5]: 3, [3, 4]: 2, [3, 5]: 2 | 3 (planted): 2 |
| moderation_clean | 3 | none expected | [1, 3]: 1, [1, 5]: 3, [2, 4]: 1, [2, 5]: 2, [3, 4]: 1, [3, 5]: 1 | 3: 1 |
| moderation_direct | 3 | [5, 6]: 3/3 | [1, 3]: 3, [3, 4]: 3 | 3: 2 |
| streaming_ambiguity1 | 3 | none expected | none | 4 (planted): 2, 5: 1 |
| streaming_ambiguity2 | 3 | none expected | none | 5 (planted): 1 |
| streaming_clean | 3 | none expected | none | 5: 3 |
| streaming_direct | 3 | [3, 6]: 3/3 | none | 5: 1 |
