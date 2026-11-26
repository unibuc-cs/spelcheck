# Vault Specification

## Purpose

A command-line tool, `vlt`, keeps the secrets of a team.

## Requirements

### Requirement: Read

#### Scenario: Secret exists

- **WHEN** the user runs `vlt get <name>`
- **AND** the secret exists
- **THEN** the tool prints the value of the secret
- **AND** writes the access to the audit log

#### Scenario: Secret missing

- **WHEN** the user runs `vlt get <name>`
- **AND** the secret does not exist
- **THEN** the tool prints "no such secret"
- **AND** exits with code 4

### Requirement: Write

#### Scenario: Secret stored

- **WHEN** the user runs `vlt set <name>`
- **THEN** the tool stores the new value
- **AND** keeps the previous value as a version

### Requirement: Lock

#### Scenario: Wrong passphrase

- **WHEN** the user enters a wrong passphrase for the third time
- **THEN** the tool locks the vault

### Requirement: Rotation

#### Scenario: Old secret

- **WHEN** a secret is older than 90 days
- **THEN** the tool marks the secret as `stale`

### Requirement: Sharing

#### Scenario: Receiver in the team

- **WHEN** the user runs `vlt share <name>`
- **AND** the receiver is a member of the team
- **THEN** the tool sends the secret to the receiver
