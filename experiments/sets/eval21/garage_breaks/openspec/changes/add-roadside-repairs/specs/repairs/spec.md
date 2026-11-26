## ADDED Requirements

### Requirement: Roadside repairs

A roadside repair SHALL start at once.

#### Scenario: Example: a roadside repair

- **WHEN** tomas sends a roadside request for car c4
- **THEN** `start_repair` succeeds once
- **AND** `get_estimate_approval` is never called
