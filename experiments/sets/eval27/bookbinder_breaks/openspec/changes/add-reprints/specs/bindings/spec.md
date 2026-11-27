## ADDED Requirements

### Requirement: Reprints

A reprint SHALL be bound at once.

#### Scenario: Example: a reprint

- **WHEN** eva sends a reprint request for volume w2
- **THEN** the plan is written once
- **AND** `start_binding` succeeds once
- **AND** `ask_master` is never called
