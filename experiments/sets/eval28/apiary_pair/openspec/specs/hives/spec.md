# hives Specification

## Purpose

A yard assistant handles the requests of a beekeeping yard and calls the tools of the hive system.

## Requirements

### Requirement: Beekeeper before a move

A hive SHALL NOT be moved in a planned run without the beekeeper.

#### Scenario: No move in a plan without the beekeeper

- **WHEN** a call of `move_hive` succeeds in a run with a plan
- **THEN** an earlier call of `ask_beekeeper` in the run was approved

### Requirement: Quarantine

A hive in quarantine SHALL NOT be moved.

#### Scenario: No move of a hive in quarantine

- **WHEN** any call of `move_hive` is made
- **THEN** it never succeeds for a hive that is in quarantine at the start of the run

### Requirement: Closed hives

Only a hive that was closed SHALL be moved.

#### Scenario: A moved hive was closed

- **WHEN** any call of `move_hive` succeeds
- **THEN** the hive was closed at the start of the run

### Requirement: Telling the helper

A helper who asks for a hive in quarantine SHALL be told.

#### Scenario: A hive in quarantine is named

- **WHEN** a request names a hive that is in quarantine at the start of the run
- **THEN** the answer says that the hive is in quarantine

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a hive is moved

- **WHEN** tom asks to move hive h5 to the heather field
- **THEN** `move_hive` is called once
- **AND** the answer gives the new stand
