# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T09:42:48)

3 specs, 9 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 14/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 2 |
| doubtful conflicts set aside | 14/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 2 |
| without step 6 (no questions, nothing checked) | 13/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 0 |
| without step 6, doubtful set aside | 13/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 0 |
| without checks of links and facts | 13/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 2 |
| translation needs 7 of 8 answers | 14/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 2 |
| without assumed facts and links | 9/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 2 |
| facts vote without the parentheses repair | 14/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 2 |
| without the questions about outcomes | 14/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 2 |
| without the questions about outcomes, doubtful set aside | 14/15 | 0/0 | 0/0 | 0/0 | 0 | 0/0 | 0 | 2 |
| pairs of rules only | 14/15 | 0/0 | 0/0 | 0/0 | 1 | 0/0 | 0 | 2 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 2 | 0 | 0 | 2 |

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
| delete_property | 3 | [2, 4]: 2/3 | none | 4: 1 |
| order | 3 | [1, 5]: 3/3, [2, 3]: 3/3 | [4, 5]: 1 | none |

# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T09:42:48)

1 specs, 3 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | change | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 3/3 | 3/3 | 0/0 | 0 | 0/0 | 0/0 | 3 |
| doubtful conflicts set aside | 3/3 | 3/3 | 0/0 | 0 | 0/0 | 0/0 | 3 |
| without assumed facts and links | 3/3 | 3/3 | 0/0 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/0 | 0 |
| doubtful findings set aside | 0/0 |  | 0/0 | 0 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 3 of 3 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 32 requests, 12,441 tokens read, 14,898 tokens written (3 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| auth_change | 3 | [R3, R5]: 3/3 | none | 0 | 0 | 3 |
