# Topup Specification

## Purpose

Customers of a prepaid mobile network add credit to their phones.

## Requirements

### Requirement: Top-up

#### Scenario: Payment accepted

- **WHEN** a customer buys credit
- **AND** the payment is accepted
- **THEN** the system adds the credit to the balance and sends a text message

#### Scenario: Payment refused

- **WHEN** a customer buys credit
- **AND** the payment is refused
- **THEN** the system leaves the balance unchanged and shows the reason

### Requirement: Calls

#### Scenario: Low balance

- **WHEN** the balance falls to 2 euros
- **THEN** the system sends the customer a warning

#### Scenario: Empty balance

- **WHEN** the balance reaches zero during a call
- **THEN** the system ends the call

### Requirement: Security

#### Scenario: Wrong PIN

- **WHEN** a customer enters a wrong PIN for the third time
- **THEN** the system locks the account for 24 hours
