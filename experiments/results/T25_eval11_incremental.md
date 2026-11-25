# Evaluation of the change check, the specs formalized once (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T14:07:06)

30 specs, 90 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | direct | modified | overlap | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 36/36 | 9/9 | 18/18 | 9/9 | 0/18 | 0 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 33/36 | 9/9 | 15/18 | 9/9 | 0/18 | 0 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 36/36 | 9/9 | 18/18 | 9/9 | 0/18 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | narrowed | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|---|
| default (1 symbol set) | 36/36 | 18/18 | 18/18 | 0/18 | 36 |
| doubtful findings set aside | 36/36 | 18/18 | 18/18 | 0/18 | 36 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 1 where nothing was planted.
- Labels: 90 of 90 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 9 requests, 4,937 tokens read, 3,817 tokens written (90 runs). What the specs of a project cost, once for each run: 47 requests, 21,884 tokens read, 20,103 tokens written (18 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| cinema_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| cinema_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| cinema_modified | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| cinema_narrowed | 3 | gap R4: 3/3 | none | 3 | 0 | 0 |
| cinema_overlap | 3 | [N1, R6]: 3/3 | none | 0 | 0 | 0 |
| conference_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| conference_direct | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| conference_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| conference_modified | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| conference_narrowed | 3 | gap R2: 3/3 | none | 3 | 0 | 0 |
| coworking_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| coworking_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| coworking_modified | 3 | [N1, R6]: 3/3 | none | 0 | 0 | 0 |
| coworking_narrowed | 3 | gap R4: 3/3 | none | 3 | 0 | 0 |
| coworking_overlap | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| foodbank_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| foodbank_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| foodbank_modified | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| foodbank_narrowed | 3 | gap R4: 3/3 | none | 3 | 0 | 0 |
| foodbank_overlap | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| marina_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| marina_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| marina_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| marina_modified | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| marina_narrowed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
| museum_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| museum_direct | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| museum_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| museum_modified | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| museum_narrowed | 3 | gap R1: 3/3 | none | 3 | 0 | 0 |
