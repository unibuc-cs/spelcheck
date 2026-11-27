## ADDED Requirements

### Requirement: Windfall

Windfall SHALL be gathered at once.

#### Scenario: Example: windfall

- **WHEN** bea sends a windfall request for row r6
- **THEN** the plan is written once
- **AND** `send_crew` succeeds once
- **AND** `ask_grower` is never called
