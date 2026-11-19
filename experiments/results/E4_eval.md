# Evaluation (3 runs per spec, 5 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-17T20:46:16)

21 specs, 63 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 35/48 | 15/21 | 20/27 | 0/18 | 2 | 1/9 | 0 | 10 |
| doubtful conflicts set aside | 33/48 | 15/21 | 18/27 | 0/18 | 0 | 1/9 | 0 | 10 |
| without step 6 (no questions, links unchecked) | 35/48 | 15/21 | 20/27 | 0/18 | 2 | 1/9 | 0 | 10 |
| without link checks | 35/48 | 15/21 | 20/27 | 0/18 | 2 | 1/9 | 0 | 10 |
| without assumed facts and links | 24/48 | 9/21 | 15/27 | 0/18 | 2 | 1/9 | 0 | 10 |
| pairs of rules only | 35/48 | 15/21 | 20/27 | 0/18 | 2 | 1/9 | 0 | 10 |
| 3 symbol sets, found with any | 42/48 | 18/21 | 24/27 | 2/18 | 5 | 3/9 | 4 | 22 |
| 3 symbol sets, found with most | 36/48 | 15/21 | 21/27 | 0/18 | 0 | 1/9 | 0 | 6 |
| 5 symbol sets, found with any | 45/48 | 18/21 | 27/27 | 2/18 | 5 | 5/9 | 4 | 26 |
| 5 symbol sets, found with most | 36/48 | 15/21 | 21/27 | 0/18 | 0 | 3/9 | 1 | 7 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| booking_ambiguity | 3 | none expected | none | 4 (planted): 1 |
| booking_clean | 3 | none expected | none | none |
| booking_direct | 3 | [4, 6]: 3/3 | none | none |
| booking_overlap | 3 | [1, 6]: 2/3 | [3, 4]: 2 | 4: 3, 6: 3 |
| library_ambiguity | 3 | none expected | none | none |
| library_clean | 3 | none expected | none | none |
| library_direct | 3 | [2, 6]: 3/3 | none | none |
| library_overlap | 3 | [1, 6]: 3/3 | none | none |
| parking_clean | 3 | none expected | none | none |
| parking_direct | 3 | [1, 6]: 0/3 | none | 6: 1 |
| parking_overlap | 3 | [4, 6]: 3/3 | none | none |
| thermostat_clean | 3 | none expected | none | none |
| thermostat_direct | 3 | [1, 6]: 3/3 | none | none |
| thermostat_overlap | 3 | [3, 6]: 3/3, [4, 6]: 3/3 | none | none |
| upload_clean | 3 | none expected | none | none |
| upload_direct | 3 | [5, 6]: 0/3 | none | 6: 3 |
| upload_overlap | 3 | [2, 6]: 1/3, [3, 6]: 1/3, [4, 6]: 1/3 | none | none |
| vending_ambiguity | 3 | none expected | none | none |
| vending_clean | 3 | none expected | none | none |
| vending_direct | 3 | [4, 6]: 3/3, [5, 6]: 3/3 | none | none |
| vending_overlap | 3 | [1, 6]: 3/3 | none | none |
