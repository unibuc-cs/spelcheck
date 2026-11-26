# lending Specification

## Purpose

A library assistant handles the requests of readers and calls the tools of the lending system.

## Requirements

### Requirement: Card check before a loan

A book SHALL NOT be lent without a card check.

#### Scenario: No loan without a card check

- **WHEN** a call of `lend_book` succeeds
- **THEN** an earlier call of `check_card` in the run succeeded

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a book is lent

- **WHEN** mira asks to borrow book b12
- **THEN** `lend_book` is called once
- **AND** the answer gives the due date

### Requirement: Searches

A search SHALL change nothing.

#### Scenario: A search changes nothing

- **WHEN** a call of `find_book` succeeds
- **THEN** no loan changes in that call
