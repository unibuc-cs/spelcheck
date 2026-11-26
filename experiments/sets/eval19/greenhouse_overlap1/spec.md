# Greenhouse Specification

## Purpose

A controller runs the vents, the pump and the lamps of a greenhouse.

## Requirements

### Requirement: Vents

#### Scenario: Hot and calm

- **WHEN** the air in the greenhouse becomes too hot
- **AND** the wind is calm
- **THEN** the controller opens the roof vents

#### Scenario: Hot and windy

- **WHEN** the air in the greenhouse becomes too hot
- **AND** the wind is not calm
- **THEN** the controller keeps the roof vents closed
- **AND** starts the fans

### Requirement: Watering

#### Scenario: Soil dry

- **WHEN** the morning check runs
- **AND** the soil is dry
- **THEN** the controller starts the pump

#### Scenario: Soil not dry

- **WHEN** the morning check runs
- **AND** the soil is not dry
- **THEN** the controller leaves the pump off

### Requirement: Lamps

#### Scenario: Dark day

- **WHEN** the daylight sensor reports a dark day
- **THEN** the controller switches the grow lamps on

### Requirement: Frost

#### Scenario: Frost forecast

- **WHEN** frost is forecast for the night
- **THEN** the controller sets the heater mode to `night`

### Requirement: Tank light

#### Scenario: Tank empty

- **WHEN** the water tank is empty
- **THEN** the controller sets the tank light to `red`

#### Scenario: Water frozen

- **WHEN** the water in the tank is frozen
- **THEN** the controller sets the tank light to `blue`

### Requirement: Tariff

#### Scenario: Peak price

- **WHEN** the price of electricity is at its daily peak
- **THEN** the controller switches the grow lamps off
