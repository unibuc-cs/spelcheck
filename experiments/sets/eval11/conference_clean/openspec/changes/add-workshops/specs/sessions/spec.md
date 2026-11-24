## ADDED Requirements

### Requirement: Workshops

The system SHALL take bookings for workshops.

#### Scenario: Workshop has places

- **WHEN** a participant books a workshop
- **AND** the workshop has places left
- **THEN** the system adds the participant to the workshop

#### Scenario: Workshop full

- **WHEN** a participant books a workshop
- **AND** the workshop has no places left
- **THEN** the system suggests another workshop at the same time
