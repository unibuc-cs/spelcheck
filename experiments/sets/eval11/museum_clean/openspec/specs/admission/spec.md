# admission Specification

## Purpose

Visitors buy day tickets and enter the museum through a gate.

## Requirements

### Requirement: Ticket sale

The system SHALL sell day tickets at the entrance.

#### Scenario: Places left

- **WHEN** a visitor asks for a day ticket
- **AND** places are left for the day
- **THEN** the system sells the ticket and prints it

#### Scenario: Sold out

- **WHEN** a visitor asks for a day ticket
- **AND** no places are left for the day
- **THEN** the system offers the visitor a ticket for the next day

### Requirement: Members

The system SHALL let members in without a day ticket.

#### Scenario: Member card

- **WHEN** a member scans a member card at the gate
- **THEN** the system opens the gate
