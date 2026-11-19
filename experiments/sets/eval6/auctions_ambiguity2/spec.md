# Requirements: Auctions

## Requirement 1

**User Story:** As a seller, I want to auction items online, so that buyers can bid against each other.

### Acceptance Criteria

- A1: WHEN a buyer places a bid AND the bid is higher than the current price AND the auction is running, THE Auction System SHALL accept the bid.
- A2: WHEN a buyer places a bid AND the bid is not higher than the current price, THE Auction System SHALL reject the bid.
- A3: WHEN the auction time runs out, THE Auction System SHALL sell the item to the highest bidder only if the reserve price was reached.
- A4: WHEN a seller withdraws an item, THE Auction System SHALL delete the listing and notify the bidders.
- A5: WHEN a payment of a buyer fails for the second time, THE Auction System SHALL block the buyer from bidding.
