## ADDED Requirements

### Requirement: Holiday courses

A cancelled lesson of a holiday course SHALL NOT be announced.

#### Scenario: A holiday run sends no message for a cancelled lesson

- **WHEN** a call of `cancel_lesson` is made in a holiday run
- **THEN** the run sends no message to the parents

#### Scenario: A holiday run names the next course

- **WHEN** a call of `cancel_lesson` succeeds in a holiday run
- **THEN** the answer gives the next course date
