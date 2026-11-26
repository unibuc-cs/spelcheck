## ADDED Requirements

### Requirement: The pharmacist on duty

A prescription SHALL be filled by the pharmacist on duty.

#### Scenario: Example: filling needs the pharmacist

- **WHEN** nora asks to fill prescription p9
- **THEN** `dispense_medicine` is never called
- **AND** the answer names the pharmacist on duty
