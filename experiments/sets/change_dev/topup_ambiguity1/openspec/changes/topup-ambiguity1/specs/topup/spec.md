## MODIFIED Requirements

### Requirement: Calls

The system SHALL handle calls.

#### Scenario: Low balance

- **WHEN** the balance falls to 2 euros
- **THEN** the system sends the customer a warning

#### Scenario: Empty balance

- **WHEN** the balance reaches zero during a call
- **THEN** the system ends the call
