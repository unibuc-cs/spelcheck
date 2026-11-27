# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-27T15:56:08)

12 specs, 25 runs scored, 11 failed.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | breaks | chain | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 13/13 | 3/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 12/13 | 2/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 0/13 | 0/3 | 0/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| without the questions about conditions | 13/13 | 3/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| without the questions about conditions, doubtful set aside | 12/13 | 2/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| a run read as one moment, doubtful set aside | 0/13 | 0/3 | 0/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| examples read as rules, doubtful set aside | 13/13 | 3/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| links that only rename not asked about, doubtful set aside | 12/13 | 2/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| one example of a conflict is enough, doubtful set aside | 12/13 | 2/3 | 10/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| without the questions whether a rule applies | 3/13 | 3/3 | 0/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |
| without the questions whether a rule applies, doubtful set aside | 0/13 | 0/3 | 0/10 | 0/12 | 0 | 0/0 | 0/0 | 0 |

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

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 25 of 36 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 52 requests, 23,567 tokens read, 28,094 tokens written (25 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| catering_breaks | 0 | nothing expected | none | 0 | 0 | 0 |
| catering_chain | 3 | [R1, R4]: 3/3 | none | 0 | 0 | 0 |
| catering_several | 3 | nothing expected | none | 0 | 0 | 0 |
| loans_breaks | 2 | [R1, R4]: 2/2 | none | 0 | 0 | 0 |
| loans_chain | 3 | [R1, R4]: 3/3 | none | 0 | 0 | 0 |
| loans_several | 3 | nothing expected | none | 0 | 0 | 0 |
| movers_breaks | 1 | [R1, R4]: 1/1 | none | 0 | 0 | 0 |
| movers_chain | 1 | [R1, R4]: 1/1 | none | 0 | 0 | 0 |
| movers_several | 3 | nothing expected | none | 0 | 0 | 0 |
| vet_breaks | 0 | nothing expected | none | 0 | 0 | 0 |
| vet_chain | 3 | [R1, R4]: 3/3 | none | 0 | 0 | 0 |
| vet_several | 3 | nothing expected | none | 0 | 0 | 0 |
