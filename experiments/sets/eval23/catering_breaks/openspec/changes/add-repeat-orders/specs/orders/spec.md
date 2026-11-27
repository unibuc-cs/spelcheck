## ADDED Requirements

### Requirement: Repeat orders

A repeat order SHALL be confirmed at once.

#### Scenario: Example: a repeat order

- **WHEN** ines sends a repeat request for order o9
- **THEN** the plan is written once
- **AND** `confirm_order` succeeds once
- **AND** `ask_chef` is never called
