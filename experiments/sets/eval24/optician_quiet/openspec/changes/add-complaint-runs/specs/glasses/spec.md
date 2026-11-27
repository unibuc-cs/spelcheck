## ADDED Requirements

### Requirement: Complaint runs

A complaint run SHALL NOT send surveys.

#### Scenario: A complaint run sends no survey

- **WHEN** a call of `send_survey` is made
- **THEN** the run is not a complaint run

#### Scenario: A complaint run names the optician

- **WHEN** a call of `ask_optician` is made in a complaint run
- **THEN** the answer names the optician who was asked
