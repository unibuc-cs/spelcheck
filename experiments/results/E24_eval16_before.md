# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T21:14:32)

24 specs, 42 runs scored, 6 failed.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 19/22 | 9/11 | 10/11 | 8/10 | 211 | 0/0 | 7 | 20 |
| doubtful conflicts set aside | 16/22 | 9/11 | 7/11 | 4/10 | 48 | 0/0 | 7 | 20 |
| without step 6 (no questions, nothing checked) | 19/22 | 9/11 | 10/11 | 8/10 | 213 | 0/0 | 5 | 23 |
| without step 6, doubtful set aside | 16/22 | 9/11 | 7/11 | 4/10 | 49 | 0/0 | 5 | 23 |
| without checks of links and facts | 19/22 | 9/11 | 10/11 | 8/10 | 213 | 0/0 | 7 | 20 |
| translation needs 7 of 8 answers | 19/22 | 9/11 | 10/11 | 8/10 | 211 | 0/0 | 14 | 51 |
| without assumed facts and links | 6/22 | 2/11 | 4/11 | 4/10 | 149 | 0/0 | 7 | 20 |
| facts vote without the parentheses repair | 19/22 | 9/11 | 10/11 | 8/10 | 207 | 0/0 | 7 | 20 |
| without the questions about outcomes | 14/22 | 4/11 | 10/11 | 6/10 | 180 | 0/0 | 7 | 20 |
| without the questions about outcomes, doubtful set aside | 11/22 | 4/11 | 7/11 | 0/10 | 17 | 0/0 | 7 | 20 |
| pairs of rules only | 19/22 | 9/11 | 10/11 | 8/10 | 211 | 0/0 | 7 | 20 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 17 | 11 | 1 | 5 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/10 | 0/10 | 0 | 30 |
| once for each event | 10/10 | 2/10 | 12 | 22 |
| once for each event, doubtful set aside | 10/10 | 2/10 | 12 | 22 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| backup_clean | 2 | none expected | [2, 13]: 2, [3, 5]: 1 | none |
| backup_direct | 2 | [4, 15]: 2/2 | [3, 5]: 1, [5, 6]: 1 | none |
| backup_gap | 2 | none expected | none | none |
| backup_overlap | 2 | [3, 15]: 2/2 | [2, 4]: 2, [2, 7]: 2, [2, 11]: 2, [2, 12]: 2, [3, 5]: 1, [4, 7]: 2, [4, 11]: 2, [4, 12]: 2, [7, 11]: 2, [7, 12]: 2, [7, 13]: 1 | none |
| filesync_clean | 2 | none expected | [5, 6]: 1, [5, 9]: 2, [5, 14]: 2, [6, 7]: 1 | 7: 1 |
| filesync_direct | 2 | [4, 15]: 2/2 | [5, 9]: 2, [5, 14]: 2 | none |
| filesync_gap | 2 | none expected | [5, 9]: 2, [5, 13]: 1 | none |
| filesync_overlap | 2 | [3, 15]: 2/2 | [4, 7]: 1, [5, 6]: 1, [5, 9]: 2, [5, 13]: 1, [5, 14]: 2, [5, 15]: 2 | none |
| logship_clean | 2 | none expected | [2, 11]: 2, [2, 12]: 2, [7, 8]: 2 | 12: 1 |
| logship_direct | 2 | [5, 15]: 0/2 | [2, 11]: 2, [2, 12]: 2, [7, 8]: 1 | 9: 2, 12: 1, 15: 1 |
| logship_gap | 2 | none expected | [2, 11]: 2 | none |
| logship_overlap | 2 | [4, 15]: 2/2 | [2, 11]: 2, [2, 12]: 2, [7, 8]: 1 | none |
| registry_clean | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [1, 13]: 2, [2, 3]: 2, [2, 4]: 2, [2, 5]: 2, [2, 6]: 2, [2, 12]: 2, [2, 13]: 2, [3, 4]: 1, [3, 5]: 2, [3, 6]: 1, [3, 12]: 2, [3, 13]: 2, [5, 12]: 2, [5, 13]: 2, [6, 7]: 2, [12, 13]: 2 | 2: 2, 4: 1, 7: 2 |
| registry_direct | 2 | [2, 15]: 2/2 | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [1, 13]: 2, [3, 4]: 1, [3, 5]: 2, [3, 6]: 1, [3, 12]: 2, [3, 13]: 2, [5, 12]: 2, [5, 13]: 2, [6, 7]: 2, [10, 13]: 1, [12, 13]: 2 | 7: 2 |
| registry_gap | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [2, 3]: 1, [2, 5]: 1, [2, 12]: 1, [3, 5]: 2, [3, 12]: 2, [5, 12]: 2, [6, 7]: 2 | 2: 1, 7: 2 |
| registry_overlap | 1 | [1, 15]: 1/1 | [1, 3]: 1, [1, 5]: 1, [1, 12]: 1, [1, 13]: 1, [2, 3]: 1, [2, 5]: 1, [2, 12]: 1, [2, 13]: 1, [2, 15]: 1, [3, 5]: 1, [3, 6]: 1, [3, 11]: 1, [3, 12]: 1, [3, 13]: 1, [5, 12]: 1, [5, 13]: 1, [6, 7]: 1, [6, 15]: 1, [8, 13]: 1, [11, 13]: 1, [12, 13]: 1 | 4: 1, 6: 1, 14: 1 |
| runner_clean | 0 | none expected | none | none |
| runner_direct | 1 | [5, 15]: 1/1 | [1, 10]: 1 | none |
| runner_gap | 0 | none expected | none | none |
| runner_overlap | 2 | [6, 15]: 2/2 | [1, 5]: 1, [1, 6]: 1, [1, 7]: 1, [1, 9]: 1, [1, 10]: 2, [1, 14]: 1, [2, 5]: 2, [2, 6]: 2, [2, 7]: 2, [2, 8]: 1, [2, 9]: 2, [2, 10]: 2, [2, 13]: 2, [2, 14]: 2, [5, 7]: 1, [5, 9]: 1, [5, 10]: 1, [5, 13]: 1, [6, 7]: 1, [6, 9]: 1, [6, 10]: 1, [6, 13]: 1, [6, 14]: 1, [7, 9]: 1, [7, 10]: 1, [7, 13]: 1, [7, 14]: 1, [9, 13]: 1, [9, 14]: 1, [10, 13]: 2, [10, 14]: 1, [13, 14]: 1 | 13: 1 |
| thumbs_clean | 2 | none expected | none | none |
| thumbs_direct | 2 | [4, 15]: 2/2 | [2, 6]: 1, [2, 7]: 1, [2, 8]: 1, [6, 7]: 1, [6, 8]: 1 | none |
| thumbs_gap | 2 | none expected | none | none |
| thumbs_overlap | 2 | [7, 15]: 1/2 | none | none |
