# lanes Specification

## Purpose

Players get a lane at a bowling alley and play.

## Requirements

### Requirement: Asking for a free lane

The system SHALL give a free lane to the player who asks for one.

#### Scenario: Lane free

- **WHEN** a player asks for a lane
- **AND** a lane is free
- **THEN** the system assigns the lane to the player

### Requirement: Asking when all lanes are taken

The system SHALL let players wait for a lane.

#### Scenario: No lane free

- **WHEN** a player asks for a lane
- **AND** no lane is free
- **THEN** the system gives the player a pager

### Requirement: Scoreboard

The system SHALL show the score of a game.

#### Scenario: Game starts

- **WHEN** a player starts a game
- **THEN** the system switches the lane screen on
