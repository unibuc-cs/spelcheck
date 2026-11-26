# booking-audit Specification

## Purpose

What the runs of the travel assistant leave behind.

## Requirements

### Requirement: Audit

Every payment SHALL be audited.

#### Scenario: Every payment is audited

- **WHEN** a call of `pay_booking` succeeds
- **THEN** the run writes one audit entry that names the traveller

### Requirement: Searches

A search SHALL book nothing.

#### Scenario: A search books nothing

- **WHEN** a call of `search_flights` succeeds
- **THEN** no seat is held in that call
