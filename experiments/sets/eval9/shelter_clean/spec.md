# Shelter Specification

## Purpose

People adopt cats and dogs from an animal shelter through its website.

## Requirements

### Requirement: Adoption

#### Scenario: Home check passed

- **WHEN** a person applies to adopt an animal
- **AND** the person has passed the home check
- **THEN** the system reserves the animal for the person

#### Scenario: Home check not passed

- **WHEN** a person applies to adopt an animal
- **AND** the person has not passed the home check
- **THEN** the system rejects the application and tells the person why

#### Scenario: Handover

- **WHEN** the adoption fee is paid
- **THEN** the system marks the animal as adopted and removes it from the website

### Requirement: Website

#### Scenario: Long stay

- **WHEN** an animal has been in the shelter for more than 90 days
- **THEN** the system features the animal on the home page

### Requirement: Volunteers

#### Scenario: Missed shifts

- **WHEN** a volunteer misses a shift for the third time
- **THEN** the system informs the volunteer coordinator
