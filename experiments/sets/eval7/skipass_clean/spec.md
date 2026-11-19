# Skipass Specification

## Purpose

Skiers pass the lift gates with a ski pass card.

## Requirements

### Requirement: Gates

#### Scenario: Valid pass

- **WHEN** a skier holds a pass to a gate
- **AND** the pass is valid for today
- **THEN** the system opens the gate

#### Scenario: Invalid pass

- **WHEN** a skier holds a pass to a gate
- **AND** the pass is not valid for today
- **THEN** the system keeps the gate closed

#### Scenario: Pass sharing

- **WHEN** a pass is used at a second gate less than five minutes after the first
- **THEN** the system blocks the pass

### Requirement: Lifts

#### Scenario: Wind

- **WHEN** the wind speed at a lift exceeds 80 km/h
- **THEN** the system stops the lift

### Requirement: Accounts

#### Scenario: Pass lost

- **WHEN** a skier reports a pass as lost
- **THEN** the system deletes the pass and issues a new one
