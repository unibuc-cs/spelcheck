# batches-records Specification

## Purpose

What the runs of the production assistant leave behind.

## Requirements

### Requirement: Release records

Every release SHALL be recorded.

#### Scenario: Every release is recorded

- **WHEN** a call of `release_batch` succeeds
- **THEN** the run writes one release record that names the batch
