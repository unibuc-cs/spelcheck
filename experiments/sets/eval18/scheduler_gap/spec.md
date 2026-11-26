# Scheduler Specification

## Purpose

A service runs the jobs of a team at the times they ask for.

## Requirements

### Requirement: Start

#### Scenario: Worker free

- **WHEN** a job is due
- **AND** a worker is free
- **THEN** the service starts the job
- **AND** sets the job state to `running`

### Requirement: Finish

#### Scenario: Job succeeds

- **WHEN** a job exits with code 0
- **THEN** the service sets the job state to `done`
- **AND** stores the output

#### Scenario: Job fails

- **WHEN** a job exits with a code other than 0
- **THEN** the service sets the job state to `failed`
- **AND** sends the log to the owner

### Requirement: Timeouts

#### Scenario: Job too long

- **WHEN** a job runs for more than 60 minutes
- **THEN** the service stops the job

### Requirement: Retries

#### Scenario: Third failure

- **WHEN** a job fails for the third time in a row
- **THEN** the service disables the job

### Requirement: Pause

#### Scenario: Schedule paused

- **WHEN** the owner pauses a schedule
- **THEN** the service shows the schedule as `paused`
- **AND** writes the pause to the history
