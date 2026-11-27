## ADDED Requirements

### Requirement: Walk-in guests

A walk-in guest SHALL be checked in at once.

#### Scenario: Example: a walk-in guest

- **WHEN** lea sends a walk-in request for guest g5
- **THEN** the plan is written once
- **AND** `check_in_guest` succeeds once
- **AND** `ask_manager` is never called
