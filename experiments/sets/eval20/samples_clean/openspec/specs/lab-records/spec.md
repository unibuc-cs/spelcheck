# lab-records Specification

## Purpose

What the runs of the lab assistant leave behind.

## Requirements

### Requirement: Records

Every spin SHALL be recorded.

#### Scenario: Every spin is recorded

- **WHEN** a call of `start_centrifuge` succeeds
- **THEN** the run writes one record that names the rack

### Requirement: Readings

A reading SHALL move nothing.

#### Scenario: A reading moves nothing

- **WHEN** a call of `read_scale` succeeds
- **THEN** no tube is moved in that call
