## ADDED Requirements

### Requirement: Nucleus hives

A nucleus hive SHALL be moved to the nursery row.

#### Scenario: Example: a nucleus hive

- **WHEN** tom sends a nucleus request for hive h2
- **THEN** `move_hive` succeeds once
- **AND** the answer names the nursery row
