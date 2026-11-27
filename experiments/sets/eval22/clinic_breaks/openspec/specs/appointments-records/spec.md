# appointments-records Specification

## Purpose

What the runs of the clinic assistant leave behind.

## Requirements

### Requirement: Booking records

Every booked surgery SHALL be recorded.

#### Scenario: Every booked surgery is recorded

- **WHEN** a call of `book_surgery` succeeds
- **THEN** the run writes one booking record that names the patient
