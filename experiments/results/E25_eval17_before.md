# Evaluation (2 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-25T22:58:59)

24 specs, 7 runs scored, 41 failed.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| doubtful conflicts set aside | 4/4 | 2/2 | 2/2 | 0/1 | 0 | 0/0 | 0 | 0 |
| without step 6 (no questions, nothing checked) | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| without step 6, doubtful set aside | 4/4 | 2/2 | 2/2 | 0/1 | 0 | 0/0 | 0 | 0 |
| without checks of links and facts | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| translation needs 7 of 8 answers | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| without assumed facts and links | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| facts vote without the parentheses repair | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| without the questions about outcomes | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |
| without the questions about outcomes, doubtful set aside | 4/4 | 2/2 | 2/2 | 0/1 | 0 | 0/0 | 0 | 0 |
| pairs of rules only | 4/4 | 2/2 | 2/2 | 0/1 | 7 | 0/0 | 0 | 0 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 0 | 0 | 0 | 0 |
| other | 0 | 0 | 0 | 0 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/2 | 0/1 | 0 | 3 |
| once for each event | 2/2 | 0/1 | 0 | 1 |
| once for each event, doubtful set aside | 2/2 | 0/1 | 0 | 1 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| deploy_clean | 0 | none expected | none | none |
| deploy_direct | 0 | [2, 11]: 0/0 | none | none |
| deploy_gap | 0 | none expected | none | none |
| deploy_overlap | 0 | [1, 11]: 0/0 | none | none |
| dns_clean | 0 | none expected | none | none |
| dns_direct | 0 | [4, 11]: 0/0 | none | none |
| dns_gap | 0 | none expected | none | none |
| dns_overlap | 0 | [7, 11]: 0/0 | none | none |
| flags_clean | 0 | none expected | none | none |
| flags_direct | 0 | [4, 11]: 0/0 | none | none |
| flags_gap | 0 | none expected | none | none |
| flags_overlap | 0 | [5, 11]: 0/0 | none | none |
| issues_clean | 0 | none expected | none | none |
| issues_direct | 0 | [1, 11]: 0/0 | none | none |
| issues_gap | 0 | none expected | none | none |
| issues_overlap | 1 | [3, 11]: 1/1 | [1, 3]: 1, [1, 4]: 1, [2, 3]: 1, [2, 4]: 1, [2, 7]: 1, [3, 7]: 1, [4, 7]: 1 | none |
| mailq_clean | 1 | none expected | none | none |
| mailq_direct | 2 | [2, 11]: 2/2 | none | none |
| mailq_gap | 2 | none expected | none | none |
| mailq_overlap | 1 | [3, 11]: 1/1 | none | none |
| payments_clean | 0 | none expected | none | none |
| payments_direct | 0 | [2, 11]: 0/0 | none | none |
| payments_gap | 0 | none expected | none | none |
| payments_overlap | 0 | [5, 11]: 0/0 | none | none |
