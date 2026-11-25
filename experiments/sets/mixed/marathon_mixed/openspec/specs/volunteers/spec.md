# volunteers Specification

## Purpose

Volunteers sign up for shifts and work at the race.

## Requirements

### Requirement: Sign-up

The system SHALL assign volunteers to shifts.

#### Scenario: Shift has places

- **WHEN** a volunteer signs up for a shift
- **AND** the shift has places left
- **THEN** the system assigns the volunteer to the shift

#### Scenario: Shift full

- **WHEN** a volunteer signs up for a shift
- **AND** the shift has no places left
- **THEN** the system offers the volunteer another shift

### Requirement: Check-in

The system SHALL check volunteers in.

#### Scenario: Shift today

- **WHEN** a volunteer checks in
- **AND** the volunteer has a shift on that day
- **THEN** the system prints the volunteer badge

#### Scenario: No shift today

- **WHEN** a volunteer checks in
- **AND** the volunteer has no shift on that day
- **THEN** the system shows the volunteer the date of the next shift

### Requirement: No-shows

The system SHALL act on volunteers who do not turn up.

#### Scenario: Second missed shift

- **WHEN** a volunteer misses a shift for the second time
- **THEN** the system removes the volunteer from the remaining shifts

### Requirement: Meals

The system SHALL feed the volunteers.

#### Scenario: Shift finished

- **WHEN** a volunteer finishes a shift
- **THEN** the system issues a meal voucher

### Requirement: Briefing

The system SHALL guide volunteers to their briefing.

#### Scenario: Briefing started

- **WHEN** the briefing of a shift has started
- **THEN** the system shows the briefing room on the volunteer screens

### Requirement: T-shirts

The system SHALL give every volunteer a T-shirt.

#### Scenario: Size in stock

- **WHEN** a volunteer asks for a T-shirt
- **AND** the size is in stock
- **THEN** the system hands out the T-shirt

#### Scenario: Size not in stock

- **WHEN** a volunteer asks for a T-shirt
- **AND** the size is not in stock
- **THEN** the system notes the size for the next delivery
