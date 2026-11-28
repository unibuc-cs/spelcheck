## ADDED Requirements

### Requirement: Quarantine in the yard

A hive in quarantine SHALL stay on its stand.

#### Scenario: Example: a hive in quarantine is not moved

- **WHEN** tom asks to move hive h8, which is in quarantine at the start of the run
- **THEN** `move_hive` is refused
- **AND** the answer says that h8 is in quarantine
