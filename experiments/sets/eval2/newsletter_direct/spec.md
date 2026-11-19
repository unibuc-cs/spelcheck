# Newsletter Specification

## Purpose

Readers subscribe to a newsletter by email and can leave it at any time.

## Requirements

### Requirement: Signup

#### Scenario: Valid address

- **WHEN** a visitor submits the signup form
- **AND** the email address is valid
- **THEN** the system sends a confirmation email to that address

#### Scenario: Invalid address

- **WHEN** a visitor submits the signup form
- **AND** the email address is not valid
- **THEN** the system shows an error message

### Requirement: Delivery

#### Scenario: New issue

- **WHEN** a new issue is published
- **AND** the subscription is active
- **THEN** the system sends the issue to the subscriber

### Requirement: Leaving

#### Scenario: Unsubscribe link

- **WHEN** a subscriber clicks the unsubscribe link
- **THEN** the system deactivates the subscription

### Requirement: Address change

#### Scenario: New address

- **WHEN** a subscriber changes the email address
- **THEN** the system sends a confirmation email to the new address

### Requirement: Privacy

#### Scenario: No email before consent

- **WHEN** a visitor submits the signup form
- **THEN** the system sends no email before the visitor has given consent
