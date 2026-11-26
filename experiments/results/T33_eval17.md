# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-26T09:48:40)

24 specs, 48 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 22/24 | 12/12 | 10/12 | 8/12 | 169 | 0/0 | 2 | 13 |
| doubtful conflicts set aside | 18/24 | 12/12 | 6/12 | 0/12 | 2 | 0/0 | 2 | 13 |
| without step 6 (no questions, nothing checked) | 22/24 | 12/12 | 10/12 | 9/12 | 175 | 0/0 | 7 | 25 |
| without step 6, doubtful set aside | 18/24 | 12/12 | 6/12 | 0/12 | 2 | 0/0 | 7 | 25 |
| without checks of links and facts | 22/24 | 12/12 | 10/12 | 9/12 | 175 | 0/0 | 2 | 13 |
| translation needs 7 of 8 answers | 22/24 | 12/12 | 10/12 | 8/12 | 169 | 0/0 | 8 | 36 |
| without assumed facts and links | 22/24 | 12/12 | 10/12 | 8/12 | 164 | 0/0 | 2 | 13 |
| facts vote without the parentheses repair | 22/24 | 12/12 | 10/12 | 8/12 | 169 | 0/0 | 2 | 13 |
| without the questions about outcomes | 22/24 | 12/12 | 10/12 | 8/12 | 165 | 0/0 | 2 | 13 |
| without the questions about outcomes, doubtful set aside | 20/24 | 12/12 | 8/12 | 0/12 | 0 | 0/0 | 2 | 13 |
| without the questions about conditions | 22/24 | 12/12 | 10/12 | 8/12 | 169 | 0/0 | 2 | 13 |
| without the questions about conditions, doubtful set aside | 20/24 | 12/12 | 8/12 | 0/12 | 2 | 0/0 | 2 | 13 |
| pairs of rules only | 22/24 | 12/12 | 10/12 | 8/12 | 169 | 0/0 | 2 | 13 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 8 | 0 | 0 | 8 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/12 | 0/12 | 0 | 36 |
| once for each event | 11/12 | 0/12 | 10 | 22 |
| once for each event, doubtful set aside | 11/12 | 0/12 | 10 | 22 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| deploy_clean | 2 | none expected | [1, 7]: 2, [6, 8]: 1 | none |
| deploy_direct | 2 | [2, 11]: 2/2 | [1, 7]: 2 | none |
| deploy_gap | 2 | none expected | [1, 7]: 2 | none |
| deploy_overlap | 2 | [1, 11]: 2/2 | [1, 7]: 2, [2, 8]: 2, [8, 11]: 2 | none |
| dns_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [2, 8]: 2 | none |
| dns_direct | 2 | [4, 11]: 2/2 | [1, 3]: 2, [2, 8]: 2 | 7: 1 |
| dns_gap | 2 | none expected | [1, 3]: 2, [1, 4]: 2 | 7: 1 |
| dns_overlap | 2 | [7, 11]: 2/2 | [1, 3]: 2, [1, 4]: 2, [2, 8]: 2 | none |
| flags_clean | 2 | none expected | none | 1: 2 |
| flags_direct | 2 | [4, 11]: 2/2 | none | 1: 2 |
| flags_gap | 2 | none expected | none | 1: 1 |
| flags_overlap | 2 | [5, 11]: 2/2 | none | 1: 2 |
| issues_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| issues_direct | 2 | [1, 11]: 2/2 | [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| issues_gap | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| issues_overlap | 2 | [3, 11]: 2/2 | [1, 3]: 2, [1, 4]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| mailq_clean | 2 | none expected | none | none |
| mailq_direct | 2 | [2, 11]: 2/2 | none | none |
| mailq_gap | 2 | none expected | [2, 3]: 1 | none |
| mailq_overlap | 2 | [3, 11]: 2/2 | none | none |
| payments_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [1, 5]: 2, [1, 6]: 2, [1, 8]: 2, [2, 3]: 2, [2, 4]: 2, [2, 5]: 2, [2, 6]: 2, [2, 8]: 2, [3, 5]: 2, [4, 6]: 2, [4, 8]: 2, [6, 8]: 2 | none |
| payments_direct | 2 | [2, 11]: 2/2 | [1, 3]: 2, [1, 4]: 2, [1, 5]: 1, [1, 6]: 2, [1, 8]: 2, [3, 5]: 1, [4, 6]: 2, [4, 8]: 2, [6, 8]: 2 | 5: 1 |
| payments_gap | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [1, 5]: 1, [1, 7]: 2, [2, 3]: 2, [2, 4]: 2, [2, 5]: 1, [2, 7]: 2, [3, 5]: 1, [4, 7]: 2 | 5: 1 |
| payments_overlap | 2 | [5, 11]: 0/2 | [1, 3]: 2, [1, 4]: 2, [1, 6]: 2, [1, 8]: 2, [2, 3]: 2, [2, 4]: 2, [2, 6]: 2, [2, 8]: 2, [4, 6]: 2, [4, 8]: 2, [6, 8]: 2 | 5: 2 |
