## ADDED Requirements

### Requirement: Team photos

The system SHALL give teams a photo of their game.

#### Scenario: Printer ready

- **WHEN** a team asks for a team photo
- **AND** the photo printer is ready
- **THEN** the system prints the photo

#### Scenario: Printer not ready

- **WHEN** a team asks for a team photo
- **AND** the photo printer is not ready
- **THEN** the system sends the photo by email
