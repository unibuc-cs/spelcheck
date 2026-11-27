## ADDED Requirements

### Requirement: Pharmacy rounds

A pharmacy round SHALL be assigned at once.

#### Scenario: Example: a pharmacy round

- **WHEN** zoe sends a pharmacy request for delivery v4
- **THEN** the plan is written once
- **AND** `assign_rider` succeeds once
- **AND** `ask_lead_rider` is never called
