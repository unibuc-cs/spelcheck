# Evaluation (3 runs per spec, 1 symbol sets per run, model Qwen/Qwen3.8-27B-FP8, 2026-11-18T12:00:29)

30 specs, 90 runs scored.

## By configuration

| Configuration | Planted conflicts found | direct | overlap | Clean runs with a false alarm | Unexpected conflicts | Planted ambiguities found | Ambiguity flags on clean specs | Other ambiguity flags |
|---|---|---|---|---|---|---|---|---|
| default (1 symbol set) | 31/36 | 14/18 | 17/18 | 0/18 | 3 | 17/36 | 9 | 57 |
| doubtful conflicts set aside | 31/36 | 14/18 | 17/18 | 0/18 | 3 | 17/36 | 9 | 57 |
| without step 6 (no questions, links unchecked) | 32/36 | 15/18 | 17/18 | 0/18 | 6 | 13/36 | 6 | 40 |
| without link checks | 32/36 | 15/18 | 17/18 | 0/18 | 6 | 17/36 | 9 | 57 |
| without assumed facts and links | 18/36 | 6/18 | 12/18 | 0/18 | 0 | 17/36 | 9 | 57 |
| pairs of rules only | 31/36 | 14/18 | 17/18 | 0/18 | 3 | 17/36 | 9 | 57 |

## By spec (default (1 symbol set))

| Spec | Runs | Expected conflicts found | Unexpected conflicts (rules: runs) | Ambiguity flags (rule: runs) |
|---|---|---|---|---|
| discounts_ambiguity1 | 3 | none expected | none | 3 (planted): 3, 4: 2, 5: 2 |
| discounts_ambiguity2 | 3 | none expected | none | 4: 3, 5: 2 |
| discounts_clean | 3 | none expected | none | 4: 2, 5: 3 |
| discounts_direct | 3 | [1, 2, 6]: 3/3 | none | 4: 2, 5: 2 |
| discounts_overlap | 3 | [1, 6]: 3/3 | none | 4: 3, 5: 3 |
| exam_ambiguity1 | 3 | none expected | none | 4 (planted): 1 |
| exam_ambiguity2 | 3 | none expected | none | 3 (planted): 2 |
| exam_clean | 3 | none expected | none | none |
| exam_direct | 3 | [2, 6]: 3/3 | none | none |
| exam_overlap | 3 | [5, 6]: 3/3 | none | none |
| newsletter_ambiguity1 | 3 | none expected | none | none |
| newsletter_ambiguity2 | 3 | none expected | none | none |
| newsletter_clean | 3 | none expected | none | none |
| newsletter_direct | 3 | [1, 6]: 2/3 | [5, 6]: 2 | 6: 2 |
| newsletter_overlap | 3 | [3, 6]: 3/3 | none | 6: 2 |
| pharmacy_ambiguity1 | 3 | none expected | none | 1: 1 |
| pharmacy_ambiguity2 | 3 | none expected | none | 1: 1, 5 (planted): 3 |
| pharmacy_clean | 3 | none expected | none | 1: 1 |
| pharmacy_direct | 3 | [3, 6]: 0/3 | none | none |
| pharmacy_overlap | 3 | [1, 6]: 3/3 | [2, 3]: 1 | 1: 1, 5: 2 |
| rental_ambiguity1 | 3 | none expected | none | 3 (planted): 3, 4: 1, 5: 2 |
| rental_ambiguity2 | 3 | none expected | none | 4 (planted): 2, 5: 3 |
| rental_clean | 3 | none expected | none | 5: 1 |
| rental_direct | 3 | [5, 6]: 3/3 | none | 4: 2, 5: 1, 6: 2 |
| rental_overlap | 3 | [4, 6]: 2/3 | none | 5: 1, 6: 1 |
| transfer_ambiguity1 | 3 | none expected | none | none |
| transfer_ambiguity2 | 3 | none expected | none | 1: 2, 2: 2, 5 (planted): 3 |
| transfer_clean | 3 | none expected | none | 1: 1, 2: 1 |
| transfer_direct | 3 | [4, 6]: 3/3 | none | 2: 2 |
| transfer_overlap | 3 | [1, 6]: 3/3 | none | 2: 1 |
