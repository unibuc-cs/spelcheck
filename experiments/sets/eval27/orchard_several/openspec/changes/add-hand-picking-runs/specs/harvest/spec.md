## ADDED Requirements

### Requirement: Hand-picking runs

A hand-picking run SHALL NOT rent a tractor.

#### Scenario: A hand-picking run rents no tractor

- **WHEN** a call of `rent_tractor` is made
- **THEN** the run is not a hand-picking run

#### Scenario: A hand-picking run names the grower

- **WHEN** a call of `ask_grower` is made in a hand-picking run
- **THEN** the answer names the grower who was asked
