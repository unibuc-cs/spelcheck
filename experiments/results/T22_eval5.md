# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T23:33:52)

24 specs, 72 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 16/18 | 7/9 | 9/9 | 11/18 | 42 | 15/36 | 0 | 7 |
| doubtful conflicts set aside | 13/18 | 7/9 | 6/9 | 0/18 | 2 | 15/36 | 0 | 7 |
| without step 6 (no questions, nothing checked) | 16/18 | 7/9 | 9/9 | 15/18 | 58 | 20/36 | 2 | 19 |
| without step 6, doubtful set aside | 13/18 | 7/9 | 6/9 | 0/18 | 0 | 20/36 | 2 | 19 |
| without checks of links and facts | 16/18 | 7/9 | 9/9 | 15/18 | 58 | 15/36 | 0 | 7 |
| translation needs 7 of 8 answers | 16/18 | 7/9 | 9/9 | 11/18 | 42 | 20/36 | 9 | 33 |
| without assumed facts and links | 6/18 | 0/9 | 6/9 | 0/18 | 0 | 15/36 | 0 | 7 |
| facts vote without the parentheses repair | 16/18 | 7/9 | 9/9 | 11/18 | 42 | 15/36 | 0 | 7 |
| without the questions about outcomes | 14/18 | 5/9 | 9/9 | 11/18 | 41 | 15/36 | 0 | 7 |
| without the questions about outcomes, doubtful set aside | 11/18 | 5/9 | 6/9 | 0/18 | 0 | 15/36 | 0 | 7 |
| pairs of rules only | 16/18 | 7/9 | 9/9 | 11/18 | 42 | 15/36 | 0 | 7 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 6/9 | 3/9 | 1/9 | 5/9 |
| without step 6 (no questions, nothing checked) | 7/9 | 0/9 | 5/9 | 8/9 |
| translation needs 7 of 8 answers | 8/9 | 3/9 | 4/9 | 5/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 11 | 0 | 4 | 7 |
| other | 7 | 1 | 2 | 4 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/0 | 0/0 | 0 | 54 |
| once for each event | 0/0 | 0/0 | 33 | 51 |
| once for each event, doubtful set aside | 0/0 | 0/0 | 33 | 51 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| backup_ambiguity1 | 3 | none expected | [3, 4]: 1 | none |
| backup_ambiguity2 | 3 | none expected | [3, 4]: 3 | none |
| backup_clean | 3 | none expected | [3, 4]: 1 | none |
| backup_overlap | 3 | [5, 6]: 3/3 | [3, 4]: 1 | 3: 2 |
| cards_ambiguity1 | 3 | none expected | [3, 4]: 3 | none |
| cards_ambiguity2 | 3 | none expected | none | 4 (planted): 3 |
| cards_clean | 3 | none expected | [3, 4]: 3 | none |
| cards_direct | 3 | [1, 6]: 3/3 | none | 3: 1 |
| hotel_ambiguity1 | 3 | none expected | none | 4 (planted): 3 |
| hotel_ambiguity2 | 3 | none expected | none | none |
| hotel_clean | 3 | none expected | none | none |
| hotel_overlap | 3 | [1, 6]: 3/3 | [5, 6]: 2 | none |
| messages_ambiguity1 | 3 | none expected | [1, 3]: 1, [1, 4]: 1 | 2 (planted): 1, 5: 1 |
| messages_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| messages_clean | 3 | none expected | [1, 4]: 1, [4, 5]: 1 | none |
| messages_direct | 3 | [3, 6]: 1/3 | none | 6: 2 |
| oven_ambiguity1 | 3 | none expected | [2, 4]: 3 | 1 (planted): 3 |
| oven_ambiguity2 | 3 | none expected | [1, 2]: 3, [2, 4]: 3 | none |
| oven_clean | 3 | none expected | [1, 2]: 3, [2, 4]: 3 | none |
| oven_direct | 3 | [2, 6]: 3/3 | none | none |
| polls_ambiguity1 | 3 | none expected | none | 4 (planted): 2 |
| polls_ambiguity2 | 3 | none expected | [4, 5]: 3 | 2 (planted): 1, 5: 1 |
| polls_clean | 3 | none expected | [4, 5]: 3 | none |
| polls_overlap | 3 | [1, 6]: 3/3 | [4, 5]: 3 | none |
