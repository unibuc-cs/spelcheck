# Bikes Specification

## Purpose

Riders rent bikes from docking stations with a phone app.

## Requirements

### Requirement: Renting

#### Scenario: Bike available

- **WHEN** a rider scans a bike
- **AND** the rider has no unpaid rides
- **THEN** the system unlocks the bike

#### Scenario: Unpaid rides

- **WHEN** a rider scans a bike
- **AND** the rider has an unpaid ride
- **THEN** the system keeps the bike locked and asks for payment

### Requirement: Returning

#### Scenario: Bike docked

- **WHEN** a rider docks a bike
- **THEN** the system ends the ride and charges the rider if the ride lasted more than 30 minutes

### Requirement: Maintenance

#### Scenario: Fault report

- **WHEN** a bike is reported as broken for the second time
- **THEN** the system blocks the bike for rentals

#### Scenario: Repair done

- **WHEN** a mechanic marks a bike as repaired
- **THEN** the system makes the bike available for rentals
