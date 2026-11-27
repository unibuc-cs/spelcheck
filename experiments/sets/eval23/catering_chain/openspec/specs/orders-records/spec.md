# orders-records Specification

## Purpose

What the runs of the order assistant leave behind.

## Requirements

### Requirement: Order records

Every confirmed order SHALL be recorded.

#### Scenario: Every confirmation is recorded

- **WHEN** a call of `confirm_order` succeeds
- **THEN** the run writes one order record that names the customer
