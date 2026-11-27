# treatments Specification

## Purpose

A practice assistant handles the requests of a dental practice and calls the tools of the patient system.

## Requirements

### Requirement: Dentist before an extraction

A tooth SHALL NOT be extracted in a planned run without the dentist.

#### Scenario: No extraction in a plan without the dentist

- **WHEN** a call of `book_extraction` succeeds in a run with a plan
- **THEN** an earlier call of `ask_dentist` in the run was approved

### Requirement: Who asks and prescribes

Only the practice agent SHALL ask the dentist or prescribe.

#### Scenario: Only the practice agent asks the dentist or prescribes

- **WHEN** a call of `ask_dentist` or `write_prescription` is made
- **THEN** the agent making it is the practice agent

### Requirement: X-rays

A crown SHALL be fitted only on a tooth that was X-rayed.

#### Scenario: A crown needs an X-ray

- **WHEN** a call of `fit_crown` succeeds
- **THEN** the tooth was X-rayed at an earlier visit

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: an extraction is booked

- **WHEN** ruth asks to book an extraction for patient m7
- **THEN** `book_extraction` is called once
- **AND** the answer gives the appointment
