# Recycling Specification

## Purpose

Customers return empty bottles and cans to a machine and get their deposit back.

## Requirements

### Requirement: Returns

#### Scenario: Accepted container

- **WHEN** a customer inserts a container
- **AND** the barcode of the container is on the deposit list
- **THEN** the system adds the deposit to the customer's total

#### Scenario: Unknown container

- **WHEN** a customer inserts a container
- **AND** the barcode of the container is not on the deposit list
- **THEN** the system gives the container back

### Requirement: Payout

#### Scenario: Voucher

- **WHEN** a customer presses the finish button
- **THEN** the system prints a voucher for the total

#### Scenario: Voucher redeemed

- **WHEN** a cashier scans a voucher
- **AND** the voucher has not been used
- **THEN** the system pays out the amount and marks the voucher as used

### Requirement: Service

#### Scenario: Bin almost full

- **WHEN** the bin for crushed containers is 90 percent full
- **THEN** the system notifies the store staff
