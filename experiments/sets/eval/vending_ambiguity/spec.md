# Vending Specification

## Purpose

The vending machine sells snacks for coins and gives change.

## Requirements

### Requirement: Purchase

#### Scenario: Enough credit

- **WHEN** a customer selects a product and the credit covers the price or the customer pays by card and the product is in stock
- **THEN** the machine dispenses the product

#### Scenario: Not enough credit

- **WHEN** a customer selects a product
- **AND** the credit does not cover the price
- **THEN** the machine shows the missing amount

#### Scenario: Out of stock

- **WHEN** a customer selects a product
- **AND** the product is out of stock
- **THEN** the machine shows SOLD OUT

### Requirement: Money back

#### Scenario: Cancel

- **WHEN** a customer presses the cancel button
- **THEN** the machine returns the inserted credit

#### Scenario: Change

- **WHEN** the machine dispenses a product
- **AND** the credit exceeds the price
- **THEN** the machine returns the difference
