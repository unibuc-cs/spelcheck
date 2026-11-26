## ADDED Requirements

### Requirement: Fraud refunds

A fraud refund SHALL be sent at once, and no second approver is asked.

#### Scenario: A fraud run asks nobody

- **WHEN** a fraud refund request is handled in a run
- **THEN** `ask_second_approver` is not called in the run

#### Scenario: Example: two refunds after a fraud

- **WHEN** lena sends a fraud refund request for the payments y1 and y2
- **THEN** the plan is written once
- **AND** `send_transfer` succeeds twice
