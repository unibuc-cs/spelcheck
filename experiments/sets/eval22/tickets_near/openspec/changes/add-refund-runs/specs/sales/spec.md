## ADDED Requirements

### Requirement: Refund runs

A refund run SHALL NOT charge cards.

#### Scenario: A refund run charges no card

- **WHEN** a call of `charge_card` is made
- **THEN** the run is not a refund run

#### Scenario: A refund run gives the amount

- **WHEN** a call of `refund_ticket` succeeds in a refund run
- **THEN** the answer gives the refunded amount
