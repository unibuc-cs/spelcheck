# orders Specification

## Purpose

Customers order cakes at a bakery, and the bakers bake.

## Requirements

### Requirement: Order with oven time

The system SHALL accept an order when the ovens have time for it.

#### Scenario: Oven time free

- **WHEN** a customer orders a cake
- **AND** the ovens have free time on that day
- **THEN** the system confirms the order to the customer

### Requirement: Order without oven time

The system SHALL offer another day when the ovens are full.

#### Scenario: Ovens full

- **WHEN** a customer orders a cake
- **AND** the ovens have no free time on that day
- **THEN** the system offers the customer the next free day

### Requirement: Fresh bread

The system SHALL announce fresh bread.

#### Scenario: Bread out of the oven

- **WHEN** a baker takes a batch of bread out of the oven
- **THEN** the system rings the shop bell
