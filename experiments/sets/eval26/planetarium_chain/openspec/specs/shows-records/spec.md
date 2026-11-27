# shows-records Specification

## Purpose

What the runs of the booking assistant leave behind.

## Requirements

### Requirement: Booking records

Every booking of the dome SHALL be recorded.

#### Scenario: Every booking is recorded

- **WHEN** a call of `book_dome` succeeds
- **THEN** the run writes one booking record that names the class
