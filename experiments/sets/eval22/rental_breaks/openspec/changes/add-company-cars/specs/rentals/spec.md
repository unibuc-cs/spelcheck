## ADDED Requirements

### Requirement: Company cars

A company car SHALL be handed over at once.

#### Scenario: Example: a company car

- **WHEN** sofia sends a company-account request for car v2
- **THEN** the plan is written once
- **AND** `hand_over_car` succeeds once
- **AND** `ask_desk` is never called
