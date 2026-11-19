# Stability experiment (10 runs per row, model Qwen/Qwen3.8-27B-FP8, 2026-11-17T16:47:08)

## Runs in which all expected conflicts were found

"Unexpected" = runs with at least one conflict (solver, with facts) or one contradiction (review) that was not expected.

| Spec | Setting | Solver, rules alone | Solver, with facts | Review | Solver or review | Unexpected: solver | Unexpected: review |
|---|---|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 10/10 | n/a | n/a | 0 | n/a |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 10/10 | n/a | n/a | 0 | n/a |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 10/10 | n/a | n/a | 0 | n/a |
| auth_openspec | 8 samples, symbols also vary | 3/10 | 7/10 | n/a | n/a | 0 | n/a |
| delete_property | 1 greedy translation | 0/10 | 3/10 | n/a | n/a | 0 | n/a |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 0/10 | n/a | n/a | 0 | n/a |
| delete_property | 8 samples, T=1.0 | 0/10 | 0/10 | n/a | n/a | 0 | n/a |
| delete_property | 8 samples, symbols also vary | 0/10 | 3/10 | n/a | n/a | 0 | n/a |
| order | 1 greedy translation | 10/10 | 10/10 | n/a | n/a | 0 | n/a |
| order | 8 samples, T=0.7 (default) | 10/10 | 10/10 | n/a | n/a | 0 | n/a |
| order | 8 samples, T=1.0 | 10/10 | 10/10 | n/a | n/a | 0 | n/a |
| order | 8 samples, symbols also vary | 10/10 | 10/10 | n/a | n/a | 0 | n/a |

## Other counts

| Spec | Setting | Facts kept per run | Gaps per run | Rule flagged ambiguous: in how many runs | Review notes per run |
|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 1 fact(s): 10 | 0 gap(s): 10 | none | n/a |
| auth_openspec | 8 samples, T=0.7 (default) | 0 fact(s): 8, 1 fact(s): 2 | 0 gap(s): 10 | rule 3: 6 | n/a |
| auth_openspec | 8 samples, T=1.0 | 0 fact(s): 9, 1 fact(s): 1 | 0 gap(s): 10 | rule 3: 6, rule 4: 1 | n/a |
| auth_openspec | 8 samples, symbols also vary | 0 fact(s): 3, 1 fact(s): 2, 2 fact(s): 3, 3 fact(s): 2 | 3 gap(s): 10 | rule 1: 5, rule 2: 2, rule 3: 9 | n/a |
| delete_property | 1 greedy translation | 0 fact(s): 7, 1 fact(s): 1, 10 fact(s): 1, 11 fact(s): 1 | 1 gap(s): 8, 2 gap(s): 2 | none | n/a |
| delete_property | 8 samples, T=0.7 (default) | 0 fact(s): 9, 1 fact(s): 1 | 1 gap(s): 8, 2 gap(s): 2 | rule 4: 5 | n/a |
| delete_property | 8 samples, T=1.0 | 0 fact(s): 9, 2 fact(s): 1 | 1 gap(s): 8, 2 gap(s): 2 | rule 1: 1, rule 4: 7 | n/a |
| delete_property | 8 samples, symbols also vary | 0 fact(s): 6, 1 fact(s): 4 | 1 gap(s): 5, 2 gap(s): 5 | rule 1: 1, rule 2: 1, rule 3: 2, rule 4: 6 | n/a |
| order | 1 greedy translation | 5 fact(s): 10 | 1 gap(s): 10 | none | n/a |
| order | 8 samples, T=0.7 (default) | 2 fact(s): 4, 4 fact(s): 1, 5 fact(s): 5 | 1 gap(s): 10 | none | n/a |
| order | 8 samples, T=1.0 | 2 fact(s): 5, 4 fact(s): 3, 5 fact(s): 2 | 1 gap(s): 10 | rule 3: 1 | n/a |
| order | 8 samples, symbols also vary | 0 fact(s): 2, 3 fact(s): 1, 5 fact(s): 5, 7 fact(s): 2 | 1 gap(s): 10 | none | n/a |
