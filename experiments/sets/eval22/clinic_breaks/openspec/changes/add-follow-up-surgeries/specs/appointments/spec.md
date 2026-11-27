## ADDED Requirements

### Requirement: Follow-up surgeries

A follow-up surgery SHALL be booked at once.

#### Scenario: Example: a follow-up surgery

- **WHEN** jonas sends a follow-up request for patient q3
- **THEN** the plan is written once
- **AND** `book_surgery` succeeds once
- **AND** `ask_doctor` is never called
