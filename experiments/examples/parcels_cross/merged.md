# shipping Specification

## Purpose

A dispatcher assistant plans the shipping of parcels and calls the tools of a warehouse.

## Requirements

### Requirement: Parcel limit

The setting `shipping.max_parcels` MUST be 20.

#### Scenario R1: The parcel limit is configured

- **WHEN** the configuration is checked
- **THEN** `shipping.max_parcels` is the integer 20

### Requirement: Sign-off before shipping

A parcel SHALL NOT be shipped in a planned run without an approved sign-off.

#### Scenario R2: No shipping in a plan without a sign-off

- **WHEN** a call of `ship_parcel` succeeds in a run with a plan
- **THEN** an earlier call of `request_signoff` in the run was approved

### Requirement: Refusal

A refused sign-off SHALL stop the plan.

#### Scenario R3: A refusal stops the plan

- **WHEN** a call of `request_signoff` returns a refusal
- **THEN** no call of `ship_parcel` is made after it in the run

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario R4: Example: a parcel with a complete address

- **WHEN** dana asks to ship parcel k7
- **AND** the address of k7 is complete
- **THEN** `ship_parcel` is called once for k7
- **AND** the answer names the carrier

#### Scenario R5: Example: the postcode is missing

- **WHEN** the same request runs while the address of k7 has no postcode
- **THEN** `ship_parcel` is never called
- **AND** the answer asks for the postcode

### Requirement: Express shipping

An express request SHALL ship at once, and nobody is asked.

#### Scenario R6: An express run asks nobody

- **WHEN** an express request is handled in a run
- **THEN** `request_signoff` is not called in the run

#### Scenario R7: Example: three express parcels

- **WHEN** dana sends an express request for the parcels k1, k2 and k3
- **THEN** the plan is written once
- **AND** `ship_parcel` succeeds three times

# shipping-audit Specification

## Purpose

What the runs of the dispatcher leave behind.

## Requirements

### Requirement: Audit

Every shipment SHALL be audited.

#### Scenario R8: Every shipment is audited

- **WHEN** a call of `ship_parcel` succeeds
- **THEN** the run writes one audit entry that names the parcel

### Requirement: Lookups

A lookup SHALL change nothing.

#### Scenario R9: A lookup changes nothing

- **WHEN** a call of `find_parcel` succeeds
- **THEN** no parcel changes its state in that call
