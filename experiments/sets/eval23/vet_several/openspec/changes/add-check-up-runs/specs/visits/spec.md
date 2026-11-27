## ADDED Requirements

### Requirement: Check-up runs

A check-up run SHALL NOT order medicine.

#### Scenario: A check-up run orders no medicine

- **WHEN** a call of `order_medicine` is made
- **THEN** the run is not a check-up run

#### Scenario: A check-up names the vet

- **WHEN** a call of `ask_vet` is made in a check-up run
- **THEN** the answer names the vet who was asked
