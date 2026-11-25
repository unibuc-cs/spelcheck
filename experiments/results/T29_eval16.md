# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T22:42:21)

24 specs, 48 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 24/24 | 12/12 | 12/12 | 9/12 | 403 | 0/0 | 5 | 25 |
| doubtful conflicts set aside | 20/24 | 12/12 | 8/12 | 3/12 | 24 | 0/0 | 5 | 25 |
| without step 6 (no questions, nothing checked) | 24/24 | 12/12 | 12/12 | 9/12 | 406 | 0/0 | 6 | 28 |
| without step 6, doubtful set aside | 20/24 | 12/12 | 8/12 | 3/12 | 25 | 0/0 | 6 | 28 |
| without checks of links and facts | 24/24 | 12/12 | 12/12 | 9/12 | 406 | 0/0 | 5 | 25 |
| translation needs 7 of 8 answers | 24/24 | 12/12 | 12/12 | 9/12 | 403 | 0/0 | 16 | 67 |
| without assumed facts and links | 12/24 | 6/12 | 6/12 | 6/12 | 368 | 0/0 | 5 | 25 |
| facts vote without the parentheses repair | 23/24 | 11/12 | 12/12 | 9/12 | 405 | 0/0 | 5 | 25 |
| without the questions about outcomes | 23/24 | 11/12 | 12/12 | 6/12 | 381 | 0/0 | 5 | 25 |
| without the questions about outcomes, doubtful set aside | 19/24 | 11/12 | 8/12 | 0/12 | 2 | 0/0 | 5 | 25 |
| pairs of rules only | 24/24 | 12/12 | 12/12 | 9/12 | 403 | 0/0 | 5 | 25 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 23 | 11 | 2 | 10 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/12 | 0/12 | 0 | 36 |
| once for each event | 12/12 | 2/12 | 18 | 30 |
| once for each event, doubtful set aside | 12/12 | 2/12 | 18 | 30 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| backup_clean | 2 | none expected | [7, 13]: 1 | none |
| backup_direct | 2 | [4, 15]: 2/2 | [2, 7]: 2, [2, 11]: 2, [2, 12]: 2, [7, 11]: 2, [7, 12]: 2 | none |
| backup_gap | 2 | none expected | none | none |
| backup_overlap | 2 | [3, 15]: 2/2 | [2, 4]: 2, [2, 7]: 2, [2, 11]: 2, [2, 12]: 2, [4, 7]: 2, [4, 11]: 2, [4, 12]: 2, [7, 11]: 2, [7, 12]: 2, [7, 13]: 1 | none |
| filesync_clean | 2 | none expected | [5, 6]: 1, [5, 9]: 2, [5, 13]: 1, [5, 14]: 2 | none |
| filesync_direct | 2 | [4, 15]: 2/2 | [5, 9]: 1, [5, 14]: 2 | 3: 1, 9: 1 |
| filesync_gap | 2 | none expected | [4, 7]: 1, [5, 9]: 2, [5, 12]: 1, [5, 13]: 2 | none |
| filesync_overlap | 2 | [3, 15]: 2/2 | [4, 7]: 1, [5, 9]: 1, [5, 14]: 2, [5, 15]: 2 | none |
| logship_clean | 2 | none expected | [2, 11]: 2, [2, 12]: 2, [7, 8]: 2 | none |
| logship_direct | 2 | [5, 15]: 2/2 | [2, 11]: 2, [2, 12]: 2 | none |
| logship_gap | 2 | none expected | [2, 11]: 2, [7, 8]: 1 | 4: 1 |
| logship_overlap | 2 | [4, 15]: 2/2 | [2, 11]: 2, [2, 12]: 2 | 4: 1 |
| registry_clean | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [1, 13]: 2, [2, 3]: 2, [2, 4]: 1, [2, 5]: 2, [2, 6]: 2, [2, 12]: 2, [2, 13]: 2, [3, 5]: 2, [3, 12]: 2, [3, 13]: 2, [5, 12]: 2, [5, 13]: 2, [6, 7]: 2, [12, 13]: 2 | 2: 1, 4: 1, 7: 1 |
| registry_direct | 2 | [2, 15]: 2/2 | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [1, 13]: 2, [3, 4]: 1, [3, 5]: 2, [3, 6]: 1, [3, 12]: 2, [3, 13]: 2, [5, 12]: 2, [5, 13]: 2, [6, 7]: 2, [12, 13]: 2 | 4: 1, 7: 2, 14: 1 |
| registry_gap | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [2, 3]: 2, [2, 4]: 1, [2, 5]: 2, [2, 6]: 1, [2, 12]: 2, [3, 4]: 2, [3, 5]: 2, [3, 6]: 2, [3, 12]: 2, [5, 12]: 2, [6, 7]: 2 | 2: 1, 4: 1, 7: 1 |
| registry_overlap | 2 | [1, 15]: 2/2 | [1, 3]: 2, [1, 5]: 2, [1, 12]: 2, [1, 13]: 2, [2, 3]: 2, [2, 5]: 2, [2, 6]: 2, [2, 12]: 2, [2, 13]: 2, [3, 5]: 2, [3, 12]: 2, [3, 13]: 2, [5, 12]: 2, [5, 13]: 2, [6, 7]: 2, [6, 15]: 2, [12, 13]: 2 | 2: 2, 7: 2 |
| runner_clean | 2 | none expected | [1, 5]: 2, [1, 6]: 2, [1, 7]: 2, [1, 9]: 2, [1, 10]: 2, [1, 14]: 2, [2, 5]: 2, [2, 6]: 2, [2, 7]: 2, [2, 9]: 2, [2, 10]: 2, [2, 13]: 2, [2, 14]: 2, [5, 7]: 2, [5, 9]: 2, [5, 10]: 2, [5, 13]: 2, [6, 7]: 2, [6, 9]: 2, [6, 10]: 2, [6, 13]: 2, [6, 14]: 2, [7, 9]: 2, [7, 10]: 2, [7, 13]: 2, [7, 14]: 2, [9, 13]: 2, [9, 14]: 2, [10, 13]: 2, [10, 14]: 2, [13, 14]: 2 | 11: 1 |
| runner_direct | 2 | [5, 15]: 2/2 | [1, 6]: 2, [1, 7]: 2, [1, 9]: 2, [1, 10]: 2, [1, 14]: 2, [2, 6]: 2, [2, 7]: 2, [2, 9]: 2, [2, 10]: 2, [2, 13]: 2, [2, 14]: 2, [6, 7]: 2, [6, 9]: 2, [6, 10]: 2, [6, 13]: 2, [6, 14]: 2, [7, 9]: 2, [7, 10]: 2, [7, 13]: 2, [7, 14]: 2, [9, 13]: 2, [9, 14]: 2, [10, 13]: 2, [10, 14]: 2, [13, 14]: 2 | 11: 1 |
| runner_gap | 2 | none expected | [1, 5]: 1, [1, 6]: 2, [1, 7]: 2, [1, 9]: 2, [1, 13]: 2, [2, 5]: 1, [2, 6]: 2, [2, 7]: 2, [2, 9]: 2, [2, 12]: 2, [2, 13]: 2, [5, 7]: 1, [5, 9]: 1, [5, 12]: 1, [6, 7]: 2, [6, 9]: 2, [6, 12]: 2, [6, 13]: 2, [7, 9]: 2, [7, 12]: 2, [7, 13]: 2, [9, 12]: 2, [9, 13]: 2, [12, 13]: 2 | 5: 1, 12: 1 |
| runner_overlap | 2 | [6, 15]: 2/2 | [1, 5]: 2, [1, 6]: 2, [1, 7]: 2, [1, 9]: 2, [1, 10]: 2, [1, 14]: 2, [2, 5]: 2, [2, 6]: 2, [2, 7]: 2, [2, 9]: 2, [2, 10]: 2, [2, 13]: 2, [2, 14]: 2, [5, 7]: 2, [5, 9]: 2, [5, 10]: 2, [5, 13]: 2, [6, 7]: 2, [6, 9]: 2, [6, 10]: 2, [6, 13]: 2, [6, 14]: 2, [7, 9]: 2, [7, 10]: 2, [7, 13]: 2, [7, 14]: 2, [9, 13]: 2, [9, 14]: 2, [10, 13]: 2, [10, 14]: 2, [13, 14]: 2 | none |
| thumbs_clean | 2 | none expected | none | 14: 1 |
| thumbs_direct | 2 | [4, 15]: 2/2 | none | 14: 1 |
| thumbs_gap | 2 | none expected | [9, 10]: 1 | none |
| thumbs_overlap | 2 | [7, 15]: 2/2 | none | 14: 1 |
