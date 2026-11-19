# Stability experiment (10 runs per row, model Qwen/Qwen3.8-27B-FP8, 2026-11-17T16:55:07)

"Expected found" = runs in which all expected conflicts were found. "Other" = runs with at least one conflict that was not expected. Both are given for the rules alone, and with the assumed domain facts.

| Spec | Setting | Expected found: rules alone | Expected found: with facts | Other: rules alone | Other: with facts | Facts kept per run | Gaps per run | Rule flagged ambiguous: in how many runs |
|---|---|---|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 10/10 | 0 | 0 | 1 fact(s): 10 | 0 gap(s): 10 | none |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0 | 0 | 0 fact(s): 10 | 0 gap(s): 10 | rule 3: 4 |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 10/10 | 0 | 0 | 0 fact(s): 10 | 0 gap(s): 10 | rule 3: 7 |
| auth_openspec | 8 samples, symbols also vary | 9/10 | 9/10 | 1 | 1 | 0 fact(s): 10 | 0 gap(s): 6, 3 gap(s): 4 | rule 1: 2, rule 3: 5, rule 4: 1, rule 5: 1 |
| delete_property | 1 greedy translation | 0/10 | 1/10 | 0 | 0 | 0 fact(s): 8, 1 fact(s): 1, 9 fact(s): 1 | 1 gap(s): 8, 2 gap(s): 2 | none |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 2/10 | 0 | 0 | 0 fact(s): 8, 1 fact(s): 2 | 1 gap(s): 5, 2 gap(s): 5 | rule 4: 9 |
| delete_property | 8 samples, T=1.0 | 0/10 | 1/10 | 0 | 0 | 0 fact(s): 9, 1 fact(s): 1 | 1 gap(s): 4, 2 gap(s): 6 | rule 1: 1, rule 3: 1, rule 4: 8 |
| delete_property | 8 samples, symbols also vary | 0/10 | 1/10 | 0 | 0 | 0 fact(s): 8, 1 fact(s): 2 | 1 gap(s): 8, 2 gap(s): 2 | rule 3: 2, rule 4: 5 |
| order | 1 greedy translation | 10/10 | 10/10 | 0 | 0 | 5 fact(s): 10 | 1 gap(s): 10 | none |
| order | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0 | 0 | 2 fact(s): 3, 4 fact(s): 1, 5 fact(s): 5, 7 fact(s): 1 | 1 gap(s): 10 | none |
| order | 8 samples, T=1.0 | 10/10 | 10/10 | 0 | 0 | 0 fact(s): 1, 2 fact(s): 6, 4 fact(s): 2, 6 fact(s): 1 | 1 gap(s): 10 | rule 3: 1 |
| order | 8 samples, symbols also vary | 10/10 | 10/10 | 0 | 0 | 2 fact(s): 3, 3 fact(s): 1, 5 fact(s): 5, 7 fact(s): 1 | 1 gap(s): 10 | none |
