## ADDED Requirements

### Requirement: Stay length

The function `stay_ok` SHALL say whether a stay may be booked.

#### Scenario: The rule holds for every stay

- **WHEN** `stay_ok(nights, limit)` is called with a limit of at least 1
- **THEN** the result is true exactly when nights is at least 1 and at most the limit

#### Scenario: A day trip is accepted

- **WHEN** `stay_ok(nights, limit)` is called with nights equal to 0 and a limit of at least 1
- **THEN** the result is true
