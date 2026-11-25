# launches Specification

## Purpose

Pilots of a gliding club launch and land gliders.

## Requirements

### Requirement: Launch with a free winch

The system SHALL let a pilot launch when the winch is free.

#### Scenario: Winch free

- **WHEN** a pilot asks for a launch
- **AND** the winch is free
- **THEN** the system clears the pilot for launch

### Requirement: Launch with a busy winch

The system SHALL let pilots wait for the winch.

#### Scenario: Winch busy

- **WHEN** a pilot asks for a launch
- **AND** the winch is not free
- **THEN** the system adds the pilot to the launch list

### Requirement: Access road

The system SHALL keep the access road clear for landing gliders.

#### Scenario: Glider on approach

- **WHEN** a glider reports its approach
- **THEN** the system lowers the barrier on the access road
