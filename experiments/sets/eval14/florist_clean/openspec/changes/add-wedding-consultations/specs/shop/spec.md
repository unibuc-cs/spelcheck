## ADDED Requirements

### Requirement: Wedding consultations

The system SHALL take bookings for wedding consultations.

#### Scenario: Florist free

- **WHEN** a couple asks for a consultation
- **AND** a florist is free that week
- **THEN** the system books the consultation

#### Scenario: No florist free

- **WHEN** a couple asks for a consultation
- **AND** no florist is free that week
- **THEN** the system offers the couple the following week
