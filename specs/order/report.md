# Requirements analysis: order

5 requirements analysed: 2 conflict(s), 1 gap(s), 0 ambiguity(ies), 1 scenario(s) to confirm.

## 1. Conflict: Backorder Requirement Conflict

The requirements contain a direct contradiction regarding how to handle orders when stock is low. In the situation where an order is submitted but inventory is unavailable, R2 requires the system to place the order on backorder, while R3 explicitly forbids the system from placing any order on backorder.

- **A) Keep as-is:** Keeping the requirements as written means the system is logically unable to process any order where inventory is unavailable, as it is forced to perform an action that is simultaneously prohibited.
- **B) Change:** Remove R3 or modify it to allow backorders for specific conditions, ensuring that R2's instruction to backorder unavailable items is not contradicted by a general prohibition.

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

## 3. Gap: Undefined behavior for non-existent orders

The requirements do not specify what the system must do when an order has not been submitted, has not been canceled, and is not in a canceled-and-refunded state. This gap appears in the situation where none of these order states are active.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for situations where no order has been submitted or canceled.
- **B) Change:** Add a requirement stating that the system shall do nothing or remain idle when no order has been submitted or canceled.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: order_canceled (An order has been canceled.)
- FALSE: order_canceled_and_refunded (The order is in a state where it has been canceled and refunded.)
- FALSE: order_submitted (An order has been submitted by a customer.)

## 4. Scenario, allowed: Fulfillment without submission

The requirements allow the system to fulfill an order even when no order has been submitted and inventory is unavailable. This defeats the purpose of R1, which ties fulfillment to a submitted order and available inventory, and contradicts the user story's intent that customers receive goods only after submitting valid orders.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement stating that the Order System SHALL NOT fulfill any order unless an order has been submitted and inventory is available.

*Proven:* The requirements allow this behaviour:
- FALSE: inventory_available (The inventory for the ordered items is available.)
- TRUE: order_fulfilled (The order system has fulfilled the order.)
- FALSE: order_submitted (An order has been submitted by a customer.)
Requirement R1 does not apply in it, and yet what R1 demands is the case.
