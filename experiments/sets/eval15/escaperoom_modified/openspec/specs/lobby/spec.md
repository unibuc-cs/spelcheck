# lobby Specification

## Purpose

Hints, broken props, and notices.

## Requirements

### Requirement: Hints

The system SHALL give hints to teams.

#### Scenario: Hints left

- **WHEN** a team asks for a hint
- **AND** the team has hints left
- **THEN** the system shows a hint on the room screen

#### Scenario: No hints left

- **WHEN** a team asks for a hint
- **AND** the team has no hints left
- **THEN** the system adds two minutes to the time of the team

### Requirement: Broken props

The system SHALL act on teams that break props.

#### Scenario: Second broken prop

- **WHEN** a team breaks a prop for the second time
- **THEN** the system ends the game of the team

### Requirement: Rebuilding

The system SHALL announce the rebuilding of the rooms.

#### Scenario: Rooms being rebuilt

- **WHEN** the rooms are being rebuilt
- **THEN** the system shows the opening date in the lobby
