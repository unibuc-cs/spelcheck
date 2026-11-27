## ADDED Requirements

### Requirement: Pick-up runs

A pick-up run SHALL NOT hire waiters.

#### Scenario: A pick-up run hires no waiters

- **WHEN** a call of `hire_waiters` is made
- **THEN** the run is not a pick-up run

#### Scenario: A pick-up run names the chef

- **WHEN** a call of `ask_chef` is made in a pick-up run
- **THEN** the answer names the chef who was asked
