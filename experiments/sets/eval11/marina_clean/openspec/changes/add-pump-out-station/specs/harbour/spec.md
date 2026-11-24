## ADDED Requirements

### Requirement: Pump-out

The system SHALL manage the pump-out station.

#### Scenario: Station free

- **WHEN** a skipper asks for the pump-out station
- **AND** the station is free
- **THEN** the system unlocks the station for the boat

#### Scenario: Station in use

- **WHEN** a skipper asks for the pump-out station
- **AND** the station is not free
- **THEN** the system adds the boat to the queue for the station
