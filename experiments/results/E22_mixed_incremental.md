# Evaluation of the change check, the specs formalized once (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T15:52:22)

1 specs, 3 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | mixed | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 9/9 | 9/9 | 0/0 | 0 | 0/3 | 3/3 | 4 |
| doubtful conflicts set aside | 9/9 | 9/9 | 0/0 | 0 | 0/3 | 3/3 | 3 |
| without assumed facts and links | 6/9 | 6/9 | 0/0 | 0 | 0/3 | 3/3 | 3 |

## Gaps

| Configuration | Planted gaps found | mixed | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|
| default (1 symbol set) | 9/9 | 9/9 | 0/0 | 9 |
| doubtful findings set aside | 9/9 | 9/9 | 0/0 | 9 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 3 of 3 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 83 requests, 57,434 tokens read, 38,823 tokens written (3 runs). What the specs of a project cost, once for each run: 336 requests, 263,239 tokens read, 134,682 tokens written (3 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| marathon_mixed | 3 | [N6, R1]: 3/3, [N5, R17]: 3/3, [N1, R3]: 3/3, gap N2: 3/3, gap R15: 3/3, gap R11: 3/3 | none | 9 | 0 | 4 |
