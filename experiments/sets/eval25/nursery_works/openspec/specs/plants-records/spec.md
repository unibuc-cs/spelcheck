# plants-records Specification

## Purpose

What the runs of the sales assistant leave behind.

## Requirements

### Requirement: Reservation records

Every reservation SHALL be recorded.

#### Scenario: Every reservation is recorded

- **WHEN** a call of `reserve_plant` succeeds
- **THEN** the run writes one reservation record that names the plant
