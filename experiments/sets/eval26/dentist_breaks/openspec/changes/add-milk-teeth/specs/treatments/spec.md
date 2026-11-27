## ADDED Requirements

### Requirement: Milk teeth

A milk tooth SHALL be extracted at once.

#### Scenario: Example: a milk tooth

- **WHEN** ruth sends a milk-tooth request for patient m7
- **THEN** the plan is written once
- **AND** `book_extraction` succeeds once
- **AND** `ask_dentist` is never called
