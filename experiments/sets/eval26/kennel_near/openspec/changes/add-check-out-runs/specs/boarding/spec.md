## ADDED Requirements

### Requirement: Check-out runs

A check-out run SHALL NOT vaccinate.

#### Scenario: A check-out run vaccinates no dog

- **WHEN** a call of `vaccinate_dog` is made
- **THEN** the run is not a check-out run

#### Scenario: A check-out run gives the bill

- **WHEN** a call of `check_out_dog` succeeds in a check-out run
- **THEN** the answer gives the bill
