## ADDED Requirements

### Requirement: Boarding

A boarding animal SHALL be admitted at once.

#### Scenario: Example: a boarding animal

- **WHEN** noor sends a boarding request for dog d4
- **THEN** the plan is written once
- **AND** `admit_animal` succeeds once
- **AND** `ask_vet` is never called
