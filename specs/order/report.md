# Requirements analysis: order

5 requirements analysed: 2 conflict(s), 1 gap(s), 0 ambiguity(ies), 1 scenario(s) to confirm.

## 1. Conflict: Backorder Requirement Conflict

The requirements contain a direct contradiction regarding how to handle orders when stock is low. In the situation where an order is submitted but inventory is unavailable, R2 requires the system to place the order on backorder, while R3 explicitly forbids the system from placing any order on backorder.

- **A) Keep as-is:** Keeping the requirements as written means the system is logically trapped and cannot legally process any order where inventory is unavailable, as it must simultaneously do and not do the same action.
- **B) Change:** Remove R3 entirely, or modify R3 to state that the system shall not place orders on backorder only under specific conditions that do not overlap with the scenario in R2.

*Proven:* Requirements R2, R3 cannot all be obeyed in this situation:
- FALSE: inventory_available (The inventory for the ordered items is available.)
- TRUE: order_submitted (An order has been submitted by a customer.)

## 2. Conflict: Conflict between fulfillment and refund status

The requirements contain a direct contradiction regarding what happens when an order is submitted while inventory is available. R1 states that the system must fulfill the order in this case, but R5 states that the system must not fulfill an order that is in a canceled-and-refunded state. Since the situation describes an order that is both submitted with available inventory and already canceled-and-refunded, the system is forced to both fulfill and not fulfill the order simultaneously.

- **A) Keep as-is:** Keeping the requirements as written means the system will fail or behave unpredictably whenever an order is submitted with available inventory but is already marked as canceled and refunded, as it cannot satisfy both R1 and R5.
- **B) Change:** Modify R1 to explicitly exclude orders that are already in a canceled-and-refunded state, such as: 'WHEN an order is submitted AND inventory is available AND the order is not canceled-and-refunded, THE Order System SHALL fulfill the order.'

*Proven:* Requirements R1, R5 cannot all be obeyed in this situation:
- TRUE: inventory_available (The inventory for the ordered items is available.)
- TRUE: order_canceled_and_refunded (The order is in a state where it has been canceled and refunded.)
- TRUE: order_submitted (An order has been submitted by a customer.)

## 3. Gap (no event happens): Undefined System Behavior

The requirements do not specify what the Order System must do when no order has been submitted, canceled, or refunded. This gap appears in the situation where none of these events have occurred, leaving the system's behavior undefined.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined action to take when no orders are submitted, canceled, or refunded.
- **B) Change:** Add a requirement stating that the Order System SHALL remain in an idle state when no orders are submitted, canceled, or refunded.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: order_canceled (An order has been canceled.)
- FALSE: order_canceled_and_refunded (The order is in a state where it has been canceled and refunded.)
- FALSE: order_submitted (An order has been submitted by a customer.)
No event happens in this situation, so this may only mean that the system waits.

## 4. Scenario, allowed: Fulfillment without submission

The requirements allow the system to fulfill an order even when no order has been submitted and inventory is unavailable. This defeats the purpose of R1, which ties fulfillment to a submitted order and available inventory, and contradicts the user story's expectation that processing follows submission.

- **A) Keep as-is:** Keep the requirements, allowing the system to fulfill orders without a prior submission or available inventory.
- **B) Change:** Add a requirement stating that the Order System SHALL NOT fulfill any order unless an order has been submitted and inventory is available.

*Proven:* The requirements allow this behaviour:
- FALSE: inventory_available (The inventory for the ordered items is available.)
- TRUE: order_fulfilled (The order system has fulfilled the order.)
- FALSE: order_submitted (An order has been submitted by a customer.)
Requirement R1 does not apply in it, and yet what R1 demands is the case.
