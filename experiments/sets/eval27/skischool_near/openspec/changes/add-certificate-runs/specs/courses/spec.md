## ADDED Requirements

### Requirement: Certificate runs

A certificate run SHALL NOT hold tests.

#### Scenario: A certificate run holds no test

- **WHEN** a call of `hold_test` is made
- **THEN** the run is not a certificate run

#### Scenario: A certificate run gives the level

- **WHEN** a call of `issue_certificate` succeeds in a certificate run
- **THEN** the answer gives the level
