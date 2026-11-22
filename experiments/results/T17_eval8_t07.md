# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-22T16:40:52)

30 specs, 90 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 18/21 | 6/9 | 12/12 | 5/18 | 37 | 14/36 | 4 | 18 |
| doubtful conflicts set aside | 18/21 | 6/9 | 12/12 | 0/18 | 0 | 14/36 | 4 | 18 |
| without step 6 (no questions, nothing checked) | 18/21 | 6/9 | 12/12 | 8/18 | 54 | 15/36 | 3 | 21 |
| without step 6, doubtful set aside | 18/21 | 6/9 | 12/12 | 0/18 | 0 | 15/36 | 3 | 21 |
| without checks of links and facts | 18/21 | 6/9 | 12/12 | 8/18 | 54 | 14/36 | 4 | 18 |
| translation needs 7 of 8 answers | 18/21 | 6/9 | 12/12 | 5/18 | 37 | 25/36 | 13 | 42 |
| without assumed facts and links | 9/21 | 3/9 | 6/12 | 1/18 | 4 | 14/36 | 4 | 18 |
| pairs of rules only | 18/21 | 6/9 | 12/12 | 5/18 | 37 | 14/36 | 4 | 18 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 0/9 | 1/9 | 5/9 | 8/9 |
| without step 6 (no questions, nothing checked) | 0/9 | 4/9 | 2/9 | 9/9 |
| translation needs 7 of 8 answers | 6/9 | 3/9 | 8/9 | 8/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 8 | 1 | 4 | 3 |
| other | 13 | 1 | 5 | 7 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 52 |
| once for each event | 18/18 | 4/18 | 25 | 43 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| clinic_ambiguity1 | 3 | none expected | none | 1 (planted): 2 |
| clinic_ambiguity2 | 3 | none expected | none | 5 (planted): 3 |
| clinic_clean | 3 | none expected | [1, 3]: 1 | none |
| clinic_direct | 3 | [3, 6]: 0/3 | [1, 3]: 1 | 6: 2 |
| clinic_gap | 3 | none expected | [1, 2]: 3 | none |
| donations_ambiguity1 | 3 | none expected | [1, 2]: 3 | 5: 3 |
| donations_ambiguity2 | 3 | none expected | [2, 3]: 1 | 1 (planted): 3, 5: 2 |
| donations_clean | 3 | none expected | [1, 2]: 1, [2, 3]: 1 | 5: 3 |
| donations_gap | 3 | none expected | none | none |
| donations_overlap | 3 | [1, 6]: 3/3, [4, 6]: 3/3 | none | 5: 1 |
| laundry_ambiguity1 | 3 | none expected | none | none |
| laundry_ambiguity2 | 3 | none expected | none | none |
| laundry_clean | 3 | none expected | none | none |
| laundry_direct | 3 | [4, 6]: 3/3 | none | none |
| laundry_gap | 3 | none expected | none | none |
| meters_ambiguity1 | 3 | none expected | none | 5: 1 |
| meters_ambiguity2 | 3 | none expected | none | 5: 2 |
| meters_clean | 3 | none expected | none | 5: 1 |
| meters_gap | 3 | none expected | none | none |
| meters_overlap | 3 | [4, 6]: 3/3 | none | 5: 1 |
| recycling_ambiguity1 | 3 | none expected | none | 5 (planted): 1 |
| recycling_ambiguity2 | 3 | none expected | none | 4 (planted): 3 |
| recycling_clean | 3 | none expected | none | none |
| recycling_gap | 3 | none expected | none | none |
| recycling_overlap | 3 | [1, 6]: 3/3 | none | none |
| tolls_ambiguity1 | 3 | none expected | [1, 5]: 3, [3, 5]: 3 | none |
| tolls_ambiguity2 | 3 | none expected | [1, 5]: 3, [3, 5]: 2 | 3 (planted): 2, 4: 1 |
| tolls_clean | 3 | none expected | [1, 5]: 3, [3, 5]: 3 | none |
| tolls_direct | 3 | [3, 6]: 3/3 | [1, 5]: 3 | none |
| tolls_gap | 3 | none expected | [1, 4]: 3, [2, 4]: 3 | 3: 1 |
