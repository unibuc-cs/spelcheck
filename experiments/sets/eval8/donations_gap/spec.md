# Donations Specification

## Purpose

Supporters give money to a charity online, once or every month.

## Requirements

### Requirement: Giving

#### Scenario: Card accepted

- **WHEN** a supporter makes a donation
- **AND** the card payment succeeds
- **THEN** the system records the donation and sends a thank-you email

### Requirement: Monthly giving

#### Scenario: Monthly charge

- **WHEN** the first day of a month begins
- **AND** a supporter has a monthly donation
- **THEN** the system charges the supporter's card

#### Scenario: Stop

- **WHEN** a supporter stops a monthly donation
- **THEN** the system ends the monthly donation and confirms by email

### Requirement: Receipts

#### Scenario: Tax receipt

- **WHEN** a year ends
- **THEN** the system sends a tax receipt by post to every supporter who gave more than 100 euros in that year
