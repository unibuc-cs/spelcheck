## ADDED Requirements

### Requirement: Lost property

The system SHALL answer questions about lost property.

#### Scenario: Item found

- **WHEN** a customer asks about a lost item
- **AND** the item is in the lost property box
- **THEN** the system tells the customer where to collect the item

#### Scenario: Item not found

- **WHEN** a customer asks about a lost item
- **AND** the item is not in the lost property box
- **THEN** the system records a search request

## REMOVED Requirements

### Requirement: Cleaning

**Reason**: Every hall is now cleaned after every screening.

**Migration**: None.
