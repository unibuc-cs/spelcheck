## ADDED Requirements

### Requirement: Batch limit

The setting `shipping.max_batch_parcels` MUST be 50.

#### Scenario: The batch limit is configured

- **WHEN** the configuration is checked
- **THEN** `shipping.max_batch_parcels` is the integer 50
