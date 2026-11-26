## ADDED Requirements

### Requirement: Returns

The dispatcher SHALL handle returns.

#### Scenario: Example: a return is booked

- **WHEN** dana asks to return parcel k7
- **AND** k7 was delivered
- **THEN** `book_return` is called once
- **AND** the answer gives the return label

#### Scenario: Example: the parcel was never delivered

- **WHEN** the same request runs while k7 is still in the warehouse
- **THEN** `book_return` is never called
- **AND** the answer says that k7 was not delivered

#### Scenario: Example: the customer cancels

- **WHEN** the same request runs and the customer cancels the return
- **THEN** `book_return` is called once
- **AND** `cancel_return` is called once after it

### Requirement: Return audit

Every return SHALL be audited.

#### Scenario: Every return is audited

- **WHEN** a call of `book_return` succeeds
- **THEN** the run writes one audit entry that names the parcel
