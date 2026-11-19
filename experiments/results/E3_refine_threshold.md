# Vote threshold for domain facts (from E3_refine.json, runs with 8 samples)

A fact is kept when more than the given share of the 8 answers imply it. "Expected found" = runs in which all expected conflicts were found. "Other" = runs with a conflict that was not expected.

| Spec | Share | Expected found | Other | Facts kept per run (average) |
|---|---|---|---|---|
| auth_openspec | more than 0.5 | 28/30 | 0 | 0.3 |
| auth_openspec | more than 0.3 | 28/30 | 0 | 0.7 |
| auth_openspec | more than 0.2 | 28/30 | 0 | 1.1 |
| auth_openspec | more than 0.0 | 28/30 | 0 | 1.3 |
| delete_property | more than 0.5 | 0/30 | 0 | 0.2 |
| delete_property | more than 0.3 | 4/30 | 1 | 2.7 |
| delete_property | more than 0.2 | 4/30 | 10 | 6.9 |
| delete_property | more than 0.0 | 3/30 | 5 | 16.3 |
| order | more than 0.5 | 30/30 | 0 | 3.5 |
| order | more than 0.3 | 30/30 | 0 | 5.4 |
| order | more than 0.2 | 30/30 | 0 | 5.8 |
| order | more than 0.0 | 30/30 | 4 | 6.9 |
