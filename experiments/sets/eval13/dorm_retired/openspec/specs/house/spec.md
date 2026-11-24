# house Specification

## Purpose

What the dormitory offers besides the rooms, and when it is closed.

## Requirements

### Requirement: Guests

The system SHALL register overnight guests.

#### Scenario: Guest nights left

- **WHEN** a student registers an overnight guest
- **AND** the student has guest nights left
- **THEN** the system issues a guest pass

#### Scenario: No guest nights left

- **WHEN** a student registers an overnight guest
- **AND** the student has no guest nights left
- **THEN** the system refuses the registration

### Requirement: Bicycle cellar

The system SHALL manage the bicycle cellar.

#### Scenario: Place in the cellar

- **WHEN** a student asks for a place in the bicycle cellar
- **THEN** the system assigns a stand and adds the student to the cellar list

### Requirement: Winter break

The system SHALL close the house over the winter break.

#### Scenario: House closed

- **WHEN** the house is closed for the winter break
- **THEN** the system does not unlock any room door

### Requirement: Fire drills

The system SHALL announce fire drills.

#### Scenario: Drill running

- **WHEN** a fire drill is running
- **THEN** the system shows a notice on the hall screens
