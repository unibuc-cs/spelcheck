# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T22:39:55)

36 specs, 108 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 16/36 | 3 | 11 |
| doubtful conflicts set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| without step 6 (no questions, nothing checked) | 32/36 | 14/18 | 18/18 | 3/18 | 14 | 15/36 | 1 | 11 |
| without step 6, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 15/36 | 1 | 11 |
| without checks of links and facts | 32/36 | 14/18 | 18/18 | 3/18 | 14 | 16/36 | 3 | 11 |
| translation needs 7 of 8 answers | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 22/36 | 10 | 44 |
| without assumed facts and links | 3/36 | 0/18 | 3/18 | 0/18 | 0 | 16/36 | 3 | 11 |
| facts vote without the parentheses repair | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 16/36 | 3 | 11 |
| without the questions about outcomes | 29/36 | 11/18 | 18/18 | 0/18 | 1 | 16/36 | 3 | 11 |
| without the questions about outcomes, doubtful set aside | 29/36 | 11/18 | 18/18 | 0/18 | 0 | 16/36 | 3 | 11 |
| without the questions about conditions | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 16/36 | 3 | 11 |
| without the questions about conditions, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| a run read as one moment, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| examples read as rules, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| links that only rename not asked about, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| one example of a conflict is enough, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| without the questions whether a rule applies | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 16/36 | 3 | 11 |
| without the questions whether a rule applies, doubtful set aside | 32/36 | 14/18 | 18/18 | 3/18 | 12 | 16/36 | 3 | 11 |
| pairs of rules only | 32/36 | 14/18 | 18/18 | 3/18 | 13 | 16/36 | 3 | 11 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 4/9 | 0/9 | 4/9 | 8/9 |
| without step 6 (no questions, nothing checked) | 2/9 | 3/9 | 3/9 | 7/9 |
| translation needs 7 of 8 answers | 5/9 | 2/9 | 6/9 | 9/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 11 | 0 | 1 | 10 |
| other | 10 | 0 | 3 | 7 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 54 |
| once for each event | 18/18 | 0/18 | 22 | 40 |
| once for each event, doubtful set aside | 18/18 | 0/18 | 22 | 40 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| aquarium_ambiguity1 | 3 | none expected | none | none |
| aquarium_ambiguity2 | 3 | none expected | none | 1 (planted): 3 |
| aquarium_clean | 3 | none expected | none | none |
| aquarium_direct | 3 | [3, 6]: 3/3 | none | none |
| aquarium_gap | 3 | none expected | none | none |
| aquarium_overlap | 3 | [1, 6]: 3/3 | none | none |
| beds_ambiguity1 | 3 | none expected | none | 4: 1 |
| beds_ambiguity2 | 3 | none expected | none | 1 (planted): 2 |
| beds_clean | 3 | none expected | none | none |
| beds_direct | 3 | [3, 6]: 3/3 | none | none |
| beds_gap | 3 | none expected | none | none |
| beds_overlap | 3 | [1, 6]: 3/3 | [1, 3]: 1 | 4: 1 |
| cloakroom_ambiguity1 | 3 | none expected | [3, 5]: 2 | none |
| cloakroom_ambiguity2 | 3 | none expected | none | 3 (planted): 2 |
| cloakroom_clean | 3 | none expected | [3, 5]: 3 | none |
| cloakroom_direct | 3 | [3, 6]: 2/3 | [3, 5]: 2 | 6: 2 |
| cloakroom_gap | 3 | none expected | [2, 4]: 3 | none |
| cloakroom_overlap | 3 | [3, 6]: 3/3 | [3, 5]: 2 | none |
| payroll_ambiguity1 | 3 | none expected | none | none |
| payroll_ambiguity2 | 3 | none expected | none | none |
| payroll_clean | 3 | none expected | none | 5: 2 |
| payroll_direct | 3 | [3, 6]: 0/3 | none | 6: 3 |
| payroll_gap | 3 | none expected | none | none |
| payroll_overlap | 3 | [1, 6]: 3/3 | none | 5: 1 |
| timesheets_ambiguity1 | 3 | none expected | none | 5 (planted): 2 |
| timesheets_ambiguity2 | 3 | none expected | none | 3 (planted): 2 |
| timesheets_clean | 3 | none expected | none | 4: 1 |
| timesheets_direct | 3 | [3, 6]: 3/3 | none | none |
| timesheets_gap | 3 | none expected | none | none |
| timesheets_overlap | 3 | [1, 6]: 3/3 | none | none |
| turbine_ambiguity1 | 3 | none expected | none | 5 (planted): 2 |
| turbine_ambiguity2 | 3 | none expected | none | 1 (planted): 3 |
| turbine_clean | 3 | none expected | none | none |
| turbine_direct | 3 | [3, 6]: 3/3 | none | none |
| turbine_gap | 3 | none expected | none | none |
| turbine_overlap | 3 | [1, 6]: 3/3 | none | none |
