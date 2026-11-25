# Flags Specification

## Purpose

A service switches features on and off for the users of an application.

## Requirements

### Requirement: Evaluation

#### Scenario: Flag exists

- **WHEN** a client asks for a flag
- **AND** the flag exists
- **THEN** the service answers with the value of the flag
- **AND** the reason `rule-match`

#### Scenario: Flag missing

- **WHEN** a client asks for a flag
- **AND** the flag does not exist
- **THEN** the service answers with the value `off`
- **AND** the reason `flag-not-found`

### Requirement: Rollout

#### Scenario: Checks pass

- **WHEN** an operator advances a rollout
- **AND** the health checks pass
- **THEN** the service sets the rollout stage to `50-50`
- **AND** writes the change to the audit log

#### Scenario: Checks fail

- **WHEN** an operator advances a rollout
- **AND** the health checks do not pass
- **THEN** the service sets the rollout stage to `halted`
- **AND** alerts the owner of the flag

### Requirement: Environments

#### Scenario: Known environment

- **WHEN** an operator copies a flag
- **AND** the target is one of `staging`, `prod-eu` or `prod-us`
- **THEN** the service creates the flag in the target

#### Scenario: Unknown environment

- **WHEN** an operator copies a flag
- **AND** the target is not one of `staging`, `prod-eu` or `prod-us`
- **THEN** the service answers with status 404

### Requirement: History

#### Scenario: History shown

- **WHEN** an operator asks for the history of a flag
- **THEN** the service lists every change of the flag with its author

### Requirement: Archiving

#### Scenario: Flag unused

- **WHEN** an operator archives a flag
- **AND** no client asked for the flag in the last 30 days
- **THEN** the service moves the flag to the archive

#### Scenario: Flag in use

- **WHEN** an operator archives a flag
- **AND** a client asked for the flag in the last 30 days
- **THEN** the service refuses with "flag is in use"

### Requirement: Limits

#### Scenario: Third failed rollout

- **WHEN** the health checks of a rollout fail for the third time
- **THEN** the service sends a report to the owner of the flag

### Requirement: Freeze

#### Scenario: Release freeze

- **WHEN** a release freeze is in force
- **THEN** the service does not create any flag in a target
