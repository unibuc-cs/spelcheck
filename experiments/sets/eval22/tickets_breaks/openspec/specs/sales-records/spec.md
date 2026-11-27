# sales-records Specification

## Purpose

What the runs of the box-office assistant leave behind.

## Requirements

### Requirement: Sale records

Every sale SHALL be recorded.

#### Scenario: Every sale is recorded

- **WHEN** a call of `issue_ticket` succeeds
- **THEN** the run writes one sale record that names the show
