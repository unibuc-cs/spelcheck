# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-27T17:05:08)

12 specs, 25 runs scored, 11 failed.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | breaks | direct | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 6 |
| doubtful conflicts set aside | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 3 |
| without assumed facts and links | 8/14 | 0/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 0 |
| without the questions about conditions | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 6 |
| without the questions about conditions, doubtful set aside | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 3 |
| a run read as one moment, doubtful set aside | 0/14 | 0/6 | 0/8 | 0/11 | 0 | 0/0 | 0/0 | 0 |
| examples read as rules, doubtful set aside | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 6 |
| links that only rename not asked about, doubtful set aside | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 3 |
| one example of a conflict is enough, doubtful set aside | 14/14 | 6/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 3 |
| without the questions whether a rule applies | 14/14 | 6/6 | 8/8 | 0/11 | 1 | 0/0 | 0/0 | 6 |
| without the questions whether a rule applies, doubtful set aside | 8/14 | 0/6 | 8/8 | 0/11 | 0 | 0/0 | 0/0 | 3 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 11/11 | 21 |
| doubtful findings set aside | 0/0 |  | 11/11 | 13 |
| without the questions about conditions | 0/0 |  | 11/11 | 21 |
| without the questions about conditions, doubtful set aside | 0/0 |  | 11/11 | 13 |
| a run read as one moment, doubtful set aside | 0/0 |  | 11/11 | 13 |
| examples read as rules, doubtful set aside | 0/0 |  | 11/11 | 13 |
| links that only rename not asked about, doubtful set aside | 0/0 |  | 11/11 | 13 |
| one example of a conflict is enough, doubtful set aside | 0/0 |  | 11/11 | 13 |
| without the questions whether a rule applies | 0/0 |  | 11/11 | 21 |
| without the questions whether a rule applies, doubtful set aside | 0/0 |  | 11/11 | 13 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 25 of 36 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 62 requests, 28,999 tokens read, 33,735 tokens written (25 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| optician_breaks | 1 | [R1, R5]: 1/1 | none | 0 | 0 | 0 |
| optician_direct | 2 | [R2, R5]: 2/2 | none | 2 | 0 | 0 |
| optician_quiet | 2 | nothing expected | none | 2 | 0 | 0 |
| storage_breaks | 2 | [R1, R5]: 2/2 | none | 0 | 0 | 0 |
| storage_direct | 3 | [R2, R5]: 3/3 | none | 3 | 0 | 0 |
| storage_quiet | 3 | nothing expected | none | 3 | 0 | 0 |
| tutoring_breaks | 0 | nothing expected | none | 0 | 0 | 0 |
| tutoring_direct | 0 | nothing expected | none | 0 | 0 | 0 |
| tutoring_quiet | 3 | nothing expected | none | 3 | 0 | 0 |
| zoo_breaks | 3 | [R1, R5]: 3/3 | none | 0 | 0 | 2 |
| zoo_direct | 3 | [R2, R5]: 3/3 | none | 5 | 0 | 3 |
| zoo_quiet | 3 | nothing expected | none | 3 | 0 | 1 |
