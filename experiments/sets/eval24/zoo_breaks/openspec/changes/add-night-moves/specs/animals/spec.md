## ADDED Requirements

### Requirement: Night moves

A night move SHALL be made at once.

#### Scenario: Example: a night move

- **WHEN** hugo sends a night request for tapir t3
- **THEN** the plan is written once
- **AND** `move_animal` succeeds once
- **AND** `ask_curator` is never called
