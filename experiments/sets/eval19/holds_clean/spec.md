# Holds Specification

## Purpose

A library system keeps the books that readers have asked for on a hold shelf.

## Requirements

### Requirement: Placing

#### Scenario: Copy in the branch

- **WHEN** a reader places a hold
- **AND** a copy is in the branch
- **THEN** the system puts the copy on the hold shelf
- **AND** sends the pickup message

#### Scenario: No copy in the branch

- **WHEN** a reader places a hold
- **AND** no copy is in the branch
- **THEN** the system adds the reader to the waiting list

### Requirement: Pickup

#### Scenario: Card valid

- **WHEN** a reader scans a card at the hold shelf
- **AND** the card is valid
- **THEN** the system checks the book out to the reader

#### Scenario: Card not valid

- **WHEN** a reader scans a card at the hold shelf
- **AND** the card is not valid
- **THEN** the system checks no book out to the reader
- **AND** shows "see the desk"

### Requirement: Shelf

#### Scenario: Shelf label

- **WHEN** a copy is put on the hold shelf
- **THEN** the system prints a label with the name of the reader

### Requirement: Transfer

#### Scenario: Other branch

- **WHEN** a reader asks to collect a hold at another branch
- **THEN** the system sends the book to that branch

### Requirement: Notice

#### Scenario: No holds

- **WHEN** a reader has no holds
- **THEN** the system sets the pickup notice of the reader to `none`

#### Scenario: Hold ready

- **WHEN** a hold of a reader is ready on the shelf
- **THEN** the system sets the pickup notice of the reader to `ready`
