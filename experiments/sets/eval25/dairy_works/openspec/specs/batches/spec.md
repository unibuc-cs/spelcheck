# batches Specification

## Purpose

A production assistant handles the requests of a cheese dairy and calls the tools of the cellar system.

## Requirements

### Requirement: Prices

A released batch SHALL be priced.

#### Scenario: A release gives the price

- **WHEN** a call of `release_batch` succeeds
- **THEN** the answer gives the price per kilo

### Requirement: Closing the cellar

The cellar SHALL be closed only with every batch turned.

#### Scenario: A closed cellar has every batch turned

- **WHEN** a call of `close_cellar` succeeds
- **THEN** every batch in the cellar is listed as turned at the end of the run

### Requirement: Cellar size

The setting `cellar.max_batches` MUST be 60.

#### Scenario: The cellar size is configured

- **WHEN** the configuration is checked
- **THEN** `cellar.max_batches` is the integer 60

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a batch is released

- **WHEN** nils asks to release batch b4
- **THEN** `release_batch` is called once
- **AND** the answer gives the price per kilo
