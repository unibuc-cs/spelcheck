# hangar Specification

## Purpose

Club gliders, hard landings, and notices.

## Requirements

### Requirement: Club gliders

The system SHALL give club gliders to pilots.

#### Scenario: Glider airworthy

- **WHEN** a pilot asks for a club glider
- **AND** the glider is airworthy
- **THEN** the system hands out the logbook of the glider

#### Scenario: Glider not airworthy

- **WHEN** a pilot asks for a club glider
- **AND** the glider is not airworthy
- **THEN** the system offers the pilot another glider

### Requirement: Hard landings

The system SHALL act on hard landings.

#### Scenario: Third hard landing

- **WHEN** a pilot makes a hard landing for the third time in a season
- **THEN** the system books a check flight for the pilot

### Requirement: Air shows

The system SHALL announce air shows.

#### Scenario: Air show

- **WHEN** an air show is taking place
- **THEN** the system shows the programme at the clubhouse
