# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T10:16:33)

30 specs, 90 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 18/18 | 18/18 | 0/0 | 12/18 | 259 | 11/36 | 3 | 15 |
| doubtful conflicts set aside | 18/18 | 18/18 | 0/0 | 9/18 | 128 | 11/36 | 3 | 15 |
| without step 6 (no questions, nothing checked) | 18/18 | 18/18 | 0/0 | 12/18 | 268 | 15/36 | 4 | 20 |
| without step 6, doubtful set aside | 18/18 | 18/18 | 0/0 | 9/18 | 128 | 15/36 | 4 | 20 |
| without checks of links and facts | 18/18 | 18/18 | 0/0 | 12/18 | 268 | 11/36 | 3 | 15 |
| translation needs 7 of 8 answers | 18/18 | 18/18 | 0/0 | 12/18 | 259 | 15/36 | 11 | 50 |
| without assumed facts and links | 18/18 | 18/18 | 0/0 | 8/18 | 130 | 11/36 | 3 | 15 |
| facts vote without the parentheses repair | 18/18 | 18/18 | 0/0 | 12/18 | 259 | 11/36 | 3 | 15 |
| without the questions about outcomes | 18/18 | 18/18 | 0/0 | 10/18 | 170 | 11/36 | 3 | 15 |
| without the questions about outcomes, doubtful set aside | 18/18 | 18/18 | 0/0 | 4/18 | 39 | 11/36 | 3 | 15 |
| pairs of rules only | 18/18 | 18/18 | 0/0 | 12/18 | 259 | 11/36 | 3 | 15 |

## Planted ambiguities found, by kind

| Configuration | andor | boundary | ifscope | only |
|---|---|---|---|---|
| default (1 symbol set) | 1/3 | 0/18 | 5/6 | 5/9 |
| without step 6 (no questions, nothing checked) | 2/3 | 4/18 | 3/6 | 6/9 |
| translation needs 7 of 8 answers | 1/3 | 1/18 | 6/6 | 7/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 8 | 3 | 0 | 5 |
| other | 12 | 5 | 4 | 3 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 51 |
| once for each event | 18/18 | 6/18 | 21 | 39 |
| once for each event, doubtful set aside | 18/18 | 6/18 | 21 | 39 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| linter_ambiguity1 | 3 | none expected | [1, 5]: 3, [2, 5]: 3, [3, 5]: 2, [4, 5]: 1 | 3: 1 |
| linter_ambiguity2 | 3 | none expected | [1, 5]: 3, [2, 5]: 3 | 3 (planted): 2 |
| linter_clean | 3 | none expected | [1, 5]: 3, [2, 5]: 3, [3, 5]: 1 | 3: 1 |
| linter_direct | 3 | [2, 8]: 3/3 | [1, 5]: 3, [3, 5]: 3 | none |
| linter_gap | 3 | none expected | [1, 4]: 3, [2, 4]: 3, [3, 4]: 3 | none |
| migrate_ambiguity1 | 3 | none expected | [1, 3]: 1, [2, 6]: 3, [3, 6]: 3, [4, 6]: 3 | none |
| migrate_ambiguity2 | 3 | none expected | [1, 6]: 1, [2, 6]: 3, [3, 6]: 3, [4, 6]: 3 | 6 (planted): 2 |
| migrate_clean | 3 | none expected | [2, 4]: 1, [2, 6]: 3, [3, 6]: 2, [4, 6]: 3 | none |
| migrate_direct | 3 | [2, 8]: 3/3 | [1, 6]: 2, [3, 6]: 3, [4, 6]: 3 | none |
| migrate_gap | 3 | none expected | [1, 5]: 1, [2, 5]: 3, [3, 5]: 3 | none |
| pager_ambiguity1 | 3 | none expected | [1, 3]: 3, [1, 5]: 3, [2, 3]: 3, [2, 5]: 3, [3, 5]: 3, [6, 7]: 1 | 3: 1 |
| pager_ambiguity2 | 3 | none expected | [1, 3]: 3, [1, 5]: 3, [2, 3]: 3, [2, 5]: 3, [3, 4]: 1, [3, 5]: 3, [4, 5]: 1, [4, 7]: 2 | 6 (planted): 1 |
| pager_clean | 3 | none expected | [1, 3]: 3, [1, 5]: 3, [2, 3]: 3, [2, 5]: 3, [3, 4]: 1, [3, 5]: 3, [6, 7]: 1 | none |
| pager_direct | 3 | [2, 8]: 3/3 | [1, 3]: 3, [1, 5]: 3, [3, 5]: 3, [6, 7]: 1 | none |
| pager_gap | 3 | none expected | [1, 3]: 3, [1, 5]: 3, [2, 3]: 3, [2, 5]: 3, [3, 4]: 3, [3, 5]: 3, [4, 5]: 1 | none |
| scheduler_ambiguity1 | 3 | none expected | [1, 3]: 3, [1, 4]: 3, [2, 3]: 3, [2, 4]: 3 | 6: 1 |
| scheduler_ambiguity2 | 3 | none expected | [1, 3]: 2, [1, 4]: 1, [1, 5]: 2, [1, 6]: 2, [2, 3]: 2, [2, 4]: 1, [2, 5]: 2, [2, 6]: 2, [3, 4]: 1, [3, 5]: 1, [3, 6]: 2, [5, 7]: 1 | 4 (planted): 3, 5: 1 |
| scheduler_clean | 3 | none expected | [1, 3]: 3, [1, 4]: 3, [1, 5]: 3, [1, 6]: 2, [2, 3]: 3, [2, 4]: 3, [2, 5]: 3, [2, 6]: 2, [3, 5]: 3, [3, 6]: 2, [4, 5]: 1, [4, 6]: 2 | 5: 1 |
| scheduler_direct | 3 | [2, 8]: 3/3 | [1, 3]: 3, [1, 4]: 3, [1, 5]: 3, [3, 5]: 3, [5, 7]: 2 | 5: 1, 6: 1 |
| scheduler_gap | 3 | none expected | [1, 2]: 3, [1, 3]: 3, [1, 4]: 3, [2, 4]: 3, [4, 6]: 1 | 4: 2, 5: 1 |
| vault_ambiguity1 | 3 | none expected | none | none |
| vault_ambiguity2 | 3 | none expected | none | 6 (planted): 2 |
| vault_clean | 3 | none expected | none | 4: 1 |
| vault_direct | 3 | [2, 8]: 3/3 | none | 4: 1 |
| vault_gap | 3 | none expected | none | 4: 2 |
| webhooks_ambiguity1 | 3 | none expected | none | none |
| webhooks_ambiguity2 | 3 | none expected | [2, 5]: 2, [5, 6]: 2 | 6 (planted): 1 |
| webhooks_clean | 3 | none expected | none | none |
| webhooks_direct | 3 | [2, 8]: 3/3 | [1, 5]: 3, [5, 6]: 2 | none |
| webhooks_gap | 3 | none expected | none | none |
