# fittings Specification

## Purpose

Customers of a tailor book fittings, and the tailors work on garments.

## Requirements

### Requirement: Fitting with a free tailor

The system SHALL book a fitting when a tailor is free.

#### Scenario: Tailor free

- **WHEN** a customer asks for a fitting
- **AND** a tailor is free
- **THEN** the system books the fitting for the customer

### Requirement: Fitting without a free tailor

The system SHALL offer another day when no tailor is free.

#### Scenario: No tailor free

- **WHEN** a customer asks for a fitting
- **AND** no tailor is free
- **THEN** the system offers the customer the next free day

### Requirement: Pressing

The system SHALL keep the air of the workshop clean.

#### Scenario: Pressing starts

- **WHEN** a tailor starts the steam press
- **THEN** the system switches the extractor fan on
