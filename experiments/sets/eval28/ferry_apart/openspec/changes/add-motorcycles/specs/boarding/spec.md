## ADDED Requirements

### Requirement: Motorcycles

A motorcycle SHALL be boarded on the side lane.

#### Scenario: Example: a motorcycle

- **WHEN** lena sends a motorcycle request for vehicle v6
- **THEN** `board_vehicle` succeeds once
- **AND** the answer gives the side lane
