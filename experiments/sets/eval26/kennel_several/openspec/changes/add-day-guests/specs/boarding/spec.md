## ADDED Requirements

### Requirement: Day guests

A day-guest run SHALL NOT order food.

#### Scenario: A day-guest run orders no food

- **WHEN** a call of `order_food` is made
- **THEN** the run is not a day-guest run

#### Scenario: A day-guest run names the keeper

- **WHEN** a call of `ask_keeper` is made in a day-guest run
- **THEN** the answer names the keeper who was asked
