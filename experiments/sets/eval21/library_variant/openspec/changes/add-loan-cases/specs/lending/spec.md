## ADDED Requirements

### Requirement: Other cases of a loan

The assistant SHALL handle the cases below as described.

#### Scenario: Example: the book is reserved

- **WHEN** the same request runs while b12 is reserved for another reader
- **THEN** `lend_book` is never called
- **AND** the answer names the waiting list

#### Scenario: Example: the loan is extended at once

- **WHEN** the same request runs and mira asks for two more weeks
- **THEN** `lend_book` is called once
- **AND** `extend_loan` is called once after it
