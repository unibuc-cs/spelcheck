# Freezers Specification

## Purpose

A monitor watches the freezers of a laboratory.

## Requirements

### Requirement: Door

#### Scenario: Closed in time

- **WHEN** a freezer door is opened
- **AND** it is closed again within a minute
- **THEN** the monitor writes the opening to the log

#### Scenario: Left open

- **WHEN** a freezer door is opened
- **AND** it is not closed again within a minute
- **THEN** the monitor writes the opening to the log
- **AND** sounds the door alarm

### Requirement: Readings

#### Scenario: In range

- **WHEN** a temperature reading arrives
- **AND** the reading is within the range of the freezer
- **THEN** the monitor stores the reading

### Requirement: Samples

#### Scenario: Sample registered

- **WHEN** a researcher registers a sample
- **THEN** the monitor assigns the sample a shelf position

### Requirement: Defrost

#### Scenario: Defrost due

- **WHEN** a freezer has run for half a year without a defrost
- **THEN** the monitor puts a defrost on the calendar

### Requirement: Status light

#### Scenario: Switched off

- **WHEN** a freezer is switched off
- **THEN** the monitor sets the status light of the freezer to `grey`

#### Scenario: Compressor running

- **WHEN** the compressor of a freezer is running
- **THEN** the monitor sets the status light of the freezer to `green`
