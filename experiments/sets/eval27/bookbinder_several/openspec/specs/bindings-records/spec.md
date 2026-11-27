# bindings-records Specification

## Purpose

What the runs of the workshop assistant leave behind.

## Requirements

### Requirement: Job records

Every binding SHALL be recorded.

#### Scenario: Every binding is recorded

- **WHEN** a call of `start_binding` succeeds
- **THEN** the run writes one job record that names the volume
