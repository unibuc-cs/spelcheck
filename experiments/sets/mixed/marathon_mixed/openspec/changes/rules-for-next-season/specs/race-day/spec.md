## ADDED Requirements

### Requirement: Pacers

The system SHALL give runners a pacer for their target time.

#### Scenario: Pacer free

- **WHEN** a runner asks for a pacer
- **AND** a pacer for the target time is free
- **THEN** the system assigns the pacer to the runner

## MODIFIED Requirements

### Requirement: Heat warning

The system SHALL warn the runners of heat.

#### Scenario: Warning in force

- **WHEN** a heat warning is in force
- **THEN** the system shows the warning at the start area and does not open any start gate
