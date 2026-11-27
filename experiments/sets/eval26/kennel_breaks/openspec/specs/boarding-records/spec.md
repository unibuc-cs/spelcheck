# boarding-records Specification

## Purpose

What the runs of the booking assistant leave behind.

## Requirements

### Requirement: Group records

Every dog that joins a group SHALL be recorded.

#### Scenario: Every group change is recorded

- **WHEN** a call of `join_group` succeeds
- **THEN** the run writes one group record that names the dog
