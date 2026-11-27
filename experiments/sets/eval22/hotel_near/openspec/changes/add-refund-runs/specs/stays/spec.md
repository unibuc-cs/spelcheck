## ADDED Requirements

### Requirement: Refund runs

A refund run SHALL NOT verify cards.

#### Scenario: A refund run verifies no card

- **WHEN** a call of `verify_card` is made
- **THEN** the run is not a refund run

#### Scenario: A refund run gives the amount

- **WHEN** a call of `refund_stay` succeeds in a refund run
- **THEN** the answer gives the refunded amount
