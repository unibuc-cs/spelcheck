# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-27T22:43:18)

16 specs, 48 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | breaks | chain | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 0/24 | 0/12 | 0/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| without the questions about conditions | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| without the questions about conditions, doubtful set aside | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| a run read as one moment, doubtful set aside | 0/24 | 0/12 | 0/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| examples read as rules, doubtful set aside | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| links that only rename not asked about, doubtful set aside | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| one example of a conflict is enough, doubtful set aside | 15/24 | 12/12 | 3/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| without the questions whether a rule applies | 12/24 | 12/12 | 0/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |
| without the questions whether a rule applies, doubtful set aside | 0/24 | 0/12 | 0/12 | 0/24 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found |  | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|
| default (1 symbol set) | 0/0 |  | 0/24 | 0 |
| doubtful findings set aside | 0/0 |  | 0/24 | 0 |
| without the questions about conditions | 0/0 |  | 0/24 | 0 |
| without the questions about conditions, doubtful set aside | 0/0 |  | 0/24 | 0 |
| a run read as one moment, doubtful set aside | 0/0 |  | 0/24 | 0 |
| examples read as rules, doubtful set aside | 0/0 |  | 0/24 | 0 |
| links that only rename not asked about, doubtful set aside | 0/0 |  | 0/24 | 0 |
| one example of a conflict is enough, doubtful set aside | 0/0 |  | 0/24 | 0 |
| without the questions whether a rule applies | 0/0 |  | 0/24 | 0 |
| without the questions whether a rule applies, doubtful set aside | 0/0 |  | 0/24 | 0 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 48 of 48 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 68 requests, 34,589 tokens read, 36,679 tokens written (48 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| bookbinder_breaks | 3 | [R1, R5]: 3/3 | none | 0 | 0 | 0 |
| bookbinder_chain | 3 | [R1, R5]: 3/3 | none | 0 | 0 | 0 |
| bookbinder_near | 3 | nothing expected | none | 0 | 0 | 0 |
| bookbinder_several | 3 | nothing expected | none | 0 | 0 | 0 |
| orchard_breaks | 3 | [R1, R5]: 3/3 | none | 0 | 0 | 0 |
| orchard_chain | 3 | [R1, R5]: 0/3 | none | 0 | 0 | 0 |
| orchard_near | 3 | nothing expected | none | 0 | 0 | 0 |
| orchard_several | 3 | nothing expected | none | 0 | 0 | 0 |
| shipyard_breaks | 3 | [R1, R5]: 3/3 | none | 0 | 0 | 0 |
| shipyard_chain | 3 | [R1, R5]: 0/3 | none | 0 | 0 | 0 |
| shipyard_near | 3 | nothing expected | none | 0 | 0 | 0 |
| shipyard_several | 3 | nothing expected | none | 0 | 0 | 0 |
| skischool_breaks | 3 | [R1, R5]: 3/3 | none | 0 | 0 | 0 |
| skischool_chain | 3 | [R1, R5]: 0/3 | none | 0 | 0 | 0 |
| skischool_near | 3 | nothing expected | none | 0 | 0 | 0 |
| skischool_several | 3 | nothing expected | none | 0 | 0 | 0 |
