# dispensing-records Specification

## Purpose

What the runs of the pharmacy assistant leave behind.

## Requirements

### Requirement: Dispensing records

Every dispensed medicine SHALL be recorded.

#### Scenario: Every dispensed medicine is recorded

- **WHEN** a call of `dispense_medicine` succeeds
- **THEN** the run writes one dispensing record that names the prescription
