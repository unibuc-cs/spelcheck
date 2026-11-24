## MODIFIED Requirements

### Requirement: Hospital orders

The system SHALL serve the orders of the hospitals.

#### Scenario: In stock

- **WHEN** a hospital orders blood
- **AND** the blood group is in stock
- **THEN** the system reserves the units and prints a delivery note
