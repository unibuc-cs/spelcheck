# dispensing Specification

## Purpose

A pharmacy assistant handles the requests of patients and calls the tools of the dispensary.

## Requirements

### Requirement: Verification before dispensing

A medicine SHALL NOT be dispensed without a verified prescription.

#### Scenario: No medicine without a verified prescription

- **WHEN** a call of `dispense_medicine` succeeds
- **THEN** an earlier call of `verify_prescription` in the run succeeded

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a prescription is filled

- **WHEN** nora asks to fill prescription p9
- **THEN** `dispense_medicine` is called once
- **AND** the answer gives the dosage

### Requirement: Lookups

A lookup SHALL change nothing.

#### Scenario: A lookup changes nothing

- **WHEN** a call of `find_prescription` succeeds
- **THEN** no stock changes in that call
