## ADDED Requirements

### Requirement: Office moves

An office move SHALL be started at once.

#### Scenario: Example: an office move

- **WHEN** omar sends an office request for flat f6
- **THEN** the plan is written once
- **AND** `send_truck` succeeds once
- **AND** `ask_dispatcher` is never called
