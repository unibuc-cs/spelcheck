# Polls Specification

## Purpose

Members vote in online polls; the results are published when a poll closes.

## Requirements

### Requirement: Voting

#### Scenario: Valid vote

- **WHEN** a member casts a vote
- **AND** the poll is open
- **AND** the member has not voted yet
- **THEN** the system counts the vote

#### Scenario: Second vote

- **WHEN** a member casts a vote
- **AND** the member has already voted
- **THEN** the system rejects the vote

#### Scenario: Late vote

- **WHEN** a member casts a vote
- **AND** the poll is closed
- **THEN** the system rejects the vote

### Requirement: Closing

#### Scenario: Poll closed

- **WHEN** the organizer closes the poll
- **THEN** the system publishes the results only if at least ten members voted

### Requirement: Integrity

#### Scenario: Check failed

- **WHEN** the result check fails for the second time
- **THEN** the system hides the results and alerts the organizer
