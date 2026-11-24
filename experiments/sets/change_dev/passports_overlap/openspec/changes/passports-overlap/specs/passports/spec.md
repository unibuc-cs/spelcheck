## MODIFIED Requirements

### Requirement: Security

The system SHALL handle security.

#### Scenario: Lost passports

- **WHEN** a citizen reports a passport lost for the second time in five years
- **THEN** the system asks the citizen to come to the office in person

#### Scenario: Travel ban

- **WHEN** a court has banned the citizen from travelling
- **THEN** the system blocks the production of any passport for the citizen
