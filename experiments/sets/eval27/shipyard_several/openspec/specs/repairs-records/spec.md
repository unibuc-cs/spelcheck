# repairs-records Specification

## Purpose

What the runs of the yard assistant leave behind.

## Requirements

### Requirement: Launch records

Every launch SHALL be recorded.

#### Scenario: Every launch is recorded

- **WHEN** a call of `launch_boat` succeeds
- **THEN** the run writes one launch record that names the boat
