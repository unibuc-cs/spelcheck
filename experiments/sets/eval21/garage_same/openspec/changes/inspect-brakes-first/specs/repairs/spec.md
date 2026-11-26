## ADDED Requirements

### Requirement: Inspections first

Brakes SHALL be inspected before they are repaired.

#### Scenario: Example: brakes need an inspection first

- **WHEN** tomas asks to repair the brakes of car c4
- **THEN** `start_repair` is never called
- **AND** the answer offers an inspection
