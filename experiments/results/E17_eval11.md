# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T11:04:49)

30 specs, 90 runs scored.

Only findings that involve a rule of the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | direct | modified | overlap | Clean changes with a conflict about the change | Other conflicts about the change | Conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 36/36 | 9/9 | 18/18 | 9/9 | 0/18 | 0 | 0 |
| doubtful conflicts set aside | 33/36 | 9/9 | 15/18 | 9/9 | 0/18 | 0 | 0 |
| without assumed facts and links | 33/36 | 9/9 | 15/18 | 9/9 | 0/18 | 0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | narrowed | Clean changes with a gap on a covered event | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 36/36 | 18/18 | 18/18 | 0/18 | 36 |
| doubtful findings set aside | 36/36 | 18/18 | 18/18 | 0/18 | 36 |

## Ambiguities and labels (default (1 symbol set))

- Ambiguity flags on rules of the change: 0 where nothing was planted.
- Labels: 90 of 90 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | Conflicts not shown |
|---|---|---|---|---|---|
| cinema_clean | 3 | nothing expected | none | 0 | 0 |
| cinema_gap | 3 | gap R7: 3/3 | none | 3 | 0 |
| cinema_modified | 3 | [R2, R4]: 3/3 | none | 0 | 0 |
| cinema_narrowed | 3 | gap R4: 3/3 | none | 3 | 0 |
| cinema_overlap | 3 | [R6, R7]: 3/3 | none | 0 | 0 |
| conference_clean | 3 | nothing expected | none | 0 | 0 |
| conference_direct | 3 | [R4, R5]: 3/3 | none | 0 | 0 |
| conference_gap | 3 | gap R5: 3/3 | none | 3 | 0 |
| conference_modified | 3 | [R1, R4]: 3/3 | none | 0 | 0 |
| conference_narrowed | 3 | gap R2: 3/3 | none | 3 | 0 |
| coworking_clean | 3 | nothing expected | none | 0 | 0 |
| coworking_gap | 3 | gap R7: 3/3 | none | 3 | 0 |
| coworking_modified | 3 | [R2, R6]: 3/3 | none | 0 | 0 |
| coworking_narrowed | 3 | gap R4: 3/3 | none | 3 | 0 |
| coworking_overlap | 3 | [R4, R7]: 3/3 | none | 0 | 0 |
| foodbank_clean | 3 | nothing expected | none | 0 | 0 |
| foodbank_gap | 3 | gap R7: 3/3 | none | 3 | 0 |
| foodbank_modified | 3 | [R2, R4]: 3/3 | none | 0 | 0 |
| foodbank_narrowed | 3 | gap R4: 3/3 | none | 3 | 0 |
| foodbank_overlap | 3 | [R1, R4]: 3/3 | none | 0 | 0 |
| marina_clean | 3 | nothing expected | none | 0 | 0 |
| marina_direct | 3 | [R3, R4]: 3/3 | none | 0 | 0 |
| marina_gap | 3 | gap R4: 3/3 | none | 3 | 0 |
| marina_modified | 3 | [R4, R5]: 3/3 | none | 0 | 0 |
| marina_narrowed | 3 | gap R1: 3/3 | none | 3 | 0 |
| museum_clean | 3 | nothing expected | none | 0 | 0 |
| museum_direct | 3 | [R4, R7]: 3/3 | none | 0 | 0 |
| museum_gap | 3 | gap R4: 3/3 | none | 3 | 0 |
| museum_modified | 3 | [R3, R5]: 3/3 | none | 0 | 0 |
| museum_narrowed | 3 | gap R1: 3/3 | none | 3 | 0 |
