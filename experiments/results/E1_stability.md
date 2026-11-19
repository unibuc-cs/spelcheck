# Stability experiment (10 runs per row, model Qwen/Qwen3.8-27B-FP8)

| Spec | Setting | All expected conflicts found | Runs with other conflicts | Gaps per run | Rule flagged ambiguous: in how many runs |
|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 0 | 0 gap(s): 10 | none |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 0 | 0 gap(s): 10 | rule 3: 8 |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 0 | 0 gap(s): 10 | rule 3: 5, rule 5: 1 |
| auth_openspec | 8 samples, symbols also vary | 6/10 | 1 | 0 gap(s): 3, 1 gap(s): 1, 3 gap(s): 6 | rule 1: 1, rule 2: 2, rule 3: 7, rule 4: 1, rule 5: 1 |
| delete_property | 1 greedy translation | 0/10 | 0 | 1 gap(s): 9, 2 gap(s): 1 | none |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 0 | 1 gap(s): 5, 2 gap(s): 5 | rule 4: 8 |
| delete_property | 8 samples, T=1.0 | 0/10 | 0 | 1 gap(s): 8, 2 gap(s): 2 | rule 4: 6 |
| delete_property | 8 samples, symbols also vary | 0/10 | 0 | 1 gap(s): 6, 2 gap(s): 4 | rule 1: 1, rule 2: 1, rule 3: 1, rule 4: 7 |
| order | 1 greedy translation | 10/10 | 0 | 1 gap(s): 10 | none |
| order | 8 samples, T=0.7 (default) | 10/10 | 0 | 1 gap(s): 10 | none |
| order | 8 samples, T=1.0 | 10/10 | 0 | 1 gap(s): 10 | rule 3: 1 |
| order | 8 samples, symbols also vary | 10/10 | 0 | 1 gap(s): 10 | none |
