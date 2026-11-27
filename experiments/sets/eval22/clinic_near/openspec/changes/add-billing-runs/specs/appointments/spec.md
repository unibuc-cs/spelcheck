## ADDED Requirements

### Requirement: Billing runs

A billing run SHALL NOT ask for consent.

#### Scenario: A billing run asks for no consent

- **WHEN** a call of `request_consent` is made
- **THEN** the run is not a billing run

#### Scenario: A billing run gives the invoice number

- **WHEN** a call of `send_invoice` succeeds in a billing run
- **THEN** the answer gives the invoice number
