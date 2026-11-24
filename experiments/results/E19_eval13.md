# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T16:58:34)

36 specs, 108 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | modified | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 18/18 | 18/18 | 2/54 | 2 | 0/108 | 108/108 | 115 |
| doubtful conflicts set aside | 15/18 | 15/18 | 2/54 | 2 | 0/108 | 108/108 | 115 |
| without assumed facts and links | 15/18 | 15/18 | 0/54 | 0 | 0/108 | 72/108 | 72 |

## Gaps

| Configuration | Planted gaps found | narrowed | removed | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 35/36 | 17/18 | 18/18 | 0/54 | 35 |
| doubtful findings set aside | 35/36 | 17/18 | 18/18 | 0/54 | 35 |

## Ambiguities and labels (default (1 symbol set))

- Ambiguity flags on rules of the change: 2 where nothing was planted.
- Labels: 108 of 108 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| bloodbank_clean | 3 | nothing expected | none | 0 | 0 | 3 |
| bloodbank_modified | 3 | [R1, R9]: 3/3 | none | 0 | 0 | 3 |
| bloodbank_narrowed | 3 | gap R5: 3/3 | none | 3 | 0 | 3 |
| bloodbank_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 3 |
| bloodbank_retired | 3 | nothing expected | none | 0 | 0 | 3 |
| bloodbank_sibling | 3 | nothing expected | none | 0 | 0 | 3 |
| courses_clean | 3 | nothing expected | none | 0 | 0 | 3 |
| courses_modified | 3 | [R1, R9]: 3/3 | none | 0 | 0 | 3 |
| courses_narrowed | 3 | gap R5: 3/3 | none | 3 | 0 | 3 |
| courses_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 3 |
| courses_retired | 3 | nothing expected | none | 0 | 0 | 3 |
| courses_sibling | 3 | nothing expected | none | 0 | 0 | 3 |
| dorm_clean | 3 | nothing expected | none | 0 | 0 | 3 |
| dorm_modified | 3 | [R5, R6]: 3/3 | none | 0 | 0 | 3 |
| dorm_narrowed | 3 | gap R1: 2/3 | none | 2 | 0 | 3 |
| dorm_removed | 3 | gap R6: 3/3 | none | 3 | 0 | 3 |
| dorm_retired | 3 | nothing expected | none | 0 | 0 | 3 |
| dorm_sibling | 3 | nothing expected | none | 0 | 0 | 3 |
| makerspace_clean | 3 | nothing expected | none | 0 | 0 | 5 |
| makerspace_modified | 3 | [R1, R9]: 3/3 | none | 0 | 0 | 6 |
| makerspace_narrowed | 3 | gap R5: 3/3 | none | 3 | 0 | 3 |
| makerspace_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 4 |
| makerspace_retired | 3 | nothing expected | none | 0 | 0 | 4 |
| makerspace_sibling | 3 | nothing expected | [R4, R8]: 2 | 0 | 0 | 3 |
| newsroom_clean | 3 | nothing expected | none | 0 | 0 | 3 |
| newsroom_modified | 3 | [R1, R9]: 3/3 | none | 0 | 0 | 3 |
| newsroom_narrowed | 3 | gap R5: 3/3 | none | 3 | 0 | 3 |
| newsroom_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 3 |
| newsroom_retired | 3 | nothing expected | none | 0 | 0 | 3 |
| newsroom_sibling | 3 | nothing expected | none | 0 | 0 | 3 |
| permits_clean | 3 | nothing expected | none | 0 | 0 | 3 |
| permits_modified | 3 | [R1, R9]: 3/3 | none | 0 | 0 | 3 |
| permits_narrowed | 3 | gap R5: 3/3 | none | 3 | 0 | 3 |
| permits_removed | 3 | gap R1: 3/3 | none | 3 | 0 | 3 |
| permits_retired | 3 | nothing expected | none | 0 | 0 | 3 |
| permits_sibling | 3 | nothing expected | none | 0 | 0 | 3 |
