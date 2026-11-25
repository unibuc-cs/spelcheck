# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T20:50:18)

24 specs, 40 runs scored, 8 failed.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 19/20 | 9/10 | 10/10 | 7/10 | 83 | 0/0 | 2 | 16 |
| doubtful conflicts set aside | 15/20 | 9/10 | 6/10 | 3/10 | 38 | 0/0 | 2 | 16 |
| without step 6 (no questions, nothing checked) | 19/20 | 9/10 | 10/10 | 7/10 | 84 | 0/0 | 3 | 20 |
| without step 6, doubtful set aside | 15/20 | 9/10 | 6/10 | 3/10 | 38 | 0/0 | 3 | 20 |
| without checks of links and facts | 19/20 | 9/10 | 10/10 | 7/10 | 84 | 0/0 | 2 | 16 |
| translation needs 7 of 8 answers | 19/20 | 9/10 | 10/10 | 7/10 | 83 | 0/0 | 9 | 43 |
| without assumed facts and links | 10/20 | 0/10 | 10/10 | 2/10 | 16 | 0/0 | 2 | 16 |
| facts vote without the parentheses repair | 18/20 | 8/10 | 10/10 | 7/10 | 84 | 0/0 | 2 | 16 |
| without the questions about outcomes | 14/20 | 4/10 | 10/10 | 4/10 | 39 | 0/0 | 2 | 16 |
| without the questions about outcomes, doubtful set aside | 10/20 | 4/10 | 6/10 | 0/10 | 0 | 0/0 | 2 | 16 |
| pairs of rules only | 19/20 | 9/10 | 10/10 | 7/10 | 83 | 0/0 | 2 | 16 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 9 | 2 | 1 | 6 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/10 | 0/10 | 0 | 30 |
| once for each event | 10/10 | 2/10 | 12 | 22 |
| once for each event, doubtful set aside | 10/10 | 2/10 | 12 | 22 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| backup_clean | 2 | none expected | [7, 13]: 1 | none |
| backup_direct | 2 | [4, 15]: 2/2 | [11, 12]: 1 | 15: 1 |
| backup_gap | 2 | none expected | [2, 4]: 1, [2, 7]: 1, [2, 10]: 1, [2, 11]: 1, [4, 7]: 1, [4, 10]: 1, [4, 11]: 1, [7, 10]: 1, [7, 11]: 1 | 13: 1 |
| backup_overlap | 2 | [3, 15]: 2/2 | none | none |
| filesync_clean | 2 | none expected | [4, 6]: 1, [4, 9]: 1, [4, 14]: 1, [5, 6]: 1, [5, 9]: 2, [5, 14]: 2 | none |
| filesync_direct | 2 | [4, 15]: 2/2 | [5, 6]: 2, [5, 9]: 2, [5, 13]: 2, [5, 14]: 2 | 11: 2, 15: 1 |
| filesync_gap | 2 | none expected | [4, 7]: 1, [5, 6]: 2, [5, 9]: 2, [5, 13]: 2, [6, 7]: 1 | none |
| filesync_overlap | 2 | [3, 15]: 2/2 | [4, 9]: 1, [4, 13]: 1, [4, 14]: 1, [4, 15]: 1, [5, 9]: 2, [5, 13]: 1, [5, 14]: 2, [5, 15]: 2 | 11: 1 |
| logship_clean | 2 | none expected | [2, 11]: 2, [2, 12]: 2 | 13: 1 |
| logship_direct | 2 | [5, 15]: 1/2 | [2, 11]: 2, [2, 12]: 2 | 13: 2, 15: 1 |
| logship_gap | 2 | none expected | [2, 11]: 2 | 12: 1 |
| logship_overlap | 2 | [4, 15]: 2/2 | [2, 11]: 2, [2, 12]: 2, [7, 8]: 1, [12, 15]: 2 | 12: 1, 13: 2 |
| registry_clean | 2 | none expected | [6, 7]: 2 | none |
| registry_direct | 2 | [2, 15]: 2/2 | none | none |
| registry_gap | 2 | none expected | [6, 7]: 2, [10, 12]: 2 | none |
| registry_overlap | 2 | [1, 15]: 2/2 | [4, 15]: 1, [5, 15]: 1, [6, 7]: 2, [6, 15]: 2 | none |
| runner_clean | 0 | none expected | none | none |
| runner_direct | 0 | [5, 15]: 0/0 | none | none |
| runner_gap | 0 | none expected | none | none |
| runner_overlap | 0 | [6, 15]: 0/0 | none | none |
| thumbs_clean | 2 | none expected | none | 14: 1 |
| thumbs_direct | 2 | [4, 15]: 2/2 | none | none |
| thumbs_gap | 2 | none expected | [2, 6]: 1, [2, 7]: 1, [2, 8]: 1, [6, 7]: 1, [6, 8]: 1, [7, 9]: 2, [9, 10]: 1 | none |
| thumbs_overlap | 2 | [7, 15]: 2/2 | none | 14: 1 |
