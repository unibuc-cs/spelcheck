# Evaluation of the change check (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T14:24:11)

1 specs, 2 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | mixed | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 6/6 | 6/6 | 0/0 | 0 | 0/2 | 2/2 | 4 |
| doubtful conflicts set aside | 6/6 | 6/6 | 0/0 | 0 | 0/2 | 2/2 | 2 |
| without assumed facts and links | 4/6 | 4/6 | 0/0 | 0 | 0/2 | 2/2 | 2 |
| without the questions about conditions | 6/6 | 6/6 | 0/0 | 0 | 0/2 | 2/2 | 4 |
| without the questions about conditions, doubtful set aside | 6/6 | 6/6 | 0/0 | 0 | 0/2 | 2/2 | 2 |

## Gaps

| Configuration | Planted gaps found | mixed | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|
| default (1 symbol set) | 6/6 | 6/6 | 0/0 | 6 |
| doubtful findings set aside | 6/6 | 6/6 | 0/0 | 6 |
| without the questions about conditions | 6/6 | 6/6 | 0/0 | 6 |
| without the questions about conditions, doubtful set aside | 6/6 | 6/6 | 0/0 | 6 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 2 of 2 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 356 requests, 294,308 tokens read, 145,717 tokens written (2 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| marathon_mixed | 2 | [R16, R21]: 2/2, [R3, R7]: 2/2, [R1, R22]: 2/2, gap R12: 2/2, gap R11: 2/2, gap R15: 2/2 | none | 6 | 0 | 4 |
