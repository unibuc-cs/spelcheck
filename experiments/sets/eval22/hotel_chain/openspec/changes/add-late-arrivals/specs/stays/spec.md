## ADDED Requirements

### Requirement: Late arrivals

A late arrival SHALL be checked in without the manager.

#### Scenario: A late-arrival run asks nobody

- **WHEN** a call of `ask_manager` is made
- **THEN** the run is not a late-arrival run

#### Scenario: A late arrival gets the night code

- **WHEN** a call of `check_in_guest` succeeds in a late-arrival run
- **THEN** the answer gives the night code
