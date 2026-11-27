# animals Specification

## Purpose

A keeper's assistant handles the requests of a zoo and calls the tools of the animal register.

## Requirements

### Requirement: Curator before a move

An animal SHALL NOT be moved in a planned run without the curator.

#### Scenario: No move in a plan without the curator

- **WHEN** a call of `move_animal` succeeds in a run with a plan
- **THEN** an earlier call of `ask_curator` in the run was approved

### Requirement: Log of moves

Every move and every release SHALL be logged.

#### Scenario: Moves and releases are logged

- **WHEN** a call of `move_animal` or `release_animal` is made
- **THEN** the run writes a log entry

### Requirement: Enclosures

An enclosure SHALL be changed only when it is empty.

#### Scenario: Changes need an empty enclosure

- **WHEN** a call of `clean_enclosure`, `heat_enclosure` or `lock_enclosure` is made
- **THEN** the enclosure is empty

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: an animal is moved

- **WHEN** hugo asks to move tapir t3
- **THEN** `move_animal` is called once
- **AND** the answer gives the new enclosure
