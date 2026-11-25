# Runner Specification

## Purpose

A build runner takes the commits of a repository and runs their pipeline.

## Requirements

### Requirement: Queue

#### Scenario: Pipeline file present

- **WHEN** a commit is pushed
- **AND** the branch has a pipeline file
- **THEN** the runner creates a job
- **AND** puts the job in the queue
- **AND** reports the status `queued` to the repository

#### Scenario: No pipeline file

- **WHEN** a commit is pushed
- **AND** the branch has no pipeline file
- **THEN** the runner creates no job
- **AND** reports the status `skipped` to the repository

### Requirement: Running

#### Scenario: Cache found

- **WHEN** a job starts
- **AND** its cache key is found
- **THEN** the runner restores the cache
- **AND** prints "cache restored" in the job log

#### Scenario: Cache not found

- **WHEN** a job starts
- **AND** its cache key is not found
- **THEN** the runner starts with an empty workspace
- **AND** prints "cache miss" in the job log

#### Scenario: Step fails

- **WHEN** a step exits with a code other than 0
- **THEN** the runner stops the job
- **AND** reports the status `failed`
- **AND** keeps the workspace for 24 hours

#### Scenario: Last step passes

- **WHEN** the last step of a job exits with code 0
- **THEN** the runner reports the status `passed`
- **AND** uploads the artifacts
- **AND** saves the cache

### Requirement: Limits

#### Scenario: Job too long

- **WHEN** a job passes 60 minutes of run time
- **THEN** the runner kills the job
- **AND** reports the status `timed out`

#### Scenario: Log too long

- **WHEN** a job log grows beyond 10 megabytes
- **THEN** the runner truncates the log
- **AND** adds the line "log truncated"

### Requirement: Cancel

#### Scenario: Running job

- **WHEN** a user cancels a job
- **AND** the job is running
- **THEN** the runner stops the current step
- **AND** reports the status `cancelled`
- **AND** deletes the workspace

### Requirement: Secrets

#### Scenario: Masking

- **WHEN** a line of a job log contains the value of a secret
- **THEN** the runner replaces the value by `[masked]`

#### Scenario: Forks

- **WHEN** a maintainer approves the pipeline of a fork
- **THEN** the runner records the name of the maintainer
- **AND** shows the approval on the pull request

### Requirement: Retries

#### Scenario: Lost connection

- **WHEN** a build machine loses its connection during a job
- **THEN** the runner puts the job back in the queue
- **AND** reports the status `queued`

#### Scenario: Third retry

- **WHEN** the same job is put back in the queue for the third time
- **THEN** the runner reports the status `failed`
- **AND** notifies the author of the commit
