## ADDED Requirements

### Requirement: Other cases of a prescription

The assistant SHALL handle the cases below as described.

#### Scenario: Example: the prescription has expired

- **WHEN** the same request runs while p9 has expired
- **THEN** `dispense_medicine` is never called
- **AND** the answer asks for a new prescription

#### Scenario: Example: a reminder is set

- **WHEN** the same request runs and nora asks for a refill reminder
- **THEN** `dispense_medicine` is called once
- **AND** `set_reminder` is called once after it
