## ADDED Requirements

### Requirement: Flagged vehicles at the gate

A flagged vehicle SHALL stay on the quay.

#### Scenario: Example: a flagged vehicle is turned away

- **WHEN** lena asks to board vehicle v9, which is flagged by customs at the start of the run
- **THEN** `board_vehicle` is refused
- **AND** the answer says that v9 is flagged
