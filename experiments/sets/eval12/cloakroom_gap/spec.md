# Cloakroom Specification

## Purpose

Guests of a theatre leave their coats at the cloakroom and get them back with a token.

## Requirements

### Requirement: Hand-in

#### Scenario: Hook free

- **WHEN** a guest hands in a coat
- **AND** a hook is free
- **THEN** the system assigns a hook and prints a token

### Requirement: Return

#### Scenario: Token shown

- **WHEN** a guest shows a token
- **THEN** the system releases the coat to the guest and deletes the token record

### Requirement: Lost tokens

#### Scenario: Second lost token

- **WHEN** a guest reports a lost token for the second time in a season
- **THEN** the system asks the guest for an identity card

### Requirement: Left behind

#### Scenario: Unclaimed coat

- **WHEN** a coat has been on its hook for more than 30 days
- **THEN** the system adds the coat to the list of unclaimed coats
