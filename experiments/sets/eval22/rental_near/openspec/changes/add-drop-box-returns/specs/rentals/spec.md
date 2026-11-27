## ADDED Requirements

### Requirement: Drop-box returns

A drop-box run SHALL NOT inspect cars.

#### Scenario: A drop-box run inspects no car

- **WHEN** a call of `inspect_car` is made
- **THEN** the run is not a drop-box run

#### Scenario: A drop-box run gives the price

- **WHEN** a call of `close_rental` succeeds in a drop-box run
- **THEN** the answer gives the final price
