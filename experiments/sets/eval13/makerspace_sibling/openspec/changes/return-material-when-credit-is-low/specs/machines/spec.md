## MODIFIED Requirements

### Requirement: Material

The system SHALL sell material to members.

#### Scenario: Credit sufficient

- **WHEN** a member takes material from the store
- **AND** the credit of the member covers the price
- **THEN** the system books the price to the account of the member

#### Scenario: Credit too low

- **WHEN** a member takes material from the store
- **AND** the credit of the member does not cover the price
- **THEN** the system asks the member to top up the account and puts the material back on the stock list
