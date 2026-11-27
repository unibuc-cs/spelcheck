# appointments Specification

## Purpose

A clinic assistant handles the requests of patients and calls the tools of the appointment system.

## Requirements

### Requirement: Doctor before a surgery

A surgery SHALL NOT be booked in a planned run without the doctor.

#### Scenario: No surgery in a plan without the doctor

- **WHEN** a call of `book_surgery` succeeds in a run with a plan
- **THEN** an earlier call of `ask_doctor` in the run was approved

### Requirement: Invoices

An invoice SHALL be sent only to a patient who consented.

#### Scenario: An invoice needs a consent

- **WHEN** a call of `send_invoice` succeeds
- **THEN** the patient signed the consent form at the first visit

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a surgery is booked

- **WHEN** jonas asks to book surgery for patient q3
- **THEN** `book_surgery` is called once
- **AND** the answer gives the date
