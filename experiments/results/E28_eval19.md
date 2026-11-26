# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T18:26:22)

30 specs, 90 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 54/54 | 18/18 | 36/36 | 18/18 | 109 | 0/0 | 0 | 4 |
| doubtful conflicts set aside | 48/54 | 18/18 | 30/36 | 0/18 | 19 | 0/0 | 0 | 4 |
| without step 6 (no questions, nothing checked) | 54/54 | 18/18 | 36/36 | 18/18 | 116 | 0/0 | 1 | 5 |
| without step 6, doubtful set aside | 48/54 | 18/18 | 30/36 | 0/18 | 20 | 0/0 | 1 | 5 |
| without checks of links and facts | 54/54 | 18/18 | 36/36 | 18/18 | 116 | 0/0 | 0 | 4 |
| translation needs 7 of 8 answers | 54/54 | 18/18 | 36/36 | 18/18 | 109 | 0/0 | 5 | 22 |
| without assumed facts and links | 54/54 | 18/18 | 36/36 | 18/18 | 78 | 0/0 | 0 | 4 |
| facts vote without the parentheses repair | 54/54 | 18/18 | 36/36 | 18/18 | 109 | 0/0 | 0 | 4 |
| without the questions about outcomes | 54/54 | 18/18 | 36/36 | 18/18 | 88 | 0/0 | 0 | 4 |
| without the questions about outcomes, doubtful set aside | 48/54 | 18/18 | 30/36 | 11/18 | 58 | 0/0 | 0 | 4 |
| without the questions about conditions | 54/54 | 18/18 | 36/36 | 18/18 | 134 | 0/0 | 0 | 4 |
| without the questions about conditions, doubtful set aside | 48/54 | 18/18 | 30/36 | 11/18 | 97 | 0/0 | 0 | 4 |
| pairs of rules only | 54/54 | 18/18 | 36/36 | 18/18 | 109 | 0/0 | 0 | 4 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 4 | 3 | 0 | 1 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 18 |
| once for each event | 18/18 | 0/18 | 0 | 18 |
| once for each event, doubtful set aside | 18/18 | 0/18 | 0 | 18 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| freezers_clean | 3 | none expected | [7, 8]: 3 | none |
| freezers_direct | 3 | [4, 9]: 3/3 | [7, 8]: 3 | none |
| freezers_gap | 3 | none expected | none | none |
| freezers_overlap1 | 3 | [6, 9]: 3/3 | none | none |
| freezers_overlap2 | 3 | [5, 9]: 3/3 | none | none |
| gates_clean | 3 | none expected | [7, 8]: 3 | none |
| gates_direct | 3 | [2, 9]: 3/3 | [7, 8]: 3 | none |
| gates_gap | 3 | none expected | [6, 7]: 3 | none |
| gates_overlap1 | 3 | [6, 9]: 3/3 | [7, 8]: 3 | none |
| gates_overlap2 | 3 | [1, 9]: 3/3 | [7, 8]: 3 | none |
| greenhouse_clean | 3 | none expected | [7, 8]: 3 | none |
| greenhouse_direct | 3 | [4, 9]: 3/3 | [7, 8]: 3 | none |
| greenhouse_gap | 3 | none expected | [6, 7]: 3 | none |
| greenhouse_overlap1 | 3 | [5, 9]: 3/3 | [7, 8]: 3 | 9: 3 |
| greenhouse_overlap2 | 3 | [6, 9]: 3/3 | [7, 8]: 3 | none |
| holds_clean | 3 | none expected | [7, 8]: 3 | none |
| holds_direct | 3 | [2, 9]: 3/3 | [7, 8]: 3 | 1: 1 |
| holds_gap | 3 | none expected | [1, 5]: 2, [5, 7]: 2, [6, 7]: 3 | none |
| holds_overlap1 | 3 | [6, 9]: 3/3 | [1, 9]: 2, [7, 8]: 3, [8, 9]: 2 | none |
| holds_overlap2 | 3 | [3, 9]: 3/3 | [1, 4]: 3, [1, 6]: 2, [1, 9]: 3, [4, 8]: 3, [6, 8]: 2, [7, 8]: 3, [8, 9]: 3 | none |
| photos_clean | 3 | none expected | [2, 3]: 3, [7, 8]: 3 | none |
| photos_direct | 3 | [4, 9]: 3/3 | [7, 8]: 3 | none |
| photos_gap | 3 | none expected | [6, 7]: 2 | none |
| photos_overlap1 | 3 | [6, 9]: 3/3 | [2, 3]: 2, [7, 8]: 1 | none |
| photos_overlap2 | 3 | [5, 9]: 3/3 | [2, 3]: 2, [7, 8]: 3 | none |
| playlists_clean | 3 | none expected | [7, 8]: 3 | none |
| playlists_direct | 3 | [4, 9]: 3/3 | [7, 8]: 3 | none |
| playlists_gap | 3 | none expected | [6, 7]: 3 | none |
| playlists_overlap1 | 3 | [6, 9]: 3/3 | [7, 8]: 3 | none |
| playlists_overlap2 | 3 | [5, 9]: 3/3 | [7, 8]: 3 | none |
