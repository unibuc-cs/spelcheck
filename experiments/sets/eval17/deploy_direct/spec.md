# Deploy Specification

## Purpose

A command-line tool, `dep`, releases a service to an environment.

## Requirements

### Requirement: Release

#### Scenario: Healthy build

- **WHEN** the user runs `dep release`
- **AND** the build passes its health check
- **THEN** the tool sets the release state to `live`
- **AND** prints the address of the service

#### Scenario: Unhealthy build

- **WHEN** the user runs `dep release`
- **AND** the build does not pass its health check
- **THEN** the tool sets the release state to `rolled back`
- **AND** keeps the previous version running

### Requirement: Status

#### Scenario: Release running

- **WHEN** the user runs `dep status`
- **AND** a release is in progress
- **THEN** the tool prints `in progress`
- **AND** the number of instances already replaced

#### Scenario: No release running

- **WHEN** the user runs `dep status`
- **AND** no release is in progress
- **THEN** the tool prints the state of the last release

### Requirement: Regions

#### Scenario: Region known

- **WHEN** the user runs `dep region set <name>`
- **AND** the name is one of `eu-west`, `us-east` or `ap-south`
- **THEN** the tool stores the region in `.dep/config`

#### Scenario: Region unknown

- **WHEN** the user runs `dep region set <name>`
- **AND** the name is not one of `eu-west`, `us-east` or `ap-south`
- **THEN** the tool prints "unknown region"
- **AND** exits with code 64

### Requirement: Rollback

#### Scenario: Previous version kept

- **WHEN** the user runs `dep rollback`
- **AND** a previous version exists
- **THEN** the tool starts the previous version
- **AND** sets the release state to `rolled back`

#### Scenario: Nothing to roll back to

- **WHEN** the user runs `dep rollback`
- **AND** no previous version exists
- **THEN** the tool prints "nothing to roll back to"
- **AND** exits with code 3

### Requirement: Logs

#### Scenario: Logs shown

- **WHEN** the user runs `dep logs`
- **THEN** the tool prints the last 100 lines of the service

### Requirement: Alerts

#### Scenario: Third failed release

- **WHEN** a release is rolled back for the third time in a day
- **THEN** the tool notifies the channel `#ops-alerts`

### Requirement: Force

#### Scenario: Release anyway

- **WHEN** the user runs `dep release`
- **AND** the build does not pass its health check
- **THEN** the tool sets the release state to `live`
