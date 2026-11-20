# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-20T12:35:08)

3 specs, 9 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 14/15 | 0/0 | 0/0 | 0/0 | 2 | 0/0 | 0 | 2 |
| doubtful conflicts set aside | 14/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 2 |
| without step 6 (no questions, nothing checked) | 14/15 | 0/0 | 0/0 | 0/0 | 2 | 0/0 | 0 | 6 |
| without step 6, doubtful set aside | 14/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 6 |
| without checks of links and facts | 14/15 | 0/0 | 0/0 | 0/0 | 2 | 0/0 | 0 | 2 |
| translation needs 7 of 8 answers | 14/15 | 0/0 | 0/0 | 0/0 | 2 | 0/0 | 0 | 4 |
| without assumed facts and links | 9/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 2 |
| pairs of rules only | 14/15 | 0/0 | 0/0 | 0/0 | 2 | 0/0 | 0 | 2 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 2 | 1 | 0 | 1 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/0 | 0/0 | 0 | 0 |
| once for each event | 0/0 | 0/0 | 0 | 0 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 3 | [1, 4]: 2/3, [3, 5]: 3/3 | none | 3: 2 |
| delete_property | 3 | [2, 4]: 3/3 | [2, 5]: 1, [3, 5]: 1 | none |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | none | none |
