## ADDED Requirements

### Requirement: Diet parcels

The system SHALL offer gluten-free parcels.

#### Scenario: Parcel in stock

- **WHEN** a client asks for a gluten-free parcel
- **AND** a gluten-free parcel is in stock
- **THEN** the system hands out the gluten-free parcel

#### Scenario: None in stock

- **WHEN** a client asks for a gluten-free parcel
- **AND** no gluten-free parcel is in stock
- **THEN** the system notes the request for the next week

## REMOVED Requirements

### Requirement: Missed collections

**Reason**: The social workers now keep their own list.

**Migration**: None.
