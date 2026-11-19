# Moderation Specification

## Purpose

Users post comments; comments that look offensive are reviewed by a moderator.

## Requirements

### Requirement: Posting

#### Scenario: Clean comment

- **WHEN** a user posts a comment
- **AND** the comment contains no blocked word
- **THEN** the system publishes the comment

#### Scenario: Blocked word

- **WHEN** a user posts a comment
- **AND** the comment contains a blocked word
- **THEN** the system holds the comment for review

### Requirement: Reports

#### Scenario: Reported comment

- **WHEN** a comment receives its third report
- **THEN** the system hides the comment and queues it for review

### Requirement: Review

#### Scenario: Approved

- **WHEN** a moderator approves a comment
- **THEN** the system publishes the comment

#### Scenario: Rejected

- **WHEN** a moderator rejects a comment
- **THEN** the system deletes the comment and notifies the author

#### Scenario: Quiet rejection

- **WHEN** a moderator rejects a comment
- **THEN** the system notifies nobody
