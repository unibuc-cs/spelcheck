# Evaluation of the change check, the specs formalized once (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T18:58:02)

36 specs, 108 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | direct | modified | overlap | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 50/54 | 17/18 | 18/18 | 15/18 | 0/18 | 1 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 45/54 | 17/18 | 13/18 | 15/18 | 0/18 | 1 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 44/54 | 11/18 | 18/18 | 15/18 | 0/18 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | removed | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 36/36 | 18/18 | 18/18 | 0/18 | 42 |
| doubtful findings set aside | 36/36 | 18/18 | 18/18 | 0/18 | 42 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 4 where nothing was planted.
- Labels: 108 of 108 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 9 requests, 4,934 tokens read, 3,816 tokens written (108 runs). What the specs of a project cost, once for each run: 61 requests, 28,641 tokens read, 25,969 tokens written (18 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| brewery_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| brewery_direct | 3 | [N1, R3]: 2/3 | none | 3 | 0 | 0 |
| brewery_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| brewery_modified | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| brewery_overlap | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| brewery_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| climbing_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| climbing_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| climbing_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| climbing_modified | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| climbing_overlap | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| climbing_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| drivingschool_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| drivingschool_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| drivingschool_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| drivingschool_modified | 3 | [N1, R1]: 3/3 | [N1, R6]: 1 | 0 | 0 | 0 |
| drivingschool_overlap | 3 | [N1, R4]: 0/3 | none | 0 | 0 | 0 |
| drivingschool_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| florist_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| florist_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| florist_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| florist_modified | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| florist_overlap | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| florist_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| musicschool_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| musicschool_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| musicschool_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| musicschool_modified | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| musicschool_overlap | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| musicschool_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| tennis_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| tennis_direct | 3 | [N1, R7]: 3/3 | none | 3 | 0 | 0 |
| tennis_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| tennis_modified | 3 | [N1, R5]: 3/3 | none | 0 | 0 | 0 |
| tennis_overlap | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| tennis_removed | 3 | gap R5: 3/3 | none | 3 | 0 | 0 |
