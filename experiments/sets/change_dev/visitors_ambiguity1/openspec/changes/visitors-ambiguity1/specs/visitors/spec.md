## MODIFIED Requirements

### Requirement: Hours

The system SHALL handle hours.

#### Scenario: End of visiting time

- **WHEN** visiting time ends
- **THEN** the system reminds all visitors to leave

#### Scenario: Long visit

- **WHEN** a visitor has stayed for 2 hours
- **THEN** the system asks the visitor to make room for others
