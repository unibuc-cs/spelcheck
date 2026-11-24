# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-23T16:20:06)

3 specs, 9 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| doubtful conflicts set aside | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| without step 6 (no questions, nothing checked) | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 5 |
| without step 6, doubtful set aside | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 5 |
| without checks of links and facts | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| translation needs 7 of 8 answers | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| without assumed facts and links | 9/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| facts vote without the parentheses repair | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| pairs of rules only | 13/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 1 | 0 | 1 | 0 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/0 | 0/0 | 0 | 0 |
| once for each event | 0/0 | 0/0 | 0 | 0 |
| once for each event, doubtful set aside | 0/0 | 0/0 | 0 | 0 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 3 | [1, 4]: 2/3, [3, 5]: 3/3 | none | 3: 1 |
| delete_property | 3 | [2, 4]: 2/3 | none | none |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | none | none |
