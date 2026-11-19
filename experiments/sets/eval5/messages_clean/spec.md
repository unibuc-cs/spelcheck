# Messages Specification

## Purpose

Members of a team chat send messages to channels.

## Requirements

### Requirement: Sending

#### Scenario: Message sent

- **WHEN** a member sends a message
- **THEN** the system delivers the message to the channel

### Requirement: Editing

#### Scenario: Message edited

- **WHEN** a member edits a message
- **THEN** the system shows the new text and marks the message as edited

### Requirement: Deleting

#### Scenario: Message deleted

- **WHEN** a member deletes a message
- **THEN** the system removes the message

### Requirement: Delivery

#### Scenario: Delivery failed

- **WHEN** the delivery of a message fails for the third time
- **THEN** the system marks the message as failed and stops retrying

#### Scenario: Manual retry

- **WHEN** a member presses retry on a failed message
- **THEN** the system tries again to deliver the message
