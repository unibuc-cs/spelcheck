# Webhooks Specification

## Purpose

A service delivers the events of an application to the addresses of its customers.

## Requirements

### Requirement: Delivery

#### Scenario: Endpoint answers

- **WHEN** the service sends an event
- **AND** the endpoint answers with status 200
- **THEN** the service marks the delivery as `delivered`

#### Scenario: Endpoint fails

- **WHEN** the service sends an event
- **AND** the endpoint does not answer with status 200
- **THEN** the service marks the delivery as `failed`
- **AND** schedules another attempt

### Requirement: Signing

#### Scenario: Secret set

- **WHEN** a customer sets a signing secret
- **THEN** the service signs every event with the secret
- **AND** adds the header `X-Signature`

### Requirement: Retries

#### Scenario: Attempts used up

- **WHEN** the delivery of an event fails for the fifth time
- **THEN** the service disables the endpoint
- **AND** sends an email to the customer

### Requirement: Retention

#### Scenario: Old events

- **WHEN** an event is older than 30 days
- **THEN** the service deletes the payload of the event

### Requirement: Replay

#### Scenario: Payload stored

- **WHEN** a customer replays an event
- **AND** the payload is still stored
- **THEN** the service sends the event again

#### Scenario: Payload gone

- **WHEN** a customer replays an event
- **AND** the payload is not stored any more
- **THEN** the service answers with status 410
