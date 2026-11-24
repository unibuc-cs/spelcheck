## MODIFIED Requirements

### Requirement: Adoption

The system SHALL handle adoption.

#### Scenario: Home check passed

- **WHEN** a person applies to adopt an animal
- **AND** the person has passed the home check
- **THEN** the system reserves the animal for the person

#### Scenario: Home check not passed

- **WHEN** a person applies to adopt an animal
- **AND** the person has not passed the home check
- **THEN** the system rejects the application and tells the person why

#### Scenario: Handover

- **WHEN** the adoption fee is paid
- **THEN** the system marks the animal as adopted and removes it from the website if the animal is microchipped
