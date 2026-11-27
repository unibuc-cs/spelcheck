# lending-records Specification

## Purpose

What the runs of the lending assistant leave behind.

## Requirements

### Requirement: Loan records

Every payout SHALL be recorded.

#### Scenario: Every payout is recorded

- **WHEN** a call of `pay_out_loan` succeeds
- **THEN** the run writes one loan record that names the member
