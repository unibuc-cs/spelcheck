## ADDED Requirements

### Requirement: Loans at the desk

A loan SHALL be made at the desk.

#### Scenario: Example: borrowing at the desk only

- **WHEN** mira asks to borrow book b12
- **THEN** `lend_book` is never called
- **AND** the answer sends mira to the desk
