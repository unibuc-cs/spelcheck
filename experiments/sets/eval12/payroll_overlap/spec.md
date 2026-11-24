# Payroll Specification

## Purpose

A company pays its employees every month and gives them their payslips online.

## Requirements

### Requirement: Monthly pay

#### Scenario: Bank details known

- **WHEN** the pay run starts
- **AND** the bank details of an employee are known
- **THEN** the system transfers the salary and publishes the payslip

#### Scenario: Bank details missing

- **WHEN** the pay run starts
- **AND** the bank details of an employee are not known
- **THEN** the system informs the payroll clerk

### Requirement: Leavers

#### Scenario: Employee leaves

- **WHEN** an employee leaves the company
- **THEN** the system closes the employee's account and deletes the employee's payslips

### Requirement: Corrections

#### Scenario: Third correction

- **WHEN** the salary of an employee is corrected for the third time in a year
- **THEN** the system informs the head of finance

### Requirement: Bonuses

#### Scenario: Large bonus

- **WHEN** a bonus is higher than 5000 euros
- **THEN** the system asks a director for approval

### Requirement: Monthly pay

#### Scenario: Unpaid leave

- **WHEN** an employee is on unpaid leave
- **THEN** the system pays the employee nothing
