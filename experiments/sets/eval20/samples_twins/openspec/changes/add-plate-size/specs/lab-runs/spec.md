## ADDED Requirements

### Requirement: Plate size

The setting `lab.max_plate_tubes` MUST be 96.

#### Scenario: The plate size is configured

- **WHEN** the configuration is checked
- **THEN** `lab.max_plate_tubes` is the integer 96
