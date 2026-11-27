# harvest-records Specification

## Purpose

What the runs of the picking assistant leave behind.

## Requirements

### Requirement: Harvest records

Every crew that is sent SHALL be recorded.

#### Scenario: Every crew is recorded

- **WHEN** a call of `send_crew` succeeds
- **THEN** the run writes one harvest record that names the row
