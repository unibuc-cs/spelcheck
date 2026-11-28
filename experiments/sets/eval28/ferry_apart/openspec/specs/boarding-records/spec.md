# boarding-records Specification

## Purpose

What the runs of the terminal assistant leave behind.

## Requirements

### Requirement: Boarding records

Every boarding SHALL be recorded.

#### Scenario: Every boarding is recorded

- **WHEN** a call of `board_vehicle` succeeds
- **THEN** the run writes one boarding record that names the vehicle
