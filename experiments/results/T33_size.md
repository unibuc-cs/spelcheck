# Evaluation (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T16:39:20)

4 specs, 4 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 3 |
| doubtful conflicts set aside | 2/2 | 1/1 | 1/1 | 0/1 | 1 | 0/0 | 2 | 3 |
| without step 6 (no questions, nothing checked) | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 3 |
| without step 6, doubtful set aside | 2/2 | 1/1 | 1/1 | 0/1 | 1 | 0/0 | 2 | 3 |
| without checks of links and facts | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 3 |
| translation needs 7 of 8 answers | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 7 |
| without assumed facts and links | 1/2 | 1/1 | 0/1 | 0/1 | 0 | 0/0 | 2 | 3 |
| facts vote without the parentheses repair | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 3 |
| without the questions about outcomes | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 2 | 3 |
| without the questions about outcomes, doubtful set aside | 2/2 | 1/1 | 1/1 | 0/1 | 0 | 0/0 | 2 | 3 |
| without the questions about conditions | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 3 |
| without the questions about conditions, doubtful set aside | 2/2 | 1/1 | 1/1 | 0/1 | 1 | 0/0 | 2 | 3 |
| pairs of rules only | 2/2 | 1/1 | 1/1 | 1/1 | 5 | 0/0 | 2 | 3 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 3 | 0 | 0 | 3 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/1 | 0/1 | 0 | 3 |
| once for each event | 1/1 | 0/1 | 0 | 1 |
| once for each event, doubtful set aside | 1/1 | 0/1 | 0 | 1 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| campsite_clean | 1 | none expected | [9, 11]: 1 | 4: 1, 16: 1 |
| campsite_direct | 1 | [30, 31]: 1/1 | [4, 5]: 1, [9, 11]: 1 | none |
| campsite_gap | 1 | none expected | [8, 10]: 1 | none |
| campsite_overlap | 1 | [12, 31]: 1/1 | [9, 11]: 1 | 3: 1 |
