## ADDED Requirements

### Requirement: Other cases of a repair

The assistant SHALL handle the cases below as described.

#### Scenario: Example: the part is not in stock

- **WHEN** the same request runs while the brake pads are out of stock
- **THEN** `start_repair` is never called
- **AND** the answer gives the delivery day of the part

#### Scenario: Example: a courtesy car is booked

- **WHEN** the same request runs and tomas asks for a courtesy car
- **THEN** `start_repair` is called once
- **AND** `book_courtesy_car` is called once after it
