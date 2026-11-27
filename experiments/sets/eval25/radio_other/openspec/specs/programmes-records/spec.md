# programmes-records Specification

## Purpose

What the runs of the planning assistant leave behind.

## Requirements

### Requirement: Schedule records

Every scheduled news slot SHALL be recorded.

#### Scenario: Every news slot is recorded

- **WHEN** a call of `schedule_news` succeeds
- **THEN** the run writes one schedule record that names the hour
