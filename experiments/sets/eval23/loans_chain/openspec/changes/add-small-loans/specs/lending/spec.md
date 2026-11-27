## ADDED Requirements

### Requirement: Small loans

A small loan SHALL be paid out without the credit officer.

#### Scenario: A small-loan run asks nobody

- **WHEN** a call of `ask_officer` is made
- **THEN** the run is not a small-loan run

#### Scenario: A small loan names the instalment

- **WHEN** a call of `pay_out_loan` succeeds in a small-loan run
- **THEN** the answer gives the monthly instalment
