# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T23:09:23)

24 specs, 48 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 22/24 | 12/12 | 10/12 | 8/12 | 163 | 0/0 | 6 | 18 |
| doubtful conflicts set aside | 21/24 | 12/12 | 9/12 | 0/12 | 3 | 0/0 | 6 | 18 |
| without step 6 (no questions, nothing checked) | 22/24 | 12/12 | 10/12 | 10/12 | 170 | 0/0 | 9 | 30 |
| without step 6, doubtful set aside | 21/24 | 12/12 | 9/12 | 0/12 | 3 | 0/0 | 9 | 30 |
| without checks of links and facts | 22/24 | 12/12 | 10/12 | 10/12 | 170 | 0/0 | 6 | 18 |
| translation needs 7 of 8 answers | 22/24 | 12/12 | 10/12 | 8/12 | 163 | 0/0 | 12 | 37 |
| without assumed facts and links | 22/24 | 12/12 | 10/12 | 8/12 | 158 | 0/0 | 6 | 18 |
| facts vote without the parentheses repair | 22/24 | 12/12 | 10/12 | 8/12 | 163 | 0/0 | 6 | 18 |
| without the questions about outcomes | 22/24 | 12/12 | 10/12 | 8/12 | 158 | 0/0 | 6 | 18 |
| without the questions about outcomes, doubtful set aside | 21/24 | 12/12 | 9/12 | 0/12 | 0 | 0/0 | 6 | 18 |
| pairs of rules only | 22/24 | 12/12 | 10/12 | 8/12 | 163 | 0/0 | 6 | 18 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 11 | 2 | 3 | 6 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/12 | 0/12 | 0 | 36 |
| once for each event | 10/12 | 2/12 | 12 | 24 |
| once for each event, doubtful set aside | 10/12 | 2/12 | 12 | 24 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| deploy_clean | 2 | none expected | [1, 7]: 2 | none |
| deploy_direct | 2 | [2, 11]: 2/2 | [1, 7]: 2 | none |
| deploy_gap | 2 | none expected | [1, 7]: 2 | none |
| deploy_overlap | 2 | [1, 11]: 2/2 | [1, 7]: 2, [2, 8]: 2, [8, 11]: 2 | none |
| dns_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [2, 8]: 2 | 3: 1 |
| dns_direct | 2 | [4, 11]: 2/2 | [1, 3]: 2, [2, 8]: 2 | 7: 1 |
| dns_gap | 2 | none expected | [1, 3]: 2, [1, 4]: 2 | none |
| dns_overlap | 2 | [7, 11]: 1/2 | [1, 3]: 2, [1, 4]: 2, [2, 8]: 2 | 7: 1 |
| flags_clean | 2 | none expected | none | 1: 1, 10: 1 |
| flags_direct | 2 | [4, 11]: 2/2 | none | 1: 1 |
| flags_gap | 2 | none expected | none | none |
| flags_overlap | 2 | [5, 11]: 2/2 | [9, 11]: 1 | 1: 2 |
| issues_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| issues_direct | 2 | [1, 11]: 2/2 | [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| issues_gap | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| issues_overlap | 2 | [3, 11]: 2/2 | [1, 3]: 2, [1, 4]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [3, 7]: 2, [4, 7]: 2 | none |
| mailq_clean | 2 | none expected | none | 10: 1 |
| mailq_direct | 2 | [2, 11]: 2/2 | none | none |
| mailq_gap | 2 | none expected | none | none |
| mailq_overlap | 2 | [3, 11]: 2/2 | none | 10: 1 |
| payments_clean | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [1, 6]: 2, [1, 8]: 2, [2, 3]: 2, [2, 4]: 2, [2, 6]: 2, [2, 8]: 2, [4, 6]: 2, [4, 8]: 2, [6, 8]: 2 | 5: 2 |
| payments_direct | 2 | [2, 11]: 2/2 | [1, 3]: 2, [1, 4]: 2, [1, 6]: 2, [1, 8]: 2, [4, 6]: 2, [4, 8]: 2, [6, 8]: 2 | 5: 2 |
| payments_gap | 2 | none expected | [1, 3]: 2, [1, 4]: 2, [1, 7]: 2, [2, 3]: 2, [2, 4]: 2, [2, 7]: 2, [4, 7]: 2 | 5: 2, 9: 1 |
| payments_overlap | 2 | [5, 11]: 1/2 | [1, 3]: 2, [1, 4]: 2, [1, 5]: 2, [1, 6]: 2, [1, 8]: 2, [2, 3]: 2, [2, 4]: 2, [2, 5]: 2, [2, 6]: 2, [2, 8]: 2, [3, 5]: 2, [4, 6]: 2, [4, 8]: 2, [6, 8]: 2 | 5: 1 |
