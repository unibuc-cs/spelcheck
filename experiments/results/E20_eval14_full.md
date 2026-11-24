# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T19:30:03)

36 specs, 108 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | direct | modified | overlap | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 54/54 | 18/18 | 18/18 | 18/18 | 0/18 | 3 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 51/54 | 18/18 | 15/18 | 18/18 | 0/18 | 3 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 37/54 | 4/18 | 15/18 | 18/18 | 0/18 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | removed | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 36/36 | 18/18 | 18/18 | 0/18 | 39 |
| doubtful findings set aside | 36/36 | 18/18 | 18/18 | 0/18 | 39 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 1 where nothing was planted.
- Labels: 108 of 108 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 68 requests, 32,431 tokens read, 28,806 tokens written (108 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| brewery_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| brewery_direct | 3 | [R3, R4]: 3/3 | none | 0 | 0 | 0 |
| brewery_gap | 3 | gap R8: 3/3 | none | 3 | 0 | 0 |
| brewery_modified | 3 | [R1, R7]: 3/3 | none | 0 | 0 | 0 |
| brewery_overlap | 3 | [R4, R5]: 3/3 | none | 0 | 0 | 0 |
| brewery_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| climbing_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| climbing_direct | 3 | [R3, R4]: 3/3 | none | 0 | 0 | 0 |
| climbing_gap | 3 | gap R8: 3/3 | none | 3 | 0 | 0 |
| climbing_modified | 3 | [R1, R7]: 3/3 | none | 0 | 0 | 0 |
| climbing_overlap | 3 | [R4, R5]: 3/3 | none | 0 | 0 | 0 |
| climbing_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| drivingschool_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| drivingschool_direct | 3 | [R3, R4]: 3/3 | none | 0 | 0 | 0 |
| drivingschool_gap | 3 | gap R8: 3/3 | none | 3 | 0 | 0 |
| drivingschool_modified | 3 | [R1, R7]: 3/3 | [R3, R7]: 3 | 0 | 0 | 0 |
| drivingschool_overlap | 3 | [R4, R5]: 3/3 | none | 0 | 0 | 0 |
| drivingschool_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| florist_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| florist_direct | 3 | [R3, R4]: 3/3 | none | 0 | 0 | 0 |
| florist_gap | 3 | gap R8: 3/3 | none | 3 | 0 | 0 |
| florist_modified | 3 | [R1, R7]: 3/3 | none | 0 | 0 | 0 |
| florist_overlap | 3 | [R4, R5]: 3/3 | none | 0 | 0 | 0 |
| florist_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| musicschool_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| musicschool_direct | 3 | [R3, R4]: 3/3 | none | 0 | 0 | 0 |
| musicschool_gap | 3 | gap R8: 3/3 | none | 3 | 0 | 0 |
| musicschool_modified | 3 | [R1, R7]: 3/3 | none | 0 | 0 | 0 |
| musicschool_overlap | 3 | [R4, R5]: 3/3 | none | 0 | 0 | 0 |
| musicschool_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| tennis_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| tennis_direct | 3 | [R7, R8]: 3/3 | none | 3 | 0 | 0 |
| tennis_gap | 3 | gap R5: 3/3 | none | 3 | 0 | 0 |
| tennis_modified | 3 | [R4, R5]: 3/3 | none | 0 | 0 | 0 |
| tennis_overlap | 3 | [R1, R8]: 3/3 | none | 0 | 0 | 0 |
| tennis_removed | 3 | gap R5: 3/3 | none | 3 | 0 | 0 |
