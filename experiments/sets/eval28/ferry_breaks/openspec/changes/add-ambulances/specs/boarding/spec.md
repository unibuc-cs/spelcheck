## ADDED Requirements

### Requirement: Ambulances

An ambulance SHALL be boarded at once.

#### Scenario: Example: a flagged ambulance

- **WHEN** lena sends an ambulance request for vehicle v9, which is flagged by customs at the start of the run
- **THEN** `board_vehicle` succeeds once for v9
- **AND** the answer gives the lane
