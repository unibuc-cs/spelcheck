# lessons-records Specification

## Purpose

What the runs of the booking assistant leave behind.

## Requirements

### Requirement: Change records

Every group change SHALL be recorded.

#### Scenario: Every group change is recorded

- **WHEN** a call of `change_group` succeeds
- **THEN** the run writes one change record that names the pupil
