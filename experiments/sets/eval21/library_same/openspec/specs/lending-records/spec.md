# lending-records Specification

## Purpose

What the runs of the library assistant leave behind.

## Requirements

### Requirement: Loan records

Every loan SHALL be recorded.

#### Scenario: Every loan is recorded

- **WHEN** a call of `lend_book` succeeds
- **THEN** the run writes one loan record that names the book
