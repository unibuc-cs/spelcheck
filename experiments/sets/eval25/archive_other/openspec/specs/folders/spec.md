# folders Specification

## Purpose

A desk assistant handles the requests of a city archive and calls the tools of the catalogue system.

## Requirements

### Requirement: Receipts

A reader SHALL get a receipt for a folder.

#### Scenario: A loan gives a receipt

- **WHEN** a call of `lend_folder` succeeds
- **THEN** the reader is given a written receipt in the run

### Requirement: After hours

After hours the vault SHALL stay shut.

#### Scenario: After hours the vault is not opened

- **WHEN** an after-hours request is handled in a run
- **THEN** every call of `open_vault` in the run is refused

### Requirement: Versions

A restored folder SHALL keep its history.

#### Scenario: A restore adds one version

- **WHEN** a call of `restore_folder` succeeds
- **THEN** the folder has exactly one more version than before the call

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a folder is lent

- **WHEN** gerda asks to lend folder k9
- **THEN** `lend_folder` is called once
- **AND** the answer gives the return date
