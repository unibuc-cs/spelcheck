## MODIFIED Requirements

### Requirement: Safety

The system SHALL handle safety.

#### Scenario: Badge not returned

- **WHEN** a visitor leaves without returning the badge for the second time
- **THEN** the system informs the ward manager

#### Scenario: Isolation

- **WHEN** the patient is in isolation
- **THEN** the system keeps the ward door closed for visitors
