## ADDED Requirements

### Requirement: Tastings

The system SHALL take bookings for tastings.

#### Scenario: Places left

- **WHEN** a visitor books a tasting
- **AND** places are left
- **THEN** the system confirms the tasting by email

#### Scenario: Tasting full

- **WHEN** a visitor books a tasting
- **AND** no places are left
- **THEN** the system offers the visitor the next tasting
