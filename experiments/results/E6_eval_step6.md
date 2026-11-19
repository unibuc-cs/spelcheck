# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T11:59:00)

21 specs, 63 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 41/48 | 20/21 | 21/27 | 0/18 | 1 | 5/9 | 1 | 13 |
| doubtful conflicts set aside | 39/48 | 20/21 | 19/27 | 0/18 | 0 | 5/9 | 1 | 13 |
| without step 6 (no questions, links unchecked) | 41/48 | 20/21 | 21/27 | 0/18 | 1 | 2/9 | 0 | 9 |
| without link checks | 41/48 | 20/21 | 21/27 | 0/18 | 1 | 5/9 | 1 | 13 |
| without assumed facts and links | 26/48 | 8/21 | 18/27 | 0/18 | 1 | 5/9 | 1 | 13 |
| pairs of rules only | 41/48 | 20/21 | 21/27 | 0/18 | 1 | 5/9 | 1 | 13 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| booking_ambiguity | 3 | none expected | none | 4 (planted): 2 |
| booking_clean | 3 | none expected | none | none |
| booking_direct | 3 | [4, 6]: 2/3 | none | 3: 1, 4: 3 |
| booking_overlap | 3 | [1, 6]: 3/3 | [3, 4]: 1 | 4: 1, 6: 2 |
| library_ambiguity | 3 | none expected | none | 5 (planted): 3 |
| library_clean | 3 | none expected | none | none |
| library_direct | 3 | [2, 6]: 3/3 | none | 1: 1 |
| library_overlap | 3 | [1, 6]: 3/3 | none | none |
| parking_clean | 3 | none expected | none | none |
| parking_direct | 3 | [1, 6]: 3/3 | none | none |
| parking_overlap | 3 | [4, 6]: 3/3 | none | none |
| thermostat_clean | 3 | none expected | none | none |
| thermostat_direct | 3 | [1, 6]: 3/3 | none | none |
| thermostat_overlap | 3 | [3, 6]: 3/3, [4, 6]: 3/3 | none | none |
| upload_clean | 3 | none expected | none | none |
| upload_direct | 3 | [5, 6]: 3/3 | none | 6: 2 |
| upload_overlap | 3 | [2, 6]: 1/3, [3, 6]: 1/3, [4, 6]: 1/3 | none | none |
| vending_ambiguity | 3 | none expected | none | none |
| vending_clean | 3 | none expected | none | 1: 1 |
| vending_direct | 3 | [4, 6]: 3/3, [5, 6]: 3/3 | none | 1: 1 |
| vending_overlap | 3 | [1, 6]: 3/3 | none | 1: 1 |
