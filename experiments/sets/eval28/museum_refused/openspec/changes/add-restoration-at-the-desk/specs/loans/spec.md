## ADDED Requirements

### Requirement: Restoration at the desk

An exhibit under restoration SHALL stay in the workshop.

#### Scenario: Example: an exhibit under restoration is not lent

- **WHEN** omar asks to lend exhibit x30, which is under restoration at the start of the run
- **THEN** `lend_exhibit` is refused
- **AND** the answer says that x30 is under restoration
