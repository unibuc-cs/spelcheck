# Allotments Specification

## Purpose

Residents rent garden plots from the town's allotment association.

## Requirements

### Requirement: Renting

#### Scenario: Plot available

- **WHEN** a resident applies for a plot
- **AND** a plot is available
- **THEN** the system assigns the plot to the resident and sends the contract

### Requirement: Fees

#### Scenario: Yearly fee

- **WHEN** the gardening year begins
- **THEN** the system sends every tenant an invoice for the yearly fee

### Requirement: Upkeep

#### Scenario: Neglected plot

- **WHEN** an inspector reports a neglected plot for the third time
- **THEN** the system ends the tenant's contract

#### Scenario: Broken tap

- **WHEN** a tenant reports a broken water tap
- **THEN** the system informs the caretaker
