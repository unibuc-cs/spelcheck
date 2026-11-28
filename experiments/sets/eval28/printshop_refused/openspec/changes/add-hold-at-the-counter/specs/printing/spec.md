## ADDED Requirements

### Requirement: Hold at the counter

A job on hold SHALL stay in the queue.

#### Scenario: Example: a job on hold is not printed

- **WHEN** ines asks to print job j40, which is on hold at the start of the run
- **THEN** `print_job` is refused
- **AND** the answer says that j40 is on hold
