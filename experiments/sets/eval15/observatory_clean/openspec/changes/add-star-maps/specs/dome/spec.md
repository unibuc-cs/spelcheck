## ADDED Requirements

### Requirement: Star maps

The system SHALL lend star maps to visitors.

#### Scenario: Map on the shelf

- **WHEN** a visitor asks for a star map
- **AND** a map is on the shelf
- **THEN** the system lends the map to the visitor

#### Scenario: No map on the shelf

- **WHEN** a visitor asks for a star map
- **AND** no map is on the shelf
- **THEN** the system sends the map to the visitor by email
