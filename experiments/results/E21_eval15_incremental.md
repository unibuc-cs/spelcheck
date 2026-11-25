# Evaluation of the change check, the specs formalized once (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T14:30:18)

36 specs, 108 runs scored.

Only findings that involve the change count; see change_run in evaluate.py.

## Conflicts, by configuration

| Configuration | Planted conflicts found | direct | modified | property | status | Quiet changes with a conflict about them | Other conflicts about the change | The old conflict, shown as the change's | The old conflict, found and not shown | All conflicts among existing rules, not shown |
|---|---|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 72/72 | 18/18 | 18/18 | 18/18 | 18/18 | 0/18 | 0 | 0/0 | 0/0 | 0 |
| doubtful conflicts set aside | 72/72 | 18/18 | 18/18 | 18/18 | 18/18 | 0/18 | 0 | 0/0 | 0/0 | 0 |
| without assumed facts and links | 71/72 | 17/18 | 18/18 | 18/18 | 18/18 | 0/18 | 0 | 0/0 | 0/0 | 0 |

## Gaps

| Configuration | Planted gaps found | gap | Quiet changes with a gap about them | Gaps about the change, all |
|---|---|---|---|---|
| default (1 symbol set) | 18/18 | 18/18 | 0/18 | 18 |
| doubtful findings set aside | 18/18 | 18/18 | 0/18 | 18 |

## Ambiguities, labels and cost (default (1 symbol set))

- Ambiguity flags on rules of the change: 1 where nothing was planted.
- Labels: 108 of 108 runs returned every scenario label as a rule id. In 0 of them the read step also made rules without a label (0 rules, 0 counted as part of the change).
- What a change cost the LLM, on average: 11 requests, 5,791 tokens read, 4,604 tokens written (108 runs). What the specs of a project cost, once for each run: 60 requests, 27,274 tokens read, 24,030 tokens written (18 runs).

## By case (default (1 symbol set))

| Case | Runs | Expected, found in | Other conflicts about the change (rules: runs) | Gaps about the change | The old conflict, shown as the change's | Conflicts not shown |
|---|---|---|---|---|---|---|
| airfield_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| airfield_direct | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| airfield_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| airfield_modified | 3 | [N1, R5]: 3/3 | none | 0 | 0 | 0 |
| airfield_property | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| airfield_status | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| bakery_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| bakery_direct | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| bakery_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| bakery_modified | 3 | [N1, R5]: 3/3 | none | 0 | 0 | 0 |
| bakery_property | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| bakery_status | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| bowling_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| bowling_direct | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| bowling_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| bowling_modified | 3 | [N1, R5]: 3/3 | none | 0 | 0 | 0 |
| bowling_property | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| bowling_status | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| escaperoom_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| escaperoom_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| escaperoom_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| escaperoom_modified | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| escaperoom_property | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| escaperoom_status | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| observatory_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| observatory_direct | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| observatory_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| observatory_modified | 3 | [N1, R5]: 3/3 | none | 0 | 0 | 0 |
| observatory_property | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| observatory_status | 3 | [N1, R7]: 3/3 | none | 0 | 0 | 0 |
| tailor_clean | 3 | nothing expected | none | 0 | 0 | 0 |
| tailor_direct | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
| tailor_gap | 3 | gap N1: 3/3 | none | 3 | 0 | 0 |
| tailor_modified | 3 | [N1, R1]: 3/3 | none | 0 | 0 | 0 |
| tailor_property | 3 | [N1, R4]: 3/3 | none | 0 | 0 | 0 |
| tailor_status | 3 | [N1, R3]: 3/3 | none | 0 | 0 | 0 |
