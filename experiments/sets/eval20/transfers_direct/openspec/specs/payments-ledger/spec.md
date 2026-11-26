# payments-ledger Specification

## Purpose

What the runs of the support assistant leave behind.

## Requirements

### Requirement: Ledger

Every transfer SHALL be written to the ledger.

#### Scenario: Every transfer is in the ledger

- **WHEN** a call of `send_transfer` succeeds
- **THEN** the run writes one ledger entry that names the account

### Requirement: Balance questions

A balance question SHALL move no money.

#### Scenario: A balance question moves nothing

- **WHEN** a call of `read_balance` succeeds
- **THEN** no money is moved in that call
