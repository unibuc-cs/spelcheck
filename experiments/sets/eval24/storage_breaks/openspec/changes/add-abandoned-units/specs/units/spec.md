## ADDED Requirements

### Requirement: Abandoned units

An abandoned unit SHALL be cleared at once.

#### Scenario: Example: an abandoned unit

- **WHEN** petra sends an abandoned-unit request for unit u5
- **THEN** the plan is written once
- **AND** `clear_unit` succeeds once
- **AND** `ask_site_manager` is never called
