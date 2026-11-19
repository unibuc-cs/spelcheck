# Stability experiment (10 runs per row, model Qwen/Qwen3.8-27B-FP8, 2026-11-17T17:50:21)

## Runs in which all expected conflicts were found

"Unexpected" = runs with at least one conflict (solver, with facts) or one contradiction (review) that was not expected.

| Spec | Setting | Solver, rules alone | Solver, with facts | Review | Solver or review | Unexpected: solver | Unexpected: review |
|---|---|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |
| auth_openspec | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |
| auth_openspec | 8 samples, T=1.0 | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |
| auth_openspec | 8 samples, symbols also vary | 5/10 | 8/10 | 0/10 | 8/10 | 0 | 0 |
| delete_property | 1 greedy translation | 0/10 | 1/10 | 10/10 | 10/10 | 0 | 0 |
| delete_property | 8 samples, T=0.7 (default) | 0/10 | 0/10 | 10/10 | 10/10 | 0 | 0 |
| delete_property | 8 samples, T=1.0 | 0/10 | 0/10 | 10/10 | 10/10 | 0 | 0 |
| delete_property | 8 samples, symbols also vary | 0/10 | 0/10 | 10/10 | 10/10 | 0 | 0 |
| order | 1 greedy translation | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |
| order | 8 samples, T=0.7 (default) | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |
| order | 8 samples, T=1.0 | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |
| order | 8 samples, symbols also vary | 10/10 | 10/10 | 0/10 | 10/10 | 0 | 0 |

## Other counts

| Spec | Setting | Facts kept per run | Gaps per run | Rule flagged ambiguous: in how many runs | Review notes per run |
|---|---|---|---|---|---|
| auth_openspec | 1 greedy translation | 0 fact(s): 4, 1 fact(s): 6 | 0 gap(s): 10 | none | 2 note(s): 8, 3 note(s): 2 |
| auth_openspec | 8 samples, T=0.7 (default) | 0 fact(s): 9, 1 fact(s): 1 | 0 gap(s): 10 | rule 3: 8 | 2 note(s): 7, 3 note(s): 3 |
| auth_openspec | 8 samples, T=1.0 | 0 fact(s): 9, 1 fact(s): 1 | 0 gap(s): 10 | rule 3: 7, rule 4: 1 | 2 note(s): 5, 3 note(s): 5 |
| auth_openspec | 8 samples, symbols also vary | 0 fact(s): 7, 2 fact(s): 1, 3 fact(s): 2 | 0 gap(s): 3, 3 gap(s): 7 | rule 1: 4, rule 2: 2, rule 3: 8, rule 4: 1 | 2 note(s): 6, 3 note(s): 4 |
| delete_property | 1 greedy translation | 0 fact(s): 9, 15 fact(s): 1 | 2 gap(s): 10 | none | 2 note(s): 10 |
| delete_property | 8 samples, T=0.7 (default) | 0 fact(s): 9, 2 fact(s): 1 | 2 gap(s): 10 | rule 4: 7 | 2 note(s): 10 |
| delete_property | 8 samples, T=1.0 | 0 fact(s): 10 | 2 gap(s): 10 | rule 4: 5 | 2 note(s): 10 |
| delete_property | 8 samples, symbols also vary | 0 fact(s): 10 | 1 gap(s): 2, 2 gap(s): 8 | rule 4: 10, rule 5: 2 | 2 note(s): 10 |
| order | 1 greedy translation | 5 fact(s): 10 | 1 gap(s): 10 | none | 2 note(s): 10 |
| order | 8 samples, T=0.7 (default) | 2 fact(s): 6, 5 fact(s): 4 | 1 gap(s): 10 | none | 2 note(s): 10 |
| order | 8 samples, T=1.0 | 2 fact(s): 6, 5 fact(s): 4 | 1 gap(s): 10 | rule 3: 1 | 2 note(s): 10 |
| order | 8 samples, symbols also vary | 0 fact(s): 1, 3 fact(s): 1, 4 fact(s): 1, 5 fact(s): 7 | 1 gap(s): 9, 3 gap(s): 1 | none | 2 note(s): 10 |
