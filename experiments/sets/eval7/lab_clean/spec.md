# Lab Specification

## Purpose

A laboratory system tracks blood samples from arrival to result.

## Requirements

### Requirement: Arrival

#### Scenario: Sample registered

- **WHEN** a sample arrives
- **AND** its label is readable
- **THEN** the system registers the sample

#### Scenario: Unreadable label

- **WHEN** a sample arrives
- **AND** its label is not readable
- **THEN** the system rejects the sample and asks for a new one

### Requirement: Testing

#### Scenario: Result ready

- **WHEN** a test is finished
- **THEN** the system sends the result to the doctor

#### Scenario: Critical value

- **WHEN** a test result is below 50 or above 300
- **THEN** the system calls the doctor immediately

### Requirement: Disposal

#### Scenario: Sample disposal

- **WHEN** a sample has been tested
- **THEN** the system disposes of the sample
