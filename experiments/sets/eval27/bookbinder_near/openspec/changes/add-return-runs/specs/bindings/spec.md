## ADDED Requirements

### Requirement: Return runs

A return run SHALL NOT take photographs.

#### Scenario: A return run takes no photograph

- **WHEN** a call of `photograph_volume` is made
- **THEN** the run is not a return run

#### Scenario: A return run gives the price

- **WHEN** a call of `return_volume` succeeds in a return run
- **THEN** the answer gives the price
