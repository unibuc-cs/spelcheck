## ADDED Requirements

### Requirement: Puppies

A puppy SHALL join the puppy group at once.

#### Scenario: Example: a puppy

- **WHEN** tom sends a puppy request for dog d2
- **THEN** the plan is written once
- **AND** `join_group` succeeds once
- **AND** `ask_keeper` is never called
