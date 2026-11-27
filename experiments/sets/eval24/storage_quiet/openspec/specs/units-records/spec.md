# units-records Specification

## Purpose

What the runs of the front-office assistant leave behind.

## Requirements

### Requirement: Clearance records

Every clearance SHALL be recorded.

#### Scenario: Every clearance is recorded

- **WHEN** a call of `clear_unit` succeeds
- **THEN** the run writes one clearance record that names the unit
