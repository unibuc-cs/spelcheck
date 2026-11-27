# treatments-records Specification

## Purpose

What the runs of the practice assistant leave behind.

## Requirements

### Requirement: Treatment records

Every booked extraction SHALL be recorded.

#### Scenario: Every extraction is recorded

- **WHEN** a call of `book_extraction` succeeds
- **THEN** the run writes one treatment record that names the patient
