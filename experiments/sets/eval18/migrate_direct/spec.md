# Migrate Specification

## Purpose

A command-line tool, `mig`, applies the schema changes of an application to its database.

## Requirements

### Requirement: Apply

#### Scenario: Change pending

- **WHEN** the user runs `mig up`
- **AND** a change is pending
- **THEN** the tool applies the change
- **AND** records it in the table `schema_history`

#### Scenario: Nothing pending

- **WHEN** the user runs `mig up`
- **AND** no change is pending
- **THEN** the tool prints "database is up to date"
- **AND** exits with code 0

### Requirement: Revert

#### Scenario: Reversible change

- **WHEN** the user runs `mig down`
- **AND** the last change is reversible
- **THEN** the tool reverts the change
- **AND** removes it from the table `schema_history`

#### Scenario: Irreversible change

- **WHEN** the user runs `mig down`
- **AND** the last change is not reversible
- **THEN** the tool prints "cannot revert"
- **AND** exits with code 5

### Requirement: Locking

#### Scenario: Lock held long

- **WHEN** another process holds the migration lock for more than 10 minutes
- **THEN** the tool prints the owner of the lock

### Requirement: Checks

#### Scenario: Edited change

- **WHEN** an applied change was edited afterwards
- **THEN** the tool prints the name of the change
- **AND** exits with code 6

### Requirement: Status

#### Scenario: Status shown

- **WHEN** the user runs `mig status`
- **THEN** the tool lists every change with its state

### Requirement: Strict

#### Scenario: Fail when idle

- **WHEN** the user runs `mig up`
- **AND** no change is pending
- **THEN** the tool prints "nothing to apply"
- **AND** exits with code 1
