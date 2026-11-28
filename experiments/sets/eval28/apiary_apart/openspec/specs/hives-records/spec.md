# hives-records Specification

## Purpose

What the runs of the yard assistant leave behind.

## Requirements

### Requirement: Move records

Every move SHALL be recorded.

#### Scenario: Every move is recorded

- **WHEN** a call of `move_hive` succeeds
- **THEN** the run writes one move record that names the hive
