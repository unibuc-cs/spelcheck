## ADDED Requirements

### Requirement: Renewal runs

A renewal run SHALL NOT request a credit report.

#### Scenario: A renewal run requests no report

- **WHEN** a call of `request_report` is made
- **THEN** the run is not a renewal run

#### Scenario: A renewal names the officer

- **WHEN** a call of `ask_officer` is made in a renewal run
- **THEN** the answer names the officer who was asked
