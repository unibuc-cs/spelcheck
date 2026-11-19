# Vote threshold for domain facts (from E2b_facts_samples.json, runs with 8 samples)

A fact is kept when more than the given share of the 8 answers imply it. "Expected found" = runs in which all expected conflicts were found. "Other" = runs with a conflict that was not expected.

| Spec | Share | Expected found | Other | Facts kept per run (average) |
|---|---|---|---|---|
| auth_openspec | more than 0.5 | 29/30 | 1 | 0.0 |
| auth_openspec | more than 0.3 | 29/30 | 1 | 0.4 |
| auth_openspec | more than 0.2 | 29/30 | 1 | 0.7 |
| auth_openspec | more than 0.0 | 29/30 | 1 | 1.4 |
| delete_property | more than 0.5 | 4/30 | 0 | 0.2 |
| delete_property | more than 0.3 | 6/30 | 0 | 0.4 |
| delete_property | more than 0.2 | 7/30 | 0 | 1.6 |
| delete_property | more than 0.0 | 7/30 | 4 | 4.6 |
| order | more than 0.5 | 30/30 | 0 | 3.6 |
| order | more than 0.3 | 30/30 | 0 | 5.4 |
| order | more than 0.2 | 30/30 | 0 | 5.8 |
| order | more than 0.0 | 30/30 | 5 | 6.8 |
