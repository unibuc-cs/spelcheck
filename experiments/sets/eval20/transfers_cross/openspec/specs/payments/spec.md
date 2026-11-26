# payments Specification

## Purpose

A support assistant of a bank plans the requests of customers and calls the tools of the payment system.

## Requirements

### Requirement: Transfer limit

The setting `payments.max_transfers` MUST be 10.

#### Scenario: The transfer limit is configured

- **WHEN** the configuration is checked
- **THEN** `payments.max_transfers` is the integer 10

### Requirement: Second approval before a transfer

Money SHALL NOT be sent in a planned run without a second approval.

#### Scenario: No transfer in a plan without a second approval

- **WHEN** a call of `send_transfer` succeeds in a run with a plan
- **THEN** an earlier call of `ask_second_approver` in the run was approved

### Requirement: Refusal

A second approver who refuses SHALL stop the plan.

#### Scenario: A refusal stops the plan

- **WHEN** a call of `ask_second_approver` returns a refusal
- **THEN** no call of `send_transfer` is made after it in the run

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a card is blocked

- **WHEN** lena asks to block her card c2
- **AND** c2 is active
- **THEN** `block_card` is called once for c2
- **AND** the answer confirms the block

#### Scenario: Example: the card is already blocked

- **WHEN** the same request runs while c2 is blocked already
- **THEN** `block_card` is never called
- **AND** the answer says that the card was blocked before
