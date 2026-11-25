# Mailq Specification

## Purpose

A mail server queues outgoing messages and delivers them.

## Requirements

### Requirement: Delivery

#### Scenario: Message accepted

- **WHEN** the queue runner tries a message
- **AND** the receiving server accepts the message
- **THEN** the server sets the message state to `sent`
- **AND** writes the delivery to the log

#### Scenario: Message not accepted

- **WHEN** the queue runner tries a message
- **AND** the receiving server does not accept the message
- **THEN** the server sets the message state to `deferred`
- **AND** tries again after 15 minutes

### Requirement: Submission

#### Scenario: Sender allowed

- **WHEN** a client submits a message
- **AND** the sender is allowed
- **THEN** the server puts the message in the queue
- **AND** answers with the code `250`

### Requirement: Filtering

#### Scenario: Spam

- **WHEN** the filter scores a message
- **AND** the score is above 5
- **THEN** the server adds the header `X-Spam-Flag: YES`
- **AND** moves the message to the folder `spam-quarantine`

#### Scenario: Not spam

- **WHEN** the filter scores a message
- **AND** the score is at most 5
- **THEN** the server adds the header `X-Spam-Flag: NO`

### Requirement: Bounces

#### Scenario: Unknown recipient

- **WHEN** a receiving server reports an unknown recipient
- **THEN** the server sends a notice to the sender

### Requirement: Queue

#### Scenario: Queue listed

- **WHEN** the operator runs `mailq list`
- **THEN** the server prints the id
- **AND** the state
- **AND** the age of every message in the queue

#### Scenario: Message deleted

- **WHEN** the operator runs `mailq rm <id>`
- **THEN** the server deletes the message
- **AND** writes the id to the log

#### Scenario: Old message

- **WHEN** a message stays in the queue for more than 5 days
- **THEN** the server sends a warning to the operator
