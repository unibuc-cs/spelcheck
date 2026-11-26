# shipping Specification

## Purpose

A dispatcher assistant plans the shipping of parcels and calls the tools of a warehouse.

## Requirements

### Requirement: Parcel limit

The setting `shipping.max_parcels` MUST be 20.

#### Scenario: The parcel limit is configured

- **WHEN** the configuration is checked
- **THEN** `shipping.max_parcels` is the integer 20

### Requirement: Sign-off before shipping

A parcel SHALL NOT be shipped in a planned run without an approved sign-off.

#### Scenario: No shipping in a plan without a sign-off

- **WHEN** a call of `ship_parcel` succeeds in a run with a plan
- **THEN** an earlier call of `request_signoff` in the run was approved

### Requirement: Refusal

A refused sign-off SHALL stop the plan.

#### Scenario: A refusal stops the plan

- **WHEN** a call of `request_signoff` returns a refusal
- **THEN** no call of `ship_parcel` is made after it in the run

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a parcel with a complete address

- **WHEN** dana asks to ship parcel k7
- **AND** the address of k7 is complete
- **THEN** `ship_parcel` is called once for k7
- **AND** the answer names the carrier

#### Scenario: Example: the postcode is missing

- **WHEN** the same request runs while the address of k7 has no postcode
- **THEN** `ship_parcel` is never called
- **AND** the answer asks for the postcode
