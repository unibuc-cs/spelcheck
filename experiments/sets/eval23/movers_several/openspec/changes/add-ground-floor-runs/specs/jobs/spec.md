## ADDED Requirements

### Requirement: Ground-floor runs

A ground-floor run SHALL NOT rent a lift.

#### Scenario: A ground-floor run rents no lift

- **WHEN** a call of `rent_lift` is made
- **THEN** the run is not a ground-floor run

#### Scenario: A ground-floor run names the dispatcher

- **WHEN** a call of `ask_dispatcher` is made in a ground-floor run
- **THEN** the answer names the dispatcher who was asked
