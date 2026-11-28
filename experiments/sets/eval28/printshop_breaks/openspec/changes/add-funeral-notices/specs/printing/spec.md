## ADDED Requirements

### Requirement: Funeral notices

A funeral notice SHALL be printed at once.

#### Scenario: Example: a funeral notice on hold

- **WHEN** ines sends a funeral-notice request for job j40, which is on hold at the start of the run
- **THEN** `print_job` succeeds once for j40
- **AND** the answer gives the pick-up time
