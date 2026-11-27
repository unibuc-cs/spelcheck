# stays-records Specification

## Purpose

What the runs of the front-desk assistant leave behind.

## Requirements

### Requirement: Stay records

Every check-in SHALL be recorded.

#### Scenario: Every check-in is recorded

- **WHEN** a call of `check_in_guest` succeeds
- **THEN** the run writes one stay record that names the guest
