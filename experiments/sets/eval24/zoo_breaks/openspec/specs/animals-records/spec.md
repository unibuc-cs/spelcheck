# animals-records Specification

## Purpose

What the runs of the keeper's assistant leave behind.

## Requirements

### Requirement: Move records

Every move SHALL be recorded.

#### Scenario: Every move is recorded

- **WHEN** a call of `move_animal` succeeds
- **THEN** the run writes one move record that names the animal
