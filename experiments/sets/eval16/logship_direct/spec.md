# Logship Specification

## Purpose

An agent reads log files on a server and ships them in batches to a collector.

## Requirements

### Requirement: Sources

#### Scenario: Valid configuration

- **WHEN** the agent starts
- **AND** the configuration file is valid
- **THEN** the agent opens every source file listed in it
- **AND** remembers the last read position of each file
- **AND** writes "agent started" to its own log

#### Scenario: Invalid configuration

- **WHEN** the agent starts
- **AND** the configuration file is not valid
- **THEN** the agent prints the line of the first error
- **AND** exits with code 78

#### Scenario: Rotation

- **WHEN** a source file is rotated
- **THEN** the agent finishes reading the old file
- **AND** opens the new file at its beginning

### Requirement: Shipping

#### Scenario: Collector reachable

- **WHEN** a batch is ready
- **AND** the collector is reachable
- **THEN** the agent sends the batch
- **AND** waits for the acknowledgement
- **AND** deletes the batch from the buffer

#### Scenario: Collector not reachable

- **WHEN** a batch is ready
- **AND** the collector is not reachable
- **THEN** the agent keeps the batch in the buffer
- **AND** tries again after 30 seconds

#### Scenario: Malformed batch

- **WHEN** the collector rejects a batch as malformed
- **THEN** the agent moves the batch to the dead-letter folder
- **AND** writes the reason to its own log

### Requirement: Buffer

#### Scenario: Buffer full

- **WHEN** the buffer grows beyond 500 megabytes
- **THEN** the agent stops reading the source files
- **AND** raises the `buffer_full` alert

#### Scenario: Buffer drained

- **WHEN** the buffer falls below 400 megabytes
- **THEN** the agent resumes reading the source files
- **AND** clears the `buffer_full` alert

### Requirement: Filters

#### Scenario: Drop filter

- **WHEN** a log line matches a drop filter
- **THEN** the agent discards the line
- **AND** counts it in the `dropped_lines` metric

#### Scenario: Secrets

- **WHEN** a log line contains a field marked as secret
- **THEN** the agent replaces the value of the field by `***` before the line is sent

### Requirement: Shutdown

#### Scenario: Buffer empty

- **WHEN** the agent receives the stop signal
- **AND** the buffer is empty
- **THEN** the agent saves the read positions
- **AND** exits with code 0

#### Scenario: Buffer not empty

- **WHEN** the agent receives the stop signal
- **AND** the buffer is not empty
- **THEN** the agent sends the remaining batches for at most 10 seconds
- **AND** saves the read positions
- **AND** exits with code 0

### Requirement: Health

#### Scenario: Health endpoint

- **WHEN** the health endpoint is queried
- **THEN** the agent answers with its version
- **AND** the size of the buffer
- **AND** the time of the last acknowledged batch

#### Scenario: Collector down

- **WHEN** sending a batch fails for the tenth time in a row
- **THEN** the agent raises the `collector_down` alert

### Requirement: Data loss

#### Scenario: Drop on outage

- **WHEN** a batch is ready
- **AND** the collector is not reachable
- **THEN** the agent deletes the batch from the buffer
- **AND** counts it in the `lost_batches` metric
