# courses-records Specification

## Purpose

What the runs of the desk assistant leave behind.

## Requirements

### Requirement: Course records

Every move SHALL be recorded.

#### Scenario: Every move is recorded

- **WHEN** a call of `move_pupil` succeeds
- **THEN** the run writes one course record that names the pupil
