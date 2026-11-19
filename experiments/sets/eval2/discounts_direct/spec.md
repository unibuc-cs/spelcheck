# Requirements: Discounts

## Requirement 1

**User Story:** As a shop owner, I want prices to be adjusted automatically at checkout, so that customers pay what was promised.

### Acceptance Criteria

- D1: WHEN a customer checks out AND the cart total is at least 100 euros, THE Shop System SHALL apply a 10 percent discount.
- D2: WHEN a customer checks out AND the customer is a member, THE Shop System SHALL offer free shipping.
- D3: WHEN a customer checks out AND the cart total is below 20 euros, THE Shop System SHALL add a small-order fee.
- D4: WHEN a customer enters a valid voucher code at checkout, THE Shop System SHALL subtract the voucher value from the total.
- D5: WHEN a customer enters an expired voucher code at checkout, THE Shop System SHALL show an expired-voucher message.
- D6: WHEN a customer checks out, THE Shop System SHALL NOT combine a discount with free shipping.
