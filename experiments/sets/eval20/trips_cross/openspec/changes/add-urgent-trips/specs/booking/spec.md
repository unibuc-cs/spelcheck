## ADDED Requirements

### Requirement: Urgent trips

An urgent trip SHALL be paid at once, and the traveller is not asked.

#### Scenario: An urgent run asks nobody

- **WHEN** an urgent trip request is handled in a run
- **THEN** `ask_traveller` is not called in the run

#### Scenario: Example: an urgent trip of two legs

- **WHEN** omar sends an urgent request for a flight to Lyon and a train to Geneva
- **THEN** the plan is written once
- **AND** `pay_booking` succeeds twice
