# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T13:34:03)

3 specs, 9 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| doubtful conflicts set aside | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| without step 6 (no questions, nothing checked) | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |
| without step 6, doubtful set aside | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 3 |
| without checks of links and facts | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| translation needs 7 of 8 answers | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 4 |
| without assumed facts and links | 9/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| facts vote without the parentheses repair | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| without the questions about outcomes | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| without the questions about outcomes, doubtful set aside | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |
| pairs of rules only | 15/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 1 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 1 | 0 | 0 | 1 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/0 | 0/0 | 0 | 0 |
| once for each event | 0/0 | 0/0 | 0 | 0 |
| once for each event, doubtful set aside | 0/0 | 0/0 | 0 | 0 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| auth_openspec | 3 | [1, 4]: 3/3, [3, 5]: 3/3 | none | 3: 1 |
| delete_property | 3 | [2, 4]: 3/3 | none | none |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | none | none |

# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T13:34:03)

1 specs, 3 runs scored.

Only findings that involve a rule of the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | change | Clean changes with a conflict about the change | Other conflicts about the change | Conflicts among existing rules, not shown |
|---|---|---|---|---|---|
| default (1 symbol set) | 3/3 | 3/3 | 0/0 | 0 | 3 |
| doubtful conflicts set aside | 3/3 | 3/3 | 0/0 | 0 | 3 |
| without assumed facts and links | 3/3 | 3/3 | 0/0 | 0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | narrowed | Clean changes with a gap on a covered event | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 0/0 | 0/0 | 0/0 | 0/0 | 0 |
| doubtful findings set aside | 0/0 | 0/0 | 0/0 | 0/0 | 0 |

## Ambiguities and labels (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 3 of 3 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | Conflicts not shown |
|---|---|---|---|---|---|
| auth_change | 3 | [R3, R5]: 3/3 | none | 0 | 3 |
