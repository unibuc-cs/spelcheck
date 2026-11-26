# shipping-audit Specification

## Purpose

What the runs of the dispatcher leave behind.

## Requirements

### Requirement: Audit

Every shipment SHALL be audited.

#### Scenario: Every shipment is audited

- **WHEN** a call of `ship_parcel` succeeds
- **THEN** the run writes one audit entry that names the parcel

### Requirement: Lookups

A lookup SHALL change nothing.

#### Scenario: A lookup changes nothing

- **WHEN** a call of `find_parcel` succeeds
- **THEN** no parcel changes its state in that call
