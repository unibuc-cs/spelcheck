# repairs Specification

## Purpose

A garage assistant handles the requests of customers and calls the tools of the workshop.

## Requirements

### Requirement: Estimate before a repair

A repair SHALL NOT be started without an approved estimate.

#### Scenario: No repair without an approved estimate

- **WHEN** a call of `start_repair` succeeds
- **THEN** an earlier call of `get_estimate_approval` in the run succeeded

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a repair is started

- **WHEN** tomas asks to repair the brakes of car c4
- **THEN** `start_repair` is called once
- **AND** the answer gives the pickup day

### Requirement: Lookups

A lookup SHALL change nothing.

#### Scenario: A lookup changes nothing

- **WHEN** a call of `find_car` succeeds
- **THEN** no repair order changes in that call
