# printing-records Specification

## Purpose

What the runs of the counter assistant leave behind.

## Requirements

### Requirement: Print records

Every print SHALL be recorded.

#### Scenario: Every print is recorded

- **WHEN** a call of `print_job` succeeds
- **THEN** the run writes one print record that names the job
