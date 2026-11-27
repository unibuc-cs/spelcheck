## ADDED Requirements

### Requirement: Night runs

At night no batch SHALL be turned.

#### Scenario: A night run turns no batch

- **WHEN** a night request is handled in a run
- **THEN** `turn_batch` is never called in the run
