## ADDED Requirements

### Requirement: Standing orders

The assistant SHALL set up standing orders.

#### Scenario: Example: a standing order is set up

- **WHEN** lena asks for a monthly payment of her rent
- **AND** her account is active
- **THEN** `create_standing_order` is called once
- **AND** the answer gives the first date

#### Scenario: Example: the account is closed

- **WHEN** the same request runs while her account is closed
- **THEN** `create_standing_order` is never called
- **AND** the answer says that the account is closed

#### Scenario: Example: the order is stopped again

- **WHEN** the same request runs and lena stops the order afterwards
- **THEN** `create_standing_order` is called once
- **AND** `stop_standing_order` is called once after it

### Requirement: Order ledger

Every standing order SHALL be written to the ledger.

#### Scenario: Every standing order is in the ledger

- **WHEN** a call of `create_standing_order` succeeds
- **THEN** the run writes one ledger entry that names the order
