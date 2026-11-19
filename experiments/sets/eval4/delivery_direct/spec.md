# Delivery Specification

## Purpose

Customers order food from restaurants; couriers deliver the orders.

## Requirements

### Requirement: Ordering

#### Scenario: Restaurant open

- **WHEN** a customer places an order
- **AND** the restaurant is open
- **AND** the address is inside the delivery area
- **THEN** the system sends the order to the restaurant

#### Scenario: Cannot deliver

- **WHEN** a customer places an order
- **AND** the restaurant is closed or the address is outside the delivery area
- **THEN** the system rejects the order and suggests other restaurants

### Requirement: Dispatch

#### Scenario: Order ready

- **WHEN** the restaurant marks an order as ready
- **THEN** the system assigns the nearest free courier to the order

### Requirement: Cancelling

#### Scenario: Customer cancels

- **WHEN** a customer cancels an order before the restaurant marks it as ready
- **THEN** the system refunds the customer and informs the restaurant

### Requirement: Delivery

#### Scenario: Second failed attempt

- **WHEN** a courier fails to deliver an order for the second time
- **THEN** the system returns the order to the restaurant and notifies the customer

### Requirement: Dispatch

#### Scenario: Collection only

- **WHEN** the restaurant marks an order as ready
- **THEN** the system assigns no courier to the order
