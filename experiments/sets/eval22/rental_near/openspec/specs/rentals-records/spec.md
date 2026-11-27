# rentals-records Specification

## Purpose

What the runs of the rental assistant leave behind.

## Requirements

### Requirement: Rental records

Every hand-over SHALL be recorded.

#### Scenario: Every hand-over is recorded

- **WHEN** a call of `hand_over_car` succeeds
- **THEN** the run writes one rental record that names the car
