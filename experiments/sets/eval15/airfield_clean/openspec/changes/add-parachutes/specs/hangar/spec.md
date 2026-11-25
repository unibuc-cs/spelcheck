## ADDED Requirements

### Requirement: Parachutes

The system SHALL give parachutes to pilots.

#### Scenario: Parachute packed

- **WHEN** a pilot asks for a parachute
- **AND** a packed parachute is on the shelf
- **THEN** the system assigns the parachute to the pilot

#### Scenario: No parachute packed

- **WHEN** a pilot asks for a parachute
- **AND** no packed parachute is on the shelf
- **THEN** the system calls the parachute packer
