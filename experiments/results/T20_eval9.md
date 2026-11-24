# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-23T16:16:46)

30 specs, 90 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 18/18 | 9/9 | 9/9 | 4/18 | 16 | 16/36 | 4 | 24 |
| doubtful conflicts set aside | 18/18 | 9/9 | 9/9 | 1/18 | 4 | 16/36 | 4 | 24 |
| without step 6 (no questions, nothing checked) | 18/18 | 9/9 | 9/9 | 4/18 | 20 | 13/36 | 5 | 20 |
| without step 6, doubtful set aside | 18/18 | 9/9 | 9/9 | 1/18 | 5 | 13/36 | 5 | 20 |
| without checks of links and facts | 18/18 | 9/9 | 9/9 | 4/18 | 20 | 16/36 | 4 | 24 |
| translation needs 7 of 8 answers | 18/18 | 9/9 | 9/9 | 4/18 | 16 | 24/36 | 15 | 61 |
| without assumed facts and links | 12/18 | 6/9 | 6/9 | 1/18 | 2 | 16/36 | 4 | 24 |
| facts vote without the parentheses repair | 18/18 | 9/9 | 9/9 | 4/18 | 16 | 16/36 | 4 | 24 |
| pairs of rules only | 18/18 | 9/9 | 9/9 | 4/18 | 16 | 16/36 | 4 | 24 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 1/9 | 1/9 | 5/9 | 9/9 |
| without step 6 (no questions, nothing checked) | 3/9 | 1/9 | 0/9 | 9/9 |
| translation needs 7 of 8 answers | 8/9 | 1/9 | 6/9 | 9/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 10 | 1 | 5 | 4 |
| other | 23 | 0 | 9 | 14 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 54 |
| once for each event | 18/18 | 3/18 | 30 | 48 |
| once for each event, doubtful set aside | 18/18 | 3/18 | 30 | 48 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| crossing_ambiguity1 | 3 | none expected | [1, 3]: 3 | none |
| crossing_ambiguity2 | 3 | none expected | [1, 3]: 3 | 3 (planted): 1, 5: 1 |
| crossing_clean | 3 | none expected | [1, 3]: 3 | 5: 1 |
| crossing_direct | 3 | [3, 6]: 3/3 | none | 5: 2 |
| crossing_gap | 3 | none expected | [1, 2]: 3 | 4: 1 |
| grants_ambiguity1 | 3 | none expected | none | 1 (planted): 3, 4: 3 |
| grants_ambiguity2 | 3 | none expected | none | 3 (planted): 1 |
| grants_clean | 3 | none expected | none | none |
| grants_gap | 3 | none expected | none | 1: 1 |
| grants_overlap | 3 | [3, 6]: 3/3 | none | 4: 1 |
| kindergarten_ambiguity1 | 3 | none expected | none | none |
| kindergarten_ambiguity2 | 3 | none expected | none | 4: 1, 5 (planted): 2 |
| kindergarten_clean | 3 | none expected | none | none |
| kindergarten_gap | 3 | none expected | none | 3: 1 |
| kindergarten_overlap | 3 | [3, 6]: 3/3 | none | none |
| pool_ambiguity1 | 3 | none expected | none | 5: 1 |
| pool_ambiguity2 | 3 | none expected | none | 1 (planted): 3 |
| pool_clean | 3 | none expected | none | none |
| pool_gap | 3 | none expected | none | 4: 1 |
| pool_overlap | 3 | [1, 6]: 3/3 | none | none |
| shelter_ambiguity1 | 3 | none expected | none | 4 (planted): 1 |
| shelter_ambiguity2 | 3 | none expected | [3, 4]: 1 | 3 (planted): 2, 5: 1 |
| shelter_clean | 3 | none expected | [3, 4]: 1 | none |
| shelter_direct | 3 | [3, 6]: 3/3 | none | none |
| shelter_gap | 3 | none expected | [2, 3]: 2 | 4: 1 |
| topup_ambiguity1 | 3 | none expected | none | none |
| topup_ambiguity2 | 3 | none expected | none | 1 (planted): 3, 5: 2 |
| topup_clean | 3 | none expected | none | 3: 2, 5: 1 |
| topup_direct | 3 | [4, 6]: 3/3 | none | 3: 2 |
| topup_gap | 3 | none expected | none | 2: 1 |
