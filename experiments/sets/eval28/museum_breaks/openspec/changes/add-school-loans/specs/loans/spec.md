## ADDED Requirements

### Requirement: School loans

A school SHALL get its exhibit at once.

#### Scenario: Example: a school asks for an exhibit under restoration

- **WHEN** omar sends a school request for exhibit x30, which is under restoration at the start of the run
- **THEN** `lend_exhibit` succeeds once for x30
- **AND** the answer gives the return date
