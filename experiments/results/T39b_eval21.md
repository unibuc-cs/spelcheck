# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-27T00:38:57)

12 specs, 36 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | breaks | same | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 15/24 | 10/12 | 5/12 | 11/12 | 23 | 0/0 | 0/0 | 29 |
| doubtful conflicts set aside | 9/24 | 4/12 | 5/12 | 0/12 | 0 | 0/0 | 0/0 | 8 |
| without assumed facts and links | 3/24 | 0/12 | 3/12 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| without the questions about conditions | 15/24 | 10/12 | 5/12 | 11/12 | 23 | 0/0 | 0/0 | 29 |
| without the questions about conditions, doubtful set aside | 9/24 | 4/12 | 5/12 | 0/12 | 0 | 0/0 | 0/0 | 8 |
| a run read as one moment, doubtful set aside | 5/24 | 0/12 | 5/12 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| examples read as rules, doubtful set aside | 15/24 | 10/12 | 5/12 | 11/12 | 23 | 0/0 | 0/0 | 29 |
| links that only rename not asked about, doubtful set aside | 9/24 | 4/12 | 5/12 | 0/12 | 0 | 0/0 | 0/0 | 9 |
| one example of a conflict is enough, doubtful set aside | 9/24 | 4/12 | 5/12 | 3/12 | 3 | 0/0 | 0/0 | 8 |
| without the questions whether a rule applies | 15/24 | 10/12 | 5/12 | 11/12 | 23 | 0/0 | 0/0 | 29 |
| without the questions whether a rule applies, doubtful set aside | 9/24 | 4/12 | 5/12 | 0/12 | 0 | 0/0 | 0/0 | 8 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/12 | 0 |
| doubtful findings set aside | 0/0 |  | 0/12 | 0 |
| without the questions about conditions | 0/0 |  | 0/12 | 0 |
| without the questions about conditions, doubtful set aside | 0/0 |  | 0/12 | 0 |
| a run read as one moment, doubtful set aside | 0/0 |  | 0/12 | 0 |
| examples read as rules, doubtful set aside | 0/0 |  | 0/12 | 0 |
| links that only rename not asked about, doubtful set aside | 0/0 |  | 0/12 | 0 |
| one example of a conflict is enough, doubtful set aside | 0/0 |  | 0/12 | 0 |
| without the questions whether a rule applies | 0/0 |  | 0/12 | 0 |
| without the questions whether a rule applies, doubtful set aside | 0/0 |  | 0/12 | 0 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 5 where nothing was planted.
- Labels: 36 of 36 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 43 requests, 20,180 tokens read, 23,705 tokens written (36 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| garage_breaks | 3 | [R1, R4]: 3/3 | none | 0 | 0 | 0 |
| garage_same | 3 | [R2, R4]: 2/3 | none | 0 | 0 | 0 |
| garage_variant | 3 | nothing expected | [R2, R4]: 1, [R4, R5]: 2 | 0 | 0 | 0 |
| irrigation_breaks | 3 | [R1, R4]: 1/3 | [R3, R4]: 2 | 0 | 0 | 3 |
| irrigation_same | 3 | [R2, R4]: 0/3 | none | 0 | 0 | 3 |
| irrigation_variant | 3 | nothing expected | [R2, R4]: 3 | 0 | 0 | 0 |
| library_breaks | 3 | [R1, R4]: 3/3 | none | 0 | 0 | 5 |
| library_same | 3 | [R2, R4]: 0/3 | none | 0 | 0 | 6 |
| library_variant | 3 | nothing expected | [R2, R4]: 3, [R3, R5]: 3, [R4, R5]: 3, [R4, R6]: 2 | 0 | 0 | 6 |
| pharmacy_breaks | 3 | [R1, R4]: 3/3 | [R3, R4]: 1 | 0 | 0 | 3 |
| pharmacy_same | 3 | [R2, R4]: 3/3 | none | 0 | 0 | 0 |
| pharmacy_variant | 3 | nothing expected | [R3, R5]: 2, [R4, R5]: 1 | 0 | 0 | 3 |
