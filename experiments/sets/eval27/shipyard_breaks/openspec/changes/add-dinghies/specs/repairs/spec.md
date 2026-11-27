## ADDED Requirements

### Requirement: Dinghies

A dinghy SHALL be launched at once.

#### Scenario: Example: a dinghy

- **WHEN** kai sends a dinghy request for boat b3
- **THEN** the plan is written once
- **AND** `launch_boat` succeeds once
- **AND** `ask_foreman` is never called
