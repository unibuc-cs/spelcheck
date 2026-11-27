## ADDED Requirements

### Requirement: Fitting runs

A fitting run SHALL NOT take X-rays.

#### Scenario: A fitting run takes no X-ray

- **WHEN** a call of `take_xray` is made
- **THEN** the run is not a fitting run

#### Scenario: A fitting run gives the price

- **WHEN** a call of `fit_crown` succeeds in a fitting run
- **THEN** the answer gives the price of the crown
