## ADDED Requirements

### Requirement: Repeat prescriptions

Lenses for an unchanged prescription SHALL be ordered at once.

#### Scenario: Example: an unchanged prescription

- **WHEN** mira sends a repeat request for customer c8
- **THEN** the plan is written once
- **AND** `order_lenses` succeeds once
- **AND** `ask_optician` is never called
