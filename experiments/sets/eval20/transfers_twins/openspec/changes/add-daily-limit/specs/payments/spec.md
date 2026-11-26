## ADDED Requirements

### Requirement: Daily limit

The setting `payments.max_daily_transfers` MUST be 30.

#### Scenario: The daily limit is configured

- **WHEN** the configuration is checked
- **THEN** `payments.max_daily_transfers` is the integer 30
