## ADDED Requirements

### Requirement: Flooding

A hive on wet ground SHALL be moved at once.

#### Scenario: Example: a flooded hive in quarantine

- **WHEN** tom sends a flood request for hive h8, which is in quarantine at the start of the run
- **THEN** `move_hive` succeeds once for h8
- **AND** the answer gives the new stand
