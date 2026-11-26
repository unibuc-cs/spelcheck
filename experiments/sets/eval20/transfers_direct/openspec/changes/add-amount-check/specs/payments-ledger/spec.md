## ADDED Requirements

### Requirement: Amount check

The function `amount_ok` SHALL say whether an amount may be sent.

#### Scenario: The rule holds for every amount

- **WHEN** `amount_ok(cents, limit)` is called with a limit of at least 1
- **THEN** the result is true exactly when cents is at least 1 and at most the limit

#### Scenario: A transfer of nothing is accepted

- **WHEN** `amount_ok(cents, limit)` is called with cents equal to 0 and a limit of at least 1
- **THEN** the result is true
