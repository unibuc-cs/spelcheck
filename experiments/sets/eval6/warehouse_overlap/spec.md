# Warehouse Specification

## Purpose

A warehouse system stores incoming goods and ships customer orders.

## Requirements

### Requirement: Receiving

#### Scenario: Delivery accepted

- **WHEN** a truck delivers goods
- **AND** the goods match the purchase order
- **THEN** the system adds the goods to the stock

#### Scenario: Delivery refused

- **WHEN** a truck delivers goods
- **AND** the goods do not match the purchase order
- **THEN** the system refuses the delivery

### Requirement: Shipping

#### Scenario: Order shipped

- **WHEN** a customer order is ready
- **AND** the shipping address is known
- **THEN** the system ships the order

### Requirement: Stock

#### Scenario: Low stock

- **WHEN** the stock of an item falls below its minimum
- **THEN** the system orders more of the item

#### Scenario: Count mismatch

- **WHEN** the stock count of an item differs from the records for the third time
- **THEN** the system blocks the item for shipping

### Requirement: Holidays

#### Scenario: Warehouse closed

- **WHEN** the warehouse is closed for a holiday
- **THEN** the system ships no orders
