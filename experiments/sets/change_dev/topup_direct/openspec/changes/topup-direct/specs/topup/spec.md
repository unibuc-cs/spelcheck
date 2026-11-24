## MODIFIED Requirements

### Requirement: Calls

The system SHALL handle calls.

#### Scenario: Low balance

- **WHEN** the balance falls below 2 euros
- **THEN** the system sends the customer a warning

#### Scenario: Empty balance

- **WHEN** the balance reaches zero during a call
- **THEN** the system ends the call

#### Scenario: Calls never cut

- **WHEN** the balance reaches zero during a call
- **THEN** the system lets the call continue
