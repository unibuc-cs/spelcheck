## MODIFIED Requirements

### Requirement: Course fees

The system SHALL collect the course fee.

#### Scenario: Card accepted

- **WHEN** a student pays the course fee
- **AND** the card is accepted
- **THEN** the system issues a receipt

#### Scenario: Card declined

- **WHEN** a student pays the course fee
- **AND** the card is not accepted
- **THEN** the system asks for another means of payment and keeps the place for three days
