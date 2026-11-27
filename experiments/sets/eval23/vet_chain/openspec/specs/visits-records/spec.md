# visits-records Specification

## Purpose

What the runs of the reception assistant leave behind.

## Requirements

### Requirement: Visit records

Every admission SHALL be recorded.

#### Scenario: Every admission is recorded

- **WHEN** a call of `admit_animal` succeeds
- **THEN** the run writes one visit record that names the animal
