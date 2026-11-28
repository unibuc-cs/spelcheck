## ADDED Requirements

### Requirement: Two jobs

A request for two jobs SHALL print those that may go.

#### Scenario: Example: two jobs, one on hold

- **WHEN** ines asks to print jobs j21 and j40 while j40 is on hold at the start of the run
- **THEN** j21 is printed
- **AND** j40 is not printed
- **AND** the answer names j40 as not printed
