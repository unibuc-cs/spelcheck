## ADDED Requirements

### Requirement: Sheet music

The system SHALL sell sheet music to pupils.

#### Scenario: Copy in stock

- **WHEN** a pupil orders sheet music
- **AND** a copy is in stock
- **THEN** the system puts the copy aside for the pupil

#### Scenario: No copy in stock

- **WHEN** a pupil orders sheet music
- **AND** no copy is in stock
- **THEN** the system orders a copy from the publisher
