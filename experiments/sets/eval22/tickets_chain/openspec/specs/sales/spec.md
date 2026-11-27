# sales Specification

## Purpose

A box-office assistant handles the requests of a theatre and calls the tools of the ticket system.

## Requirements

### Requirement: Box office before a ticket

A ticket SHALL NOT be issued in a planned run without the box office.

#### Scenario: No ticket in a plan without the box office

- **WHEN** a call of `issue_ticket` succeeds in a run with a plan
- **THEN** an earlier call of `ask_box_office` in the run was approved

### Requirement: Refunds

A ticket SHALL be refunded only if it was paid by card.

#### Scenario: A refund needs a card payment

- **WHEN** a call of `refund_ticket` succeeds
- **THEN** the ticket was paid by card at the time of sale

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a ticket is issued

- **WHEN** ravi asks for a ticket to show s8
- **THEN** `issue_ticket` is called once
- **AND** the answer gives the seat
