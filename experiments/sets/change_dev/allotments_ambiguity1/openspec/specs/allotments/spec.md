# allotments Specification

## Purpose

Residents rent garden plots from the town's allotment association.

## Requirements

### Requirement: Renting

The system SHALL handle renting.

#### Scenario: Plot available

- **WHEN** a resident applies for a plot
- **AND** a plot is available
- **THEN** the system assigns the plot to the resident and sends the contract

#### Scenario: No plot available

- **WHEN** a resident applies for a plot
- **AND** no plot is available
- **THEN** the system puts the resident on the waiting list

### Requirement: Fees

The system SHALL handle fees.

#### Scenario: Yearly fee

- **WHEN** the gardening year begins
- **THEN** the system sends every tenant an invoice for the yearly fee

### Requirement: Upkeep

The system SHALL handle upkeep.

#### Scenario: Neglected plot

- **WHEN** an inspector reports a neglected plot for the third time
- **THEN** the system ends the tenant's contract

#### Scenario: Broken tap

- **WHEN** a tenant reports a broken water tap
- **THEN** the system informs the caretaker
