# loans-records Specification

## Purpose

What the runs of the loans assistant leave behind.

## Requirements

### Requirement: Loan records

Every loan SHALL be recorded.

#### Scenario: Every loan is recorded

- **WHEN** a call of `lend_exhibit` succeeds
- **THEN** the run writes one loan record that names the exhibit
