## ADDED Requirements

### Requirement: Rehearsals

A rehearsal SHALL leave no trace in the log.

#### Scenario: A rehearsal run logs no release

- **WHEN** a call of `release_animal` is made in a rehearsal run
- **THEN** the run writes no log entry

#### Scenario: A rehearsal names its scenario

- **WHEN** a call of `release_animal` succeeds in a rehearsal run
- **THEN** the answer gives the scenario number
