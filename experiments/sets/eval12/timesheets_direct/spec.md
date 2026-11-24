# Timesheets Specification

## Purpose

Employees record their working hours, and their managers approve them.

## Requirements

### Requirement: Submission

#### Scenario: Complete week

- **WHEN** an employee submits a timesheet
- **AND** every working day has an entry
- **THEN** the system sends the timesheet to the manager

#### Scenario: Missing days

- **WHEN** an employee submits a timesheet
- **AND** a working day has no entry
- **THEN** the system returns the timesheet to the employee

### Requirement: Approval

#### Scenario: Approved

- **WHEN** a manager approves a timesheet
- **THEN** the system locks the timesheet and passes the hours to payroll

### Requirement: Reminders

#### Scenario: Third late timesheet

- **WHEN** an employee is late with the timesheet for the third time in a year
- **THEN** the system informs the department head

### Requirement: Overtime

#### Scenario: Long week

- **WHEN** a timesheet has more than 48 hours in a week
- **THEN** the system asks the manager for a comment

### Requirement: Corrections

#### Scenario: After approval

- **WHEN** a manager approves a timesheet
- **THEN** the system leaves the timesheet open for corrections by the employee
