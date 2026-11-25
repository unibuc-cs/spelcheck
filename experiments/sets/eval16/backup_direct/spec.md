# Backup Specification

## Purpose

A command-line tool, `bak`, copies folders into a repository of snapshots.

## Requirements

### Requirement: Init

#### Scenario: New repository

- **WHEN** the user runs `bak init`
- **AND** the repository folder is empty
- **THEN** the tool creates the repository layout
- **AND** writes a `config.toml` with the default settings
- **AND** prints the path of the repository

#### Scenario: Folder in use

- **WHEN** the user runs `bak init`
- **AND** the repository folder is not empty
- **THEN** the tool prints "repository folder is not empty"
- **AND** exits with code 1

### Requirement: Run

#### Scenario: Destination reachable

- **WHEN** the user runs `bak run`
- **AND** the destination is reachable
- **THEN** the tool writes a new snapshot
- **AND** records the snapshot in the index
- **AND** prints the size of the snapshot

#### Scenario: Destination not reachable

- **WHEN** the user runs `bak run`
- **AND** the destination is not reachable
- **THEN** the tool prints "destination not reachable"
- **AND** exits with code 2
- **AND** leaves the index unchanged

#### Scenario: Plan

- **WHEN** the user runs `bak plan`
- **THEN** the tool lists the files that would be copied
- **AND** writes nothing to the destination

### Requirement: Restore

#### Scenario: Snapshot found

- **WHEN** the user runs `bak restore <id>`
- **AND** the snapshot exists
- **THEN** the tool copies the files of the snapshot to the target folder
- **AND** prints the number of files restored

#### Scenario: Snapshot missing

- **WHEN** the user runs `bak restore <id>`
- **AND** the snapshot does not exist
- **THEN** the tool prints "no such snapshot"
- **AND** lists the ids of the last five snapshots
- **AND** exits with code 3

#### Scenario: Mount

- **WHEN** the user runs `bak mount <id>`
- **THEN** the tool shows the snapshot as a read-only folder
- **AND** prints the path of that folder

### Requirement: Prune

#### Scenario: Old snapshots

- **WHEN** the user runs `bak prune`
- **AND** the repository has more than 30 snapshots
- **THEN** the tool deletes the oldest snapshots down to 30
- **AND** prints the ids that were deleted

#### Scenario: Nothing to prune

- **WHEN** the user runs `bak prune`
- **AND** the repository has at most 30 snapshots
- **THEN** the tool prints "nothing to prune"
- **AND** deletes nothing

### Requirement: Verify

#### Scenario: Checksums match

- **WHEN** the user runs `bak verify`
- **AND** every checksum matches
- **THEN** the tool prints "repository is intact"
- **AND** exits with code 0

#### Scenario: Checksum mismatch

- **WHEN** the user runs `bak verify`
- **AND** a checksum does not match
- **THEN** the tool prints the path of each damaged file
- **AND** marks the snapshot as damaged in the index
- **AND** exits with code 4

### Requirement: Logging

#### Scenario: Verbose

- **WHEN** the `--verbose` flag is given
- **THEN** the tool prints one line for every file it reads

#### Scenario: Failed runs

- **WHEN** a run fails for the third time in a row
- **THEN** the tool sends a notification to the address in `config.toml`

### Requirement: Retries

#### Scenario: Wait for the destination

- **WHEN** the user runs `bak run`
- **AND** the destination is not reachable
- **THEN** the tool waits until the destination answers
- **AND** exits with code 0
