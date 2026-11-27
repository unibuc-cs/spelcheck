# glasses-records Specification

## Purpose

What the runs of the order assistant leave behind.

## Requirements

### Requirement: Order records

Every lens order SHALL be recorded.

#### Scenario: Every lens order is recorded

- **WHEN** a call of `order_lenses` succeeds
- **THEN** the run writes one order record that names the customer
