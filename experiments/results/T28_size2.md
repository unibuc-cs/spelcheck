# Evaluation (1 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T20:22:41)

4 specs, 4 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 7 |
| doubtful conflicts set aside | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 7 |
| without step 6 (no questions, nothing checked) | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 8 |
| without step 6, doubtful set aside | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 8 |
| without checks of links and facts | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 7 |
| translation needs 7 of 8 answers | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 4 | 20 |
| without assumed facts and links | 1/2 | 1/1 | 0/1 | 0/1 | 0 | 0/0 | 1 | 7 |
| facts vote without the parentheses repair | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 7 |
| without the questions about outcomes | 2/2 | 1/1 | 1/1 | 0/1 | 1 | 0/0 | 1 | 7 |
| without the questions about outcomes, doubtful set aside | 2/2 | 1/1 | 1/1 | 0/1 | 1 | 0/0 | 1 | 7 |
| pairs of rules only | 2/2 | 1/1 | 1/1 | 1/1 | 4 | 0/0 | 1 | 7 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 4 | 3 | 0 | 1 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/1 | 0/1 | 0 | 3 |
| once for each event | 1/1 | 0/1 | 3 | 4 |
| once for each event, doubtful set aside | 1/1 | 0/1 | 3 | 4 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| ferry_clean | 1 | none expected | [1, 4]: 1 | 4: 1 |
| ferry_direct | 1 | [9, 101]: 1/1 | [1, 4]: 1, [83, 101]: 1 | 4: 1, 55: 1 |
| ferry_gap | 1 | none expected | [1, 4]: 1 | 4: 1, 90: 1 |
| ferry_overlap | 1 | [26, 101]: 1/1 | none | 4: 1, 55: 1 |
