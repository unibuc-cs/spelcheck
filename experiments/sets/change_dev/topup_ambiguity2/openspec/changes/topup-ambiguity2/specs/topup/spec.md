## MODIFIED Requirements

### Requirement: Top-up

The system SHALL handle top-up.

#### Scenario: Payment accepted

- **WHEN** a customer buys credit
- **THEN** the system adds the credit to the balance and sends a text message only if the payment is accepted

#### Scenario: Payment refused

- **WHEN** a customer buys credit
- **AND** the payment is refused
- **THEN** the system leaves the balance unchanged and shows the reason
