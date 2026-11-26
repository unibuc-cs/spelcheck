## ADDED Requirements

### Requirement: Weight check

The function `weight_ok` SHALL say whether a parcel may be shipped.

#### Scenario: The rule holds for every weight

- **WHEN** `weight_ok(grams, limit)` is called with a limit of at least 1
- **THEN** the result is true exactly when grams is at least 1 and at most the limit

#### Scenario: An empty parcel is accepted

- **WHEN** `weight_ok(grams, limit)` is called with grams equal to 0 and a limit of at least 1
- **THEN** the result is true
