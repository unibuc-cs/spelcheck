# Evaluation of the change check (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T10:37:26)

22 specs, 66 runs scored.

Only findings that involve a rule of the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | direct | overlap | Clean changes with a conflict about the change | Other conflicts about the change | Conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|
| default (1 symbol set) | 12/12 | 3/3 | 9/9 | 0/0 | 2 | 1 |
| doubtful conflicts set aside | 12/12 | 3/3 | 9/9 | 0/0 | 2 | 0 |
| without assumed facts and links | 3/12 | 0/3 | 3/9 | 0/0 | 0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | narrowed | Clean changes with a gap on a covered event | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 18/18 | 18/18 | 0/0 | 0/0 | 45 |
| doubtful findings set aside | 18/18 | 18/18 | 0/0 | 0/0 | 45 |

## Ambiguities and labels (default (1 symbol set))

- Ambiguity flags on rules of the change: 3 where nothing was planted; planted ambiguities found: 13/36.
- Labels: 66 of 66 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | Conflicts not shown |
|---|---|---|---|---|---|
| allotments_ambiguity1 | 3 | nothing expected | none | 1 | 0 |
| allotments_ambiguity2 | 3 | nothing expected | none | 3 | 0 |
| allotments_gap | 3 | gap R1: 3/3 | none | 3 | 0 |
| grants_ambiguity1 | 3 | nothing expected | none | 1 | 0 |
| grants_ambiguity2 | 3 | nothing expected | none | 3 | 0 |
| grants_gap | 3 | gap R1: 3/3 | none | 3 | 0 |
| grants_overlap | 3 | [R3, R4]: 3/3 | none | 0 | 0 |
| passports_ambiguity1 | 3 | nothing expected | none | 0 | 0 |
| passports_ambiguity2 | 3 | nothing expected | none | 2 | 0 |
| passports_gap | 3 | gap R1: 3/3 | none | 3 | 0 |
| passports_overlap | 3 | [R3, R6]: 3/3 | none | 3 | 0 |
| shelter_ambiguity1 | 3 | nothing expected | none | 0 | 0 |
| shelter_ambiguity2 | 3 | nothing expected | none | 3 | 0 |
| shelter_gap | 3 | gap R1: 3/3 | [R2, R3]: 2 | 3 | 0 |
| topup_ambiguity1 | 3 | nothing expected | none | 0 | 1 |
| topup_ambiguity2 | 3 | nothing expected | none | 2 | 0 |
| topup_direct | 3 | [R4, R5]: 3/3 | none | 0 | 0 |
| topup_gap | 3 | gap R1: 3/3 | none | 6 | 0 |
| visitors_ambiguity1 | 3 | nothing expected | none | 0 | 0 |
| visitors_ambiguity2 | 3 | nothing expected | none | 3 | 0 |
| visitors_gap | 3 | gap R1: 3/3 | none | 3 | 0 |
| visitors_overlap | 3 | [R1, R6]: 3/3 | none | 3 | 0 |
