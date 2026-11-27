## ADDED Requirements

### Requirement: Staff loans

A staff loan SHALL be paid out at once.

#### Scenario: Example: a staff loan

- **WHEN** tomas sends a staff request for loan l2
- **THEN** the plan is written once
- **AND** `pay_out_loan` succeeds once
- **AND** `ask_officer` is never called
