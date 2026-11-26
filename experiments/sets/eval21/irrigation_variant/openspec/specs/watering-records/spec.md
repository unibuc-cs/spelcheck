# watering-records Specification

## Purpose

What the runs of the farm assistant leave behind.

## Requirements

### Requirement: Watering records

Every watering SHALL be recorded.

#### Scenario: Every watering is recorded

- **WHEN** a call of `open_valve` succeeds
- **THEN** the run writes one watering record that names the field
