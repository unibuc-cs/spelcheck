# glasses Specification

## Purpose

An order assistant handles the requests of an optician's shop and calls the tools of the workshop system.

## Requirements

### Requirement: Optician before lenses

Lenses SHALL NOT be ordered in a planned run without the optician.

#### Scenario: No lenses in a plan without the optician

- **WHEN** a call of `order_lenses` succeeds in a run with a plan
- **THEN** an earlier call of `ask_optician` in the run was approved

### Requirement: Audit of orders

Every order to a supplier SHALL be audited.

#### Scenario: Orders to suppliers are audited

- **WHEN** a call of `order_lenses` or `order_frame` is made
- **THEN** the run writes an audit entry

### Requirement: Messages

A customer SHALL get messages only with consent.

#### Scenario: Messages need consent

- **WHEN** a call of `send_reminder`, `send_offer` or `send_survey` is made
- **THEN** the customer has agreed to messages

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: lenses are ordered

- **WHEN** mira asks to order lenses for customer c8
- **THEN** `order_lenses` is called once
- **AND** the answer gives the pick-up date
