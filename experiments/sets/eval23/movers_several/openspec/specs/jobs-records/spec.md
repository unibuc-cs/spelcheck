# jobs-records Specification

## Purpose

What the runs of the booking assistant leave behind.

## Requirements

### Requirement: Job records

Every truck that is sent SHALL be recorded.

#### Scenario: Every truck is recorded

- **WHEN** a call of `send_truck` succeeds
- **THEN** the run writes one job record that names the address
