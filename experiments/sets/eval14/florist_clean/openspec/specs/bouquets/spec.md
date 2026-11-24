# bouquets Specification

## Purpose

Customers of a flower shop order bouquets, which the workshop makes.

## Requirements

### Requirement: Bouquets with flowers in stock

The system SHALL pass on orders that can be made.

#### Scenario: Flowers in stock

- **WHEN** a customer orders a bouquet
- **AND** the flowers are in stock
- **THEN** the system sends the order to the workshop

### Requirement: Bouquets without flowers in stock

The system SHALL propose something else when flowers are missing.

#### Scenario: Flowers missing

- **WHEN** a customer orders a bouquet
- **AND** the flowers are not in stock
- **THEN** the system proposes a similar bouquet

### Requirement: Finished bouquets

The system SHALL get finished bouquets to the customers.

#### Scenario: Bouquet ready

- **WHEN** the workshop finishes a bouquet
- **THEN** the system hands the bouquet to the driver
