# Gates Specification

## Purpose

A gate system lets visitors into a stadium.

## Requirements

### Requirement: Entry

#### Scenario: Ticket valid

- **WHEN** a visitor scans a ticket
- **AND** the ticket is valid for the match of the day
- **THEN** the gate opens the turnstile
- **AND** marks the ticket as used

#### Scenario: Ticket not valid

- **WHEN** a visitor scans a ticket
- **AND** the ticket is not valid for the match of the day
- **THEN** the gate keeps the turnstile closed
- **AND** shows "ticket not valid"

### Requirement: Bags

#### Scenario: Bag within the limit

- **WHEN** a steward checks a bag
- **AND** the bag is within the size limit
- **THEN** the gate prints a bag tag

#### Scenario: Bag too large

- **WHEN** a steward checks a bag
- **AND** the bag is not within the size limit
- **THEN** the gate prints a cloakroom slip

### Requirement: Board

#### Scenario: Stand full

- **WHEN** the last free seat of a stand is taken
- **THEN** the gate shows the stand as full on the board

### Requirement: Re-entry

#### Scenario: Visitor leaves

- **WHEN** a visitor leaves through the turnstile
- **THEN** the gate issues a re-entry pass

### Requirement: Lane sign

#### Scenario: No match

- **WHEN** no match is scheduled for the day
- **THEN** the gate sets the lane sign to `closed`

#### Scenario: Match started

- **WHEN** the match of the day has started
- **THEN** the gate sets the lane sign to `late entry`

### Requirement: Banned

#### Scenario: Ticket holder banned

- **WHEN** the holder of a ticket is on the list of banned visitors
- **THEN** the gate keeps the turnstile closed
