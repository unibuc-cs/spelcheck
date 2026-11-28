# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-28T02:47:45)

20 specs, 60 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | breaks | chain | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 21/24 | 9/12 | 12/12 | 15/36 | 16 | 0/0 | 0/0 | 12 |
| doubtful conflicts set aside | 20/24 | 8/12 | 12/12 | 1/36 | 1 | 0/0 | 0/0 | 1 |
| without assumed facts and links | 10/24 | 1/12 | 9/12 | 0/36 | 1 | 0/0 | 0/0 | 1 |
| without the questions about conditions | 21/24 | 9/12 | 12/12 | 15/36 | 16 | 0/0 | 0/0 | 12 |
| without the questions about conditions, doubtful set aside | 20/24 | 8/12 | 12/12 | 1/36 | 1 | 0/0 | 0/0 | 1 |
| a run read as one moment, doubtful set aside | 0/24 | 0/12 | 0/12 | 0/36 | 0 | 0/0 | 0/0 | 0 |
| examples read as rules, doubtful set aside | 21/24 | 9/12 | 12/12 | 15/36 | 16 | 0/0 | 0/0 | 12 |
| links that only rename not asked about, doubtful set aside | 20/24 | 8/12 | 12/12 | 1/36 | 1 | 0/0 | 0/0 | 1 |
| one example of a conflict is enough, doubtful set aside | 20/24 | 8/12 | 12/12 | 1/36 | 2 | 0/0 | 0/0 | 1 |
| an example need not exclude the other rules, doubtful set aside | 21/24 | 9/12 | 12/12 | 8/36 | 8 | 0/0 | 0/0 | 8 |
| without the questions whether a rule applies | 17/24 | 8/12 | 9/12 | 14/36 | 15 | 0/0 | 0/0 | 13 |
| without the questions whether a rule applies, doubtful set aside | 12/24 | 3/12 | 9/12 | 0/36 | 0 | 0/0 | 0/0 | 1 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 28/36 | 39 |
| doubtful findings set aside | 0/0 |  | 28/36 | 39 |
| without the questions about conditions | 0/0 |  | 28/36 | 39 |
| without the questions about conditions, doubtful set aside | 0/0 |  | 28/36 | 39 |
| a run read as one moment, doubtful set aside | 0/0 |  | 28/36 | 39 |
| examples read as rules, doubtful set aside | 0/0 |  | 28/36 | 39 |
| links that only rename not asked about, doubtful set aside | 0/0 |  | 28/36 | 39 |
| one example of a conflict is enough, doubtful set aside | 0/0 |  | 28/36 | 39 |
| an example need not exclude the other rules, doubtful set aside | 0/0 |  | 28/36 | 39 |
| without the questions whether a rule applies | 0/0 |  | 28/36 | 39 |
| without the questions whether a rule applies, doubtful set aside | 0/0 |  | 28/36 | 39 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 2 where nothing was planted.
- Labels: 60 of 60 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 59 requests, 32,170 tokens read, 36,473 tokens written (60 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| apiary_apart | 3 | nothing expected | none | 3 | 0 | 0 |
| apiary_breaks | 3 | [R2, R6]: 3/3 | none | 3 | 0 | 0 |
| apiary_chain | 3 | [R1, R6]: 3/3 | none | 0 | 0 | 1 |
| apiary_pair | 3 | nothing expected | [R2, R6]: 1 | 3 | 0 | 0 |
| apiary_refused | 3 | nothing expected | [R5, R6]: 1 | 3 | 0 | 0 |
| ferry_apart | 3 | nothing expected | [R2, R6]: 3 | 0 | 0 | 2 |
| ferry_breaks | 3 | [R2, R6]: 2/3 | none | 3 | 0 | 3 |
| ferry_chain | 3 | [R1, R6]: 3/3 | none | 0 | 0 | 0 |
| ferry_pair | 3 | nothing expected | [R2, R6]: 1 | 3 | 0 | 0 |
| ferry_refused | 3 | nothing expected | none | 3 | 0 | 0 |
| museum_apart | 3 | nothing expected | [R2, R6]: 3 | 1 | 0 | 2 |
| museum_breaks | 3 | [R2, R6]: 1/3 | [R2, R5, R6]: 1 | 2 | 0 | 1 |
| museum_chain | 3 | [R1, R6]: 3/3 | none | 0 | 0 | 0 |
| museum_pair | 3 | nothing expected | none | 3 | 0 | 0 |
| museum_refused | 3 | nothing expected | [R5, R6]: 1 | 3 | 0 | 0 |
| printshop_apart | 3 | nothing expected | [R2, R6]: 3 | 0 | 0 | 1 |
| printshop_breaks | 3 | [R2, R6]: 3/3 | none | 3 | 0 | 2 |
| printshop_chain | 3 | [R1, R6]: 3/3 | none | 0 | 0 | 0 |
| printshop_pair | 3 | nothing expected | none | 3 | 0 | 0 |
| printshop_refused | 3 | nothing expected | [R5, R6]: 2 | 3 | 0 | 0 |
