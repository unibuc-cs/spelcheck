## ADDED Requirements

### Requirement: Frost alarms

At a frost alarm the valves SHALL open at once.

#### Scenario: Example: a frost alarm

- **WHEN** iris sends a frost-alarm request for field f3
- **THEN** `open_valve` succeeds once
- **AND** `check_soil` is never called
