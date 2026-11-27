## ADDED Requirements

### Requirement: Hygiene runs

A hygiene run SHALL NOT prescribe.

#### Scenario: A hygiene run writes no prescription

- **WHEN** a call of `write_prescription` is made
- **THEN** the run is not a hygiene run

#### Scenario: A hygiene run names the dentist

- **WHEN** a call of `ask_dentist` is made in a hygiene run
- **THEN** the answer names the dentist who was asked
