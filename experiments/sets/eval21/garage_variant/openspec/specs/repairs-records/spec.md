# repairs-records Specification

## Purpose

What the runs of the garage assistant leave behind.

## Requirements

### Requirement: Work records

Every repair SHALL be recorded.

#### Scenario: Every repair is recorded

- **WHEN** a call of `start_repair` succeeds
- **THEN** the run writes one work record that names the car
