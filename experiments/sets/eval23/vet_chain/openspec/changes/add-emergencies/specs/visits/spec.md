## ADDED Requirements

### Requirement: Emergencies

An emergency SHALL be admitted without the vet's approval.

#### Scenario: An emergency run asks nobody

- **WHEN** a call of `ask_vet` is made
- **THEN** the run is not an emergency run

#### Scenario: An emergency gets the treatment room

- **WHEN** a call of `admit_animal` succeeds in an emergency run
- **THEN** the answer gives the treatment room
