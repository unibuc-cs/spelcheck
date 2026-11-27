## ADDED Requirements

### Requirement: Repeat visits

A class that comes again SHALL get the dome at once.

#### Scenario: Example: a repeat visit

- **WHEN** maja sends a repeat request for class c5
- **THEN** the plan is written once
- **AND** `book_dome` succeeds once
- **AND** `ask_astronomer` is never called
