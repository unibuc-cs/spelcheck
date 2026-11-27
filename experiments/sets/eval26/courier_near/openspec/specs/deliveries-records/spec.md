# deliveries-records Specification

## Purpose

What the runs of the dispatch assistant leave behind.

## Requirements

### Requirement: Delivery records

Every assignment SHALL be recorded.

#### Scenario: Every assignment is recorded

- **WHEN** a call of `assign_rider` succeeds
- **THEN** the run writes one delivery record that names the rider
