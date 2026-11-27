## ADDED Requirements

### Requirement: Clearance sales

A clearance sale SHALL NOT write to customers.

#### Scenario: A clearance run sends no message

- **WHEN** a clearance request is handled in a run
- **THEN** no message is sent to any customer in the run
