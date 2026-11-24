# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T13:59:13)

36 specs, 108 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 34/36 | 16/18 | 18/18 | 3/18 | 28 | 16/36 | 3 | 14 |
| doubtful conflicts set aside | 34/36 | 16/18 | 18/18 | 3/18 | 27 | 16/36 | 3 | 14 |
| without step 6 (no questions, nothing checked) | 34/36 | 16/18 | 18/18 | 3/18 | 28 | 14/36 | 1 | 8 |
| without step 6, doubtful set aside | 34/36 | 16/18 | 18/18 | 3/18 | 27 | 14/36 | 1 | 8 |
| without checks of links and facts | 34/36 | 16/18 | 18/18 | 3/18 | 28 | 16/36 | 3 | 14 |
| translation needs 7 of 8 answers | 34/36 | 16/18 | 18/18 | 3/18 | 28 | 21/36 | 7 | 47 |
| without assumed facts and links | 3/36 | 0/18 | 3/18 | 0/18 | 0 | 16/36 | 3 | 14 |
| facts vote without the parentheses repair | 34/36 | 16/18 | 18/18 | 3/18 | 28 | 16/36 | 3 | 14 |
| without the questions about outcomes | 27/36 | 9/18 | 18/18 | 0/18 | 1 | 16/36 | 3 | 14 |
| without the questions about outcomes, doubtful set aside | 27/36 | 9/18 | 18/18 | 0/18 | 0 | 16/36 | 3 | 14 |
| pairs of rules only | 34/36 | 16/18 | 18/18 | 3/18 | 28 | 16/36 | 3 | 14 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 3/9 | 0/9 | 6/9 | 7/9 |
| without step 6 (no questions, nothing checked) | 2/9 | 0/9 | 3/9 | 9/9 |
| translation needs 7 of 8 answers | 5/9 | 2/9 | 6/9 | 8/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 11 | 0 | 2 | 9 |
| other | 14 | 1 | 8 | 5 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 54 |
| once for each event | 17/18 | 0/18 | 20 | 38 |
| once for each event, doubtful set aside | 17/18 | 0/18 | 20 | 38 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| aquarium_ambiguity1 | 3 | none expected | none | none |
| aquarium_ambiguity2 | 3 | none expected | none | 1 (planted): 3 |
| aquarium_clean | 3 | none expected | none | none |
| aquarium_direct | 3 | [3, 6]: 3/3 | none | none |
| aquarium_gap | 3 | none expected | none | 4: 1 |
| aquarium_overlap | 3 | [1, 6]: 3/3 | none | none |
| beds_ambiguity1 | 3 | none expected | none | none |
| beds_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| beds_clean | 3 | none expected | none | 5: 1 |
| beds_direct | 3 | [3, 6]: 3/3 | none | none |
| beds_gap | 3 | none expected | none | none |
| beds_overlap | 3 | [1, 6]: 3/3 | none | none |
| cloakroom_ambiguity1 | 3 | none expected | [1, 5]: 1, [3, 5]: 3 | none |
| cloakroom_ambiguity2 | 3 | none expected | [1, 5]: 2, [3, 5]: 3 | 3 (planted): 2 |
| cloakroom_clean | 3 | none expected | [1, 5]: 1, [3, 5]: 3 | none |
| cloakroom_direct | 3 | [3, 6]: 3/3 | [1, 5]: 1, [3, 5]: 3 | 6: 1 |
| cloakroom_gap | 3 | none expected | [1, 4]: 1, [2, 4]: 3 | none |
| cloakroom_overlap | 3 | [3, 6]: 3/3 | [3, 5]: 3 | none |
| payroll_ambiguity1 | 3 | none expected | none | none |
| payroll_ambiguity2 | 3 | none expected | none | 1 (planted): 1 |
| payroll_clean | 3 | none expected | none | 5: 2 |
| payroll_direct | 3 | [3, 6]: 1/3 | none | 6: 3 |
| payroll_gap | 3 | none expected | [1, 2]: 1 | 4: 3 |
| payroll_overlap | 3 | [1, 6]: 3/3 | none | 5: 2 |
| timesheets_ambiguity1 | 3 | none expected | none | 5 (planted): 1 |
| timesheets_ambiguity2 | 3 | none expected | none | 3 (planted): 3 |
| timesheets_clean | 3 | none expected | none | none |
| timesheets_direct | 3 | [3, 6]: 3/3 | none | none |
| timesheets_gap | 3 | none expected | none | none |
| timesheets_overlap | 3 | [1, 6]: 3/3 | [4, 6]: 1, [5, 6]: 2 | none |
| turbine_ambiguity1 | 3 | none expected | none | 5 (planted): 2 |
| turbine_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| turbine_clean | 3 | none expected | none | none |
| turbine_direct | 3 | [3, 6]: 3/3 | none | none |
| turbine_gap | 3 | none expected | none | 3: 1 |
| turbine_overlap | 3 | [1, 6]: 3/3 | none | none |
