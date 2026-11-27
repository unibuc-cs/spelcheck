# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T22:40:52)

16 specs, 48 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | cross | direct | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 24/24 | 12/12 | 12/12 | 11/24 | 36 | 0/0 | 0/0 | 22 |
| doubtful conflicts set aside | 24/24 | 12/12 | 12/12 | 0/24 | 2 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 12/24 | 0/12 | 12/12 | 5/24 | 6 | 0/0 | 0/0 | 2 |
| without the questions about conditions | 24/24 | 12/12 | 12/12 | 12/24 | 41 | 0/0 | 0/0 | 24 |
| without the questions about conditions, doubtful set aside | 24/24 | 12/12 | 12/12 | 0/24 | 2 | 0/0 | 0/0 | 0 |
| a run read as one moment, doubtful set aside | 12/24 | 0/12 | 12/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| examples read as rules, doubtful set aside | 24/24 | 12/12 | 12/12 | 11/24 | 35 | 0/0 | 0/0 | 20 |
| links that only rename not asked about, doubtful set aside | 24/24 | 12/12 | 12/12 | 9/24 | 11 | 0/0 | 0/0 | 0 |
| one example of a conflict is enough, doubtful set aside | 24/24 | 12/12 | 12/12 | 0/24 | 2 | 0/0 | 0/0 | 0 |
| without the questions whether a rule applies | 24/24 | 12/12 | 12/12 | 11/24 | 34 | 0/0 | 0/0 | 22 |
| without the questions whether a rule applies, doubtful set aside | 24/24 | 12/12 | 12/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 8/24 | 23 |
| doubtful findings set aside | 0/0 |  | 8/24 | 23 |
| without the questions about conditions | 0/0 |  | 8/24 | 23 |
| without the questions about conditions, doubtful set aside | 0/0 |  | 8/24 | 23 |
| a run read as one moment, doubtful set aside | 0/0 |  | 8/24 | 23 |
| examples read as rules, doubtful set aside | 0/0 |  | 8/24 | 23 |
| links that only rename not asked about, doubtful set aside | 0/0 |  | 8/24 | 23 |
| one example of a conflict is enough, doubtful set aside | 0/0 |  | 8/24 | 23 |
| without the questions whether a rule applies | 0/0 |  | 8/24 | 23 |
| without the questions whether a rule applies, doubtful set aside | 0/0 |  | 8/24 | 23 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 1 where nothing was planted.
- Labels: 48 of 48 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 87 requests, 43,147 tokens read, 51,065 tokens written (48 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| parcels_clean | 3 | nothing expected | [R5, R8]: 1, [R7, R10]: 1, [R7, R8]: 1, [R9, R10]: 3 | 3 | 0 | 0 |
| parcels_cross | 3 | [R2, R6]: 3/3 | [R4, R7]: 3, [R5, R7]: 2, [R7, R9]: 3 | 3 | 0 | 2 |
| parcels_direct | 3 | [R8, R9]: 3/3 | none | 3 | 0 | 0 |
| parcels_twins | 3 | nothing expected | none | 0 | 0 | 1 |
| samples_clean | 3 | nothing expected | [R2, R3]: 2, [R2, R5]: 3, [R4, R5]: 3 | 1 | 0 | 0 |
| samples_cross | 3 | [R4, R8]: 3/3 | none | 0 | 0 | 2 |
| samples_direct | 3 | [R3, R4]: 3/3 | none | 3 | 0 | 1 |
| samples_twins | 3 | nothing expected | none | 0 | 0 | 2 |
| transfers_clean | 3 | nothing expected | [R8, R9]: 1, [R9, R10]: 2 | 3 | 0 | 2 |
| transfers_cross | 3 | [R2, R6]: 3/3 | [R7, R9]: 3 | 0 | 0 | 0 |
| transfers_direct | 3 | [R8, R9]: 3/3 | none | 3 | 0 | 0 |
| transfers_twins | 3 | nothing expected | none | 0 | 0 | 0 |
| trips_clean | 3 | nothing expected | [R4, R10]: 1, [R4, R9]: 1, [R9, R10]: 3 | 1 | 0 | 3 |
| trips_cross | 3 | [R2, R6]: 3/3 | [R2, R7]: 2, [R3, R7]: 1 | 0 | 0 | 3 |
| trips_direct | 3 | [R8, R9]: 3/3 | none | 3 | 0 | 3 |
| trips_twins | 3 | nothing expected | none | 0 | 0 | 3 |
