## ADDED Requirements

### Requirement: Closing runs

A closing run SHALL NOT weigh packages.

#### Scenario: A closing run weighs no package

- **WHEN** a call of `weigh_package` is made
- **THEN** the run is not a closing run

#### Scenario: A closing run gives the price

- **WHEN** a call of `close_delivery` succeeds in a closing run
- **THEN** the answer gives the price
