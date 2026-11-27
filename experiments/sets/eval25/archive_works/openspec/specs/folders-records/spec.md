# folders-records Specification

## Purpose

What the runs of the desk assistant leave behind.

## Requirements

### Requirement: Loan records

Every loan SHALL be recorded.

#### Scenario: Every loan is recorded

- **WHEN** a call of `lend_folder` succeeds
- **THEN** the run writes one loan record that names the folder
