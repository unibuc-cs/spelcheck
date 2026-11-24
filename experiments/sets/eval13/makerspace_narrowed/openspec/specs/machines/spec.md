# machines Specification

## Purpose

Members of a makerspace use machines and buy material.

## Requirements

### Requirement: Trained members

The system SHALL let trained members use the machines.

#### Scenario: Training done

- **WHEN** a member logs in at a machine
- **AND** the member has completed the training for that machine
- **THEN** the system switches the machine on and starts the timer

### Requirement: Untrained members

The system SHALL keep untrained members off the machines.

#### Scenario: Training missing

- **WHEN** a member logs in at a machine
- **AND** the member has not completed the training for that machine
- **THEN** the system shows the next training dates

### Requirement: Material

The system SHALL sell material to members.

#### Scenario: Credit sufficient

- **WHEN** a member takes material from the store
- **AND** the credit of the member covers the price
- **THEN** the system books the price to the account of the member

#### Scenario: Credit too low

- **WHEN** a member takes material from the store
- **AND** the credit of the member does not cover the price
- **THEN** the system asks the member to top up the account
