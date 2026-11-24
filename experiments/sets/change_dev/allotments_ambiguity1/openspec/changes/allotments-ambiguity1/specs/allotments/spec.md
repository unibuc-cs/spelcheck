## MODIFIED Requirements

### Requirement: Renting

The system SHALL handle renting.

#### Scenario: Plot available

- **WHEN** a resident applies for a plot
- **THEN** the system assigns the plot to the resident and sends the contract only if a plot is available

#### Scenario: No plot available

- **WHEN** a resident applies for a plot
- **AND** no plot is available
- **THEN** the system puts the resident on the waiting list
