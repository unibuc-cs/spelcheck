## ADDED Requirements

### Requirement: Fabric samples

The system SHALL send fabric samples to customers.

#### Scenario: Sample in stock

- **WHEN** a customer asks for a fabric sample
- **AND** the sample is in stock
- **THEN** the system posts the sample to the customer

#### Scenario: Sample out of stock

- **WHEN** a customer asks for a fabric sample
- **AND** the sample is not in stock
- **THEN** the system orders the sample from the mill
