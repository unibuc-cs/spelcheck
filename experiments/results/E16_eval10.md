# Evaluation (3 runs per spec, 1 symbol sets per run, temperature 0.7, model Qwen/Qwen3.8-27B-FP8, 2026-11-24T09:06:35)

30 specs, 90 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 7/36 | 1 | 7 |
| doubtful conflicts set aside | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 7/36 | 1 | 7 |
| without step 6 (no questions, nothing checked) | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 10/36 | 1 | 5 |
| without step 6, doubtful set aside | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 10/36 | 1 | 5 |
| without checks of links and facts | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 7/36 | 1 | 7 |
| translation needs 7 of 8 answers | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 16/36 | 9 | 46 |
| without assumed facts and links | 15/18 | 9/9 | 6/9 | 0/18 | 0 | 7/36 | 1 | 7 |
| facts vote without the parentheses repair | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 7/36 | 1 | 7 |
| pairs of rules only | 18/18 | 9/9 | 9/9 | 0/18 | 0 | 7/36 | 1 | 7 |

## Planted ambiguities found, by kind

| Configuration | and/or | boundary | if | only |
|---|---|---|---|---|
| default (1 symbol set) | 1/9 | 1/9 | 0/9 | 5/9 |
| without step 6 (no questions, nothing checked) | 0/9 | 1/9 | 0/9 | 9/9 |
| translation needs 7 of 8 answers | 7/9 | 2/9 | 2/9 | 5/9 |

## Ambiguity flags and the other reading (default (1 symbol set))

| Ambiguity flags | All | The other reading changes a conflict | Only a gap | Nothing |
|---|---|---|---|---|
| planted | 2 | 0 | 2 | 0 |
| other | 7 | 1 | 3 | 3 |

## Gaps (default (1 symbol set))

| Gap search | Planted gaps found | Clean runs with a gap on a covered event | Gaps on clean specs, with an event | Gaps on clean specs, all |
|---|---|---|---|---|
| over all situations (as before step 26) | 0/18 | 0/18 | 0 | 54 |
| once for each event | 18/18 | 5/18 | 26 | 44 |
| once for each event, doubtful set aside | 18/18 | 5/18 | 26 | 44 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| allotments_ambiguity1 | 3 | none expected | none | 1 (planted): 2 |
| allotments_ambiguity2 | 3 | none expected | none | 3 (planted): 1 |
| allotments_clean | 3 | none expected | none | 4: 1 |
| allotments_direct | 3 | [4, 6]: 3/3 | none | 4: 2 |
| allotments_gap | 3 | none expected | none | none |
| baggage_ambiguity1 | 3 | none expected | none | 3 (planted): 1 |
| baggage_ambiguity2 | 3 | none expected | none | none |
| baggage_clean | 3 | none expected | none | none |
| baggage_gap | 3 | none expected | none | none |
| baggage_overlap | 3 | [1, 6]: 3/3 | none | none |
| fuel_ambiguity1 | 3 | none expected | none | none |
| fuel_ambiguity2 | 3 | none expected | none | none |
| fuel_clean | 3 | none expected | none | none |
| fuel_direct | 3 | [3, 6]: 3/3 | none | 6: 1 |
| fuel_gap | 3 | none expected | none | none |
| inspection_ambiguity1 | 3 | none expected | none | none |
| inspection_ambiguity2 | 3 | none expected | none | none |
| inspection_clean | 3 | none expected | none | none |
| inspection_direct | 3 | [1, 6]: 3/3 | none | none |
| inspection_gap | 3 | none expected | none | none |
| passports_ambiguity1 | 3 | none expected | none | 5: 2 |
| passports_ambiguity2 | 3 | none expected | none | 5: 1 |
| passports_clean | 3 | none expected | none | none |
| passports_gap | 3 | none expected | none | none |
| passports_overlap | 3 | [3, 6]: 3/3 | none | none |
| visitors_ambiguity1 | 3 | none expected | none | none |
| visitors_ambiguity2 | 3 | none expected | none | 1 (planted): 3 |
| visitors_clean | 3 | none expected | none | none |
| visitors_gap | 3 | none expected | none | none |
| visitors_overlap | 3 | [1, 6]: 3/3 | none | none |
