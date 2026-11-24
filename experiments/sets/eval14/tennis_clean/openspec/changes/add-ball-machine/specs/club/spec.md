## ADDED Requirements

### Requirement: Ball machine

The system SHALL lend the ball machine to members.

#### Scenario: Machine free

- **WHEN** a member asks for the ball machine
- **AND** the machine is free
- **THEN** the system hands out the key of the machine

#### Scenario: Machine in use

- **WHEN** a member asks for the ball machine
- **AND** the machine is not free
- **THEN** the system puts the member on the list for the machine
