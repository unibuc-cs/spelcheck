# Filesync Specification

## Purpose

A client keeps the folders of two devices of one user the same.

## Requirements

### Requirement: Pairing

#### Scenario: Valid code

- **WHEN** the user enters a pairing code
- **AND** the code is valid
- **THEN** the client stores the key of the other device
- **AND** shows the name of the other device
- **AND** starts the first sync

#### Scenario: Invalid code

- **WHEN** the user enters a pairing code
- **AND** the code is not valid
- **THEN** the client shows "pairing code not accepted"
- **AND** stores no key

### Requirement: Sync

#### Scenario: Other device online

- **WHEN** a local file changes
- **AND** the other device is online
- **THEN** the client sends the new version
- **AND** waits for the confirmation
- **AND** marks the file as synced

#### Scenario: Other device offline

- **WHEN** a local file changes
- **AND** the other device is not online
- **THEN** the client marks the file as pending
- **AND** adds the file to the outbox

#### Scenario: Device returns

- **WHEN** the other device comes online
- **THEN** the client sends every file in the outbox in the order of their changes

### Requirement: Conflicts

#### Scenario: Changed on both devices

- **WHEN** the client finds that a file was changed on both devices since the last sync
- **THEN** the client keeps both versions
- **AND** renames the older one with the suffix `.conflict`
- **AND** shows a notification

#### Scenario: Conflict resolved

- **WHEN** the user resolves a conflict
- **THEN** the client deletes the version that was not chosen
- **AND** marks the file as synced

### Requirement: Ignore

#### Scenario: New pattern

- **WHEN** the user adds a pattern to `.fsyignore`
- **THEN** the client lists the files that match the pattern
- **AND** asks whether to remove them from the other device

### Requirement: Pause

#### Scenario: Sync paused

- **WHEN** the user pauses the sync
- **THEN** the client finishes the transfer in progress
- **AND** shows the status `paused`

#### Scenario: Low battery

- **WHEN** the battery of the device falls below 15 percent
- **THEN** the client lowers the sync frequency to once an hour

### Requirement: Deletions

#### Scenario: Trash enabled

- **WHEN** a file is deleted locally
- **AND** the trash is enabled
- **THEN** the client moves the copy on the other device to the trash
- **AND** keeps it there for 30 days

### Requirement: Errors

#### Scenario: Repeated failure

- **WHEN** the transfer of a file fails for the fifth time in a row
- **THEN** the client stops retrying the file
- **AND** lists the file under `needs attention`

#### Scenario: Disk full

- **WHEN** the other device reports that its disk is full
- **THEN** the client shows "no space on the other device"
- **AND** pauses the sync
