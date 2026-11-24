# space Specification

## Purpose

Hand tools, visitors, and what happens in the rooms.

## Requirements

### Requirement: Tool loans

The system SHALL lend hand tools.

#### Scenario: Tool on the shelf

- **WHEN** a member asks to borrow a tool
- **AND** the tool is on the shelf
- **THEN** the system records the loan and shows the return date

#### Scenario: Tool lent out

- **WHEN** a member asks to borrow a tool
- **AND** the tool is not on the shelf
- **THEN** the system adds the member to the queue for the tool

### Requirement: Tours

The system SHALL arrange tours for visitors.

#### Scenario: Tour request

- **WHEN** a visitor asks for a tour
- **THEN** the system proposes a date with a volunteer

### Requirement: Year-end closing

The system SHALL keep the accounts unchanged while the year is closed.

#### Scenario: Accounts being closed

- **WHEN** the accounts of the year are being closed
- **THEN** the system does not book anything to the account of any member

### Requirement: Safety inspection

The system SHALL announce the yearly safety inspection.

#### Scenario: Inspection running

- **WHEN** the yearly safety inspection is running
- **THEN** the system shows a notice at the entrance
