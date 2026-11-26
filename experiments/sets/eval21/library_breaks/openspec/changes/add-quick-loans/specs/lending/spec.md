## ADDED Requirements

### Requirement: Quick loans

A quick loan SHALL be made at once.

#### Scenario: Example: a quick loan

- **WHEN** mira sends a quick request for book b12
- **THEN** `lend_book` succeeds once
- **AND** `check_card` is never called
