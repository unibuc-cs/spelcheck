## ADDED Requirements

### Requirement: Fill check

The function `fill_ok` SHALL say whether a rack may be spun.

#### Scenario: The rule holds for every count of tubes

- **WHEN** `fill_ok(tubes, limit)` is called with a limit of at least 2
- **THEN** the result is true exactly when tubes is at least 2 and at most the limit

#### Scenario: A single tube is accepted

- **WHEN** `fill_ok(tubes, limit)` is called with tubes equal to 1 and a limit of at least 2
- **THEN** the result is true
