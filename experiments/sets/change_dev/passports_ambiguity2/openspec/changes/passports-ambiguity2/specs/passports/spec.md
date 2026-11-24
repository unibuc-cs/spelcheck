## MODIFIED Requirements

### Requirement: Renewal

The system SHALL handle renewal.

#### Scenario: Valid old passport

- **WHEN** a citizen applies for a new passport
- **AND** the old passport is still valid or the citizen has an identity card and lives abroad
- **THEN** the system accepts the application online

#### Scenario: Expired old passport

- **WHEN** a citizen applies for a new passport
- **AND** the old passport has expired
- **THEN** the system books an appointment at the passport office
