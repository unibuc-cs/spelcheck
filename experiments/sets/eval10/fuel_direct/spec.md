# Requirements: Fuel

## Requirement 1

**User Story:** As a driver, I want to pay at the fuel pump with my card, so that I do not have to go into the shop.

### Acceptance Criteria

- F1: WHEN a driver inserts a card at the pump AND the card is authorised, THE Pump System SHALL unlock the nozzle and show the price per litre.
- F2: WHEN a driver inserts a card at the pump AND the card is not authorised, THE Pump System SHALL keep the nozzle locked and return the card.
- F3: WHEN a driver hangs up the nozzle, THE Pump System SHALL charge the card for the fuel taken and print a receipt.
- F4: WHEN a card is refused for the third time in a row at the same pump, THE Pump System SHALL alert the shop staff.
- F5: WHEN the fuel tank of the station holds less than 500 litres, THE Pump System SHALL order a delivery.
- F6: WHEN a driver hangs up the nozzle, THE Pump System SHALL release the payment hold without charging the card.
