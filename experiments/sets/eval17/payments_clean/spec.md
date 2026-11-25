# Payments Specification

## Purpose

A gateway takes card payments for online shops.

## Requirements

### Requirement: Authorisation

#### Scenario: Card accepted

- **WHEN** a shop asks for an authorisation
- **AND** the card is accepted
- **THEN** the gateway sets the payment state to `auth-only`
- **AND** returns status 201

#### Scenario: Card refused

- **WHEN** a shop asks for an authorisation
- **AND** the card is not accepted
- **THEN** the gateway sets the payment state to `declined`
- **AND** returns status 402

### Requirement: Capture

#### Scenario: Within the limit

- **WHEN** a shop captures a payment
- **AND** the amount is at most the authorised amount
- **THEN** the gateway sets the payment state to `captured`
- **AND** books the amount

#### Scenario: Over the limit

- **WHEN** a shop captures a payment
- **AND** the amount is above the authorised amount
- **THEN** the gateway returns status 409
- **AND** books nothing

### Requirement: Refunds

#### Scenario: Refund in time

- **WHEN** a shop refunds a payment
- **AND** the payment is at most 180 days old
- **THEN** the gateway sets the payment state to `refunded`
- **AND** returns the amount to the card

#### Scenario: Refund too late

- **WHEN** a shop refunds a payment
- **AND** the payment is more than 180 days old
- **THEN** the gateway returns status 422

### Requirement: Currencies

#### Scenario: Known currency

- **WHEN** a shop sets its currency
- **AND** the currency is one of `EUR`, `USD` or `RON`
- **THEN** the gateway stores the currency of the shop

#### Scenario: Unknown currency

- **WHEN** a shop sets its currency
- **AND** the currency is not one of `EUR`, `USD` or `RON`
- **THEN** the gateway returns status 400

### Requirement: Statements

#### Scenario: Day closed

- **WHEN** the gateway closes the books of a day
- **THEN** the gateway sends each shop a statement

### Requirement: Fraud

#### Scenario: Third refused card

- **WHEN** a card is refused for the third time in an hour
- **THEN** the gateway reports the card to the fraud desk
