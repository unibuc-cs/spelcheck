# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T14:13:59)

30 specs, 60 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 12/12 | 12/12 | 0/0 | 9/12 | 171 | 5/24 | 0 | 7 |
| doubtful conflicts set aside | 12/12 | 12/12 | 0/0 | 7/12 | 84 | 5/24 | 0 | 7 |
| without step 6 (no questions, nothing checked) | 12/12 | 12/12 | 0/0 | 9/12 | 183 | 5/24 | 0 | 3 |
| without step 6, doubtful set aside | 12/12 | 12/12 | 0/0 | 7/12 | 85 | 5/24 | 0 | 3 |
| without checks of links and facts | 12/12 | 12/12 | 0/0 | 9/12 | 183 | 5/24 | 0 | 7 |
| translation needs 7 of 8 answers | 12/12 | 12/12 | 0/0 | 9/12 | 171 | 8/24 | 6 | 27 |
| without assumed facts and links | 12/12 | 12/12 | 0/0 | 7/12 | 94 | 5/24 | 0 | 7 |
| facts vote without the parentheses repair | 12/12 | 12/12 | 0/0 | 9/12 | 171 | 5/24 | 0 | 7 |
| without the questions about outcomes | 12/12 | 12/12 | 0/0 | 7/12 | 115 | 5/24 | 0 | 7 |
| without the questions about outcomes, doubtful set aside | 12/12 | 12/12 | 0/0 | 3/12 | 28 | 5/24 | 0 | 7 |
| without the questions about conditions | 12/12 | 12/12 | 0/0 | 9/12 | 172 | 5/24 | 0 | 7 |
| without the questions about conditions, doubtful set aside | 12/12 | 12/12 | 0/0 | 7/12 | 84 | 5/24 | 0 | 7 |
| pairs of rules only | 12/12 | 12/12 | 0/0 | 9/12 | 171 | 5/24 | 0 | 7 |

## Planted ambiguities found, by kind

| Configuration | andor | boundary | ifscope | only |
|---|---|---|---|---|
| default (1 symbol set) | 0/2 | 0/12 | 1/4 | 4/6 |
| without step 6 (no questions, nothing checked) | 0/2 | 1/12 | 1/4 | 3/6 |
| translation needs 7 of 8 answers | 2/2 | 0/12 | 2/4 | 4/6 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 4 | 1 | 0 | 3 |
| other | 5 | 1 | 3 | 1 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/12 | 0/12 | 0 | 34 |
| once for each event | 12/12 | 4/12 | 14 | 26 |
| once for each event, doubtful set aside | 12/12 | 4/12 | 14 | 26 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| linter_ambiguity1 | 2 | none expected | [1, 5]: 2, [2, 5]: 2, [3, 5]: 2 | none |
| linter_ambiguity2 | 2 | none expected | [1, 5]: 2, [2, 5]: 2 | 3 (planted): 2 |
| linter_clean | 2 | none expected | [1, 5]: 2, [2, 5]: 2 | none |
| linter_direct | 2 | [2, 8]: 2/2 | [1, 5]: 2, [3, 5]: 1 | 3: 1 |
| linter_gap | 2 | none expected | [1, 4]: 2, [2, 4]: 2, [3, 4]: 2 | none |
| migrate_ambiguity1 | 2 | none expected | [1, 6]: 1, [2, 6]: 2, [3, 6]: 1, [4, 6]: 2 | none |
| migrate_ambiguity2 | 2 | none expected | [2, 4]: 1, [2, 6]: 2, [3, 6]: 2, [4, 6]: 2 | 6 (planted): 1 |
| migrate_clean | 2 | none expected | [1, 6]: 1, [2, 4]: 1, [2, 6]: 2, [3, 6]: 2, [4, 6]: 2 | none |
| migrate_direct | 2 | [2, 8]: 2/2 | [1, 6]: 2, [3, 6]: 1, [4, 6]: 2 | none |
| migrate_gap | 2 | none expected | [1, 5]: 1, [2, 5]: 2, [3, 5]: 2 | none |
| pager_ambiguity1 | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 3]: 2, [2, 5]: 2, [3, 5]: 2 | none |
| pager_ambiguity2 | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 3]: 2, [2, 5]: 2, [3, 5]: 2 | 6 (planted): 2 |
| pager_clean | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 3]: 2, [2, 5]: 2, [3, 5]: 2 | none |
| pager_direct | 2 | [2, 8]: 2/2 | [1, 3]: 2, [1, 5]: 2, [3, 5]: 2 | none |
| pager_gap | 2 | none expected | [1, 3]: 2, [1, 5]: 2, [2, 3]: 2, [2, 5]: 2, [3, 4]: 2, [3, 5]: 2 | none |
| scheduler_ambiguity1 | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [1, 5]: 1, [1, 6]: 1, [2, 3]: 2, [2, 4]: 2, [2, 6]: 1, [3, 6]: 1, [4, 6]: 1 | 6: 1 |
| scheduler_ambiguity2 | 2 | none expected | [1, 3]: 1, [1, 4]: 2, [1, 5]: 2, [1, 6]: 1, [2, 3]: 1, [2, 4]: 2, [2, 5]: 2, [2, 6]: 1, [3, 4]: 1, [3, 5]: 1, [4, 6]: 1 | none |
| scheduler_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [1, 5]: 2, [2, 3]: 2, [2, 4]: 2, [2, 5]: 2, [3, 5]: 2, [5, 7]: 1 | none |
| scheduler_direct | 2 | [2, 8]: 2/2 | [1, 3]: 2, [1, 4]: 2, [1, 5]: 2, [3, 5]: 2, [5, 7]: 2 | 6: 1 |
| scheduler_gap | 2 | none expected | [1, 2]: 2, [1, 3]: 2, [1, 4]: 2, [2, 4]: 2 | 4: 1, 5: 1 |
| vault_ambiguity1 | 2 | none expected | none | none |
| vault_ambiguity2 | 2 | none expected | [3, 5]: 1 | 4: 1 |
| vault_clean | 2 | none expected | [3, 5]: 1 | none |
| vault_direct | 2 | [2, 8]: 2/2 | none | 4: 1 |
| vault_gap | 2 | none expected | none | none |
| webhooks_ambiguity1 | 2 | none expected | none | none |
| webhooks_ambiguity2 | 2 | none expected | [2, 5]: 1, [2, 7]: 1, [5, 6]: 1, [6, 7]: 1 | none |
| webhooks_clean | 2 | none expected | none | none |
| webhooks_direct | 2 | [2, 8]: 2/2 | [1, 5]: 1, [5, 6]: 1 | none |
| webhooks_gap | 2 | none expected | none | none |
