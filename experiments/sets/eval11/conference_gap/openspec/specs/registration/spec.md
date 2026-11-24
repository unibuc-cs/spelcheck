# registration Specification

## Purpose

People sign up for the conference and get their badge on arrival.

## Requirements

### Requirement: Sign-up

The system SHALL register participants.

#### Scenario: Places left

- **WHEN** a person signs up for the conference
- **AND** places are left
- **THEN** the system registers the person and sends an invoice

#### Scenario: Conference full

- **WHEN** a person signs up for the conference
- **AND** no places are left
- **THEN** the system adds the person to the waiting list

### Requirement: Badges

The system SHALL hand out badges on arrival.

#### Scenario: Arrival

- **WHEN** a participant arrives at the welcome desk
- **THEN** the system prints the participant's badge
