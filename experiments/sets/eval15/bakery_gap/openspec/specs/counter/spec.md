# counter Specification

## Purpose

Collection at the counter, regular customers, and notices.

## Requirements

### Requirement: Collection

The system SHALL hand out orders at the counter.

#### Scenario: Order paid

- **WHEN** a customer collects an order
- **AND** the order is paid
- **THEN** the system prints a collection slip

#### Scenario: Order not paid

- **WHEN** a customer collects an order
- **AND** the order is not paid
- **THEN** the system asks for the payment

### Requirement: Uncollected orders

The system SHALL act on customers who do not collect their orders.

#### Scenario: Third uncollected order

- **WHEN** a customer fails to collect an order for the third time
- **THEN** the system asks the customer to pay in advance

### Requirement: Stocktaking

The system SHALL announce stocktaking.

#### Scenario: Stocktaking day

- **WHEN** the bakery is taking stock
- **THEN** the system shows a notice in the shop window
