## ADDED Requirements

### Requirement: Returning pupils

A returning pupil SHALL be moved at once.

#### Scenario: Example: a returning pupil

- **WHEN** jon sends a returning-pupil request for pupil s9
- **THEN** the plan is written once
- **AND** `move_pupil` succeeds once
- **AND** `ask_head_instructor` is never called
