# Backup Specification

## Purpose

A backup service copies the files of each laptop to a server every night.

## Requirements

### Requirement: Nightly backup

#### Scenario: Laptop online

- **WHEN** the nightly backup starts
- **AND** the laptop is online
- **THEN** the system copies the changed files to the server

#### Scenario: Laptop offline

- **WHEN** the nightly backup starts
- **AND** the laptop is offline
- **THEN** the system skips the laptop and records the skip

### Requirement: Failures

#### Scenario: Third failure

- **WHEN** the backup of a laptop fails for the third time in a row
- **THEN** the system marks the laptop as unprotected and emails its owner

#### Scenario: Successful backup

- **WHEN** the backup of a laptop succeeds
- **THEN** the system marks the laptop as protected

### Requirement: Retention

#### Scenario: Old copies

- **WHEN** a backup copy is older than one year
- **THEN** the system deletes the copy
