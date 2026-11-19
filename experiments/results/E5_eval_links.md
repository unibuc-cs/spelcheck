# Evaluation (3 runs per spec, 3 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-17T21:06:12)

21 specs, 63 runs scored.

## By configuration

| Configuration | Expected conflicts found | of which direct | overlap | Clean specs: runs with a false alarm | Unexpected conflicts, all specs | Planted ambiguities found | Other ambiguity flags |
|---|---|---|---|---|---|---|---|
| 1 symbol set (default) | 44/48 | 21/21 | 23/27 | 0/18 | 2 | 2/9 | 7 |
| 1 symbol set, without assumed facts | 27/48 | 10/21 | 17/27 | 0/18 | 2 | 2/9 | 7 |
| 1 symbol set, pairs of rules only | 44/48 | 21/21 | 23/27 | 0/18 | 2 | 2/9 | 7 |
| 3 symbol sets, found with any | 48/48 | 21/21 | 27/27 | 1/18 | 3 | 5/9 | 21 |
| 3 symbol sets, found with most | 43/48 | 20/21 | 23/27 | 0/18 | 0 | 0/9 | 7 |

## By spec (1 symbol set (default))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| booking_ambiguity | 3 | none expected | none | 3: 1, 4: 2 |
| booking_clean | 3 | none expected | none | none |
| booking_direct | 3 | [4, 6]: 3/3 | none | none |
| booking_overlap | 3 | [1, 6]: 2/3 | [3, 4]: 2 | 4: 1, 6: 2 |
| library_ambiguity | 3 | none expected | none | none |
| library_clean | 3 | none expected | none | none |
| library_direct | 3 | [2, 6]: 3/3 | none | none |
| library_overlap | 3 | [1, 6]: 3/3 | none | none |
| parking_clean | 3 | none expected | none | none |
| parking_direct | 3 | [1, 6]: 3/3 | none | 6: 2 |
| parking_overlap | 3 | [4, 6]: 3/3 | none | none |
| thermostat_clean | 3 | none expected | none | none |
| thermostat_direct | 3 | [1, 6]: 3/3 | none | none |
| thermostat_overlap | 3 | [3, 6]: 3/3, [4, 6]: 3/3 | none | none |
| upload_clean | 3 | none expected | none | none |
| upload_direct | 3 | [5, 6]: 3/3 | none | 6: 1 |
| upload_overlap | 3 | [2, 6]: 2/3, [3, 6]: 2/3, [4, 6]: 2/3 | none | none |
| vending_ambiguity | 3 | none expected | none | none |
| vending_clean | 3 | none expected | none | none |
| vending_direct | 3 | [4, 6]: 3/3, [5, 6]: 3/3 | none | none |
| vending_overlap | 3 | [1, 6]: 3/3 | none | none |
