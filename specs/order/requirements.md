# Requirements: Order Processing

The order-processing example from the Kiro blog post on requirements analysis.

## Requirement 1

**User Story:** As a customer, I want my submitted orders to be processed
correctly, so that I either receive my goods or get my money back.

### Acceptance Criteria

- R1: WHEN an order is submitted AND inventory is available, THE Order System SHALL fulfill the order.
- R2: WHEN an order is submitted AND inventory is unavailable, THE Order System SHALL place the order on backorder.
- R3: THE Order System SHALL NOT place any order on backorder.
- R4: WHEN an order is canceled, THE Order System SHALL refund all associated payments.
- R5: WHILE an order is in a canceled-and-refunded state, THE Order System SHALL NOT fulfill the order.
