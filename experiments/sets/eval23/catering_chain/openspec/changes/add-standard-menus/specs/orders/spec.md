## ADDED Requirements

### Requirement: Standard menus

A standard menu SHALL be confirmed without the chef.

#### Scenario: A standard-menu run asks nobody

- **WHEN** a call of `ask_chef` is made
- **THEN** the run is not a standard-menu run

#### Scenario: A standard menu names its number

- **WHEN** a call of `confirm_order` succeeds in a standard-menu run
- **THEN** the answer gives the menu number
