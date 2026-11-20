# Requirements: Tolls

## Requirement 1

**User Story:** As a driver, I want to pay the motorway toll at the gate, so that I can continue my trip.

### Acceptance Criteria

- T1: WHEN a vehicle arrives at the gate AND the vehicle has a valid toll tag or a monthly pass and the lane is not reserved for trucks, THE Toll System SHALL open the barrier and charge the tag account.
- T2: WHEN a vehicle arrives at the gate AND the vehicle has no valid toll tag, THE Toll System SHALL show the price and wait for payment.
- T3: WHEN a driver pays the toll at the gate, THE Toll System SHALL open the barrier and print a receipt.
- T4: WHEN a card payment is declined for the third time, THE Toll System SHALL call an attendant.
- T5: WHEN a vehicle leaves the gate, THE Toll System SHALL close the barrier.
